import datetime
from dateutil import parser

def log(message):
    date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    formatted_message = f"# [{date_time}]: {message}"
    print(formatted_message)

def append_commit_messages(update):
    messages = [
        f"\t- [{parser.isoparse(commit['timestamp']).strftime("%m-%d %H:%M")}]: [{commit['title']}]({commit['url']})" for commit in update["commits"]
    ]
    return "\n".join(messages[::-1])


def append_pipeline_stages(update):
    messages = [
        f"""\t- [{get_status_emoji(build["status"])}]:\t[{build["name"]}]({update["project"]["web_url"]}/-/jobs/{build["id"]})""" for build in update["builds"]
    ]
    return "\n".join(messages)

def get_status_emoji(status):
    return str(status).strip().upper()
    # if status == "success":
    #     return "[✅ Success]:"
    # if status == "failed":
    #     return "[❌ Failed]:"
    # if status == "created":
    #     return "[👶 Created]:"
    # if status == "skipped":
    #     return "[🚶‍♂️ Skipped]:"
    # if status == "pending":
    #     return "[⏱ Pending]:"

def append_assignees(update, users, mattermost_profile_url:str):
    assignees = [
        f"\t- {assignee["name"]}" for assignee in update["assignees"]
    ]
    return "\n".join(assignees)