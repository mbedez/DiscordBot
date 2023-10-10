# FafBot
***
[Intro](#What-is-FafBot) - [Commands](#What-can-you-do-with-it) - [Setup](#What-do-you-need-in-order-to-set-FafBot-up) - [The future of FafBot](#What-is-the-future-of-FafBot)
***
## What is FafBot?
FafBot is a small project I made for fun using discord and discord and riot API.
***
## What can you do with it?
Here's a list of different things you could do with this bot:
- **&help** => Gives you all the different available commands.
- **&random** *int* => Gives you a random number **between 1 and the number provided**.
- **&dice** ( Optional : *int* ) => Gives you a random number **between 1 and 6, displayed as an emoji.**  
  If you provided an int, the returned number will be between 1 and the int. It must be less or equal to 6.
- **&poll** => Add positive and negative reactions to the previous message.
- **&shifumi** => Add stone, paper and scissors reactions to the previous message.
- **&supp** *int* => Delete the last *int* messages.
- **&lolaccount** *summoner_name* => give you the level, all his ranks, the number of aram and the date of his last aram of the summoner.
- **&lolhisto** *summoner_name* ( Optional : *nb_of_game (<=30)* *queue (soloq or flex)*) => give you the last nb_of_game of the summoner with the result (win or lose, kda) and the played champion.
- **/play** *youtube url or research* => Play the audio on your current audio channel. (Can also play playlist)
- **/seek** *Go to indicated timecode on the current song*

- The Bot also send a random definition of a french word every day on a specific channel you set for.
***
## What do you need in order to set FafBot up?
FafBot runs in python with the help of the **pycord** package. In order to run the bot, you will need a few things :
- python3 (*of course*)
- ffmpeg
- py-cord : A library used to communicate between python and discord API, fork of discord.py
- python-dotenv : A library used to secure your **config file**
- requests : A library used to make https requests
- yt-dlp : A library used to dl the audio of a youtube video
- PyNaCl : A library to play audio
- Pillow : A library used to edit an image
- bs4 : A library used to parse html
- apscheduler : A library used to schedule a task
- a *config* file containing your **discord Token** and your **Riot API Key**


You can use the Dockerfile to buid an Alpine Docker image for Raspberry pi 4 with `docker build -t your/tag .`.
You can also use `pip install -r requirements.txt` to install the necessary libraries.

***
## What is the future of FafBot
Nothing else than corrections and improvements.
