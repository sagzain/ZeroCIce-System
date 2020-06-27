#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import binascii
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

FILE_DIR = './files'

class SenderI(TrawlNet.Sender):
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(os.path.join(FILE_DIR, self.fileName),'rb')

    def receive(self, size, current=None):
        data = str(binascii.b2a_base64(self.file.read(size),newline=False))
        
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
        proxy = current.adapter.add(servant, current.adapter.getCommunicator().stringToIdentity(fileName))

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

