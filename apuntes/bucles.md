# Bucles en Python

Un bucle repite un bloque de código varias veces sin tener que escribirlo de nuevo.

## Bucle for

Se usa cuando sabes cuántas veces repetir o quieres recorrer una colección. Ejemplo: for i in range(5): print(i) imprime 0, 1, 2, 3 y 4. range(5) genera los números desde 0 hasta 4; range(1, 6) va de 1 a 5; range(0, 10, 2) avanza de dos en dos.

También recorre listas y textos: for fruta in ["manzana", "pera"]: print(fruta).

## Bucle while

Repite mientras una condición sea verdadera. Ejemplo: contador = 0 y while contador < 3: print(contador); contador += 1. Si la condición nunca se vuelve falsa, el bucle es infinito; hay que asegurarse de modificar la variable dentro del bloque.

## break y continue

break termina el bucle de inmediato. continue salta a la siguiente repetición sin ejecutar el resto del bloque.

## Acumuladores

Un patrón muy común es acumular: total = 0 y for n in [3, 5, 2]: total += n. Al final total vale 10.

## Errores comunes

Olvidar actualizar la variable del while (bucle infinito), olvidar que range(n) no incluye a n, y mala indentación del bloque.
