#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import binascii
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

BLOCK_SIZE = 1024
DOWNLOAD_DIR = './downloads'

class TransferEventI(TrawlNet.TransferEvent):
    def __init__(self, transfer):
        self.transfer = transfer

    def transferFinished(self, transfer, current=None):
        if(transfer == self.transfer):
            print('[EVENTO] El transfer \'%s\' ha finalizado' % transfer)

class ReceiverI(TrawlNet.Receiver):
    def __init__(self, fileName, sender, transfer):
        self.fileName = fileName
        self.sender = sender
        self.transfer = transfer

    def start(self, current=None):
        print('Iniciando transferencia de fichero \'%s\'' % self.fileName)
        data = binascii.a2b_base64(self.sender.receive(BLOCK_SIZE)[1:])

        with open(os.path.join(DOWNLOAD_DIR,self.fileName), "wb") as file:
            file.write(data)

        self.sender.close()

        print('Finalizada transferencia de fichero.')


    def destroy(self, current=None):
        print('Eliminando receiver')

        self.sender.destroy()

        try:
            current.adapter.remove(current.id)
        except Exception as e:
            print(e, flush=True)

class ReceiverFactoryI(TrawlNet.ReceiverFactory):
    def create(self, fileName, sender, transfer, current=None):
        servant = ReceiverI(fileName, sender, transfer)
        proxy = current.adapter.addWithUUID(servant)

        print('Creado receiver para descarga del archivo \'%s\'' % fileName)

        return TrawlNet.ReceiverPrx.checkedCast(proxy)

class Client(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            raise RuntimeError('La propiedad \'%s\' no está definida' % key)

        print('Ejecutando IceStorm en: \'%s\'' % key)
        
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        #Creamos el objeto factoria de transfers para realizar las llamadas remotas
        key = 'TransfersManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        factoria_transfer = TrawlNet.TransferFactoryPrx.checkedCast(proxy)

        #Comprobamos que existe el proxy del objeto que hemos solicitado
        if not factoria_transfer:
            raise RuntimeError('El proxy que se está intentando utilizar no es valido.')
        
        #Comprobamos también que el cliente solicite algun archivo
        if len(argv) < 2:
            raise RuntimeError('Al menos un fichero tiene que ser pasado como argumento.')

        #Crear el adaptador y activarlo para hacer uso del factory receiver
        broker = self.communicator()
        servant = ReceiverFactoryI()
        adapter = broker.createObjectAdapter("ReceiverFactoryAdapter")
        proxy2 = adapter.add(servant, broker.stringToIdentity("receiver_factory1"))

        adapter.activate()

        #Cuando acaba la transferencia del archivo con una de las peers, enviamos el evento
        topic_manager = self.get_topic_manager()

        if not topic_manager:
            raise RuntimeError('El proxy \'%s\' no es válido.' % topic_manager)
        
        peer_topic_name = 'PeerEvent'
        try:
            peer_topic = topic_manager.retrieve(peer_topic_name)
        except IceStorm.NoSuchTopic:
            peer_topic = topic_manager.create(peer_topic_name)
        
        publisher = peer_topic.getPublisher()
        peer_event = TrawlNet.PeerEventPrx.uncheckedCast(publisher)

        #Realizar llamada remota a transfer_manager para crear el objeto transfer
        transfer = factoria_transfer.newTransfer(TrawlNet.ReceiverFactoryPrx.checkedCast(proxy2))

        #Utilizamos la variable contenida en TrawlNet que consiste en una secuencia de Strings
        TrawlNet.FileList = argv[1:]

        #Usar el objeto transfer para crear las Peers
        receiver_list = transfer.createPeers(TrawlNet.FileList)
        
        #Nos subscribimos a los eventos de TransferEvent y activacion del adaptador
        servant_event = TransferEventI(transfer)
        adapter_event = broker.createObjectAdapter('TransferEventAdapter')
        subscriber = adapter_event.addWithUUID(servant_event)
        
        transfer_topic_name = 'TransferEvent'
        qos = {}
        try:
            transfer_topic = topic_manager.retrieve(transfer_topic_name)
        except IceStorm.NoSuchTopic:
            transfer_topic = topic_manager.create(transfer_topic_name)
        
        transfer_topic.subscribeAndGetPublisher(qos, subscriber)

        adapter_event.activate()

        #Una vez tenemos las peers creadas procedemos a realizar las transferencias correspondientes
        for receiver in range(len(receiver_list)):
            receiver_list[receiver].start()
            peer_event.peerFinished(TrawlNet.PeerInfo(transfer, TrawlNet.FileList[receiver]))

        transfer.destroy()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        transfer_topic.unsubscribe(subscriber)

        return 0

sys.exit(Client().main(sys.argv))