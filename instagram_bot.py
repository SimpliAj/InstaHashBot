
import yaml
import json
import time
from datetime import datetime, timedelta
from instagrapi import Client
import telegram
import discord
import asyncio
import os
import requests

# Function to read YAML configuration file
def load_config(file_path='config.yml'):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Function to load or initialize the followed users file
def load_followed_users(file_path='followed_users.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

# Function to save the followed users to a JSON file
def save_followed_users(followed_users, file_path='followed_users.json'):
    with open(file_path, 'w') as file:
        json.dump(followed_users, file)

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
unfollow_after_hours = config['settings']['unfollow_after_hours']
hashtags = config['hashtags']
blacklist = config['blacklist']
current_version = config['settings']['version']

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

# Version Check Function
def check_for_new_version(current_version, repo="SimpliAj/InstaHashBot"):
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release.get("tag_name", "0.0.0")

            # Compare versions
            if latest_version > current_version:
                return True, latest_version, latest_release.get("html_url")
        return False, None, None
    except Exception as e:
        print(f"Error checking for new version: {e}")
        return False, None, None

# Function to notify user of the new version
def notify_new_version(new_version, url):
    message = f"A new version {new_version} of the bot is available! Check it out: {url}"
    print(message)
    send_telegram_message(message)
    asyncio.run(discord_client.send_message(message))

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
    global follow_count, followed_users

    # Search for media by hashtag
    medias = client.hashtag_medias_top(hashtag, amount=max_follows)
    
    followed_list = []
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
            follow_count += 1  # Increment the follow count
            followed_list.append(user.username)
            
            # Save the followed user with a timestamp
            followed_users[user.username] = {
                "user_id": user.pk,
                "followed_at": datetime.now().isoformat()
            }
            save_followed_users(followed_users)

            message = f"Followed: {user.username} (Followers: {user_info.follower_count}, Following: {user_info.following_count})"
            print(message)
            send_telegram_message(message)
            asyncio.run(discord_client.send_message(message))
        else:
            message = f"Skipped: {user.username} (Followers: {user_info.follower_count}, Following: {user_info.following_count}) - Does not meet criteria"
            print(message)
            send_telegram_message(message)
            asyncio.run(discord_client.send_message(message))
    
    return followed_list

# Function to unfollow users after the specified time
def unfollow_old_users():
    global followed_users
    current_time = datetime.now()

    users_to_unfollow = [
        username for username, info in followed_users.items()
        if (current_time - datetime.fromisoformat(info["followed_at"])).total_seconds() / 3600 >= unfollow_after_hours
    ]

    for username in users_to_unfollow:
        user_id = followed_users[username]["user_id"]
        client.user_unfollow(user_id)
        del followed_users[username]
        save_followed_users(followed_users)

        message = f"Unfollowed: {username} after {unfollow_after_hours} hours."
        print(message)
        send_telegram_message(message)
        asyncio.run(discord_client.send_message(message))

# Run the Discord bot asynchronously
async def start_discord_bot():
    await discord_client.start(discord_token)

# Main process to follow/unfollow users and notify on both platforms
async def main():
    # Version check
    is_new_version, new_version, release_url = check_for_new_version(current_version, repo="SimpliAj/InstaHashBot")
    
    if is_new_version:
        notify_new_version(new_version, release_url)
    
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

    # Unfollow users that meet the time condition
    unfollow_old_users()

    # Ensure the Discord bot runs until it's manually stopped
    await discord_task

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
