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

Weather:

To make the "weather" command work, you need a API key to Darksky.  You can get one here:  https://darksky.net/dev/

You'll need to add the following environment variables:

- `DARKSKY_API_KEY` - This should be your API Key from Darksky.
- `LATITUDE` - Your location's latitude.
- `LONGITUDE` - Your location's longitude.

Latitude and longitude location are passed to Darksky for finding your local weather info.
