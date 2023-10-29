import slack
import os

def slackBot():
    client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
    client.chat_postMessage(channel="#botstuff", text="hello world!")
    raise NotImplementedError
    #TODO ADD SLACK ?? 