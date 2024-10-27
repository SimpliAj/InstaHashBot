import yaml
import time
from instagrapi import Client
from datetime import datetime, timedelta
import random
import requests
from telegram import Bot as TelegramBot
from discord import Client as DiscordClient
import json

# Load the configuration
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Instagram setup
username = config["instagram"]["username"]
password = config["instagram"]["password"]
client = Client()

# Settings configuration
version = config["settings"]["version"]
max_follows = config["settings"]["max_follows"]
min_followers = config["settings"]["min_followers"]
min_following = config["settings"]["min_following"]
follow_limit = config["settings"]["follow_limit"]
follow_timeframe_hours = config["settings"]["follow_timeframe_hours"]
unfollow_after_hours = config["settings"]["unfollow_after_hours"]
auto_like = config["settings"]["auto_like"]
auto_comment = config["settings"]["auto_comment"]
max_likes_per_day = config["settings"]["max_likes_per_day"]
max_comments_per_day = config["settings"]["max_comments_per_day"]

# Hashtags, blacklist, and comments
hashtags = config["hashtags"]
blacklist = config["blacklist"]
comments_list = config["comments"]

# Telegram setup
telegram_enabled = config["telegram"]["enabled"]
telegram_bot_token = config["telegram"]["bot_token"]
telegram_chat_ids = config["telegram"]["chat_ids"]  # Multiple chat IDs

# Discord setup
discord_enabled = config["discord"]["enabled"]
discord_use_webhook = config["discord"]["use_webhook"]
discord_bot_token = config["discord"]["bot_token"]
discord_channel_ids = config["discord"]["channel_ids"]  # Multiple channel IDs
discord_webhook_url = config["discord"]["webhook_url"]
discord_webhook_name = config["discord"].get("webhook_name", "InstaHashBot")
discord_webhook_avatar_url = config["discord"].get("webhook_avatar_url", "")

# Function to send Telegram messages
def send_telegram_message(message):
    if telegram_enabled:
        bot = TelegramBot(token=telegram_bot_token)
        for chat_id in telegram_chat_ids:
            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print(f"Failed to send Telegram message to chat_id {chat_id}: {e}")

# Discord bot client for sending messages
class DiscordNotifier(DiscordClient):
    async def on_ready(self):
        if discord_enabled and not discord_use_webhook:
            for channel_id in discord_channel_ids:
                channel = self.get_channel(int(channel_id))
                if channel:
                    try:
                        await channel.send(message)
                    except Exception as e:
                        print(f"Failed to send Discord message to channel_id {channel_id}: {e}")
            await self.close()

# Instantiate Discord bot globally
discord_notifier = DiscordNotifier()

# Function to send Discord messages using a bot
def send_discord_message(message):
    if discord_enabled and not discord_use_webhook:
        discord_notifier.loop.create_task(discord_notifier.start(discord_bot_token))
        time.sleep(5)  # Small delay to allow Discord bot to send messages

# Function to send Discord messages using a webhook
def send_discord_webhook_message(message):
    if discord_enabled and discord_use_webhook:
        payload = {
            "content": message,
            "username": discord_webhook_name,
            "avatar_url": discord_webhook_avatar_url
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(discord_webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send Discord webhook message: {e}")

# Login to Instagram
try:
    client.login(username, password)
except Exception as e:
    print(f"Failed to log in to Instagram: {e}")

# Function to follow users based on hashtags
def follow_users():
    followed_users = []
    for hashtag in hashtags:
        users = client.hashtag_medias_top(hashtag, amount=max_follows)
        for user in users:
            username = user.user.username
            if username not in blacklist:
                user_info = client.user_info_by_username(username)
                if user_info.follower_count >= min_followers and user_info.following_count >= min_following:
                    try:
                        client.user_follow(user_info.pk)
                        followed_users.append(username)
                        message = f"Followed {username} from #{hashtag}"
                        print(message)
                        send_telegram_message(message)
                        if discord_use_webhook:
                            send_discord_webhook_message(message)
                        else:
                            send_discord_message(message)

                        if auto_like and random.randint(1, 100) <= max_likes_per_day:
                            client.media_like(user.pk)
                            print(f"Liked a post from {username}")

                        if auto_comment and random.randint(1, 100) <= max_comments_per_day:
                            comment = random.choice(comments_list)
                            client.media_comment(user.pk, comment)
                            print(f"Commented on a post from {username}: {comment}")

                    except Exception as e:
                        print(f"Failed to follow {username}: {e}")
                else:
                    print(f"Skipped {username} due to follower/following limits.")

# Function to unfollow users after a given timeframe
def unfollow_users():
    current_time = datetime.now()
    for user in client.user_following(client.user_id):
        followed_time = client.user_follow_time(user.pk)
        if followed_time and current_time - followed_time > timedelta(hours=unfollow_after_hours):
            try:
                client.user_unfollow(user.pk)
                message = f"Unfollowed {user.username} after {unfollow_after_hours} hours"
                print(message)
                send_telegram_message(message)
                if discord_use_webhook:
                    send_discord_webhook_message(message)
                else:
                    send_discord_message(message)
            except Exception as e:
                print(f"Failed to unfollow {user.username}: {e}")

# Main execution loop
if __name__ == "__main__":
    while True:
        follow_users()
        unfollow_users()
        time.sleep(follow_timeframe_hours * 3600)  # Wait for the specified hours before running again
