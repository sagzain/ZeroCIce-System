#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class IntermediateI(TrawlNet.Intermediate):
    server = None

    def execute(self, message, current = None):
        print("Redirigiendo mensaje")
        sys.stdout.flush()

        server.execute("Hello World!")

class Intermediate(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("ERROR: Property", key, "not set")
            return None
        
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        broker = self.communicator()
        servant = IntermediateI()

        adapter = broker.createObjectAdapter("IntermediateAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("intermediate1"))

        print(proxy, flush=True)

        t_manager = self.get_topic_manager()

        if not t_manager:
            print("ERROR: Invalid proxy.")
            return 2

        t_name = "ServerTopic"
        try:
            topic = t_manager.retrieve(t_name)
        except IceStorm.NoSuchTopic:
            print("Topic not found, creating...")
            topic = t_manager.create(t_name)

        publisher = topic.getPublisher()
        server = TrawlNet.ServerPrx.uncheckedCast(publisher)

        server.execute("Hello World")

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        

        return 0

sys.exit(Intermediate().main(sys.argv))