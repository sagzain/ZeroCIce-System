#!/bin/sh
#

mkdir -p downloads/
./src/file_downloader.py --Ice.Config=./config/client.config "$@"