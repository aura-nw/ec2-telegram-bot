## Note: This bot is not ready for production
This bot is used to manage AWS EC2 instances in a region.

# Install
- setup required lib
```
pip3 install -r requirements.txt 
```
- create a bot using [BotFather](https://t.me/BotFather)
- setup env
```
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=xxx
export BOT_POLL_INTERVAL=xxx # for check new message in telegram
export TELEGRAM_BOT_TOKEN=xxx # telegram bot token from https://t.me/BotFather
```
- run bot
```
python3 bot.py
```
# How to use

In this code, a function `check_user` is used as authorization mechanism, replace with your user id to call the bot.
Command to interact with bot:
```
/help - list all available commands
/list - List all EC2 instances with id, name, statuses, type
/start_instance <instance_id> - Start an EC2 instance
/stop_instance <instance_id> - Stop an EC2 instance
/restart_instance <instance_id> - Restart an EC2 instance
/force_stop_instance <instance_id> - Force stop an EC2 instance
/change_instance_type <instance_id> <ec2-type> - Change EC2 instantype
```
