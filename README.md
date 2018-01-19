# youtube-watcher
Python 3 script that monitors channels for new uploads.

Allows you to specify which channels to monitor, as well as keywords to look for in video titles. If a video title does not contain any of your keywords, the script will ignore it.

# Usage
Put your Youtube Data API key in youtube-watcher.py:

    APIKEY = '!!!!YOUR KEY HERE!!!!'
    
Then, edit the config file to your liking. You do not need to fill in a channel ID, as the script will automatically retrieve those based on the username. The keywords are case-insensitive. 

After that, run the script:

    $python3 youtube-watcher.py
    Retrieving channel ID for baertaffy... UCCG6qI8XjyjUNgZ8jlJp_wQ
    Retrieving channel ID for northernlion... UC3tNpTOHsTnkmbwztCs30sA
    Retrieving new videos for baertaffy. Last checked: 2018-01-19T20:26:06Z...
    {...}
    Retrieving new videos for northernlion. Last checked: 2018-01-19T20:26:06Z...
    {...}
    $
