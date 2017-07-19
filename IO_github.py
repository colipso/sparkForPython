#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 21:22:06 2017

@author: hp
"""


#https://developer.github.com/v3/
from github import Github #pip install pygithub

#access Internet by VPN

import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

import config
from pprint import pprint
import time


ACCESS_TOKEN =config.gitAccessToken

USER = 'apache'
REPO = 'spark'

g = Github(ACCESS_TOKEN , per_page = 100)
user = g.get_user(USER)
repo = user.get_repo(REPO)

repos_apache = [r.name for r in user.get_repos()]
pprint(repos_apache)
time.sleep(10)

print "===output  spark languages====="
pprint(repo.get_languages())
time.sleep(10)

print "===output  stargazers====="
stargazers = [ s for s in repo.get_stargazers()]
pprint([stargazers[i] for i in range(20)])

