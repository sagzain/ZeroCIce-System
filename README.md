# zeroC-system
Sistema cliente-servidor que permite la descarga de ficheros mediante el uso de ZeroC Ice.

## Autor y Enlace
https://github.com/Samuglz6/file-downloader-system

Samuel González Linde

## Ejecución

Nos situamos en la raiz de la carpeta del proyecto y ejecutamos los diferentes comandos para poner en marcha servidor y cliente.

```sh
cd /zeroC-system
```

**Directorio para la BDD**

```sh
mkdir -p /tmp/db/registry
```

**Activación del registry**
```sh
icegridregistry --Ice.Config=./config/node.config
```

**Ejecucion del servidor**
```sh
python3 ./src/server.py --Ice.Config=./config/server.config
```

**Ejecucion del cliente**
```sh
python3 ./src/client.py --Ice.Config=./config/client.config 'server1 -t @ ServerAdapter1'
```

## Estado actual del proyecto

Comunicacion basica entre un servidor y un cliente haciendo uso de proxies indirectos (transparencia de localizacion).

Se hace uso del registry para registrar la referencia al objeto del servidor y el locator para consultar el endpoint del adaptador.

