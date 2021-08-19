# Description:
Modifies the save files of Carrier Command 2.  Currently it adds island-typed blueprints to islands without any, adds additional island-typed blueprints (avoiding duplicates if possible and using random choice if not) to difficult islands, and finally pairs up any ammo or turrets that are missing the other half of what you'd need to use them.

# Requirements:
At least Python 3 - I tested on python 3.7.4 and 3.8.10 (which works better due to xml parser ordering differences) - it's probably already on your computer though
Knowing where the save files are - start looking in %appdata%\Carrier Command 2\
  persistant_data.xml tells you which folder matches with which save game name
  then navigate to the save folder itself so you can see the save.xml.

# How to use:
Run the script (I use 'python AddBlueprintsToSaves.py' in the same directory as the save.xml you wish to modify.
It will produce some output to the console telling you what it's doing, and also a moddedsave.xml.  
Take a backup of the original (or not, if you love danger!) and then rename moddedsave.xml to save.xml
