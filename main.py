import requests
from google.cloud import storage
import json

def hello_world(request):
   
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('bucket name')
    blob = bucket.blob('file_name.json')
    data = request.get_json() 
    slack_data = json.loads(blob.download_as_string(client=None))

    for n in slack_data['users']:
        if  data['assignee_email'] == n['email']:
            slack_user = 'Hi <@' + n['slack_id'] + '> ,\n'
            message_start = 'The ticket '
            key = data['key']
            message_middle = ' has been in Ready for QA for '
            last_updated = data["last_updated"]
            message_end = ' days and is not currently blocked. Please take a look when you have time. \n' 
            issue_link = data['issue_url']
            message_ready = slack_user + message_start + key + message_middle + last_updated + message_end + issue_link
            payload = '{"text":"%s"}' % message_ready
            response = requests.post(
                'https://hooks.slack.com/services/yourslackhookurl,
                data = payload
                )
            break
        else:
            print("No such assignee email " + data['assignee_email'])

    return "success"
