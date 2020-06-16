# zeroC-system
Sistema cliente-servidor que permite la descarga de ficheros mediante el uso de ZeroC Ice - Sistemas Distribuidos - UCLM.

## Autor y Enlace
https://github.com/Samuglz6/file-downloader-system

Samuel González Linde

## Ejecución

Nos situamos en la raiz de la carpeta del proyecto y hacemos uso de los diferentes comandos que contiene el Makefile para poner en marcha nuestro proyecto.

```sh
cd /zeroC-system
```

**Activación del registry**


```sh
make run-registry
```

**Activación del servicio de eventos**

```sh
make run-icestorm
```

**Ejecucion del sender-factory**

```sh
make run-sender-factory
```

**Ejecucion del transfer-manager**

```sh
make run-transfer-manager
```

**Ejecucion del file_downloader**

```sh
make run-client
```

**Limpiar el directorio del proyecto**

```sh
make clean
```

## Estado actual del proyecto

Actualmente se hace uso del lanzador de aplicaciones IceBox para lanzar un servicio IceStorm.

Se envia un mensaje simple que contiene un "Hola Mundo" entre el [Intermediario](src/intermediate.py) y el [Servidor](src/server.py) para la comprobación del correcto funcionamento del canal de eventos.


