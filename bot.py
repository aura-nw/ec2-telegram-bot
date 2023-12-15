import os
import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
import boto3

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS credentials from environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region_name = os.environ.get('AWS_REGION', 'us-east-1')

# Load environment variables
bot_idle_time = int(os.environ.get('BOT_IDLE_TIME', 300))
bot_poll_interval = float(os.environ.get('BOT_POLL_INTERVAL', 5.0))  

# Create an EC2 client
ec2 = boto3.client('ec2', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Log each request
def log_request(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        user_name = update.effective_user.username
        command = context.args[0] if context.args else update.message.text.split()[0][1:]
        logger.info(f"Received command '{command}' from user {user_name} (ID: {user_id})")
        return func(update, context, *args, **kwargs)

    return wrapper

# Command functions with logging and user check
def check_user(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_name = update.effective_user.id
        if user_name != 5566017231:
            update.message.reply_text("You are not authorized to use this command.")
            return
        return func(update, context, *args, **kwargs)

    return wrapper
    
# Command functions with logging
@log_request
@check_user
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your EC2 control bot. Use /help to see available commands.')

@log_request
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('/list - List all EC2 instances\n'
                              '/start_instance <instance_id> - Start an EC2 instance\n'
                              '/stop_instance <instance_id> - Stop an EC2 instance\n'
                              '/restart_instance <instance_id> - Restart an EC2 instance\n'
                              '/force_stop_instance <instance_id> - Force stop an EC2 instance\n')

@log_request
@check_user
def list_instances(update: Update, context: CallbackContext) -> None:
    response = ec2.describe_instances()
    instances_info = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')
            instances_info.append(f"ID: `{instance_id}`, {instance_name}, {instance_state}")
    
    reply_text = '\n'.join(instances_info)
    update.message.reply_markdown_v2(reply_text)

@log_request
@check_user
def start_instance(update: Update, context: CallbackContext) -> None:
    instance_id = context.args[0]
    ec2.start_instances(InstanceIds=[instance_id])
    update.message.reply_text(f'Starting instance {instance_id}...')

@log_request
@check_user
def stop_instance(update: Update, context: CallbackContext) -> None:
    instance_id = context.args[0]
    ec2.stop_instances(InstanceIds=[instance_id])
    update.message.reply_text(f'Stopping instance {instance_id}...')

@log_request
@check_user
def force_stop_instance(update: Update, context: CallbackContext) -> None:
    instance_id = context.args[0]
    ec2.terminate_instances(InstanceIds=[instance_id])
    update.message.reply_text(f'Force stopping instance {instance_id}...')

@log_request
@check_user
def restart_instance(update: Update, context: CallbackContext) -> None:
    instance_id = context.args[0]
    ec2.stop_instances(InstanceIds=[instance_id])
    ec2.start_instances(InstanceIds=[instance_id])
    update.message.reply_text(f'Restarting instance {instance_id}...')

def main() -> None:
    # Get the bot token from environment variable
    token = os.environ.get('TELEGRAM_BOT_TOKEN')

    # Create the Updater and pass it your bot's token
    global updater
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("list", list_instances))
    dp.add_handler(CommandHandler("start_instance", start_instance, pass_args=True))
    dp.add_handler(CommandHandler("stop_instance", stop_instance, pass_args=True))
    dp.add_handler(CommandHandler("restart_instance", restart_instance, pass_args=True))
    dp.add_handler(CommandHandler("force_stop_instance", force_stop_instance, pass_args=True))

    # Start the Bot
    updater.start_polling(poll_interval=bot_poll_interval)

    # Run the bot until you send a signal to stop
    updater.idle()
    
if __name__ == '__main__':
    main()
