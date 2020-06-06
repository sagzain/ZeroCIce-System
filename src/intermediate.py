#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import Ice
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class IntermediateI(TrawlNet.Intermediate):
    server = None

    def execute(self, message, current = None):
        print("Redirigiendo mensaje")
        sys.stdout.flush()

        self.server.execute(message)

class Intermediate(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = IntermediateI()

        adapter = broker.createObjectAdapter("IntermediateAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("intermediate1"))

        print(proxy, flush=True)

        proxyServer = self.communicator().stringToProxy(argv[1])
        server = TrawlNet.ServerPrx.checkedCast(proxyServer)
        
        if server:
            servant.server = server
        else:
            raise RuntimeError('ERROR: The given proxy is not valid.')

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    app = Intermediate()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)