# AD5761-library
Python library for DAC AD5761 and Raspberry PI

This library provides class and methods to control DAC.

### Initialization
init method have one **essential** paremetr `CSpin`.

Other parameters (read datasheet):
| name | description | default value |
|----:|:----|:----------|
| `CV` | Clear voltage selection | 1 |
| `OVR` | Overage | False |
| `B2C` | Bipolar range | False |
| `ETS` | Termal shutdovn alert | False |
| `PV` | Power-up voltage | 1 |
| `RA` | Output range | 0 |

### Methods
1. xferToDAC(regAddr, regData) method using as private to transfer data do DAC. spidev using only here. Method return recieved data in format `[0bXXXXXXXX, 0bXXXXXXXX]`
    regAddr - int
    regData - int
4. printBytes(reg) method just print bytes using print() function python
    reg - list of int < 256
5. writeToControllReg() method takes self. attributes defined in __init__ and transfer to DAC
6. writeAndUpdateReg(num) method write to DAC register and update it (set voltage output)
    num in range [0, 65535]
7. softwareFullReset() method execute softvare full reset
8. readbackControlReg() method read control register and return it in format [0bXXXXXXXX, 0bXXXXXXXX]

### Errors
if parameters in `__init__` will in wrong range or method `writeAndUpdateReg()` get num in wrong range, exception `WrongParametersForDAC` raised. His `__str__` representation contain information about send param and acceptable range.

### Usage
```python
import main
from time import sleep

AD = AD6761(19, RA=5) #init
AD1.softwareFullReset() #reset DAC
AD1.writeToControllReg() #setup control register
AD1.printBytes(AD1.readbackControlReg()) #read back control register

#iterate range
for i in range(0, 65535, 10):
	AD1.writeAndUpdateReg(i)
	sleep(0.001)
	if i % 1000 == 0:
		print(i)
```
