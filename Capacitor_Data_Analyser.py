import serial
import serial.tools.list_ports as port_list
import xlsxwriter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as gui
import pandas as pd
import openpyxl

ports = list(port_list.comports())
comports = []
for p in ports:
	comports.append(str(p)[:4])

testrange = []
for i in range(1, 1000000, 1):
	testrange.append(i)
window = gui.Window("Capacitor Data Analyser", layout=[[gui.Text("Select COM port the arduino is connected to: "), gui.Combo(comports, key='-COM-')],
													   [gui.Text("Select Folder to store data to: "), gui.FolderBrowse("Select Folder", key='-FOLDERPATH-')],
													   [gui.Text("Enter how many tests you want to complete: "), gui.Spin(testrange, key='-TESTS-')],
													   [gui.Button("Go")]])

events, values = window.read()
COM = values['-COM-']
PATH = values['-FOLDERPATH-']
TESTNO = values['-TESTS-']
workbook = xlsxwriter.Workbook(PATH + "\capacitor.xlsx")
testcounter = 0
datasheet = []
while testcounter < TESTNO:
	testcounter += 1
	ser = serial.Serial(COM, 9600)
	data = []
	timevals = []
	voltvals = []
	tempvals = []
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
	worksheet.write('C1', 'Temp (C)')
	linenumber = 1
	for i in data[:-2]:
		linenumber += 1
		
		time = i.split(",")[0]
		voltage = i.split(",")[1]
		temp = i.split(",")[2]
		timevals.append(time)
		voltvals.append(voltage)
		tempvals.append(temp)
		timecell = "A" + str(linenumber)
		voltcell = "B" + str(linenumber)
		tempcell = "C" + str(linenumber)
		worksheet.write(timecell, time)
		worksheet.write(voltcell, voltage)
		worksheet.write(tempcell, temp)

	fig, ax = plt.subplots(figsize=(21,12))
	ax.plot(timevals, voltvals)
	ax.xaxis.set_major_locator(plt.MaxNLocator(10))
	ax.yaxis.set_major_locator(plt.MaxNLocator(4))
	ax.invert_yaxis()
	ax.set(xlabel='Time (ms)', ylabel='Voltage (V)',
	   title='Capacitor Test ' + str(testcounter))
	fig.savefig(PATH + "/test" + str(testcounter) + ".png")
	ser.close()
workbook.close()

Time = []
Voltage = []
xlsx = pd.ExcelFile(PATH + '\capacitor.xlsx')
fig, ax = plt.subplots(figsize=(21,12))
fig2, ax2 = plt.subplots(figsize=(21,12))

for i in range(1, (TESTNO + 1)):
	df = pd.read_excel (xlsx, sheet_name=str(i))
	Time = df['Time (ms)']
	Voltage = df['Voltage (v)']
	ax2.plot(Time, Voltage, label=("Test " + str(i)))
	ax.plot(Time, Voltage, label=("Test " + str(i)))
	print ("Completed " + str(i) + " of " + str(TESTNO))
	
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.yaxis.set_major_locator(plt.MaxNLocator(4))
ax.legend(ncol=4)
ax.set(xlabel='Time (ms)', ylabel='Voltage (V)',
	   title='Capacitor Test Overlapped (Tests 1 - ' + str(TESTNO) + ')')
fig.savefig(PATH + "/testOverlap.png")
ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
ax2.yaxis.set_major_locator(plt.MaxNLocator(4))
ax2.legend(ncol=4)
plt.yscale('log')
ax2.set(xlabel='Time (ms)', ylabel='Voltage (V)',
	   title='Capacitor Test Overlapped (Tests 1 - ' + str(TESTNO) + ') (Log scale)')
fig2.savefig(PATH + "/logoverlap.png")

