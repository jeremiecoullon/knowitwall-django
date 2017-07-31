import os
from slackclient import SlackClient


if os.path.isfile('le_local_setup.txt'):
    from config.local_settings import SLACK_TOKEN
else:
    SLACK_TOKEN = os.environ['SLACK_TOKEN']

SLACK_TOKEN = SLACK_TOKEN
slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None

def send_slack_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='le_user_feedback_bot',
        icon_emoji=':robot_face:'
    )

def send_feedback_to_slack(message='bige', channel_name='user-feedback'):
    channels = list_channels()
    for channel in channels:
        if channel['name'] == channel_name:
            send_slack_message(channel_id=channel['id'], message=message)
