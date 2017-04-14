# System Stats To Telegram
Simple application to send system information (like memory, cpu, etc.) to your telegram bot. 

(so useful on raspberryPi systems)

How to running:
```
$ python system_stats_to_telegram.py --help
Usage: system_stats_to_telegram.py [OPTIONS] TOKEN

Options:
  --user_ids TEXT   Authorized comma separated users ids to send information
                    to
  --usernames TEXT  Authorized comma separated usernames to send information
                    to
  --help            Show this message and exit.
```

Now open a chat with your bot and use any of this comads (only one by now):
* /stats -- gives you information about the memory usages of the system where runs this script

# Authorization
It is important to mention that if no value is set on user_ids or usernames, ANYONE knowing the supported commands and the bot username can ask iformation.

So please use always this script with a list comma separated of authorized user_ids or usernames.

