#!/usr/bin/env python
# coding: utf-8

import syslog

def debug(msg):
    print msg
    syslog.syslog(msg)
