kbot
====

This is a personal chatbot, written to use with Slack, and to scratch my own itches.  That said, if you find it useful,
here are some tips on getting started with it.  If you have any issues at all, please post a bug report in Github at 
https://github.com/ekozlowski/kbot/issues.

Getting Started
----------------

At a minimum, you will need a Slack "Bot" user created.  Instructions for doing that can be found here:
https://my.slack.com/services/new/bot.  Once you choose a name for your bot, you'll be taken to a page that lists an 
API Token for your bot.  The code written here expects this token to be an environment variable called "SLACK_BOT_TOKEN".

You'll also need to provide the name of your bot in another environment variable called "BOT_NAME".  This is so that the
bot knows who it is, and when conversations are directed at it.  It also uses this name to dynamically grab its id, and 
uses the ID to figure out if it was mentioned.  (If you inspect messages, you'll see that usernames are not mentioned,
just User IDs.)

Minimum Env Vars:

- `SLACK_BOT_TOKEN` - This is Slack's API token for your bot.
- `BOT_NAME` - Your Slackbot's name.  (ESSENTIAL)

AddOns
------

### Weather

To make the "weather" command work, you need a API key to Darksky.  You can get one here:  https://darksky.net/dev/

You'll need to add the following environment variables:

- `DARKSKY_API_KEY` - This should be your API Key from Darksky.
- `LATITUDE` - Your location's latitude.
- `LONGITUDE` - Your location's longitude.

Latitude and longitude location are passed to Darksky for finding your local weather info.

All weather functionality is Powered by Darksky.

<a href="https://darksky.net/poweredby/"><img src="https://darksky.net/dev/img/attribution/poweredby-oneline.png" width="247px" height="56px"></a>

### Minecraft Server Automation

For this, at a minimum, you will need these environment variables:

- `AWS_ACCESS_KEY_ID` - Your Amazon AWS Access Key ID
- `AWS_SECRET_ACCESS_KEY` - AWS Secret Access Key
- `AWS_DEFAULT_REGION` - AWS Region (I use 'us-east-1')

You need to create a Minecraft server so that when it starts, Minecraft is brought up on the default port.  Make sure this port is accessible through your security groups, or none of this will work!

You'll need to provide the "Instance-ID" of this box, and modify `handlers/minecraft.py`'s `servers` section accordingly.

After this, the `kbot minecraft start` and `kbot minecraft stop` should be functional.

#### Getting Fancier With The Spices

If you want your route53 DNS automatically updated when you start your server, you need two additional Environment Vars.

- `MINECRAFT_FQDN` - The fully-qualified-domain-name to your minecraft box.  Something like minecraft.mycoolsite.org
- `MINECRAFT_HOSTED_ZONE` - This is the "Hosted Zone ID" in Route53.  We need this so we CNAME the URL to the right place.

Now when Kbot starts your minecraft server, you won't have to futz with giving people a long URL, or mapping Route53 yourself. :)

#### Changelog

0.0.3
- Added github workflows

0.0.2
- Reformatted some code using the Python Black package
- Changed dependency management to use pipenv instead of a virtualenv with a 
requirements.txt file.
- If a weather icon is not found, we default to just displaying the key text
that was tried in the lookup for an icon.
