#############################################################
# This program allows the communication with the test bench #
#############################################################

import pyvisa
import sqlite3
import time


capacite = 0
tension = 36
courantDechargeTh = 4
tensionCoupure = 27
tensionBms = 31
nbs = 0


#main function in this program. The only on used by the main program
def recuperationDonees(comSelectionne, baudrateSelectionne, tension, capacite, courantDechargeTh):
    global valeurConformitePdf

    valeurConformitePdf = 1
    finDecharge = 1
    capaciteSel = float(capacite)
    tensionSel = int(tension)
    courantDechargeTh = int(courantDechargeTh)
    baudrateSelectionne = int(baudrateSelectionne)

    #When we ask  the test bench for some measures, it answers with a string like 'R100.0'. The goal of the following
    #function is to convert this string into a float 
    def passageFloat(variable):
        variableCut = variable[1:6]             #we take out the R
        variableFloat = float(variableCut)
        return(variableFloat) 


    #all of the remaining functions are used to communicate with the device. Each function contains an instruction.

    #This function is used to switch to the batttery mode
    def modeBatterie():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)         #we open the communication with the selected com
        inst.baud_rate = baudrateSelectionne            #this program allows communication with the test bench
        inst.read_termination = '\n'                    #these two lines allows the good understanding of the command by the machine 
        inst.write_termination = '\n'
        inst.query('CH:MODE BATT\x0A')                  #th 0x0A at the end of the command required to be understood by the device
        time.sleep(1)
        rm.close()

    #This function is used to start the test
    def lancementTest():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        inst.query(u'CH:SW ON\x0A')
        time.sleep(1)
        rm.close() 

    #This function is used to stop the test
    def arretTest():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        inst.query(u'CH:SW OFF\x0A')
        time.sleep(1)
        rm.close() 

    #This function is used to select the discharge current. It depends on what the user chose on the interface
    def selectionCourantDecharge(courantDechargeTh):
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        inst.query('CURR:BCC1 {}\x0A'.format(courantDechargeTh))
        time.sleep(1)
        rm.close()

    #this function is used to select the cut-off voltage
    #it can be calculated using the formula 2.7*number of cells in series
    def selectionTensionCoupure(tensionSel):

        global tensionCoupure
        global nbs


        def calculTensionCoupure(nombreCellulesSerie):
            tensionCoup = nombreCellulesSerie*2.7
            return(tensionCoup)
            
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        if tensionSel == 12:
            nbs = 4
            tensionCoupure = calculTensionCoupure(nbs)
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))
        elif tensionSel == 24:
            nbs = 7
            tensionCoupure = calculTensionCoupure(nbs)            
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))
        elif tensionSel == 36:
            nbs = 10
            tensionCoupure = calculTensionCoupure(nbs)
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))
        elif tensionSel == 48:
            nbs = 13
            tensionCoupure = calculTensionCoupure(nbs)
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))

        elif tensionSel == 60:
            nbs = 16
            tensionCoupure = calculTensionCoupure(nbs)
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))
        elif tensionSel == 72:
            nbs = 20
            tensionCoupure = calculTensionCoupure(nbs)
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))
        else:
            nbs = 10
            tensionCoupure = calculTensionCoupure(nbs)
            inst.query('VOLT:BCC1 {}\x0A'.format(tensionCoupure))
        time.sleep(1)
        rm.close()

    #test function to get the identity of the device
    def idn():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        idn = inst.query("*IDN?\x0A")
        time.sleep(1)
        rm.close()
        return(idn)

    #This function is used to get the voltage
    def tensionPratiquefonc():

        global tensionPratique

        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        tensionPratique = inst.query("MEAS:VOLT?\x0A")
        time.sleep(1)
        rm.close()
        return(tensionPratique)

    #This function is used to get the capacity
    def capacitePratique():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        capacitePratique = inst.query("BATT:CAPA?\x0A")
        time.sleep(1)
        rm.close()
        return(capacitePratique)

    #This function is used to get the discharge current
    def courantPratique():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        courantPratique = inst.query("MEAS:CURRent?\x0A")
        time.sleep(1)
        rm.close()
        return(courantPratique)

    #This function is used to get the energy
    def puissancePratique():
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(comSelectionne)
        inst.baud_rate = baudrateSelectionne
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        puissancePratique = inst.query("MEAS:POWer?\x0A")
        time.sleep(1)
        rm.close()
        return(puissancePratique)

    #the following  lines are used to generate and manage a database to store battery datas
    genBDD = '''CREATE TABLE IF NOT EXISTS COURBE (
                    id INTEGER NOT NULL PRIMARY KEY,
                    capacite FLOAT,   
                    tensionCoupure FLOAT,
                    courantDecharge FLOAT,
                    tensionInitiale FLOAT);'''

    supBDD = '''DROP TABLE IF EXISTS COURBE'''

    ajouterVal = "INSERT INTO COURBE (capacite, tensionCoupure, courantDecharge, tensionInitiale) VALUES (?, ?, ?, ?)"

    conn = sqlite3.connect('bdd.db')
    cur = conn.cursor()
    cur.execute(supBDD)
    cur.execute(genBDD)
    conn.commit()
    cur.close()
    conn.close()


    tensionInitiale = tensionPratiquefonc()
    floatTensionInitiale = passageFloat(tensionInitiale)   

    modeBatterie()
    selectionTensionCoupure(tensionSel)
    selectionCourantDecharge(courantDechargeTh)

    if floatTensionInitiale < 10:
        finDecharge = 0
        valeurConformitePdf = 0

    lancementTest()

    #this is the main loop of the program. Its goal is to get battery datas and to store it in a database.
    #If the energy is under 1 Wh, we go out of the loop and we don't store the last data in the db
    while finDecharge == 1:

        tension = tensionPratiquefonc()
        capacite = capacitePratique()
        courant = courantPratique()
        puissance = puissancePratique()

        floatTension = passageFloat(tension)
        floatCapacite = passageFloat(capacite)
        floatCourant = passageFloat(courant)
        floatPuissance = passageFloat(puissance)

        if floatPuissance <= 1:
            finDecharge = 0
            arretTest()
        else:
            val = (floatCapacite, floatTension, floatCourant, floatTensionInitiale)
            conn = sqlite3.connect('bdd.db')
            cur = conn.cursor()
            cur.execute(ajouterVal, val)
            conn.commit()
            cur.close()
            conn.close()
    time.sleep(1)

    #here are some conditions
    #depending on the previous data, we can know if the battery is compliant or not
    #the valeurConformitePDF value is used in the genererPDF program.
    capaciteSel70 = capaciteSel*0.7
    capaciteSel50 = capaciteSel*0.5

    if floatCapacite > capaciteSel70:
        print('conforme')
        valeurConformitePdf = 1
    elif floatCapacite < capaciteSel70 and floatCapacite > capaciteSel50:
        valeurConformitePdf = 2
        print("problème d'équilibrage")        
    elif floatCapacite < capaciteSel50:
        print('non conforme : reconditionnement complet')
        valeurConformitePdf = 3
    else:
        print('problème scénario, décharge à refaire')
        valeurConformitePdf = 4

    return(valeurConformitePdf)

#inst = rm.open_resource('ASRL/dev/cu.usbserial-210::INSTR', query_delay=1)



