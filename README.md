# raspberry-sensor-anemometer

Control de anemómetro con la raspberry pi 4 utilizando GND+GPIO para contar los pulsos y sacar la velocidad del viento a partir de ello.

Basado en el script de **Patrick Rudolph** dándole un enfoque más moderno con
 python3, modular, adaptable a varios tipos de anemómetros por configuración y
  con un estilo de programación orientado a objetos.

## Esquema de conexión

| Module | PCB Desc | GPIO | Pin |
| ------- | ------- | ------- | ------- |
| GND | Ground | - | 9 |
| GPIO4 | Digital Input | 4 | 7 |

## Modo de medición

A través de las vueltas se envían pulsos al pin digital, cuanto más pulsos son
enviados durante un periodo de tiempo sacamos la velocidad.

El resultado será devuelto en metros por segundos (m/s).

## Servidor

Se añade un servidor para tomar el valor desde otros dispositivos fácilmente y/o
poder depurar resultados.

## Calcular velocidad del viento

Cada giro completo del anemómetro cerrará dos veces el circuito por lo que
detectará dos pulsos (Puede ser mayor). Esto nos servirá para los siguientes c
álculos.

El número de rotaciones completa será el total de pulsos dividido entre dos, de
forma que para calcular la velocidad del viento tendremos:

velocidad = distancia / tiempo

velocidad = (rotaciones * circunferencia) / tiempo

En el caso de la circunferencia la calcularemos conociendo el radio del 
anemómetro:

velocidad = ( (pulsos/2) * (2 * pi * radio) ) / tiempo

Los anemómetros de tres palas son originales de oracle, estos tenían 9cm de 
diámetro pero puede variar según marca y modelo.

Aproximadamente y como referencia en muchas hojas de productos he leído que
para calibrar un anemómetro se puede equivaler 1 rotación por segundo (2 pulsos)
a 2,4km/h de forma que tomando datos de 5 segundos y girando 5 vueltas 
completas debería darnos esa aproximación. Claro que esto debe leerse de la 
especificación para tu anemómetro por si fuera distinto.

Tal vez lo obtenido no se corresponda a la realidad, hay una pérdida de energía
eólica al girar las palas y esto normalmente se compensa multiplicando la
velocidad final en km/h por 1,18 (aumentar un 18% el resultado obtenido).


## Otras Formulas y Cálculos

### Pasar velocidad del viento en m/s a km/h

Multiplicar los metros por segundo por 3,6 para obtener los kilómetros por hora.

