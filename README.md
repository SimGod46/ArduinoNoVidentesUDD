# Arduino no videntes
Aplicación desarrollada en python, permite utilizar sensores para detectar la conexion de pines en un arduino leonardo y esta señal es leida por voz en el ordenador donde se ejecuta el programa, además se utiliza reconocimiento de imagenes para detectar modulos arduinos y describrir sus caracteristicas.

## Paquetes necesarios:
* hidapi
* pymysql
* tensorflow

## Detección por fotopuertas:
Se utiliza el modulo voice.py, dentro de este se encuentran las funciones "hid_loop", "key_recorder" y "say_loop" además de la variable "q" de tipo queue (cola).

### hid_loop:
Se ejecuta como un Thread, identifica los elementos hid conectados y busca aquel que incluya el nombre "Leonardo", si se encuentra, se vincula la dirección de este elemento con "key_recorder" y le envia una señal cada vez que se produce un cambio.

### key_recorder:
Identifica el valor que envia el elemento hid y lo asocia a un pin, dependiendo de el valor será el pin asignado. La asignación se guarda dentro de la variable q

### say_loop:
Itera sobre los valores de la variable q y los lee por voz.

## Reconocimiento modulos:
Se utiliza el modulo recognize.py, utilización de modelo ResNet50 (.h5) para la clasificacion de imagenes, uso de la libreria tensorflow para la carga/entrenamiento del modelo, solo se retorna la prediccion más alta. Dataset entrenamiento en roboflow.

## Descripción modulos:
Se utiliza el modulo dbms.py, utilización de base de datos para almacenar nombre, numero de pines y uso de cada modulo. Conexión mediante paquete "pymysql" retornando la información y agregandola a la variable "q" para luego ser leida.

## Captura de imagenes:
Se utiliza el modulo main.py, genera el ciclo responsable de la captura y almacenamiento de imagenes para luego ser procesadas, además es donde se almacena la variable q de forma que se pueda leer por los demas modulos.

Hola
