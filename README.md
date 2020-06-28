# zeroC-system

Sistema cliente-servidor que permite la descarga de ficheros mediante el uso de ZeroC Ice - Sistemas Distribuidos - UCLM.

## Autor y Enlace

https://github.com/Samuglz6/Gonzalez

Samuel González Linde

## Manual de Usuario

Se ha recogido la informacion del proyecto en el [manual de usuario](/doc/manual_usuario.pdf) para tener más información.

Podrás consultar la estructura del proyecto y la ejecución del programa en mayor detalle.

## Ejecución

Para ejecutar el programa nos situamos en la carpeta raíz del proyecto:

```sh
$ cd /Gonzalez
```

Ejecutamos el lado del servidor en una terminal:

```sh
$ ./run_server.sh
```

Y finalmente ejecutamos el lado del cliente para la descarga de archivos:

```sh
$ ./run_client.sh <archivo1> <archivo2> ...
```

## Referencias

- [Enunciado del proyecto](/doc/enunciado.pdf)
- Manual de ZeroCIce de Moodle UCLM
- [Ice 3.7 Slice API Reference](https://doc.zeroc.com/api/ice/3.7/slice/)