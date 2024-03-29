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
Handy syntax highlighting for the Draconic language (Subset of Python) that Avrae uses for aliasing. Its set up to work automatically on `*.alias`, `*.snippet`, and `*.gvar` filetypes.

### Get and Update GVARs
Using the ``Avrae Utilities: Get GVAR`` and ``Avrae Utilities: Update GVAR`` commands in the Command Pallete, you can retrieve and update GVARs without the need to visit the dashboard. If you want to save them locally, you can use the file extension ``.gvar``, and include the ID for the GVAR anywhere in the rest of the file name. You can have labels/descriptions before or after the ID, allowing you to organize your GVARs.

### Workshop Collections
There various things you can do to grab and update workshop collections, within SublimeText.

#### Getting your collection info
You can use ``Avrae Utilities: Get Collection Data`` to collect a json of all of the aliases and snippets ids within a collection. This will ask you for a collection ID. You can find this by going to the collection on the Workshop, and looking at the url. Everything after ``avrae.io/dashboard/workshop/`` is your ID.

Once you've ran the ``Avrae Utilities: Get Collection Data`` command and given it your ID, save the result as `collection.id` in the folder you wish to save your collection in. 

![An image of the url to the Map Utilities collection, with the collection ID circled](https://media.discordapp.net/attachments/666401385335750666/877414197842030612/unknown.png)

> Now that you have the `collection.id`, if you run the ``Avrae Utilities: Get Collection Data`` command with it open, it will update the file.

#### Getting your collection descriptions
You can grab the markdown description of a collection with the ``Avrae Utilities: Get Collection Description`` command. If you have a `readme.md` file active and open, saved in a folder with a `collection.id`, it will grab the collection information from their. Otherwise, it will ask you for your collection ID.

#### Updating your collection descriptions
If you wish to update the description, you can run ``Avrae Utilities: Update Collection Description``, which will push the currently open `readme.md` to the workshop, using the `collection.id` that is saved to the same folder.

#### Getting your aliases/snippets
Inside the `collection.id`, will be a JSON containing the names and ids of each alias/subalias/snippet inside the collection. You can use the ID's within with the ``Avrae Utilities: Get Workshop Alias`` and ``Avrae Utilities: Get Workshop Snippet`` commands.

You can then retrieve each alias/snippet with ``Avrae Utilities: Get Alias``, which you can save as ``aliasName.alias``, replacing ``aliasName`` with the name of the actual alias or snippet.

> Once you save your alias/snippet in the folder with the `collection.id`, running the ``Avrae Utilities: Get Alias`` command with the alias open will grab the ID automatically from the `collection.id`. Neat!

#### Updating your aliases/snippets
If you wish to update them, you can run ``Avrae Utilities: Update Alias``, which will push the currently open alias to the workshop, using the `collection.id` that is saved to the same folder. It will then also update the currently active code version to the new one added by this command. After that, you're good to test it in Discord.

#### Updating and getting alias/snippet descriptions
You can also grab and update the descriptions for your alias and snippets, using the ``Avrae Utilities: Get Alias Description`` and ``Avrae Utilities: Update Alias Description`` (and their snippet equivalents). You can save as ``aliasName.md``, replacing ``aliasName`` with the name of the actual alias or snippet.

#### Folder Structure
Support for editing the documentation will come in a future update.

Here is an example collection folder structure:
```bash
root
 | # This is the folder your collection will live in
 ├ Collection Name
 | | # This contains the json collected by the `Get Collection Data` command
 | ├ collection.id 
 | | # This contains the markdown for the collection description
 | ├ readme.md 
 | | # This contains the alias itself, collected by the `Get Workshop Alias` command, and updated with the `Update Workshop Alias` command
 | ├ aliasName.alias 
 | | # This contains the markdown the alias description
 | ├ aliasName.md 
 | | # This contains the subalias alias itself, collected by the `Get Workshop Alias` command, and updated with the `Update Workshop Alias` command
 | ├ aliasName subAalias.alias 
 | | # This contains the markdown the alias description
 | ├ aliasName subAalias.md 
 | | # This contains the snippet itself, collected by the `Get Workshop Snippet` command, and updated with the `Update Workshop Snippet` command
 | ├ snippetName.snippet 
 | | # This contains the markdown the snippet description
 | └ snippetName.md 
```

### Copy Attack
If you have automation JSON written out, you can select it all and run the ``Avrae Utilities: Copy Attack`` command, and it will minify it, prepends ``!a import Test``, and copy it to your clipboard for easy testing within Discord.

![Converting an attack into a Discord Command](https://media.discordapp.net/attachments/666401385335750666/877409550733566002/2021-08-17_22-32-12.gif)