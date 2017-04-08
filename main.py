import os
import time
from slackclient import SlackClient
from handlers import version, grocery, weather, feeds

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

# Add more handlers here - just remember to add a help_text string in your module base, and have a "handle" method
# that accepts a command text string, and handles it appropriately.
handlers = {
    'version': version,
    'grocery': grocery,
    'weather': weather,
    'feeds': feeds
}

def handle_command(command, channel):
    """
    Receives commands directed at the bot, and determines if they
    are valid commands.  If so, then it acts on the commands.  If not,
    returns back what it needs for clarification.
    """
    # Command is always the very first word - it is what puts us down a logical context path.
    cmd = command.split()[0]
    response = ""
    if cmd not in handlers:
        if cmd.lower() != 'help':
            response += "Not sure what you mean.  :disappointed:\n"
        response += "I support these commands:\n\n"

        for h in sorted(handlers.keys()):
            response += handlers.get(h).help_text + '\n'
            response += '\n'
        response += "\nTry one of those commands."
    else:
        response = handlers.get(cmd).handle(command)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


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


def get_user_id_from_user_name(user_name):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == user_name:
                user_id = user.get('id')
                print("User ID for '" + user_name + "' is: " + user.get('id'))
                return user.get('id')
    else:
        print("could not find the user id with user name: " + user_name)
        return None

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

    # get bot name
    hide_me = """
    """
