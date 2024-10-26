
# Instagram Hashtag Bot

This Python bot automates the process of logging into your Instagram account and following users based on specific hashtags. It includes options to set a minimum threshold for followers and following counts, blacklist certain users, and limit the number of follows within a defined time frame. The bot can also send notifications to Telegram and Discord, keeping you updated on its actions. Additionally, it can automatically unfollow users after a specified amount of time and check for newer versions directly from GitHub.

<p align="center">
  <img src="https://i.imgur.com/uoJtnP6.png" alt="InstaHashBot Logo" width="250"/>
</p>
<p align="center">
  <a href="https://github.com/SimpliAj/InstaHashBot/stargazers">
    <img src="https://img.shields.io/github/forks/SimpliAj/InstaHashBot?style=flat&logo=github&logoColor=whitesmoke&label=Forks" alt="GitHub repo forks"/>
    <img src="https://img.shields.io/github/stars/SimpliAj/InstaHashBot?style=flat&logo=github&logoColor=whitesmoke&label=Stars" alt="GitHub repo stars"/>
  </a>
</p>

## Features

- Follows users based on specified hashtags.
- Allows configuring a minimum number of followers and following for users to be followed.
- Blacklists certain users to prevent following.
- Sends real-time updates to both Telegram and Discord channels.
- Limits the number of users followed per hashtag.
- Limits the number of follows within a defined time frame.
- Automatically unfollows users after a specified number of hours.
- Checks for new versions of the bot on GitHub.

## Installation

### Prerequisites

- Python 3.x
- Instagram account
- Telegram bot (optional)
- Discord bot (optional)

### Python Dependencies

Install the required Python libraries:

```bash
pip install PyYAML instagrapi python-telegram-bot discord.py requests
```

### Clone the Repository

```bash
git clone https://github.com/SimpliAj/InstaHashBot.git
cd InstaHashBot
```

### Configure Your Bot

Update the \`config.yml\` file with your Instagram login details, Telegram/Discord bot tokens, and other settings.

```yaml
instagram:
  username: "your_instagram_username"
  password: "your_instagram_password"

settings:
  version: "1.0.0"             # Current version of the bot
  max_follows: 5               # Maximum number of users to follow per hashtag
  min_followers: 100            # Minimum number of followers a user must have
  min_following: 50             # Minimum number of accounts the user must be following
  follow_limit: 20              # Maximum number of accounts to follow within the time frame
  follow_timeframe_hours: 24    # Time frame in hours to limit the number of follows
  unfollow_after_hours: 48      # Time in hours after which followed users will be unfollowed

hashtags:
  - "webdevelopment"
  - "programming"
  - "python"

blacklist:
  - "user_to_ignore1"
  - "user_to_ignore2"

telegram:
  bot_token: "your_telegram_bot_token"
  chat_id: "your_telegram_chat_id"

discord:
  bot_token: "your_discord_bot_token"
  channel_id: "your_discord_channel_id"
```

### Telegram Bot Setup (Optional)

1. Go to the [BotFather](https://t.me/botfather) in Telegram.
2. Create a new bot to get the \`bot_token\`.
3. Get your \`chat_id\` by sending a message to the bot and using an API request to retrieve your chat information.

### Discord Bot Setup (Optional)

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a bot.
2. Add the bot to your server and get the \`channel_id\` where you'd like notifications sent.

## Running the Bot

Once everything is configured, you can run the bot by executing:

```bash
python instagram_bot.py
```

The bot will log into your Instagram account, search for users using the specified hashtags, and follow users based on the configured rules. It will also unfollow users after the set period and check for updates on GitHub.

## Example Output

The bot will send updates to both your Telegram and Discord accounts, providing details such as:

- Followed users
- Skipped users (if they don’t meet the follower/following requirements)
- Unfollowed users (if they've been followed for the set duration)
- Errors (e.g., login failures, Instagram limits)
- New version notifications (if an update is available)

## Configuration Options

- **max_follows**: The maximum number of users to follow per hashtag.
- **min_followers**: The minimum number of followers required to follow a user.
- **min_following**: The minimum number of accounts the user must be following.
- **follow_limit**: The maximum number of users to follow within a set timeframe (hours).
- **follow_timeframe_hours**: Time period in hours to apply the follow limit.
- **unfollow_after_hours**: Duration in hours after which followed users will be unfollowed.
- **blacklist**: List of usernames to ignore.
- **telegram**: Telegram bot configuration (optional).
- **discord**: Discord bot configuration (optional).

## Notes

- Be mindful of Instagram's API and rate limits. Excessive following could result in temporary bans on your account.
- Use this bot responsibly. Follow Instagram’s Terms of Service.

## License

This project is licensed under the MIT License.
