# Piazza Bot (v2)
This is a refactored version of the original piazza bot. This repo should contain a well documented and maintained bot

This project is devided into 2 parts. The bot and the machine learning. The bot is responsible
for continueously monitor the web as well as scrubbing the web when necessary. The machine
learning part is suppose to take in data and return two closest post and confidence,
one from all the data gathered from previous years and another from the current year.

# Installation
To intall dependencies, type `pip install -r requirements.txt`

# Dependencies
[piazza-api](https://github.com/hfaran/piazza-api)

Thanks to the open source apis included above to make everything work!!

# Development
Sub projects are devided into 2 parts as described (bot and ml). Individual sub projects
have their own folder within the piazza-bot folder. The data generated is in the /data
folder of the root directory

