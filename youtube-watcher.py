#!/usr/bin/python3
from requests import get as requests_get
from json import loads, dumps
from sys import exit
from time import time
from datetime import datetime

##
#
# type = resource type. Examples: 'videos', 'search', 'channelSections'
#
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

YOUTUBEBASEURL = 'https://www.youtube.com/watch?v='
config_file_path = 'youtube-watcher.cfg'
APIBASEURL= 'https://www.googleapis.com/youtube/v3'
APIKEY = '!!!!YOUR KEY HERE!!!!'

config_file = open(config_file_path, 'r')
config = loads(config_file.read())
config_file.close()

channels = config
# verify that metadata from config file exists
for channel, metadata in channels.items():
    if not metadata['id']:
        print('Retrieving channel ID for %s... ' % (channel), end="")
        id = api_request(type='channels', part='id', forUsername=channel).json()['items'][0]['id']
        channels[channel]['id'] = id
        print(id)
    if not metadata['last_checked']:
        channels[channel]['last_checked'] = time()

for channel, metadata in channels.items():
    last_checked_pretty = format_timestamp(channels[channel]['last_checked'])
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
        print('%s - %s - %s' % (timePublished, title, url))

graceful_exit()
