from spidev import SpiDev
import RPi.GPIO as GPIO

# Open SPI port
spi = SpiDev()
spi.open(0, 0)
spi.mode = 0b10
spi.max_speed_hz=500000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class AD6761:
	def __init__(self, CSpin, CV=1, OVR=False, B2C=False, ETS=False, PV=1, RA=0):
		self.CSpin = CSpin
		GPIO.setup(self.CSpin, GPIO.OUT)
		GPIO.output(self.CSpin, GPIO.HIGH)
		# Validate and save DAC parameters
		if CV >= 0 and CV <= 3:
			self.CV = CV
		else:
			raise WrongParametersForDAC('CV (Clear voltage selection)', 0, 3)
		
		if OVR == True or OVR == False:
			self.OVR = OVR
		else:
			raise WrongParametersForDAC('OVR (Overage)', False, True)
			
		if B2C == True or B2C == False:
			self.B2C = B2C
		else:
			raise WrongParametersForDAC('B2C (Bipolar range)', False, True)
			
		if ETS == True or ETS == False:
			self.ETS = ETS
		else:
			raise WrongParametersForDAC('ETS (Termal shutdovn alert)', False, True)
			
		if PV >= 0 and PV <= 3:
			self.PV = PV
		else:
			raise WrongParametersForDAC('PV (Power-up voltage)', 0, 3)
		
		if RA >= 0 and RA <= 7:
			self.RA = RA 
		else:
			raise WrongParametersForDAC('RA (Output range)', 0, 7)
	
	def __del__(self):
		self.softwareFullReset()
		
	def xferToDAC(self, regAddr, regData): # method using as private to transfer data do DAC. spidev using only here
		GPIO.output(self.CSpin, GPIO.LOW)
		# first 4 bits in 0x0F don't care
		readData = spi.xfer([0x0F & regAddr] + regData)
		GPIO.output(self.CSpin, GPIO.HIGH)
		return readData[1:]
		
	def printBytes(self, reg): # comfortable print
		for i in reg:
			print(bin(i)[2:].zfill(8), end=' ')
		print(' ')
	
	def writeToControllReg(self):
		regDataHigh = 0 # first 5 bits don't care, read DataSheet
		regDataHigh += self.CV << 1
		regDataHigh += self.OVR
		regDataLow = 0 
		regDataLow += self.B2C << 7
		regDataLow += self.ETS << 6
		regDataLow += self.PV << 3
		regDataLow += self.RA
		self.xferToDAC(0b0100, [regDataHigh, regDataLow])
		
	def writeAndUpdateReg(self, num):
		if num > 65535 or num < 0:
			raise WrongParametersForDAC('Output voltage registor', 0, 65535)
		else:
			self.xferToDAC(0b0011, [(num & 0xFF00) >> 8, (num & 0x00FF) >> 0])
		
	def softwareFullReset(self):
		self.xferToDAC(0b1111, [0xFF, 0xFF])
		
	def readbackControlReg(self):
		return self.xferToDAC(0b1100, [0xFF, 0xFF])


#error will occur if one of the parameters is in the wrong range
class WrongParametersForDAC(Exception):
	def __init__(self, wrongParam, rangeLow, rangeHigh):
		self.wrongParam = wrongParam
		self.rangeLow = rangeLow
		self.rangeHigh = rangeHigh
	
	def __str__(self):
		return 'Wrong parameter. {} must be in range [{}, {}]'.format(self.wrongParam, self.rangeLow, self.rangeHigh)
