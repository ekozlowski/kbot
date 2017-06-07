"""
This module handles spinning Minecraft servers up and down on AWS.

Need to add idle detection, and shut down servers when idle.
"""

help_text = "handles minecraft stuff"


import boto3
import threading


import uuid

tasks = {}

class Task(threading.Thread):

    def __init__(self, callback, text_start, text_end, func, **args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.callback = callback
        self.text_start = text_start
        self.text_end = text_end

    def run(self):
        self.callback(self.text_start)
        ret = self.func(**self.args)
        self.callback(self.text_end)

def spinoff_request(function, callback, text_start, text_end, **args):
    t = Task(callback, text_start, text_end, function, **args)
    t.start()



servers = {
    "minecraft": "i-09aeaf1cfcbf5eab0"
}

def start_server(server_name):
    client = boto3.client('ec2')
    client.start_instances(InstanceIds=[servers.get(server_name)])



def bring_up_minecraft():
    start_server('minecraft')


def bring_up_ftb():
    # bring up the ftb server
    pass


def stop_server(server_name):
    client = boto3.client('ec2')
    client.stop_instances(InstanceIds=[servers.get(server_name)], Force=False)


def shut_down_ftb():
    # shut down ftb server
    pass


def handle(command, callback):
    # Command is the full text of whatever we're "handling"
    if "minecraft start" == command:
        spinoff_request(
            start_server,
            callback,
            'starting minecraft!',
            'minecraft started!',
            server_name='minecraft',
        )
    elif "minecraft stop" == command:
        spinoff_request(
            stop_server,
            callback,
            'stopping minecraft!',
            'minecraft stopped!',
            server_name='minecraft',
        )
if __name__ == "__main__":
    handle('minecraft start', 'eh')