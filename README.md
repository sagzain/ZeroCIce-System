# zeroC-system
Sistema cliente-servidor que permite la descarga de ficheros mediante el uso de ZeroC Ice.

## Autor y Enlace
https://github.com/Samuglz6/file-downloader-system

Samuel González Linde

## Ejecución

Nos situamos en la raiz de la carpeta del proyecto y ejecutamos los diferentes comandos para poner en marcha servidor y cliente.

**Ejecucion del servidor**
```sh
python3 ./src/server.py --Ice.Config=./config/server.config
```

**Ejecucion del cliente**
```sh
python3 ./src/client.py 'server1 -t -e 1.1:tcp -h 192.168.150.134 -p 9090'
```