#!/usr/bin/env python
# coding: utf-8

# Connect Django ORM
from django.core.management import setup_environ
import settings
setup_environ(settings)
from conference.models import *

from debug import debug

from Queue import Queue
from eventsocket import EventProtocol, superdict
from twisted.internet import reactor, protocol

import pprint

port = 1905
unique_id = {}

class InboundProxy(EventProtocol):
    def __init__(self):
	self.job_uuid = {}
	self.conf_msgs = Queue()
	EventProtocol.__init__(self)

    def authSuccess(self, ev):
        self.eventplain('CUSTOM conference::maintenance conference::dtmf')

    def authFailure(self, failure):
	self.factory.reconnect = False

    def eventplainFailure(self, failure):
	self.factory.reconnect = False
	self.exit()

    def apiSuccess(self, ev):
        #debug("api %s"%ev)
        temp = self.conf_msgs.get()
        context = temp['context']

        if context == 'conference':
            data = temp['data']
            raw = ev['data']['rawresponse']
            if '-ERR No Such Channel' in raw:
                self.conf_msgs.put(data)
                self.apiFailure(self,None)
                return
            apidata = superdict([[elem.replace('-','_') for elem in line.strip().split(': ',1)] 
                        for line in raw.strip().split('\n') if line])
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


    def apiFailure(self, failure):
        data = self.conf_msgs.get()
        debug("It seems that UUID %s is gone"%data.Unique_ID)

    def onCustom(self, data):
        pprint.pprint(data)
        if data.Event_Subclass == 'conference::dtmf':
            print data.conference
        elif data.Event_Subclass == 'conference::maintenance':
            print data.Action
            self.conf_msgs.put({'data':data,'context':'conference'})
            self.api("uuid_dump %s"%data.Unique_ID)

            if data.Action == 'add-member':
                print "member added", data.Member_ID
            elif data.Action == 'del-member':
                print "member deleted"
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

class OutboundProxy(EventProtocol):
    def __init__(self):
	self.ext = None
	self.debug_enabled = False
	EventProtocol.__init__(self)

    # when we get connection from fs, send "connect"
    def connectionMade(self):
	self.connect()

    # when we get OK from connect, send "myevents"
    def connectSuccess(self, ev):
	self.ext = unique_id[ev.Unique_ID]
	print '[outboundproxy] started controlling extension %s' % self.ext
	self.myevents()

    # after we get OK for myevents, send "answer".
    def myeventsSuccess(self, ev):
        self.answer()

    # when we get OK from answer, play something. Note: on default FreeSWITCH
    # deployments, the sounds directory is usually /usr/local/freeswitch/sounds
    def answerSuccess(self, ev):
	print '[outboundproxy] going to play audio file for extension %s' % self.ext
	self.playback('/opt/freeswitch/sounds/en/us/callie/ivr/8000/ivr-sample_submenu.wav',
	    terminators='123*#')

    # well well...
    def onDtmf(self, data):
	print '[outboundproxy] got dtmf "%s" from extension %s' % (data.DTMF_Digit, self.ext)

    # finished executing something
    def onChannelExecuteComplete(self, data):
	app = data.variable_current_application
	if app == 'playback':
	    terminator = data.get('variable_playback_terminator_used')
            response = data.get('variable_current_application_response')
	    print '[outboundproxy] extension %s finished playing file, terminator=%s, response=%s' % (self.ext, terminator, response)
	    print '[outboundproxy] bridging extension %s to public conference 888' % self.ext
	    self.bridge('sofia/external/888@conference.freeswitch.org')

	# it could also be done by onChannelUnbridge
	elif app == 'bridge':
	    print '[outboundproxy] extension %s finished the bridge' % self.ext
	    self.hangup()
    
    # goodbye...
    def exitSuccess(self, ev):
	print '[outboundproxy] control of extension %s has finished' % self.ext

class OutboundFactory(protocol.ServerFactory):
    protocol = OutboundProxy

if __name__ == '__main__':
    reactor.listenTCP(port, OutboundFactory())
    reactor.connectTCP('localhost', 8021, InboundFactory('ClueCon'))
    reactor.run()
