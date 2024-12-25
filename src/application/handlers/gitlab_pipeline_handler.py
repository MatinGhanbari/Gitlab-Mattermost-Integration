import json

import requests

from src.constants.users import users

from src.utils.config import CONFIG
from src.constants.messages import *
from src.repositories.user_repository import UserRepository
from src.utils.utils import *

mattermost_profile_url = CONFIG['mattermost_profile_url']

db_config = CONFIG["db_config"]
repo = UserRepository(dbname=db_config["dbname"],
                       user=db_config["user"], 
                       password=db_config["password"],
                       host=db_config["host"],
                       port=db_config["port"])

def handle_success_pipeline_updates(update):
    message = pipeline_success_message.format(
        update['user']['name'],
        CONFIG['gitlab_url'] +
        update['user']['username'],
        update['project']['id'],
        update['project']['name'],
        update['project']['web_url'],
        update['project']['namespace'],
        update['object_attributes']['ref'],
        update['object_attributes']['created_at'],
        update['object_attributes']['finished_at'],
        update['object_attributes']['duration'],
        update['commit']['title'],
        update['commit']['url'],
        append_pipeline_stages(update)
    )

    try:
        json_data = {
            "text": message,
            "username": update['user']['name'],
            "icon_url": update['user']['avatar_url'] if not CONFIG['use_mattermost_profile_icon']
            else mattermost_profile_url.format(users.get(str(update['user']['id']))["Token"]),
            "channel": CONFIG['bot_channel'],
            # "attachments":[
            #     {
            #         "color": "#00FF00",
            #         "text": message
            #     }
            # ]
        }
    except TypeError as e:
        json_data = {
            "text": message,
            "username": update['user']['name'],
            "icon_url": update['user']['avatar_url'],
            "channel": CONFIG['bot_channel'],
            # "attachments":[
            #     {
            #         "color": "#00FF00",
            #         "text": message
            #     }
            # ]
        }

    if CONFIG['service']['card_info']: json_data["props"]= {"card": update}

    response = requests.post(CONFIG['hook_url'], json=json_data)
    return response.content

def handle_failed_pipeline_updates(update):
    message = pipeline_failed_message.format(
        update['user']['name'],
        CONFIG['gitlab_url'] +
        update['user']['username'],
        update['project']['id'],
        update['project']['name'],
        update['project']['web_url'],
        update['project']['namespace'],
        update['object_attributes']['ref'],
        update['object_attributes']['created_at'],
        update['object_attributes']['finished_at'],
        update['object_attributes']['duration'],
        update['commit']['title'],
        update['commit']['url'],
        append_pipeline_stages(update)
    )

    try:
        json_data = {
            "text": message,
            "username": update['user']['name'],
            "icon_url": update['user']['avatar_url'] if not CONFIG['use_mattermost_profile_icon']
            else mattermost_profile_url.format(users.get(str(update['user']['id']))["Token"]),
            "channel": CONFIG['bot_channel'],
            "priority": {
                    "priority": "urgent",
                    "requested_ack": True
            },
            # "attachments":[
            #     {
            #         "color": "#FF0000",
            #         "text": message
            #     }
            # ]
        }
    except TypeError as e:
        json_data = {
            "text": message,
            "username": update['user']['name'],
            "channel": CONFIG['bot_channel'],
            "priority": {
                    "priority": "urgent",
                    "requested_ack": True
            },
            # "attachments":[
            #     {
            #         "color": "#FF0000",
            #         "text": message
            #     }
            # ]
        }
    if CONFIG['service']['card_info']: json_data["props"]= {"card": update}

    response = requests.post(CONFIG['hook_url'], json=json_data)
    return response.content


def handle_pipeline(update):
    if CONFIG['service']['log_update']:
        log(f"Incommig {update.get('object_kind')} Event.")

    if update.get('object_attributes').get("status") == 'success':
        return handle_success_pipeline_updates(update)
    elif update.get('object_attributes').get("status") == 'failed':
        return handle_failed_pipeline_updates(update)