#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
sys.path.append("/root/")

from supermegazord.db import users

try:    nids = open(sys.argv[1], 'r')
except: nids = open('/dev/stdin', 'r')
try:	logins = open(sys.argv[2], 'w')
except: logins = open('/dev/stdout', 'w')

for nid in nids:
	logins.write(users.nid_to_login(nid.strip()) + "\n")
