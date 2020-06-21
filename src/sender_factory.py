#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

FILE_DIR = './files'

class SenderI(TrawlNet.Sender):
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None

    def receive(self, size, current=None):
        with open(os.path.join(FILE_DIR, self.fileName)) as file: # Use file to refer to the file object
            self.file = file
            data = self.file.read()
        return data

    def close(self, current=None):
        self.file.close()

    def destroy(self, current=None):
        print('Eliminando sender')
        try:
            current.adapter.remove(current.id)
        except Exception as e:
            print(e, flush=True)

class SenderFactoryI(TrawlNet.SenderFactory):
    def create(self, fileName, current=None):
        if not os.path.isfile(os.path.join(FILE_DIR, fileName)):
                raise TrawlNet.FileDoesNotExistError('ERROR: The file \'%s\' does not exist' % file)

        servant = SenderI(fileName)
        proxy = current.adapter.addWithUUID(servant)

        print('Creado sender para descarga del archivo \'%s\'' % fileName)
        sys.stdout.flush()

        return TrawlNet.SenderPrx.checkedCast(proxy)

class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = SenderFactoryI()

        adapter = broker.createObjectAdapter("SenderFactoryAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("sender_factory1"))

        print(proxy, flush=True)
        
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

sys.exit(Server().main(sys.argv))

'''
    DISTRIBUCION DE EVENTOS

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)

        if proxy is None:
            print("ERROR: Property", key, "not set")
            return None
            
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
-------------------------------------------------------------
        t_manager = self.get_topic_manager()

        if not t_manager:
            print("ERROR: Invalid proxy.")
            return 2
        
        broker = self.communicator()
        servant = ServerI()

        adapter = broker.createObjectAdapter("SenderFactoryAdapter")
        subscriber = adapter.addWithUUID(servant)

        t_name = "ServerTopic"
        qos = {}
        try:
            topic = t_manager.retrieve(t_name)
        except IceStorm.NoSuchTopic:
            topic = t_manager.create(t_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        print("Waiting for events...", subscriber)

        topic.unsubscribe(subscriber)
        '''