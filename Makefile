#!/usr/bin/make -f
# -*- mode:makefile -*-


run-registry:
	mkdir -p db/Registry
	icegridregistry --Ice.Config=./config/registry.config

run-icestorm:
	mkdir -p IceStorm/
	icebox --Ice.Config=./config/icebox.config

run-server:
	./src/server.py --Ice.Config=./config/server.config

run-intermediate:
	./src/intermediate.py --Ice.Config=./config/intermediate.config 

run-client:
	./src/client.py --Ice.Config=./config/client.config "intermediate1 -t -e 1.1 @ IntermediateAdapter1"

clean:
	$(RM) -r *.out __pycache__ Registry db IceStorm
	
default:
	$(MAKE) clean
	$(MAKE) run-registry &
	$(MAKE) run-icestorm &
	$(MAKE) run-server &
	$(MAKE) run-intermediate &
	$(MAKE) run-client &






