# FafBot
***
[Intro](#What\ is\ FafBot?) - [Commands](#What\ can\ you\ do\ with\ it?) - [Setup](#What\ do\ you\ need\ in\ order\ to\ set\ FafBot\ up?) - [The future of FafBot](#What\ is\ the\ future\ of\ FafBot)
***
## What is FafBot?
FafBot is a small project I made to learn the *discord.py* python package.
His features are pretty basic, but they were a good way for me to get my hands on this package.
***
## What can you do with it?
Here's a list of different things you could do with this bot:
- **&help** => Gives you all the different available commands.
- **&random** *int* => Gives you a random number **between 1 and the number provided**. A number inferior or equal to 6 would be displayed as an emoji.
- **&morpion** => A basic **tic-tac-toe** game you can play in chat.
- **&poll** *"question"* *first_option* *second_option* => Makes a poll that everyone can respond to.
- **&delete** *int* => Delete the last *int* messages.
***
## What do you need in order to set FafBot up?
FafBot runs in python with the help of the **pycord** package. In order to run the bot, you will need a few things :
- python3 (*of course*)
- pycord : `pip install py-cord`
- dotenv : `pip install python-dotenv`
- a *config* file containing your **discord Token**
***
## What is the future of FafBot
I would like to add a feature : `&worst_kda "user" int` which would connect to the league of legends API and give back the **worst kda** from the *int* last games **on a given user**.

I also would like to improve the **morpion**, **delete** and **help** functions