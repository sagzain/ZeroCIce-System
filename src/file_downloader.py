#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class Client(Ice.Application):
    def run(self, argv):
        key = 'TransfersManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        factoria = TrawlNet.TransferFactoryPrx.checkedCast(proxy)

        if not factoria:
            raise RuntimeError('The given proxy is not valid.')
        
        if len(argv) < 2:
            raise RuntimeError('At least a file has to be given.')

        file_list = argv[1:]
        
        transfer = factoria.newTransfer('texto')
        transfer.createPeers(file_list)

        return 0

sys.exit(Client().main(sys.argv))