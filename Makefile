#!/usr/bin/make -f
# -*- mode:makefile -*-

clean:
	$(RM) *.out

run-registry:
	mkdir -p /tmp/db/registry
	icegridregistry --Ice.Config=./config/node.config

run-server:
	./src/server.py --Ice.Config=./config/server.config | tee server-proxy.out

run-intermediate:
	./src/intermediate.py --Ice.Config=./config/intermediate.config '$(shell head -1 server-proxy.out)' | tee intermediate-proxy.out

run-client:
	./src/client.py --Ice.Config=./config/client.config '$(shell head -1 intermediate-proxy.out)' 'Hola mundo'







