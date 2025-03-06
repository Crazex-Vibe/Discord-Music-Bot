# Harmony - Discord Music Bot

Harmony is a Discord music bot built using `discord.py` that streams music from YouTube using `yt-dlp`. The bot is designed to be fast, responsive, and easy to use.

## Features
- Stream music from YouTube
- Play, pause, resume, and stop commands
- Queue system for song requests
- Volume control
- Skip and remove songs from the queue

## Requirements
- Python 3.10+
- `discord.py`
- `yt-dlp`
- `ffmpeg`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Crazex-Vibe/Discord-Music-Bot
   cd Discord-Music-Bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure `ffmpeg` is installed and accessible in your system PATH.

## Configuration
1. Create a `.env` file in the project directory and add your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
2. (Optional) Set up other configurations as needed.

## Running the Bot
Start the bot with:
```bash
python Harmony.py
```

## Commands
| Command | Description |
|---------|-------------|
| `!play <url>` | Plays a song from YouTube |
| `!pause` | Pauses the current song |
| `!resume` | Resumes the paused song |
| `!stop` | Stops playback and clears the queue |
| `!skip` | Skips the current song |
| `!queue` | Displays the current queue |
| `!remove <index>` | Removes a song from the queue |
| `!volume <0-100>` | Adjusts the volume |
| `!disconnect` | Disconnects the bot from voice chat |

## Contributing
Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

