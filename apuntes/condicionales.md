# Condicionales en Python

Un condicional permite que el programa tome decisiones: ejecuta un bloque de código solo si se cumple una condición.

## if, elif y else

La estructura básica es: if condicion: (bloque), elif otra_condicion: (bloque) y else: (bloque). Python revisa las condiciones en orden y ejecuta solo el primer bloque cuya condición sea verdadera. else se ejecuta si ninguna anterior se cumplió.

Ejemplo: if nota >= 70: print("Aprobado") else: print("Reprobado").

## Operadores de comparación

== igual a, != distinto de, > mayor que, < menor que, >= mayor o igual, <= menor o igual. Ojo: = asigna un valor y == compara.

## Operadores lógicos

and exige que ambas condiciones sean verdaderas, or exige que al menos una lo sea, y not invierte el resultado. Ejemplo: if edad >= 18 and tiene_identificacion: puede entrar.

## Indentación

Python usa sangría (4 espacios) para saber qué líneas pertenecen al bloque del if. Una indentación incorrecta produce IndentationError.

## Errores comunes

Olvidar los dos puntos al final de la línea del if, usar = en lugar de ==, y mezclar espacios con tabulaciones.
