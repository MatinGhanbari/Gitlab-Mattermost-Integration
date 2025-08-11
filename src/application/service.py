import json

from flask import Flask, request

from src.application.handlers.gitlab_update_handler import handle_update
from src.application.handlers.gitlab_pipeline_handler import handle_pipeline
from src.utils.config import CONFIG

service = Flask("GITLAB INTEGRATION SERVICE")

@service.route(CONFIG['service']['route'], methods=['GET', 'POST'])
def print_request():
    if request.method != 'POST':
        return json.dumps({'ok': False, 'error_code': 102, 'error': 'METHOD_ERROR'})

    if request.environ.get('HTTP_X_GITLAB_TOKEN') != CONFIG['GITLAB_TOKEN']:
        return json.dumps({'ok': False, 'error_code': 101, 'error': 'TOKEN_ERROR'})

    if request.json["object_kind"] != "pipeline":
        response = handle_update(request.json)
    
    response = handle_pipeline(request.json)
    return json.dumps({'ok': True, 'message': 'success', 'details': str(response)})