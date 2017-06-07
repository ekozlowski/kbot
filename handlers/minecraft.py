"""
This module handles spinning Minecraft servers up and down on AWS.

Need to add idle detection, and shut down servers when idle.
"""

help_text = """`minecraft (start|stop)` - Starts (or stops) the Minecraft Server"""
import os
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
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(servers.get(server_name))
    instance.start()
    instance.wait_until_running()
    fqdn = os.environ.get("MINECRAFT_FQDN")
    hosted_zone = os.environ.get("MINECRAFT_HOSTED_ZONE")
    if fqdn and hosted_zone:
        set_dns(instance, fqdn, hosted_zone)


def set_dns(instance, fqdn, hosted_zone):
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone,
        ChangeBatch={
            "Comment": "Automatic DNS update",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": fqdn,
                        "Type": "CNAME",
                        "TTL": 180,
                        "ResourceRecords": [
                            {
                                "Value": instance.public_dns_name,
                            },
                        ],
                    }
                },
            ]
        }
    )
    print(response)

def bring_up_minecraft():
    start_server('minecraft')


def bring_up_ftb():
    # bring up the ftb server
    pass


def stop_server(server_name):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(servers.get(server_name))
    instance.stop()
    instance.wait_until_stopped()


def shut_down_ftb():
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
    #start_server('minecraft')
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(servers.get('minecraft'))
    print(instance)
    print(repr(instance))
    print(dir(instance))
    print(instance.public_ip_address)
    dns_name = instance.public_dns_name
    print(dns_name)

    client = boto3.client('route53')
    print(dir(client))
