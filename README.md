# Avrae Utilities for SublimeText
A plugin for [Sublime Text|https://www.sublimetext.com/] containing utilities for the [Avrae|https://avrae.io] Discord bot

## Setup
In order for this plugin to have your permissions to grab and update your GVARs (and in the future, workshop aliases), you need to give it your token.

1. Go to [Avrae|https://avrae.io] and log in to the dashboard
2. Press F12 to open the DevTools
3. Go to the 'Application' tab
4. On the left, select 'https://avrae.io' under 'Local Storage'
5. Copy the 'Value' next to the 'avrae-token' key
6. In Sublime Text, open the Command Pallete
7. Use the ``Avrae: Set Token`` command, pasting in the copied token

## Features
This plugin contains the following features:

### Draconic Syntax
Handy syntax highlighting for the Draconic language (Subset of Python) that Avrae uses for aliasing.

### Get and Update GVARs
Using the ``Avrae: Get GVAR`` and ``Avrae: Update GVAR`` commands in the Command Pallete, you can retrieve and update GVARs without the need to visit the dashboard.

### Copy Attack
If you have automation written out, you can select it all and run the ``Avrae: Copy Attack`` command, and it will minify it, prepend ``!a import Test``, and copy it to your clipboard for easy testing within Discord.