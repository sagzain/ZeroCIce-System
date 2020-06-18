#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class ReceiverI(TrawlNet.Receiver):
    def start(self, current=None):
        print('Iniciando')

    def destroy(self, current=None):
        print('Eliminando')

class ReceiverFactoryI(TrawlNet.ReceiverFactory):
    def create(self, fileName, sender, transfer, current=None):
        servant = ReceiverI()
        proxy = current.adapter.addWithUUID(servant)

        print('Creando receiver')

        return TrawlNet.ReceiverPrx.checkedCast(proxy)

class Client(Ice.Application):
    def run(self, argv):
        #Creamos el objeto factoria de transfers para realizar las llamadas remotas
        key = 'TransfersManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        factoria_transfer = TrawlNet.TransferFactoryPrx.checkedCast(proxy)

        if not factoria_transfer:
            raise RuntimeError('The given proxy is not valid.')
        
        if len(argv) < 2:
            raise RuntimeError('At least a file has to be given.')

        #Crear el adaptador y activarlo para hacer uso del factory receiver
        broker = self.communicator()
        servant = ReceiverFactoryI()
        adapter = broker.createObjectAdapter("ReceiverFactoryAdapter")
        proxy2 = adapter.add(servant, broker.stringToIdentity("receiver_factory1"))

        adapter.activate()

        #Realizar llamada remota a transfer_manager para crear el objeto transfer
        transfer = factoria_transfer.newTransfer(TrawlNet.ReceiverFactoryPrx.checkedCast(proxy2))
        
        #Usar el objeto transfer para crear las Peers
        receiver_list = transfer.createPeers(argv[1:])

        print(receiver_list)

        return 0

sys.exit(Client().main(sys.argv))