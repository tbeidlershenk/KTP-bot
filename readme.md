# KTP-bot

This repository contains a Discord bot implemented using [Disnake-Docker](https://github.com/jlgingrich/Disnake-Docker).

## Use

```bash
git clone https://github.com/tbeidlershenk/KTP-bot.git
```

The simplest way to start a container running a bot registered with [Discord](https://discord.com/developers/applications) is by creating an `.env` file.

The `.env` file contains the `DISCORD_TOKEN` used by the bot to connect to Discord and can contain other environment variables used to modify the image. See [example.env](./example.env) for the other suggested environment variables. If the `.env` file is misconfigured, the container will receive an error and indicate which environment variable needs adjustment.

Once the `.env` file is configured, you can run `docker compose up`.
