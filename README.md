# FafBot
***
[Intro](#What-is-FafBot) - [Commands](#What-can-you-do-with-it) - [Setup](#What-do-you-need-in-order-to-set-FafBot-up) - [The future of FafBot](#What-is-the-future-of-FafBot)
***
## What is FafBot?
FafBot is a small project I made to learn the *discord.py* python package.
His features are pretty basic, but they were a good way for me to get my hands on this package.
***
## What can you do with it?
Here's a list of different things you could do with this bot:
- **&help** => Gives you all the different available commands.
- **&random** *int* => Gives you a random number **between 1 and the number provided**.
- **&dice** ( Optional : *int* ) => Gives you a random number **between 1 and 6, displayed as an emoji.**  
  If you provided an int, the returned number will be between 1 and the int. It must be less or equal to 6.
- **&morpion** => A basic **tic-tac-toe** game you can play in chat.
- **&poll** *"question"* *first_option* *second_option* => Makes a poll that everyone can respond to.
- **&delete** *int* => Delete the last *int* messages.
- **&lolaccount** *summoner_name* => give you the level of the summoner and all his ranks.
- **&lolhisto** *summoner_name* ( Optional : *nb_of_game (<=30)* *queue (soloq or flex)*) => give you the last nb_of_game of the summoner with the result (win or lose, kda) and the played champion.
- **&lolaram** *summoner_name* => give you the number of aram the summoner did and the date of his last aram.
***
## What do you need in order to set FafBot up?
FafBot runs in python with the help of the **pycord** package. In order to run the bot, you will need a few things :
- python3 (*of course*)
- pycord : A library used to communicate between python and discord API, fork of discord.py
- dotenv : A library used to secure your **config file**
- requests : A library used to make https requests
- a *config* file containing your **discord Token** and your **Riot API Key**

You can use `pip install -r requirements.txt` to install the necessary libraries.

***
## What is the future of FafBot
idk