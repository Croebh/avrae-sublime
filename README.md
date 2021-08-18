# Avrae Utilities for SublimeText
A plugin for [Sublime Text](https://www.sublimetext.com/) containing utilities for the [Avrae](https://avrae.io) Discord bot

## Important Note
This package makes a remote connection to the Avrae API in order to collect and update the information. It only does this by request, and will not make any outward connection without being prompted to by the user.

## Setup
In order for this plugin to have your permissions to grab and update your GVARs, Workshop Aliases, or Workshop Snippets, you need to give it your token.

1. Go to [Avrae](https://avrae.io) and log in to the dashboard
2. Press F12 to open the DevTools
3. Go to the 'Application' tab
4. On the left, select 'https://avrae.io' under 'Local Storage'
5. Copy the 'Value' next to the 'avrae-token' key
6. In Sublime Text, open the Command Pallete
7. Use the ``Preferences: Avrae Utilities Settings`` command, pasting in the copied token in the 'token' key

### Note
Please keep this token private, as anyone who gains access to this token could potentially gain access to your Discord account.

## Features
This plugin contains the following features:

### Draconic Syntax
Handy syntax highlighting for the Draconic language (Subset of Python) that Avrae uses for aliasing.

### Get and Update GVARs
Using the ``Avrae Utilities: Get GVAR`` and ``Avrae Utilities: Update GVAR`` commands in the Command Pallete, you can retrieve and update GVARs without the need to visit the dashboard.

### Workshop Collections
You can use ``Avrae Utilities: Get Collection Data`` to collect a json of all of the aliases and snippets ids within a collection. Save that as `collection.id` in the folder you wish to save your collection in. You can then retrieve each alias/snippet with ``Avrae Utilities: Get Workshop Alias``, which you can save as ``aliasName.alias``. If you wish to update them, you can run ``Avrae Utilities: Update Workshop Alias``. Support for editing the documentation will come in a future update.

### Copy Attack
If you have automation JSON written out, you can select it all and run the ``Avrae Utilities: Copy Attack`` command, and it will minify it, prepends ``!a import Test``, and copy it to your clipboard for easy testing within Discord.
![Converting an attack into a Discord Command](https://media.discordapp.net/attachments/666401385335750666/877409550733566002/2021-08-17_22-32-12.gif)