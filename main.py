#!/usr/bin/python3

import sys
import time

from Anemometer import Anemometer

if __name__ == "__main__":
    anemometer = Anemometer()

    ## Inicio lecturas de datos
    anemometer.start_read()

    ## Espera de 3 segundos recopilando los primeros datos
    time.sleep(3)

    count = 0

    ## Muestro constantemente los datos recopilados para probar, calibrar o debug
    while True:
        try:
            ## Cuando ha tomado 5 lecturas devuelve y resetea contadores
            ## para indicar que comienza una nueva medición.
            count += 1
            print('Contador:', count)
            if (count % 5) == 0:
                print(anemometer.get_all_datas())
            else:
                anemometer.debug()
        except KeyboardInterrupt:
            anemometer.stop_read()
            sys.exit(0)