import time
import sys

_kvalue                 = 0.25
_kvalueLow              = 1.0
_kvalueHigh             = 1.0
_cmdReceivedBufferIndex = 0
_voltage                = 0.0
_temperature            = 25.0

GDIFF = (30/1.8)
VR0  = 0.223
G0  = 2
I  = (1.24 / 10000)


class DFRobot_EC():
	def begin(self):
		global _kvalueLow
		global _kvalueHigh
		try:
			with open('ecdata.txt','r') as f:
				kvalueLowLine  = f.readline()
				kvalueLowLine  = kvalueLowLine.strip('kvalueLow=')
				_kvalueLow     = float(kvalueLowLine)
				kvalueHighLine = f.readline()
				kvalueHighLine = kvalueHighLine.strip('kvalueHigh=')
				_kvalueHigh    = float(kvalueHighLine)
		except :
			print ("ecdata.txt ERROR ! Please run DFRobot_EC_Reset")
			sys.exit(1)
	def readEC(self,voltage,temperature):
		global _kvalueLow
		global _kvalueHigh
		global _kvalue
		print (_kvalue)
		rawEC = 1000*voltage/820.0/200.0
		valueTemp = rawEC * _kvalue
		if(valueTemp > 1.01):
			_kvalue = _kvalueHigh
		elif(valueTemp < 1.0):
			_kvalue = _kvalueLow
		#slope = (_kvalueHigh-_kvalueLow) / (12.88-1.413)
		#intercept = _kvalueLow - (slope*1.413)
		#_kvalue = (slope*rawEC)+intercept

		value = rawEC * _kvalue
		print (temperature)
		value = value / (1.0+0.0185*(temperature-25.0))
		return value
	def calibration(self,voltage,temperature):
		rawEC = 1000*voltage/820.0/200.0
		if (rawEC>0.9 and rawEC<15):
			compECsolution = 1.413*(1.0+0.0185*(temperature-25.0))
			KValueTemp = 820.0*200.0*compECsolution/1000.0/voltage
			round(KValueTemp,2)
			print (">>>Buffer Solution:1.413us/cm")
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[0]='kvalueLow='+ str(KValueTemp) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>EC:1.413us/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		elif (rawEC>20 and rawEC<50):
			compECsolution = 12.88*(1.0+0.0185*(temperature-25.0))
			KValueTemp = 820.0*200.0*compECsolution/1000.0/voltage
			print (">>>Buffer Solution:12.88ms/cm")
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[1]='kvalueHigh='+ str(KValueTemp) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>EC:12.88ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		else:
			print (">>>Buffer Solution Error Try Again<<<")
	def reset(self):
		_kvalueLow              = 1.0;
		_kvalueHigh             = 1.0;
		try:
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[0]='kvalueLow=' + str(_kvalueLow)  + '\n'
			flist[1]='kvalueHigh='+ str(_kvalueHigh) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>Reset to default parameters<<<")
		except:
			f=open('ecdata.txt','w')
			#flist=f.readlines()
			flist   ='kvalueLow=' + str(_kvalueLow)  + '\n'
			flist  +='kvalueHigh='+ str(_kvalueHigh) + '\n'
			#f=open('data.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>Reset to default parameters<<<")

class DFRobot_Temp_pt1000(object):
	def conv_voltageto_temperature_c(self,voltage):
		Rpt1000 = (voltage/1000/GDIFF+VR0)/I/G0
		temp = (Rpt1000-1000)/3.85
		return temp

