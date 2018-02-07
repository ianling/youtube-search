#!/usr/bin/python3
from requests import get as requests_get
from json import loads, dumps
from sys import exit
from time import time
from datetime import datetime
from optparse import OptionParser

VERSION = '1.2'


# Makes a request to the Youtube Data API.
# Returns: A dict representation of the API's JSON response.
#
# Paramters:
# type = API resource type. Examples: 'videos', 'search', 'channelSections'
# **kwargs = API parameters. Examples: part=snippet, channelId=DDzlMA1Zlsmb12
def api_request(request_type=None, **kwargs):
    request_url = '%s/%s?key=%s' % (APIBASEURL, request_type, APIKEY)
    return requests_get(request_url, params=kwargs).json()


def write_config():
    config_pretty = dumps(config, indent=4, sort_keys=True)
    config_file = open(config_file_path, 'w')
    config_file.write(config_pretty)
    config_file.close()


def graceful_exit():
    write_config()
    exit()


# puts the UNIX timestamp in the RFC 3339 format that YouTube requires
def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')


def print_if_verbose(message, end="\n"):
    if verbose:
        print(message, end=end)


def getChannelId(username):
    print_if_verbose('Retrieving channel ID for %s... ' % (username), end="")
    id = api_request(request_type='channels', part='id', forUsername=username)['items'][0]['id']
    print_if_verbose(id)
    return id


option_parser = OptionParser(usage="""Usage: %prog [options] [channelID_1] [channelID_2] ...""", version="%%prog v%s" % VERSION)
option_parser.add_option('-q', '--quiet', action='store_false', dest='verbose', default=True,
                         help='Do not print informational messages to STDOUT, only print results')
option_parser.add_option('-u', '--url-only', action='store_true', dest='url_only', default=False,
                         help='Do not print titles or publication dates, only print Youtube URLs')
option_parser.add_option('-c', '--config', action='store', dest='config_file_path', default='youtube-search.cfg', metavar='FILE',
                         help='Specify a configuration file to use')
option_parser.add_option('-i', '--ignore-config', action='store_false', dest='use_config', default=True,
                         help='Ignore config file')
option_parser.add_option('-s', '--search-query', action='store', dest='search_query', default=False, metavar='QUERY',
                         help='Specify a search query to use')
option_parser.add_option('-U', '--usernames', action='store_true', dest='search_by_usernames', default=False,
                         help='Treat any command-line arguments as usernames, rather than channel IDs')
option_parser.add_option('-t', '--time', type='int', action='store', dest='time_published_arg', default=None, metavar='TIMESTAMP',
                         help='Specify a UNIX timestamp to use as the time the script last checked the channels')
option_parser.add_option('-k', '--keyword', action='append', dest='keywords', default=[],
                         help="Specify a keyword to check the video's title against. You can use -k multiple times to specify several keywords")
option_parser.add_option('-n', '--max-videos', type='int', action='store', dest='max_videos', default=50, metavar='NUM',
                         help='Specify the maximum number of videos to return per channel. Max: 50')
(options, args) = option_parser.parse_args()
verbose = options.verbose
url_only = options.url_only
config_file_path = options.config_file_path
use_config = options.use_config
search_query = options.search_query
search_by_usernames = options.search_by_usernames
time_published_arg = options.time_published_arg
keywords = options.keywords
max_videos = options.max_videos

# globals
YOUTUBEBASEURL = 'https://www.youtube.com/watch?v='
APIBASEURL= 'https://www.googleapis.com/youtube/v3'
APIKEY = '!!! YOUR API KEY HERE !!!'

if use_config:
    config_file = open(config_file_path, 'r')
    config = loads(config_file.read())
    config_file.close()
    channels = config
    for channel, metadata in channels.items():
        current_time = time()
        # verify that metadata from config file exists
        if not metadata['id']:
            channels[channel]['id'] = getChannelId(channel)
        if not metadata['last_checked']:
            channels[channel]['last_checked'] = current_time
        if time_published_arg:
            timestampToUse = time_published_arg
        else:
            timestampToUse = channels[channel]['last_checked']
        last_checked_pretty = format_timestamp(timestampToUse)
        channels[channel]['last_checked'] = current_time

        print_if_verbose('Retrieving new videos for %s. Last checked: %s (%i)...' % (channel, last_checked_pretty, timestampToUse))
        results = api_request(request_type='search', channelId=metadata['id'], type='video', part='snippet', order='date', maxResults=max_videos, publishedAfter=last_checked_pretty)
        for result in results['items']:
            title = result['snippet']['title']
            if not any(keyword.lower() in title.lower() for keyword in metadata['keywords']):
                continue
            timePublished = result['snippet']['publishedAt']
            id = result['id']['videoId']
            url = YOUTUBEBASEURL + id
            if url_only:
                print(url)
            else:
                print('%s - %s - %s' % (timePublished, title, url))
    graceful_exit()

else:
    # searching by username/channel IDs
    if len(args) > 0:
        if search_by_usernames:
            ids = []
            for username in args:
                ids.append(getChannelId(username))
        else:
            ids = args
        if len(ids) < 1:
            exit('ERROR: Unable to retrieve channel IDs from input: %s' % (', '.join(args)))
        if time_published_arg:
            time_published_pretty = format_timestamp(time_published_arg)
        else:
            time_published_pretty = format_timestamp(0)
        for channelId in ids:
            results = api_request(request_type='search', channelId=channelId, q=search_query, type='video', part='snippet', order='date', maxResults=max_videos, publishedAfter=time_published_pretty)
            for result in results['items']:
                title = result['snippet']['title']
                if len(keywords) > 0:
                    if not any(keyword.lower() in title.lower() for keyword in keywords):
                        continue
                timePublished = result['snippet']['publishedAt']
                id = result['id']['videoId']
                url = YOUTUBEBASEURL + id
                if url_only:
                    print(url)
                else:
                    print('%s - %s - %s' % (timePublished, title, url))
        exit()
    # searching by general search query
    else:
        if not search_query:
            exit('ERROR: No query entered (-s/--search-query)')
        if time_published_arg:
            time_published_pretty = format_timestamp(time_published_arg)
        else:
            time_published_pretty = format_timestamp(0)
        results = api_request(request_type='search', q=search_query, type='video', part='snippet', order='date', maxResults=max_videos, publishedAfter=time_published_pretty)
        for result in results['items']:
            title = result['snippet']['title']
            if len(keywords) > 0:
                if not any(keyword.lower() in title.lower() for keyword in keywords):
                    continue
            timePublished = result['snippet']['publishedAt']
            id = result['id']['videoId']
            url = YOUTUBEBASEURL + id
            if url_only:
                print(url)
            else:
                print('%s - %s - %s' % (timePublished, title, url))
        exit()
