from quick2wire.gpio import pins, In, Out
from time import sleep
import datetime

spiCLK = 6
spiMISO = 5
spiMOSI = 4
spiCS = 1
inAnalogico = 0

def leerAnalogico():
    pinCLK = pins.pin(spiCLK , direction=Out)
    pinMISO = pins.pin(spiMISO , direction=In)
    pinMOSI = pins.pin(spiMOSI , direction=Out)
    pinCS = pins.pin(spiCS , direction=Out)
      
    pines = [pinCLK, pinMISO, pinMOSI, pinCS]

    try:
        for p in pines:
            p.open()

        pinCS.value = 1
        pinCLK.value = 0
        pinCS.value = 0

        envio = inAnalogico
        envio |= 0x18
        envio <<= 3

        for i in range(5):
            if envio & 0x80:
                pinMOSI.value = 1
            else:
                pinMOSI.value = 0

            envio <<= 1
            pinCLK.value = 1
            pinCLK.value = 0

        valor = 0
        
        for i in range(12):
            pinCLK.value = 1
            pinCLK.value = 0
            valor <<= 1

            if pinMISO.value:
                valor |= 0x1
            
        pinCS.value = 1

        valor /= 2
        
        return valor
    finally:
        for p in pines:
            p.close()


min = 407
max = 615

if __name__ == '__main__':
    try:  
        while True:
            valorX = leerAnalogico()

            #normalizo entre 0 y 1
            valorXN = (valorX-min) / (max-min)

            #convierto el rango de [0,1] a [-1,1]
            valorXNN = (valorXN - 0.5) * 2

            #para facilitar la lectura, dejo dos decimales e invierto el valor
            #para que la izquierda sea negativa y la derecha positiva
            #como en la recta de los reales
            valorXNNN = round(valorXNN,2) * (-1)

            print(str(valorXNNN))
            
            sleep(0.2)            
    except KeyboardInterrupt:
        pass
