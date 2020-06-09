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

        self.server.execute(message)

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
        t_manager =  self.get_topic_manager()
        if not t_manager:
            print("ERROR: Invalid proxy.")
            return 2
        
        broker = self.communicator()
        servant = IntermediateI()

        adapter = broker.createObjectAdapter("IntermediateAdapter")
        subscriber = adapter.addWithUUID(servant)

        t_name = "IntermediateTopic"
        qos = {}
        try:
            topic = t_manager.retrieve(t_name)
        except IceStorm.NoSuchTopic:
            topic = t_manager.create(t_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        print("Waiting for events...", subscriber)



        '''
        print(proxy, flush=True)

        proxyServer = self.communicator().stringToProxy(argv[1])
        server = TrawlNet.ServerPrx.checkedCast(proxyServer)
        
        if server:
            servant.server = server
        else:
            raise RuntimeError('ERROR: The given proxy is not valid.')
        '''
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0

sys.exit(Intermediate().main(sys.argv))
'''
if __name__ == '__main__':
    app = Intermediate()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)
'''    