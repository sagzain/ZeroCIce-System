#!/bin/sh
#

echo "Creating directories..."
mkdir -p db/Registry 
mkdir -p IceStorm/

echo "Exec registry"
icegridregistry --Ice.Config=./config/registry.config &
sleep 1

echo "Exec icestorm"
icebox --Ice.Config=./config/icebox.config &
sleep 1

echo "Exec server-side elements"
./src/sender_factory.py --Ice.Config=./config/senders.config files/ &
sleep 1
./src/transfers_manager.py --Ice.Config=./config/transfers.config

echo "Shoutting down..."
sleep 1
rm $OUT