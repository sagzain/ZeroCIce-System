#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

FILE_DIR = './files'

class PeerEventI(TrawlNet.PeerEvent):
    def peerFinished(self, peerInfo, current=None):
        print('[EVENTO] La peer con \'%s\' del transfer \'%s\'ha finalizado.' % (peerInfo.fileName, peerInfo.transfer))
        peerInfo.transfer.destroyPeer(peerInfo.fileName)

class TransferI(TrawlNet.Transfer):
    def __init__(self, receiverFactory, senderFactory):
        self.receiverFactory = receiverFactory
        self.senderFactory = senderFactory
        self.transfer = None

    def createPeers(self, files, current=None):
        TrawlNet.receiversList = []
       
        #Comprobamos que no se ha repetido el nombre de ningun archivo
        if set([file for file in files if files.count(file) > 1]):
            raise RuntimeError('Se está intentando descargar varias veces un mismo archivo.')

        #Comprobamos que todos los archivos que se han indicado existen en el directorio
        for file in files:
            if not os.path.isfile(os.path.join(FILE_DIR, file)):
                raise TrawlNet.FileDoesNotExistError('El archivo \'%s\' no existe en el directorio' % file)

        #Creamos la pareja sender-receiver para cada archivo
        for file in files:
            sender = self.senderFactory.create(file)
            receiver = self.receiverFactory.create(file, sender, self.transfer)

            #Almacenamos los receivers en la lista definida en TrawlNet
            TrawlNet.receiversList.append(receiver)
        
        print('Creadas parejas sender-receiver')
        return TrawlNet.receiversList

    def destroyPeer(self, peerId, current=None):
        print('Eliminando pareja sender-receiver de \'%s\'' % peerId)

        #Definimos los proxies para la destruccion de las peers        
        proxy = peerId + ' @ ReceiverFactoryAdapter1'
        proxy2 = peerId + ' @ SenderFactoryAdapter1'

        #Destruimos el sender indicado
        sender = TrawlNet.SenderPrx.checkedCast(current.adapter.getCommunicator().stringToProxy(proxy2))
        sender.destroy()
        
        #Destruimos el receiver indicado
        receiver = TrawlNet.ReceiverPrx.checkedCast(current.adapter.getCommunicator().stringToProxy(proxy)) 
        receiver.destroy()

        #Vamos eliminando los receivers que ya no existen de la lista de receivers
        TrawlNet.receiversList.remove(receiver)

        #Comprobamos que el transfer no tiene mas receivers para hacer uso del canal de eventos
        if not TrawlNet.receiversList:
            key = 'IceStorm.TopicManager.Proxy'
            proxy = current.adapter.getCommunicator().propertyToProxy(key)
            if proxy is None:
                raise RuntimeError('La propiedad \'%s\' no está definida' % key)
            
            topic_manager = IceStorm.TopicManagerPrx.checkedCast(proxy)
            if not topic_manager:
                raise RuntimeError('El proxy \'%s\' no es válido.' % topic_manager)
            
            topic_name = "TransferEvent"
            try:
                topic = topic_manager.retrieve(topic_name)
            except IceStorm.NoSuchTopic:
                topic = topic_manager.create(topic_name)
            
            publisher = topic.getPublisher()
            event = TrawlNet.TransferEventPrx.uncheckedCast(publisher)

            #Publicamos el evento de finalización del transfer 
            event.transferFinished(self.transfer)

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

        #Actualizamos el atributo del transfer con su proxy
        transfer = TrawlNet.TransferPrx.checkedCast(proxy)
        servant.transfer = transfer

        return transfer    

class TransfersManager(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            raise RuntimeError('La propiedad \'%s\' no está definida' % key)

        print('Ejecutando IceStorm en: \'%s\'' % key)
        
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        key = 'SenderFactory.Proxy'
        proxy2 = self.communicator().propertyToProxy(key)
        senderFactory = TrawlNet.SenderFactoryPrx.checkedCast(proxy2)

        if not senderFactory:
            raise RuntimeError('El proxy que se ha proporcionado no es valido.')

        #Creamos y activamos el adaptador para TransferFactory y el proxy para llamadas remotas
        broker = self.communicator()
        servant = TransferFactoryI(senderFactory)
        adapter = broker.createObjectAdapter("TransfersManagerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("transfers_manager1"))

        print(proxy, flush=True)

        adapter.activate()

        #Subscripción a los eventos de PeerEvent y activación del adaptador
        topic_manager = self.get_topic_manager()
        if not topic_manager:
            raise RuntimeError('El proxy \'%s\' no es válido.' % topic_manager)
        
        ic = self.communicator()
        servant_event = PeerEventI()
        adapter_event = ic.createObjectAdapter('PeerEventAdapter')
        subscriber = adapter_event.addWithUUID(servant_event)
        
        topic_name = 'PeerEvent'
        qos = {}
        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_manager.create(topic_name)
        
        topic.subscribeAndGetPublisher(qos, subscriber)

        adapter_event.activate()

        #Mantenemos al servidor a la escucha hasta que su proceso sea interrumpido
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        #Eliminamos la subscripcion del canal de eventos
        topic.unsubscribe(subscriber)

        return 0

sys.exit(TransfersManager().main(sys.argv))