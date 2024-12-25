import json

import requests

from src.constants.users import users

from src.utils.config import CONFIG
from src.constants.messages import push_message, merge_request_message
from src.repositories.user_repository import UserRepository
from src.utils.utils import *

mattermost_profile_url = CONFIG['mattermost_profile_url']

db_config = CONFIG["db_config"]
repo = UserRepository(dbname=db_config["dbname"],
                       user=db_config["user"], 
                       password=db_config["password"],
                       host=db_config["host"],
                       port=db_config["port"])

def handle_push_updates(update):
    message = push_message.format(
        update['user_name'],
        update['project_id'],
        update['project']['name'],
        update['project']['web_url'],
        update['project']['namespace'],
        str(update['ref']).split("/")[-1],
        str(update['before'])[:8],
        str(update['after'])[:8],
        append_commit_messages(update))

    json_data = {
        "text": message,
        "username": update['user_name'],
        "icon_url": update['user_avatar'] if not CONFIG['use_mattermost_profile_icon']
        else mattermost_profile_url.format(users.get(str(update['user_id']))["Token"]),
        "channel": CONFIG['bot_channel'],
    }
    if CONFIG['service']['card_info']: json_data["props"]= {"card": update}

    repo.increase_push_count(str(update['user_id']))
    repo.increase_commit_count(str(update['user_id']), str(len(update['commits'])))

    response = requests.post(CONFIG['hook_url'], json=json_data)
    return response.content

def handle_merge_request_updates(update):
    message = merge_request_message.format(
        update['user']['name'],
        update['project']['id'],
        update['project']['name'],
        update['project']['web_url'],
        update['project']['namespace'],
        update['object_attributes']['title'],
        update['object_attributes']['url'],
        update['object_attributes']['description'] if update['object_attributes']['description'] != "" else "None",
        update['object_attributes']['source_branch'],
        update['object_attributes']['target_branch'],
        update['object_attributes']['created_at'],
        append_assignees(update, users, mattermost_profile_url)
    )

    try:
        json_data = {
            "text": message,
            "username": update['user']['name'],
            "icon_url": update['user']['avatar_url'] if not CONFIG['use_mattermost_profile_icon']
            else mattermost_profile_url.format(users.get(str(update['user']['id']))["Token"]),
            "channel": CONFIG['bot_channel'],
        }
    except TypeError as e:
        json_data = {
            "text": message,
            "username": update['user']['name'],
            "channel": CONFIG['bot_channel'],
        }
    if CONFIG['service']['card_info']: json_data["props"]= {"card": update}

    repo.increase_merge_count(str(update['user']['id']))

    response = requests.post(CONFIG['hook_url'], json=json_data)
    return response.content


def handle_update(update):
    if CONFIG['service']['log_update']:
        log(f"Incommig {update.get('object_kind')} Event.")

    if update.get('object_kind') == 'push':
        return handle_push_updates(update)
    elif update.get('object_kind') == 'merge_request':
        return handle_merge_request_updates(update)