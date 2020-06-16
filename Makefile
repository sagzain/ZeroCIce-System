#!/usr/bin/make -f
# -*- mode:makefile -*-

run-server:
	$(MAKE) run-registry &
	sleep 1
	$(MAKE) run-icestorm &
	sleep 1
	$(MAKE) run-sender-factory &
	sleep 1
	$(MAKE) run-transfer-manager

run-registry:
	mkdir -p db/Registry 
	icegridregistry --Ice.Config=./config/registry.config

run-icestorm:
	mkdir -p IceStorm/
	icebox --Ice.Config=./config/icebox.config

run-sender-factory:
	./src/sender_factory.py --Ice.Config=./config/senders.config files/

run-transfer-manager:
	./src/transfers_manager.py --Ice.Config=./config/transfers.config

run-client: create-client-workspace
	./src/file_downloader.py --Ice.Config=./config/client.config file1 file2

create-client-workspace:
	mkdir -p downloads/

clean:
	$(RM) -r downloads __pycache__ IceStorm Registry db