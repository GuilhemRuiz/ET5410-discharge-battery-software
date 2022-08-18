#program developped in Python 3.10.6

##########################################################################################
# This program allows communication with the ET5410 and ET5410+ test benches             #
# This program is used to generate the interface. It will need to call on other programs #
##########################################################################################

from tkinter import *
import serial.tools.list_ports
import pyvisa

import dcLoad
import genererPDF

#The four lists below are used for the voltage and capacity lists
voltageList = [
"12", "24", "36", "48", "60", "72"
] 

capacityList = [
"6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12", "12.5", "13", \
"13.5", "14", "14.5", "15", "15.5", "16", "16.5", "17", "17.5", "18", "18.5", "19", "19.5", "20", \
"20.5", "21", "21.5", "22", "22.5", "23", "23.5", "24", "24.5", "25", "25.5", "26", "26.5", "27", \
"27.5", "28", "28.5", "29", "29.5", "30", "30.5", "31", "31.5", "32", "32.5", "33", "33.5", "34", \
"34.5", "35"
]

baudrateList = [
    "9600", "115200"
]


dischargeCurrentList = [
"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"
] 


boutonPDF = 0
clientName = " "
batteryReference = " "
tensionFull = 0

#allows you to get data entered by the user
def recupVal():
    recupVal.clientName = step2Client.get()
    recupVal.batteryReference = step2Ref.get()
    recupVal.selectedCom = format(comVar.get())
    recupVal.selectedBaud = format(baudVar.get())
    recupVal.selectedVol = format(voltVar.get())
    recupVal.selectedCapa = format(capaVar.get())
    recupVal.selectedDiscCur = format(disCurVar.get())


#function to start the test
def start():
    global boutonPDF
    global valeurConformitePdf

    recupVal()                      #the data needed to launch the test is collected
    step2Client.delete(0, END)      #we empty the fields filled in by the user
    step2Client.insert(0, "")
    step2Ref.delete(0, END)
    step2Ref.insert(0, "")
    selectedCom = recupVal.selectedCom
    selectedBaudrate = recupVal.selectedBaud
    selectedVol = int(recupVal.selectedVol)
    selectedCapa = float(recupVal.selectedCapa)
    selectedDiscCur = int(recupVal.selectedDiscCur) 
    boutonPDF = 1

    #Calls the function to communicate with the test bench and generates an error if any parameter are not compliant
    try:
        valeurConformitePdf = dcLoad.recuperationDonees(selectedCom, selectedBaudrate, selectedVol, selectedCapa, selectedDiscCur) #on appelle la fonction de la bibliothèque permettant de lancer le test
    except :
        popupWrongData = Toplevel(fen)
        popupWrongData.title("Error")
        popupData = Label(popupWrongData, text= "Wrong software parameter! It is also possible that the battery is not connected.")
        popupData.pack()
        boutonOk = Button(popupWrongData, text="Ok", command=popupWrongData.destroy).pack()
    return(boutonPDF)


#function to generate pdf
def creaPdf():

    if boutonPDF == 1:
        clientName = str(recupVal.clientName)   #we reuse the data from the recupVal function to create the pdf
        batteryReference = str(recupVal.batteryReference)
        selectedVol = int(recupVal.selectedVol)
        selectedCapa = float(recupVal.selectedCapa)
        valConformitePdf = valeurConformitePdf

        if selectedVol == 12:
            tensionFull = 17
        elif selectedVol == 24:
            tensionFull = 30
        elif selectedVol == 36:
            tensionFull = 42
        elif selectedVol == 48:
            tensionFull = 55
        elif selectedVol == 60:
            tensionFull = 67
        elif selectedVol == 72:
            tensionFull = 84
        else:
            tensionFull = 42
        rm.close()

        #calls the function to generate the pdf and generates an error if not
        try :
            genererPDF.creationPDF(clientName, batteryReference, selectedCapa, selectedVol, valConformitePdf, tensionFull)   #appel de la fonction permettant de créer le pdf
        except :
            popupTestPasLance = Toplevel(fen)
            popupTestPasLance.title("Error")
            popupPasLance = Label(popupTestPasLance, text= "The PDF could not be generated because there was a problem during the discharge!")
            popupPasLance.pack()
            boutonOk = Button(popupTestPasLance, text="Ok", command=popupTestPasLance.destroy).pack()
    else:
        popupStart= Toplevel(fen)
        popupStart.title("Error")
        popuperr = Label(popupStart, text= "Start discharging the battery first!")
        popuperr.pack()
        boutonOk = Button(popupStart, text="Ok", command=popupStart.destroy).pack()
    return(boutonPDF)

#function to update the available com ports
def rafraichir():

    global comVar
    global comList

    step1Com.destroy()
    comList = []
    find_com = serial.tools.list_ports
    COM = find_com.comports()           
    i=0
    rm = pyvisa.ResourceManager()
    for port in sorted(COM):
        comList.append(rm.list_resources()[i])
        i=i+1
    comVar = StringVar(fen)
    comVar.set(comList[0])
    step1ComBack = OptionMenu(stepOne, comVar, *comList)
    step1ComBack.grid(row=1, column=1, columnspan=1, pady=0, sticky='WE')


#is used to retrieve the available COM ports and display them in a drop down menu
#a for loop rget all available ports and stores them in a dynamic list
comList = []
find_com = serial.tools.list_ports
COM = find_com.comports()           
i=0
rm = pyvisa.ResourceManager()
for port in sorted(COM):
    comList.append(rm.list_resources()[i])
    i=i+1
if not comList:
    comList = ['No port available']

fen=Tk()
fen.iconbitmap("icone.ico")
fen.title('Battery discharge software')

#allows the use of drop down menus
comVar = StringVar(fen)
comVar.set(comList[0])
baudVar = StringVar(fen)
baudVar.set(baudrateList[0])
voltVar = StringVar(fen)
voltVar.set(voltageList[0])
capaVar = StringVar(fen)
capaVar.set(capacityList[0])
disCurVar = StringVar(fen)
disCurVar.set(dischargeCurrentList[0])


#First frame
stepOne = LabelFrame(fen, text=" 1. Software setup: ")
stepOne.grid(row=0, columnspan=7, sticky='W'+'E', padx=5, pady=5, ipadx=5, ipady=5)

#Second frame
stepTwo = LabelFrame(fen, text=" 2. Enter informations: ")
stepTwo.grid(row=2, columnspan=7, sticky='W'+'E', padx=5, pady=5, ipadx=5, ipady=5)

#Thrid frame
stepThree = LabelFrame(fen, text=" 3. Start test: ")
stepThree.grid(row=8, columnspan=7, sticky='W'+'E', padx=5, pady=5, ipadx=5, ipady=5)

#Last frame
stepFour = LabelFrame(fen, text=" 4. Generate PDF: ")
stepFour.grid(row=10, columnspan=7, sticky='W'+'E', padx=5, pady=5, ipadx=5, ipady=5)

#com selection text
com = Label(stepOne, text="Select COM port:")
com.grid(row=1, column=0, sticky='W', padx=5, pady=2)

#com selection drop down menu
step1Com = OptionMenu(stepOne, comVar, *comList)
step1Com.grid(row=1, column=1, columnspan=1, pady=0, sticky='W')

#refresh button
refresh = Button(stepOne, text="Refresh", command = rafraichir)
refresh.grid(row=1, column=2, sticky='W', padx=2, pady=0)

#baudrate selection
com = Label(stepOne, text="Select baudrate:")
com.grid(row=2, column=0, sticky='E', padx=5, pady=2)

#baudrate drop drown menu
step1Baud = OptionMenu(stepOne, baudVar, *baudrateList)
step1Baud.grid(row=2, column=1, columnspan=1, pady=0, sticky='W')

#text client name and box to insert text
client = Label(stepTwo, text="Enter customer name:")
client.grid(row=3, column=0, sticky='W', padx=5, pady=2)
step2Client = Entry(stepTwo)
step2Client.grid(row=3, column=1, columnspan=3, pady=2, sticky='WE')

#text reference battery and box to insert text
ref = Label(stepTwo, text="Enter the battery reference:")
ref.grid(row=4, column=0, sticky='W', padx=5, pady=2)
step2Ref = Entry(stepTwo)
step2Ref.grid(row=4, column=1, columnspan=3, pady=2, sticky='WE')

#voltage text
volBat = Label(stepTwo, text="Select the battery voltage (in V):")
volBat.grid(row=5, column=0, padx=5, pady=2, sticky='W')

#Mvoltage drop down menu
step2VolBat = OptionMenu(stepTwo, voltVar, *voltageList)
step2VolBat.grid(row=5, column=1, columnspan=1, pady=2, sticky='WE')
voltVar.set(voltageList[2])  # default value of the drop down menu

#capacity text
capaBat = Label(stepTwo, text="Select the battery capacity (in Ah):")
capaBat.grid(row=6, column=0, padx=5, pady=2, sticky='W')
capaVar.set(capacityList[16])

#capacity drop down menu
step2CapaBat = OptionMenu(stepTwo, capaVar, *capacityList)
step2CapaBat.grid(row=6, column=1, columnspan=1, pady=2, sticky='WE')

#discharge current text
discCur = Label(stepTwo, text="Select the battery discharge current (in A):")
discCur.grid(row=7, column=0, padx=5, pady=2, sticky='W')

#discharge current drop down menu
step2DisCur = OptionMenu(stepTwo, disCurVar, *dischargeCurrentList)
step2DisCur.grid(row=7, column=1, columnspan=1, pady=2, sticky='WE')
disCurVar.set(dischargeCurrentList[4])

#start button
start = Button(stepThree, text="Start test", command = start)
start.pack()

#pdf generation button
genPDF = Button(stepFour, text="Generate PDF", command = creaPdf)
genPDF.pack()

fen.mainloop()
