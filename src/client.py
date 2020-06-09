#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class Client(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)

        if proxy is None:
            print("ERROR: Property", key, "not set")
            return None
            
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        t_manager = self.get_topic_manager()
        if not t_manager:
            print("ERROR: Invalid proxy.")
            return 2
    
        t_name = "IntermediateTopic"
        try:
            topic = t_manager.retrieve(t_name)
        except IceStorm.NoSuchTopic:
            print("Topic not found, creating...")
            topic = t_manager.create(t_name)
        
        publisher = topic.getPublisher()
        intermediate = TrawlNet.IntermediatePrx.uncheckedCast(publisher)
        
        print("Publishing 2 'Hello World' events")
        for i in range(2):
            intermediate.execute("Hello World %s!" % i)

        return 0

sys.exit(Client().main(sys.argv))