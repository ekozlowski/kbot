import time
from slackclient import SlackClient
import os

if os.path.exists('./overrides.py'):
    import overrides
    overrides.main()

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_NAME = os.environ.get('BOT_NAME')
BOT_ID = os.environ.get('BOT_ID')
AT_BOT = "<@{}>".format(BOT_ID)
EXAMPLE_COMMAND = 'do'
READ_WEBSOCKET_DELAY = 2

slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
    Receives commands directed at the bot, and determines if they
    are valid commands.  If so, then it acts on the commands.  If not,
    returns back what it needs for clarification.
    """
    response = "Not sure what you mean.  Use the *{}* command with numbers, delimited by spaces.".format(EXAMPLE_COMMAND)
    ret = None
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...  write some more code, then I can do that."
    elif command.startswith('who is'):
        if 'alisa' in command:
            response = "Alisa is Ed's beautiful wife. :)"
    elif command.startswith('bot shutdown'):
        response = "Ok... Shutting down."
        ret = 'shutdown'
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    return ret


def parse_slack_output(slack_rtm_output):
    """
    Filter for slack messages - Returns None, unless this message is directed at the Bot, based on it's ID.
    :param slack_rtm_output:
    :return:
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return the text after the '@' mention, whitespace removed
                print(repr(output))
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
            else:
                print("Filtering out this: {}".format(repr(output)))
    return None, None

if __name__ == "__main__":


    if slack_client.rtm_connect():
        print("Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                out = handle_command(command, channel)
                if out == 'shutdown':
                    break
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed.  Invalid Slack token or Bot ID?")

    hide_me = """
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve users
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is: " + user.get('id'))
    else:
        print("could not find the bot with user name: " + BOT_NAME)
    """