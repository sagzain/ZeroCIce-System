#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import binascii
import Ice
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

BLOCK_SIZE = 1024
DOWNLOAD_DIR = './downloads'

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

        self.transfer.destroyPeer(str(current.id.name))


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

        for receiver in receiver_list:
            receiver.start()
            
        transfer.destroy()

        return 0

sys.exit(Client().main(sys.argv))