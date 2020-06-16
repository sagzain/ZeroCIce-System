#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import IceStorm
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        intermediate = TrawlNet.IntermediatePrx.checkedCast(proxy)

        if not intermediate:
            raise RuntimeError('ERROR: The given proxy is not valid.')

        '''
        if len(sys.argv) <= 2:
            raise RuntimeError('ERROR: Not a valid number of arguments given.') 
        '''
        
        intermediate.execute("Hola Mundo!")

        return 0

sys.exit(Client().main(sys.argv))