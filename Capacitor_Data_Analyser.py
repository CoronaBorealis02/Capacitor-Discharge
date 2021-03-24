import serial
import xlsxwriter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

workbook = xlsxwriter.Workbook(r"C:\Users\archi\source\repos\Capacitor Data Analyser\capacitor.xlsx")
testcounter = 0
datasheet = []
while testcounter < 1:
	testcounter += 1
	ser = serial.Serial('COM3', 9600)
	data = []
	timevals = []
	voltvals = []
	s = ''
	while (s != '255'):
		db = ser.readline()
		ds = db.decode()
		s = ds.rstrip()
		data.append(s) 
		print (s)
	datasheet.append(data)
	worksheet = workbook.add_worksheet(name=str(testcounter))
	worksheet.write('A1', 'Time (ms)')
	worksheet.write('B1', 'Voltage (v)')
	linenumber = 1
	for i in data[:-2]:
		linenumber += 1
		
		time = i.split(",")[0]
		voltage = i.split(",")[1]
		timevals.append(time)
		voltvals.append(voltage)
		timecell = "A" + str(linenumber)
		voltcell = "B" + str(linenumber)
		worksheet.write(timecell, time)
		worksheet.write(voltcell, voltage)

	fig, ax = plt.subplots(figsize=(21,12))
	ax.plot(timevals, voltvals)
	ax.xaxis.set_major_locator(plt.MaxNLocator(10))
	ax.yaxis.set_major_locator(plt.MaxNLocator(4))
	ax.invert_yaxis()
	ax.set(xlabel='Time (ms)', ylabel='Voltage (V)',
       title='Capacitor Test ' + str(testcounter))
	fig.savefig(r"C:\Users\archi\source\repos\Capacitor Data Analyser\test" + str(testcounter) + ".png")
	ser.close()
workbook.close()

#y = []
#x = []
#fig, ax = plt.subplots(figsize=(21,12))
#for i in datasheet:
#	i = i[:-2]
#	for ii in i:
#		time = ii.split(",")[0]
#		voltage = ii.split(",")[1]
#		timevals.append(time)
#		voltvals.append(voltage)
#	for ii in range(0, len(datasheet)):
#		ax.plot(timevals, voltvals)
#		print ("on graph " + str(ii) + " out of " + str(len(datasheet)))
#ax.xaxis.set_major_locator(plt.MaxNLocator(3))
#ax.yaxis.set_major_locator(plt.MaxNLocator(4))
#ax.invert_yaxis()
#ax.set(xlabel='Time (ms)', ylabel='Voltage (V)',
#       title='Capacitor Test All' + str(testcounter))
#fig.savefig(r"C:\Users\archi\source\repos\Capacitor Data Analyser\All.png")