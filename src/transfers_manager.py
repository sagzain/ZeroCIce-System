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
    def __init__(self, receiverFactory, senderFactory):
        self.receiverFactory = receiverFactory
        self.senderFactory = senderFactory
        self.transfer = None

    def createPeers(self, files, current=None):
        receiversList = []
       
        if set([file for file in files if files.count(file) > 1]):
            raise RuntimeError('Se está intentando descargar varias veces un mismo archivo.')

        for file in files:
            if not os.path.isfile(os.path.join(FILE_DIR, file)):
                raise TrawlNet.FileDoesNotExistError('El archivo \'%s\' no existe en el directorio' % file)

            sender = self.senderFactory.create(file)
            receiver = self.receiverFactory.create(file, sender, self.transfer)

            receiversList.append(receiver)
        
        print('Creadas parejas sender-receiver')
        return receiversList

    def destroyPeer(self, peerId, current=None):
        print('Eliminando pareja de peers')
        proxy = peerId + ' @ ReceiverFactoryAdapter1'
        receiver = TrawlNet.ReceiverPrx.checkedCast(current.adapter.getCommunicator().stringToProxy(proxy)) 
        receiver.destroy()

    def destroy(self, current=None):
        print('Eliminando transfer')

        try:
            current.adapter.remove(current.id)
        except Exception as e:
            print(e, flush=True)

class TransferFactoryI(TrawlNet.TransferFactory):
    def __init__(self, senderFactory):
        self.senderFactory = senderFactory

    def newTransfer(self, receiverFactory, current=None):
        servant = TransferI(receiverFactory, self.senderFactory)
        proxy = current.adapter.addWithUUID(servant)

        transfer = TrawlNet.TransferPrx.checkedCast(proxy)
        servant.transfer = transfer

        return transfer

class TransfersManager(Ice.Application):
    def run(self, argv):
        key = 'SenderFactory.Proxy'
        proxy2 = self.communicator().propertyToProxy(key)
        senderFactory = TrawlNet.SenderFactoryPrx.checkedCast(proxy2)

        if not senderFactory:
            raise RuntimeError('The given proxy is not valid.')

        broker = self.communicator()
        servant = TransferFactoryI(senderFactory)
        adapter = broker.createObjectAdapter("TransfersManagerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("transfers_manager1"))

        print(proxy, flush=True)
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

sys.exit(TransfersManager().main(sys.argv))


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
------------------------------------------------------------
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