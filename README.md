
# InstaHashBot (IHB)

This Python bot automates the process of logging into your Instagram account, following users based on specific hashtags, liking their posts, and posting comments. It includes options to set a minimum threshold for followers and following counts, auto-unfollow users after a given timeframe, and supports Telegram and Discord (with bot or webhook integration) for sending notifications.

<p align="center">
  <img src="https://i.imgur.com/uoJtnP6.png" alt="InstaHashBot Logo" width="250"/>
</p>
<p align="center">
  <a href="https://github.com/SimpliAj/InstaHashBot/stargazers">
    <img src="https://img.shields.io/github/forks/SimpliAj/InstaHashBot?style=flat&logo=github&logoColor=whitesmoke&label=Forks" alt="GitHub repo stars"/>
    <img src="https://img.shields.io/github/stars/SimpliAj/InstaHashBot?style=flat&logo=github&logoColor=whitesmoke&label=Stars" alt="GitHub repo stars"/>
  </a>
</p>

## Features

- Follows users based on specified hashtags.
- Allows configuring a minimum number of followers and following for users to be followed.
- Automatically unfollows followed users after a specified number of hours.
- Auto-likes posts and comments on them.
- Supports multiple hashtags.
- Blacklists certain users to prevent following.
- Sends real-time updates to both Telegram and Discord channels.
- Limits the number of users followed per timeframe.
- Version checking to notify about new releases.

## Installation

### Prerequisites

- Python 3.x
- Instagram account
- Telegram bot (optional)
- Discord bot or webhook (optional)

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

Update the `config.yml` file with your Instagram login details, Telegram/Discord bot tokens, webhook details, and other settings.

```yaml
instagram:
  username: "your_instagram_username"
  password: "your_instagram_password"

settings:
  version: "1.0.0"
  max_follows: 5                  # Maximum number of users to follow per hashtag
  min_followers: 100               # Minimum number of followers a user must have
  min_following: 50                # Minimum number of accounts the user must be following
  follow_limit: 50                 # Maximum number of users to follow in X hours
  follow_timeframe_hours: 1        # Hours between follow operations
  unfollow_after_hours: 24         # Hours after which followed users will be unfollowed
  auto_like: true                  # Enable auto-liking of posts
  auto_comment: true               # Enable auto-commenting on posts
  max_likes_per_day: 20            # Maximum number of likes per day
  max_comments_per_day: 10         # Maximum number of comments per day

hashtags:
  - "webdevelopment"
  - "programming"
  - "python"

blacklist:
  - "user_to_ignore1"
  - "user_to_ignore2"

comments:
  - "Great post!"
  - "Love this!"
  - "Nice work!"

telegram:
  enabled: true                    # Enable/disable Telegram bot
  bot_token: "your_telegram_bot_token"
  chat_ids:                         # List of chat IDs to send notifications
    - "chat_id_1"
    - "chat_id_2"

discord:
  enabled: true                     # Enable/disable Discord bot/webhook
  use_webhook: false                # If true, use Discord webhook, otherwise use bot
  bot_token: "your_discord_bot_token"
  channel_ids:                      # List of Discord channel IDs for notifications
    - "channel_id_1"
    - "channel_id_2"
  webhook_url: "your_webhook_url"
  webhook_name: "InstaHashBot"      # Name to show for Discord webhook messages
  webhook_avatar_url: "your_avatar_url"  # Avatar URL for webhook messages (optional)
```

### Telegram Bot Setup (Optional)

1. Go to the [BotFather](https://t.me/botfather) in Telegram.
2. Create a new bot to get the `bot_token`.
3. Get your `chat_id` by sending a message to the bot and using an API request to retrieve your chat information.

### Discord Bot/Webhook Setup (Optional)

1. For bot: Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a bot.
2. Add the bot to your server and get the `channel_id` where you'd like notifications sent.
3. For webhook: Go to your Discord server settings, create a webhook, and get the `webhook_url`.

## Running the Bot

Once everything is configured, you can run the bot by executing:

```bash
python instagram_bot.py
```

The bot will log into your Instagram account, search for users using the specified hashtags, and follow users based on the configured rules.

## Example Output

The bot will send updates to both your Telegram and Discord accounts, providing details such as:

- Followed users
- Skipped users (if they don’t meet the follower/following requirements)
- Auto-likes and comments
- Unfollowed users after the specified timeframe

## Configuration Options

- **max_follows**: The maximum number of users to follow per hashtag.
- **min_followers**: The minimum number of followers required to follow a user.
- **min_following**: The minimum number of accounts the user must be following.
- **auto_like**: Enable or disable auto-liking of user posts.
- **auto_comment**: Enable or disable auto-commenting on user posts.
- **comments**: List of potential comments to post automatically.
- **unfollow_after_hours**: The time after which followed users will be unfollowed.
- **telegram**: Telegram bot configuration (optional).
- **discord**: Discord bot or webhook configuration (optional).

## Notes

- Be mindful of Instagram's API and rate limits.
- Use this bot responsibly. Follow Instagram’s Terms of Service.

## License

This project is licensed under the MIT License.
