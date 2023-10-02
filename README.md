# AD5761-library
python library for DAC AD5761 and Raspberry PI

This library provides class and methods to control DAC.

INITIALIZATION 
init method have one essential paremetr CSpin.
Other parameters (read datasheet):
1. CV (Clear voltage selection) default: 1
2. OVR (Overage) default: False
3. B2C (Bipolar range) default: False
4. ETS (Termal shutdovn alert) default: False
5. PV (Power-up voltage) default: 1
6. RA (Output range) default: 0

METHODS
1. xferToDAC(regAddr, regData) method using as private to transfer data do DAC. spidev using only here. Method return recieved data in format [0bXXXXXXXX, 0bXXXXXXXX]
    regAddr - int
    regData - int
2. printBytes(reg) method just print bytes using print() function python
    reg - list of int < 256
3. writeToControllReg() method takes self. attributes defined in __init__ and transfer to DAC
4. writeAndUpdateReg(num) method write to DAC register and update it (set voltage output)
    num in range [0, 65535]
5. softwareFullReset() method execute softvare full reset
6. readbackControlReg() method read control register and return it in format [0bXXXXXXXX, 0bXXXXXXXX]

ERRORS
if parameters in __init__ will in wrong range or method writeAndUpdateReg() get num in wrong range, exception "WrongParametersForDAC" raised. His __str__ representation contain information about send param and acceptable range.

USAGE
'''python
import main
from time import sleep

AD = AD6761(19, RA=5) #init
AD1.softwareFullReset() #reset DAC
AD1.writeToControllReg() #setup control register
AD1.printBytes(AD1.readbackControlReg()) #read back control register

# iterate range
for i in range(0, 65535, 10):
	AD1.writeAndUpdateReg(i)
	sleep(0.001)
    if i % 1000 == 0:
		print(i)
'''