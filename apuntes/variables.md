# Variables en Python

Una variable es un nombre que guarda un valor en la memoria. En Python se crea con el signo igual, sin declarar el tipo: edad = 15 crea una variable llamada edad que guarda el número 15.

## Tipos de datos básicos

Los tipos más comunes son int (números enteros, como 7), float (decimales, como 3.14), str (texto entre comillas, como "hola") y bool (verdadero o falso: True o False). Con la función type() puedes ver el tipo de una variable: type(edad) devuelve int.

## Reglas para nombrar variables

El nombre puede tener letras, números y guion bajo, pero no puede empezar con número ni tener espacios. Python distingue mayúsculas de minúsculas: nombre y Nombre son variables distintas. Por convención se usa minúsculas con guion bajo, por ejemplo nombre_completo.

## Cambiar y reutilizar valores

Una variable puede cambiar de valor: contador = 0 y después contador = contador + 1 deja contador en 1. También puedes usar el operador abreviado contador += 1.

## Entrada y salida

print() muestra información en pantalla. input() pide un texto al usuario y siempre devuelve un str; para usarlo como número hay que convertirlo: edad = int(input("Edad: ")).
