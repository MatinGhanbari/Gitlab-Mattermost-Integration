header = "##### :gitlab_icon:  GitLab Event"
summary_message = """##### :gitlab_icon:  GitLab Daily Summary \n\n"""
no_development_message = "\tNo development has been done today."

push_message = header + """
- Event name: **Push**
- User Name: {}
- Project: {} - [{}]({})
- Project Namespace: {}
- Branch: ```{}```
- Before: {}
- After: {}
- Commits:
{}"""

card = """
### :gitlab_icon:  **Event Information:**
```
{}
```
"""

merge_request_message = header + """
- Event name: **Merge Request**
- User Name: {}
- Project: {} - [{}]({})
- Project Namespace: {}
- MergeRequest :
    - Title: [{}]({})
    - Description: *{}*
    - Source Branch: ```{}```
    - Target Branch: ```{}```
    - CreatedAt: {}
- Assignees: 
{}"""

user_summary_message="""#### {} {}:
  \\- Commits Today: {}
  \\- Pushes Today: {}
  \\- Merge Requests Today: {}"""


pipeline_failed_message = """##### :gitlab_icon:  GitLab Pipeline Event
- Event name: **Pipeline Status**
- Status: ❌ **Failed**
- User Name: [{}]({})
- Project: {} - [{}]({})
- Project Namespace: {}
- Branch: ```{}```
- Created At: {}
- Finished At: {}
- Duration: {}
- Commit: [{}]({})
- Stages:
{}"""


pipeline_success_message = """##### :gitlab_icon:  GitLab Pipeline Event
- Event name: **Pipeline Status**
- Status: ✅ **Success**
- User Name: [{}]({})
- Project: {} - [{}]({})
- Project Namespace: {}
- Branch: ```{}```
- Created At: {}
- Finished At: {}
- Duration: {}
- Commit: [{}]({})
- Stages:
{}"""