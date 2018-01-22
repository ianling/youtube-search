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
    
    $python3 youtube-watcher.py -t 1516519200 -q
    2018-01-22T14:00:05.000Z - The Binding of Isaac: AFTERBIRTH+ - Northernlion Plays - Episode 553 [Tunnel] - https://www.youtube.com/watch?v=ydE18mRyKPk
    2018-01-21T14:00:00.000Z - The Binding of Isaac: AFTERBIRTH+ - Northernlion Plays - Episode 552 [Classy] - https://www.youtube.com/watch?v=EoXGIzuezfQ
    $

# Arguments and Flags
    -q, --quiet = Suppress informational messages (for example, the "Retrieving..." messages above)
    -u, --url-only = Suppress video titles and publication dates, leaving only the video URL
    -t, --time = The UNIX timestamp to use as the time when the script last checked the channels for new videos
    
# Examples
You can feed the list of URLs this script returns into another program, like [youtube-dl](https://github.com/rg3/youtube-dl/).

    for url in $(python3 youtube-watcher.py -qu); do 
        /usr/local/bin/youtube-dl -f 22 $url;
    done
