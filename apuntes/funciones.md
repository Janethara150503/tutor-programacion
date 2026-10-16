# Funciones en Python

Una función es un bloque de código con nombre que se puede reutilizar. Evita repetir código y lo hace más ordenado.

## Definir y llamar una función

Se define con def, el nombre, paréntesis y dos puntos: def saludar(nombre): print("Hola", nombre). Para ejecutarla se llama por su nombre: saludar("Ana"). Definir una función no la ejecuta; solo la llamada lo hace.

## Parámetros y argumentos

Los parámetros son los nombres que aparecen en la definición (nombre). Los argumentos son los valores que se pasan al llamarla ("Ana"). Un parámetro puede tener valor por defecto: def saludar(nombre="amigo").

## return

return devuelve un resultado a quien llamó la función y termina la función. Ejemplo: def sumar(a, b): return a + b, y luego resultado = sumar(2, 3) deja resultado en 5. Si una función no tiene return, devuelve None. print muestra en pantalla, pero no devuelve un valor utilizable.

## Variables locales

Las variables creadas dentro de una función solo existen dentro de ella (alcance local). Fuera de la función dan NameError.

## Buenas prácticas

Usar nombres que describan lo que hace la función, que cada función haga una sola cosa y escribir una breve explicación (docstring) debajo de la definición.
