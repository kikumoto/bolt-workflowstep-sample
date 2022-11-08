import logging
import boto3

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt.workflows.step import WorkflowStep

from workflowstep import CustomWorkflowStep


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(level=logging.DEBUG)

ssm = boto3.client('ssm')
token = ssm.get_parameter(
    Name='/slackapp/bolt-workflowstep-sample/SLACK_BOT_TOKEN', 
    WithDecryption=True)['Parameter']['Value']
signing_secret = ssm.get_parameter(
    Name='/slackapp/bolt-workflowstep-sample/SLACK_SIGNING_SECRET', 
    WithDecryption=True)['Parameter']['Value']

app = App(
    token=token,
    signing_secret=signing_secret,
    process_before_response=True,
)

CustomWorkflowStep().register(app, "sample-step")

def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)