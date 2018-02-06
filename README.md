# youtube-search
Python 3 Youtube search client.

Allows you to perform Youtube search queries via the command line, or set up a config file to monitor certain channels for new uploads with titles that match keywords you specify.

    $ python3 youtube-search.py -h
    Usage: youtube-search.py [options] [channelID_1] [channelID_2] ...
    
    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -q, --quiet           Do not print informational messages to STDOUT, only
                            print results
    -u, --url-only        Do not print titles or publication dates, only print
                            Youtube URLs
    -c FILE, --config=FILE
                            Specify a configuration file to use
    -i, --ignore-config   Ignore config file
    -s QUERY, --search-query=QUERY
                            Specify a search query to use
    -U, --usernames       Treat any command-line arguments as usernames, rather
                            than channel IDs
    -t TIMESTAMP, --time=TIMESTAMP
                            Specify a UNIX timestamp to use as the time the script
                            last checked the channels
    -k KEYWORDS, --keyword=KEYWORDS
                            Specify a keyword to check the video's title against.
                            You can use -k multiple times to specify several
                            keywords
    -n NUM, --max-videos=NUM
                            Specify the maximum number of videos to return per
                            channel. Max: 50

# Usage - Command Line
The following command ignores the config file (-i), and instead searches for "northernlion live" (-s) on the channel with the username (-U) "northernlion," returning a maximum of 10 videos (-n) that were uploaded after the timestamp 1516812426 (-t).

    $ python3 youtube-search.py -i -s 'northernlion live' -n 10 -U -t 1516812426 northernlion
    Retrieving channel ID for northernlion... UC3tNpTOHsTnkmbwztCs30sA
    2018-02-03T05:23:47.000Z - The Northernlion Live Super Show! [January 31st, 2018] - https://www.youtube.com/watch?v=kghWo_stK_4
    2018-01-31T02:58:33.000Z - The Northernlion Live Super Show [January 29th, 2018] - https://www.youtube.com/watch?v=Cb6HWfTupOw
    2018-01-28T00:43:09.000Z - The Northernlion Live Super Show! [January 25th, 2018] - https://www.youtube.com/watch?v=_IOlv8T3_4c
    2018-01-26T06:34:31.000Z - The Northernlion Live Super Show! [January 24th, 2018] - https://www.youtube.com/watch?v=6yVWG9Aevq4

# Usage - Config File
Edit the config file to your liking using the format given in the repo's example config. You do not need to fill in a channel ID, as the script will automatically retrieve those based on the username. The keywords are case-insensitive. 

After that, run the script:

    $python3 youtube-search.py
    Retrieving channel ID for baertaffy... UCCG6qI8XjyjUNgZ8jlJp_wQ
    Retrieving channel ID for northernlion... UC3tNpTOHsTnkmbwztCs30sA
    Retrieving new videos for baertaffy. Last checked: 2018-01-19T20:26:06Z...
    {...}
    Retrieving new videos for northernlion. Last checked: 2018-01-19T20:26:06Z...
    {...}
    
    $python3 youtube-search.py -t 1516519200 -q
    2018-01-22T14:00:05.000Z - The Binding of Isaac: AFTERBIRTH+ - Northernlion Plays - Episode 553 [Tunnel] - https://www.youtube.com/watch?v=ydE18mRyKPk
    2018-01-21T14:00:00.000Z - The Binding of Isaac: AFTERBIRTH+ - Northernlion Plays - Episode 552 [Classy] - https://www.youtube.com/watch?v=EoXGIzuezfQ
    
# Examples
You can feed the list of URLs this script returns into another program, like [youtube-dl](https://github.com/rg3/youtube-dl/).

    for url in $(python3 youtube-watcher.py -qu); do 
        /usr/local/bin/youtube-dl -f 22 $url;
    done
