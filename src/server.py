#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class ServerI(TrawlNet.Server):
    def execute(self, message, current = None):
        print("Recepcion: %s" % message)
        sys.stdout.flush()


class Server(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)

        if proxy is None:
            print("ERROR: Property", key, "not set")
            return None
            
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, args):
        t_manager = self.get_topic_manager()

        if not t_manager:
            print("ERROR: Invalid proxy.")
            return 2
        
        broker = self.communicator()
        servant = ServerI()

        adapter = broker.createObjectAdapter("ServerAdapter")
        subscriber = adapter.addWithUUID(servant)

        t_name = "ServerTopic"
        qos = {}
        try:
            topic = t_manager.retrieve(t_name)
        except IceStorm.NoSuchTopic:
            topic = t_manager.create(t_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        print("Waiting for events...", subscriber)
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0

sys.exit(Server().main(sys.argv))