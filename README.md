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

Tanto la creacion de la BDD como la ejecución del registry estan recogidos bajo este unico comando.

```sh
make run-registry
```

**Ejecucion del servidor**

Ahora el servidor genera un fichero .out donde almacenamos el proxy para ser usado por el intermediario

```sh
make run-server
```

**Ejecucion del intermediario**

El intermediario tambien genera un proxy.out para ser usado por el cliente

```sh
make run-intermediate
```

**Ejecucion del cliente**

El mensaje que envia el cliente está definido en el Makefile con el contenido: "Hola Mundo"

```sh
make run-client
```

**Limpiar**

Tambien hay un comando nuevo que nos permite eliminar aquellos archivos temporales que son usados durante la ejecucion del sistema

```sh
make clean
```

## Estado actual del proyecto

Comunicacion basica entre un servidor, un intermediario y un cliente haciendo uso de proxies indirectos (transparencia de localizacion).

Se hace uso del registry para registrar la referencia al adaptador del servidor y el intermediario y el locator para consultar los endpoint de los adaptadores.

El envío del mensaje consiste en un envío del cliente hacia un intermediario que se encarga de redireccionar el mensaje hacia el servidor.

