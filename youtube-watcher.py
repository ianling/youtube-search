#!/usr/bin/python3
from requests import get as requests_get
from json import loads, dumps
from sys import exit
from time import time
from datetime import datetime
from optparse import OptionParser

VERSION = '1.1'


##
# Makes a request to the Youtube Data API.
# Returns: A dict representation of the API's JSON response.
#
# Paramters:
# type = API resource type. Examples: 'videos', 'search', 'channelSections'
# **kwargs = API parameters. Examples: part=snippet, channelId=DDzlMA1Zlsmb12
##
def api_request(type=None, **kwargs):
    request_url = '%s/%s?key=%s' % (APIBASEURL, type, APIKEY)
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


option_parser = OptionParser(usage="Usage: %prog [options] [url1] [url2] ...", version="%%prog v%s" % VERSION)
option_parser.add_option('-q', '--quiet', action='store_false', dest='verbose', default=True,
                         help='Do not print informational messages to STDOUT, only print results')
option_parser.add_option('-u', '--url-only', action='store_true', dest='url_only', default=False,
                         help='Do not print titles or publication dates, only print Youtube URLs')
option_parser.add_option('-t', '--time', type='int', action='store', dest='time_published_arg', default=False,
                         help='Specify a UNIX timestamp to use as the time the script last checked the channels')
(options, args) = option_parser.parse_args()
verbose = options.verbose
url_only = options.url_only
time_published_arg = options.time_published_arg

YOUTUBEBASEURL = 'https://www.youtube.com/watch?v='
config_file_path = 'youtube-watcher.cfg'
APIBASEURL= 'https://www.googleapis.com/youtube/v3'
APIKEY = '!!!! YOUR API KEY HERE !!!!'

config_file = open(config_file_path, 'r')
config = loads(config_file.read())
config_file.close()

channels = config
# verify that metadata from config file exists
for channel, metadata in channels.items():
    if not metadata['id']:
        if verbose:
            print('Retrieving channel ID for %s... ' % (channel), end="")
        id = api_request(type='channels', part='id', forUsername=channel)['items'][0]['id']
        channels[channel]['id'] = id
        if verbose:
            print(id)
    if not metadata['last_checked']:
        channels[channel]['last_checked'] = time()

for channel, metadata in channels.items():
    if time_published_arg:
        timestampToUse = time_published_arg
    else:
        timestampToUse = metadata['last_checked']
    last_checked_pretty = format_timestamp(timestampToUse)
    if verbose:
        print('Retrieving new videos for %s. Last checked: %s...' % (channel, last_checked_pretty))
    results = api_request(type='search', channelId=metadata['id'], part='snippet', order='date', maxResults=50, publishedAfter=last_checked_pretty)
    channels[channel]['last_checked'] = time()
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
