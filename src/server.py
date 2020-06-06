#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import Ice
Ice.loadSlice('./src/trawlnet.ice')
import TrawlNet

class ServerI(TrawlNet.Server):
    def execute(self, message, current = None):
        print("Recepcion: %s" % message)
        sys.stdout.flush()


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = ServerI()

        adapter = broker.createObjectAdapter("ServerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("server1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    app = Server()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)