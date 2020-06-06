#!/usr/bin/make -f
# -*- mode:makefile -*-


run-registry:
	mkdir -p db/Registry
	icegridregistry --Ice.Config=./config/registry.config

run-server:
	./src/server.py --Ice.Config=./config/server.config | tee server-proxy.out

run-intermediate:
	./src/intermediate.py --Ice.Config=./config/intermediate.config '$(shell head -1 server-proxy.out)' | tee intermediate-proxy.out

run-client:
	./src/client.py --Ice.Config=./config/client.config '$(shell head -1 intermediate-proxy.out)' 'Hola mundo'

clean:
	$(RM) -r *.out __pycache__ Registry db
	





