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

## Formulas y Cálculos

### Pasar velocidad del viento en m/s a km/h

Multiplicar los metros por segundo por 3,6 para obtener los kilómetros por hora.

