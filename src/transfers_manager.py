#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

FILE_DIR = './files'

class TransferI(TrawlNet.Transfer):
    def createPeers(self, files, current):
        for file in files:
            if not os.path.isfile(os.path.join(FILE_DIR, file)):
                raise TrawlNet.FileDoesNotExistError('ERROR: The file %s does not exist' % file)
            else:
                print('El archivo es correcto')

class TransferFactoryI(TrawlNet.TransferFactory):
    def newTransfer(self, receiverFactory, current):
        servant = TransferI()
        proxy = current.adapter.addWithUUID(servant)

        return TrawlNet.TransferPrx.checkedCast(proxy)

class TransfersManager(Ice.Application):
    '''
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        
        if proxy is None:
            print("ERROR: Property", key, "not set")
            return None
        
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
    '''

    def run(self, argv):
        broker = self.communicator()
        servant = TransferFactoryI()

        adapter = broker.createObjectAdapter("TransfersManagerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("transfers_manager1"))

        print(proxy, flush=True)
        
        '''
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

        server.execute("Hello World")'''

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

sys.exit(TransfersManager().main(sys.argv))