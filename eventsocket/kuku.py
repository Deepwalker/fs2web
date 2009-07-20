#!/usr/bin/env python
# coding: utf-8


from debug import debug

from Queue import Queue
from eventsocket import EventProtocol, superdict
from twisted.internet import reactor, protocol

import pprint

# Connect Django ORM
from django.core.management import setup_environ
import settings
setup_environ(settings)
from conference.models import *

port = 1905
unique_id = {}

conferences = {}
channels = {}

class InboundProxy(EventProtocol):
    def __init__(self):
	self.job_uuid = {}
	self.conf_msgs = Queue()
	EventProtocol.__init__(self)

    def authSuccess(self, ev):
        self.eventplain('CHANNEL_CREATE CHANNEL_DESTROY CUSTOM conference::maintenance conference::dtmf')

    def authFailure(self, failure):
	self.factory.reconnect = False

    def eventplainFailure(self, failure):
	self.factory.reconnect = False
	self.exit()

    def onChannelCreate(self,data):
        pprint.pprint(data)
        channels[data.Unique_ID] = data
        print channels
        self.api("uuid_dump %s"%data.Unique_ID)

    def onChannelDestroy(self,data):
        pprint.pprint(data)
        del channels[data.Unique_ID]
        print channels

    def apiSuccess(self, ev):
        # Update channel data with uuid_dump result
        raw = ev['data']['rawresponse']
        if '-ERR' == raw[:4]:
            print 'ERROR!'
            return
        temp = [line.strip().split(': ',1) for line in raw.strip().split('\n') if line]
        apidata = superdict([(line[0].replace('-','_'),line[1]) for line in temp])
        channels[apidata.Unique_ID].update(apidata)
        channel = channels[apidata.Unique_ID]
        kuku = channel.get('variable_kuku',None)
        print "Channel ",channel.Unique_ID,kuku

    def zaglushka(self):
        if context == 'conference':
            data = temp['data']
            if 1==1:
                self.conf_msgs.put(data)
                self.apiFailure(self,None)
                return
            #pprint.pprint(apidata)
            print "done, %s"%data.Unique_ID

            p = Participant.objects.filter(phone__number=data.Caller_Caller_ID_Number,
                    conference__number=data.Conference_Name)
            p = None
            print p
            if p:
                p=p[0]
                if data.Action == 'add-member':
                    p.active=True
                elif data.Action == 'del-member':
                    p.active=False
                elif data.Action == 'start-talking':
                    print "start talk"
                elif data.Action == 'stop-talking':
                    print "stop talk"
                elif data.Action == 'mute-member':
                    print "mute"
                elif data.Action == 'unmute-member':
                    print "unmute"
                p.save()

    def onCustom(self, data):
        #pprint.pprint(data)
        channels[data.Unique_ID].update(data)
        channel = channels[data.Unique_ID]

        if data.Event_Subclass == 'conference::dtmf':
            print data.conference
        elif data.Event_Subclass == 'conference::maintenance':
            print data.Action
            #self.conf_msgs.put({'data':data,'context':'conference'})
            #self.api("uuid_dump %s"%data.Unique_ID)
            if data.Action == 'add-member':
                if not data.Conference_Name in conferences:
                    conferences[data.Conference_Name] = {}
                conferences[data.Conference_Name][channel.Unique_ID]=channel
                pprint.pprint(conferences[data.Conference_Name])
            elif data.Action == 'del-member':
                if data.Conference_Name in conferences and channel.Unique_ID in conferences[data.Conference_Name]:
                    del conferences[data.Conference_Name][channel.Unique_ID]
                    if not conferences[data.Conference_Name]:
                        del conferences[data.Conference_Name]
                print channels
            elif data.Action == 'start-talking':
                print "start talk"
            elif data.Action == 'stop-talking':
                print "stop talk"
            elif data.Action == 'mute-member':
                print "mute"
            elif data.Action == 'unmute-member':
                print "unmute"

class InboundFactory(protocol.ClientFactory):
    protocol = InboundProxy

    def __init__(self, password):
	self.password = password
	self.reconnect = True

    def clientConnectionLost(self, connector, reason):
	if self.reconnect: connector.connect()
	else:
	    print '[inboundfactory] stopping reactor'
	    reactor.stop()

    def clientConnectionFailed(self, connector, reason):
	print '[inboundfactoy] cannot connect: %s' % reason
	reactor.stop()


if __name__ == '__main__':
    reactor.connectTCP('localhost', 8021, InboundFactory('ClueCon'))
    reactor.run()
