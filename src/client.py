#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        server = TrawlNet.ServerPrx.checkedCast(proxy)
        
        if not server:
            raise RuntimeError('ERROR: The given proxy is not valid.')

        server.execute('Hello World!')

        return 0

sys.exit(Client().main(sys.argv))