kbot
====

This is a personal chatbot, written to use with Slack, and to scratch my own itches.  That said, if you find it useful,
here are some tips on getting started with it.  If you have any issues at all, please post a bug report in Github at 
https://github.com/ekozlowski/kbot/issues.

Getting Started:
----------------

At a minimum, you will need a Slack "Bot" user created.  Instructions for doing that can be found here:
https://my.slack.com/services/new/bot.  Once you choose a name for your bot, you'll be taken to a page that lists an 
API Token for your bot.  The code written here expects this token to be an environment variable called "SLACK_BOT_TOKEN".

You'll also need to provide the name of your bot in another environment variable called "BOT_NAME".  This is so that the
bot knows who it is, and when conversations are directed at it.

