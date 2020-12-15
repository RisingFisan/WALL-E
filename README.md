# WALL-E

A [discord](https://discord.com) bot written in [Python](https://www.python.org) using the [discord.py API](https://discordpy.readthedocs.io/en/latest/api.html).

![WALL-E](db/WALL-E.png)

## Installation

First of all, make sure you have the latest version of Python installed on your system, but any version above Python 3.5 should work. If you don't have Python installed, you can use one of the following commands:

### Windows (with choco)

`choco install python`

### Ubuntu/Debian

`sudo apt install python3`

### Fedora

`sudo dnf install python3`

### Arch Linux

`sudo pacman -S python`

Alternatively, you can download it from [here](https://www.python.org/downloads/).

With Python installed, we need to install **pip**, Python's package manager. If you used the official installer from python.org or **choco**, you should already have pip installed. Otherwise, you can use one of these commands to install it:

### Ubuntu/Debian

`sudo apt install python3-pip`

### Fedora

`sudo dnf install python3-pip`

### Arch Linux

`sudo pacman -S python-pip`

Now we can install the **discord.py<span></span>** extension, required to run the bot. To do that, run the following command:

`pip install --user discord.py`

**NOTE:** Replace *pip* with *pip3* if you're on Ubuntu/Debian/Fedora or any distro that uses pip3 for Python 3.

**OPTIONAL**: To use all the bot's features, you'll also need the **openCV** and **NumPy** packages. Install them the same way as **discord.py<span></span>**: `pip install --user opencv-python numpy`

## Running

To run the bot you need to get a **discord bot token**. You can obtain one by creating an application [here](https://discord.com/developers/applications). From there, you should see a **Bot** tab on the left. In there you can find your bot token. **DON'T SHARE THIS TOKEN WITH ANYONE OR UPLOAD IT ANYWHERE PUBLIC.** Now you can place your bot token in a file called "auth" (you'll have to create it) in WALL-E's root directory.

Now that everything is set up, you can finally run WALL-E! All you need to do is:

`python bot.py`

in the bot's root directory. Try to replace *python* with *python3* if you get any errors.

If all goes well, you should now have your own WALL-E! As an additional goal, you can try to [run it as a service](https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6), so you don't have to manually start it everytime you boot your machine.

## Features

WALL-E has a plethora of features, including, but not limited to:

- Displaying the server's info.
- Displaying a user's avatar.
- A cooldown (makes a user unable to use the bot for X time).
- A punishment command (mutes a user in all text channels).
- A COVID-19 based game with a custom role (you can cough and give other people COVID-19, or cure them of the disease).
- A command that "UwUifies" a message.
- A command to generate a random quote based on the user's recent message history.
- Commands to mute/unmute everyone in a voice channel.
- [EXPERIMENTAL] A command that overlays an emoji over faces in a picture (Requires openCV and NumPy).

You can also create folders called "gifs" or "images" in the bot's root directory and place GIFs and images, respectively, in them. Then you can use the picture/GIF's name as a command that will send it as a message.

Another optional feature is an anti hate speech filter, that will delete any messages containing one or more words from a list of words. To enable it, simply create a "bad_words.txt" file in the bot's root directory and add the words you want to ban in your server, one per line. The detector takes spaces and other special characters into account, so if you ban the word "avocado" and someone types "av oc.a-do", it will get flagged by the filter.


