#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 16:10:34 2017

@author: hp
"""

import json
import mimeparse #pip install python-mimeparse
import requests
import urllib
from pprint import pprint
import config

API_KEY = config.meetup_api_key

MEETUP_API_HOST = 'https://api.meetup.com'
EVENTS_URL = MEETUP_API_HOST + '/2/events.json'
MEMBERS_URL = MEETUP_API_HOST + '/2/members.json'
GROUPS_URL = MEETUP_API_HOST + '/2/groups.json'
RSVPS_URL = MEETUP_API_HOST + '/2/rsvps.json'
PHOTOS_ULR = MEETUP_API_HOST + '/2/photos.json'
GROUP_URLNAME = 'London-Machine-Learning-Meetup'

#access Internet by VPN
if config.VPN:
    import socks
    import socket
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo


class MeetupAPI(object):
    def __init__(self , api_key , num_past_events = 10 , http_timeout = 5 , http_retries = 2):
        self.api_key = api_key
        self._http_timeout = http_timeout
        self._http_retries = http_retries
        self._num_past_events = num_past_events
        
    def get_past_events(self):
        params = {
                    'key':self.api_key,
                    'group_urlname':GROUP_URLNAME,
                    'status' : 'past',
                    'desc':'true'
                }
        if self._num_past_events:
            params['page'] = str(self._num_past_events)
            
        query = urllib.urlencode(params)
        url = '{0}?{1}'.format(EVENTS_URL , query)
        #url like:
        #https://api.meetup.com/2/events.json?status=past&desc=true&page=10&key=1f2e6a39576142177a5b7e3c535c5747&group_urlname=London-Machine-Learning-Meetup

        response = requests.get(url , timeout = self._http_timeout)
        data = response.json()
        #print data
        return data['results']
    def get_members(self):
        params = {
                    'key':self.api_key,
                    'group_urlname':GROUP_URLNAME,
                    'offset':'0',
                    'format':'json',
                    'page':'100',
                    'order':'name'
                }
        query = urllib.urlencode(params)
        url = '{0}?{1}'.format(MEMBERS_URL , query)
        response = requests.get(url , timeout = self._http_timeout)
        data = response.json()['results']
        return data
    def get_groups_by_member(self , member_id = '38680722'):
        params = {
                    'key':self.api_key,
                    'member_id':member_id,
                    'offset':'0',
                    'format':'json',
                    'page':'100',
                    'order':'id'
                }
        query = urllib.urlencode(params)
        url = '{0}?{1}'.format(GROUPS_URL , query)
        response = requests.get(url , timeout=self._http_timeout)
        data = response.json()['results']
        return data
    
    
#test
m = MeetupAPI(API_KEY)
last_meetups = m.get_past_events()
print '=================================='
#pprint(last_meetups)
pprint(m.get_members())
#endtest