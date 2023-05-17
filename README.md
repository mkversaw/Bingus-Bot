# Bingus-Bot

Discord bot built using Discord.py for posting cat memes. The bot includes a leveling system that rewards users with experience points for sending messages. Once a user reaches a certain amount of experience points, they level up and receive a notification in the chat. Users can also display the Spotify listening activity of others.

## Features

- **Level System**: Users earn experience points by sending messages, and their level increases as they accumulate experience.
- **Ranking**: Users can check their own or another user's level and experience points.
- **Random Cat Memes**: The bot can post random pictures of the Bingus or Floppa memes upon command.
- **Spotify Listening**: The bot can display the songs a user is listening to on Spotify.

## Requirements

- Python 3.8 or higher
- discord.py library
- dotenv library (you'll need your own Discord developer token!)

## Setup

1. Clone the repository or download the source code.
2. Install the required dependencies
3. Create a `.env` file in the project directory and add the following line:
   ```
   TOKEN=YOUR_DISCORD_BOT_TOKEN
   ```
   Replace `YOUR_DISCORD_BOT_TOKEN` with your own Discord bot token.
4. Prepare the image directories:
   - Inside the `images` directory, there are two subdirectories: `bingus` and `floppa`.
   - Place your own images in the respective subdirectories, or create new subdirectories as needed.
5. Run the bot using the following command:
   ```
   python main.py
   ```

## Usage

- To post a random picture of a cat meme, use the following command:
  ```
  $bingus bingus
  ```
  or
  ```
  $bingus floppa
  ```
  
- To check your own level and experience points, use the following command:
  ```
  $bingus level
  ```
- To check another user's level and experience points, mention the user when using the command:
  ```
  $bingus level @username
  ```
- To see what songs a user is listening to on Spotify, use the following command:
  ```
  $bingus listen
  ```
  or
  ```
  $bingus listen @username
  ```

## Contributing

Contributions are welcome!
If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [GNU GPL 3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
