import yaml
import time
from datetime import datetime, timedelta
from instagrapi import Client
import telegram
import discord
import asyncio

# Function to read YAML configuration file
def load_config(file_path='config.yml'):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load configuration
config = load_config()

# Extract Instagram login credentials, settings, and bot information
username = config['instagram']['username']
password = config['instagram']['password']
max_follows = config['settings']['max_follows']
min_followers = config['settings']['min_followers']
min_following = config['settings']['min_following']
follow_limit = config['settings']['follow_limit']
follow_timeframe_hours = config['settings']['follow_timeframe_hours']
hashtags = config['hashtags']
blacklist = config['blacklist']

# Initialize follow tracking variables
follow_count = 0
follow_start_time = datetime.now()

# Telegram bot info
telegram_token = config['telegram']['bot_token']
telegram_chat_id = config['telegram']['chat_id']

# Discord bot info
discord_token = config['discord']['bot_token']
discord_channel_id = int(config['discord']['channel_id'])

# Initialize the Instagram client
client = Client()

# Log into Instagram
client.login(username, password)

# Initialize Telegram bot
telegram_bot = telegram.Bot(token=telegram_token)

# Function to send a Telegram message
def send_telegram_message(message):
    telegram_bot.send_message(chat_id=telegram_chat_id, text=message)

# Discord bot setup
class MyDiscordClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def send_message(self, message):
        channel = self.get_channel(discord_channel_id)
        await channel.send(message)

# Initialize the Discord client
discord_client = MyDiscordClient()

# Function to check if the follow limit has been reached
def can_follow():
    global follow_count, follow_start_time
    current_time = datetime.now()
    elapsed_time = (current_time - follow_start_time).total_seconds() / 3600  # Convert to hours
    
    # Reset count if the time frame has passed
    if elapsed_time >= follow_timeframe_hours:
        follow_count = 0
        follow_start_time = current_time
    
    return follow_count < follow_limit

# Function to follow users by hashtag
def follow_users_by_hashtag(hashtag, max_follows=10, min_followers=0, min_following=0, blacklist=[]):
    global follow_count

    # Search for media by hashtag
    medias = client.hashtag_medias_top(hashtag, amount=max_follows)
    
    followed_users = []
    for media in medias:
        if not can_follow():
            print("Follow limit reached, waiting for the next timeframe.")
            break
        
        user = media.user

        # Skip blacklisted users
        if user.username in blacklist:
            print(f"Skipping blacklisted user: {user.username}")
            continue
        
        # Fetch the user's profile to check followers/following counts
        user_info = client.user_info(user.pk)
        
        # Only follow if they meet the min_followers and min_following criteria
        if user_info.follower_count >= min_followers and user_info.following_count >= min_following:
            client.user_follow(user.pk)
            followed_users.append(user.username)
            follow_count += 1  # Increment the follow count
            message = f"Followed: {user.username} (Followers: {user_info.follower_count}, Following: {user_info.following_count})"
            print(message)
            send_telegram_message(message)
            asyncio.run(discord_client.send_message(message))
        else:
            message = f"Skipped: {user.username} (Followers: {user_info.follower_count}, Following: {user_info.following_count}) - Does not meet criteria"
            print(message)
            send_telegram_message(message)
            asyncio.run(discord_client.send_message(message))
    
    return followed_users

# Run the Discord bot asynchronously
async def start_discord_bot():
    await discord_client.start(discord_token)

# Main process to follow users and notify on both platforms
async def main():
    # Start the Discord client in the background
    discord_task = asyncio.create_task(start_discord_bot())

    # Iterate through hashtags and follow users
    for hashtag in hashtags:
        print(f"Processing hashtag: #{hashtag}")
        followed_users = follow_users_by_hashtag(
            hashtag, 
            max_follows=max_follows, 
            min_followers=min_followers, 
            min_following=min_following, 
            blacklist=blacklist
        )
        summary_message = f"Finished processing hashtag: #{hashtag}. Total followed users: {len(followed_users)}"
        send_telegram_message(summary_message)
        await discord_client.send_message(summary_message)

    # Ensure the Discord bot runs until it's manually stopped
    await discord_task

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
