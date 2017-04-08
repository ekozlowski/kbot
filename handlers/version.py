help_text = "`version` - I'll tell you what version of my software I'm running."

def handle(command):
    """
    We don't care what we were passed.  We just return a dumb version string - (for now)
    :param command:
    :return:
    """
    return "I'm running version 0.0.1"