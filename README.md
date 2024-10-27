
# InstaHashBot (IHB)

This Python bot automates the process of logging into your Instagram account and interacting with users based on specific hashtags. It includes options to follow, like, and comment on posts, while also providing options to filter users and prevent excessive actions. The bot supports Telegram and Discord for real-time notifications.

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
- Likes posts related to specified hashtags.
- Comments on posts using predefined text templates.
- Allows configuring a minimum number of followers and following for users to be followed.
- Blacklists certain users to prevent following.
- Sends real-time updates to both Telegram and Discord channels.
- Limits the number of users followed per time frame.
- Allows specifying how long to wait before unfollowing users.
- Configurable via `config.yml` for easy customization.

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

Update the `config.yml` file with your Instagram login details, Telegram/Discord bot tokens, and other settings.

## Running the Bot

Once everything is configured, you can run the bot by executing:

```bash
python main.py
```

The bot will log into your Instagram account, search for users using the specified hashtags, and follow, like, and comment based on the configured rules.

## Notes

- Be mindful of Instagram's API and rate limits. Excessive interactions could result in temporary bans on your account.
- Use this bot responsibly. Follow Instagram’s Terms of Service.

## License

This project is licensed under the MIT License.
