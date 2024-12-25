import time

import requests
import schedule

from src.utils.config import CONFIG
from src.constants.users import users
from src.constants.messages import summary_message, no_development_message, user_summary_message
from src.repositories.user_repository import UserRepository

db_config = CONFIG["db_config"]
repo = UserRepository(dbname=db_config["dbname"],
                       user=db_config["user"], 
                       password=db_config["password"],
                       host=db_config["host"],
                       port=db_config["port"])

def prepare_users_message():
    user_image_base_string = "![{}](" + CONFIG['mattermost_profile_url'] + "?_=1697396179992 =" + CONFIG['summary_profile_pic_size'] + "x" + CONFIG['summary_profile_pic_size'] + ")"
    
    users_summeries = []
    for user_id in users:
        user_name = users[user_id]["Name"]
        user_token = users[user_id]["Token"]
        commits, pushes, merges = repo.get_user_push_merge_count(user_id)
        if commits + pushes + merges > 0:
            user_image = user_image_base_string.format(user_name, user_token)
            users_summeries.append(user_summary_message.format(user_image, user_name, commits, pushes, merges))
    
    return "\n".join(users_summeries) if len(users_summeries)>0 else None

def print_summary():
    users_message = prepare_users_message()
    summary_message_data =  (users_message if users_message is not None else no_development_message)
    
    json_data = {
        "text": summary_message + summary_message_data,
        "username": CONFIG['bot_username'],
        "icon_url": CONFIG['bot_icon_url'],
        "channel": CONFIG['bot_channel']
    }

    repo.refresh_counts()
    response = requests.post(CONFIG['hook_url'], json=json_data)

    return response.content


def run(daily_scheduler):
    schedule.every().day.at(daily_scheduler).do(print_summary)
    print(f"schedule on daily at {daily_scheduler}!")

    while True:
        schedule.run_pending()
        time.sleep(20)


def start_scheduler(service_conf):
    import threading
    scheduler_thread = threading.Thread(target=run, args=(service_conf['daily_scheduler'],))
    scheduler_thread.start()