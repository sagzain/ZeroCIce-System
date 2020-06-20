# zeroC-system
Sistema cliente-servidor que permite la descarga de ficheros mediante el uso de ZeroC Ice - Sistemas Distribuidos - UCLM.

## Autor y Enlace
https://github.com/Samuglz6/file-downloader-system

Samuel González Linde

## Ejecución

Para ejecutar el proyecto podemos hacerlo de dos formas distintas: utilizando dos cripts o utilizando un Makefile
En ambos casos nos situaremos en la raiz de la carpeta del proyecto para poder utilizarlos.

```sh
cd /zeroC-system
```

### Scripts 

Primero vamos a realizar la ejecución del lado del servidor y todas sus componentes necesarias. Para ello hacemos uso del script [run_server.sh](run_server.sh).

```sh
./run_server.sh
```

Después ejecutamos el lado del cliente haciendo uso del script [run_client.sh](run_client.sh) y pasandole como argumentos el nombre del archivo o archivos que quieren ser descargados.

```sh
./run_client.sh <archivo1> <archivo2>...
```

### Archivo MAKEFILE

Dentro del archivo [Makefile](Makefile) disponemos de diferentes comandos que nos van a ser de gran utilidad para poder ejecutar algunas de las partes del proyecto y ver su ejecución por separado.

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

Se envia una petición de descarga de un archivo desde el [cliente](src/file_downloader.py) al [gestor de transferencias](src/transfer_manager) el cual genera un objeto transfer que será encargado de crear los pares sender-receiver de cada archivo para realizar la transferencia.

Una vez creado el objeto transfer se inicia la creacion de los senders en el lado del [servidor](src/sender_factory.py) y los receiver en el lado del cliente.

Cuando todas las parejas estan creadas se inicia la transferencia del archivo (el cual debe existir en la [carpeta de archivos](/files)), el sender envía el contenido del archivo y el receiver es encargado de almacenarlo en la [carpeta de descargas](/downloads).


