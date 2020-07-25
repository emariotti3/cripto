# 66.69 - Criptografía y Seguridad Informática
## Trabajo Practico Final: esteganografía
Dependencias:
- Python3
- [Pillow](https://pillow.readthedocs.io/en/latest/installation.html)

## Esteganografía con UDP
Modo de uso:
Primero moverse al directorio que contiene el proyecto de UDP

> $ cd UDP

Para compilar el cliente y el servidor:

> $ gcc udpClient.c -o client
> $ gcc udpServer.c -o server

Para correr la prueba abrir dos terminales, una para el cliente y otra para el servidor y correrlos:

> $ ./client

> $ ./server

El cliente debería realizar un print de todos los caracteres enviados. El servidor, deber realizar un print de todos los caracteres recibidos y finalmente deberá imprimir el mensaje secreto enviado por el cliente.
