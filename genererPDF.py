##################################################
# This program  allows the generation of the PDF #
##################################################

from fpdf import FPDF
from datetime import datetime
import dessinerCourbe
import sqlite3
import os


def creationPDF(nomClient, refBatterie, capaciteTh, tensionTh, valeurConformitePdf, tensionFull):

    pdfConforme = int(valeurConformitePdf)
    capaciteTheorique = capaciteTh
    tensionTheorique = tensionTh
    nomDuClient = nomClient
    referenceBatterie = refBatterie
    tensionPleine = int(tensionFull)
    date = datetime.today().strftime('%d-%m-%Y %H:%M:%S')

    #go to the db and select all datas
    conn = sqlite3.connect('bdd.db')
    cur = conn.cursor()
    cur.execute("SELECT capacite FROM COURBE ORDER BY id DESC LIMIT 1")
    capaciteFinale = cur.fetchone()
    cur.execute("SELECT tensionCoupure FROM COURBE ORDER BY id DESC LIMIT 1")
    tensionCoupureFinale = cur.fetchone()
    cur.execute("SELECT courantDecharge FROM COURBE ORDER BY id DESC LIMIT 1")
    courantDechargeFinal = cur.fetchone()
    cur.execute("SELECT tensionInitiale FROM COURBE ORDER BY id DESC LIMIT 1")
    tensionInitiale = cur.fetchone()

    #when we fetch a a data from a db, it comes in this form '(100.0,)'
    #the following lines are used to delete the comma and the brackets
    capaciteFinale = str(capaciteFinale)
    capaciteFinale = capaciteFinale[1:len(capaciteFinale)-2]
    tensionCoupureFinale = str(tensionCoupureFinale)
    tensionCoupureFinale = tensionCoupureFinale[1:len(tensionCoupureFinale)-2]
    courantDechargeFinal = str(courantDechargeFinal)
    courantDechargeFinal = courantDechargeFinal[1:len(courantDechargeFinal)-2]
    tensionInitiale = str(tensionInitiale)
    tensionInitiale = tensionInitiale[1:len(tensionInitiale)-2]

    #all of the commands which start by pdf. are used to write or draw the pdf
    pdf = FPDF(format='letter', unit='mm')
    pdf.add_page()
    pdf.image('logo.png', w = 100, h=42)

    pdf.set_text_color(0,0,0)
    pdf.set_font('Helvetica', 'b', 22)
    pdf.ln(h=6)

    pdf.cell(75, 0, 'Battery reference: ')
    pdf.cell(0,0, '{}'.format(referenceBatterie))
    pdf.set_font('Helvetica', '', 16)
    pdf.ln(h=10)

    pdf.cell(47, 0, 'Customer name: ')
    pdf.cell(0,0, '{}'.format(nomDuClient))
    pdf.ln(h=6)

    pdf.cell(47, 0, 'Test date: ')
    pdf.cell(0, 0, date)
    pdf.ln(h=20)

    pdf.cell(100, 0, 'Initial features')
    pdf.cell(0,0, 'Discharge cycle')
    pdf.ln(h=8)

    pdf.set_font('Helvetica', '', 12)
    pdf.cell(22, 0, 'Capacity: ')
    pdf.cell(10,0, '{}'.format(capaciteTheorique))
    pdf.cell(68,0, 'Ah')
    pdf.cell(45, 0, 'Capacity: ')
    pdf.cell(13,0, '{}'.format(capaciteFinale))
    pdf.cell(0,0, 'Ah')
    pdf.ln(h=6)

    pdf.cell(22, 0, 'Voltage: ')
    pdf.cell(10,0, '{}'.format(tensionTheorique))
    pdf.cell(68,0, 'V')
    pdf.cell(45, 0, 'Cut-off voltage: ')
    pdf.cell(13,0, '{}'.format(tensionCoupureFinale))
    pdf.cell(0,0, 'V')
    pdf.ln(h=6)

    pdf.cell(100, 0, '')
    pdf.cell(45, 0, 'Initial Voltage: ')
    pdf.cell(13,0, '{}'.format(tensionInitiale))
    pdf.cell(0, 0, 'V')
    pdf.ln(h=6)

    pdf.cell(100, 0, '')
    pdf.cell(45, 0, 'Discharge current: ')
    pdf.cell(13,0, '{}'.format(courantDechargeFinal))
    pdf.cell(0, 0, 'A')
    pdf.ln(h=15)

    pdf.set_font('Helvetica', 'b', 16)

    if pdfConforme == 0:
        pdf.image('croixRouge.png', 10, 130, w =10, h=10)
        pdf.cell(10, 0, " ")
        pdf.cell(0, 0, "BATTERY NON-COMPLIANT: Test not launched")
    elif pdfConforme == 1:
        pdf.image('checkVert.png', 10, 134, w =10, h=10)
        pdf.cell(10, 0, " ")
        pdf.cell(0, 0, 'BATTERY COMPLIANT')
    elif pdfConforme == 2:
        pdf.image('croixRouge.png', 10, 130, w =10, h=10)
        pdf.cell(10, 0, " ")
        pdf.cell(0, 0, 'BATTERY NON-COMPLIANT: Provide for a rebalancing')
    elif pdfConforme == 3:
        pdf.image('croixRouge.png', 10, 130, w =10, h=10)
        pdf.cell(10, 0, " ")
        pdf.cell(0, 0, 'BATTERY NON-COMPLIANT: Provide for a complete reconditioning')
    else:
        pdf.image('croixRouge.png', 10, 130, w =10, h=10)
        pdf.cell(10, 0, " ")
        pdf.cell(0, 0, 'SCENARIO PROBLEM: the discharge has to be redone')
    pdf.ln(h=5)

    #we call the function to draw the battery discharge graph 
    floatCapaciteFinale = float(capaciteFinale)
    dessinerCourbe.dessinerGraph(floatCapaciteFinale, tensionFull)
    pdf.cell(22.5, 0, '')
    pdf.image('courbe.png', w = 150, h=112.5)

    pdf.add_page()
    pdf.ln(h=8)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 0, "Notes")
    pdf.ln(h=8)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(195, 5, "- What is rebalancing? It is possible that some rows of cells have a lower voltage than the others. The goal is to restore the voltage of these rows to the same level as those of the other rows in order to regain an autonomy equivalent to the original one.", 0, 'J', 0)
    pdf.ln(h=1)
    pdf.multi_cell(195, 5, "- What is complete reconditioning? If the battery has major defects, it may be preferable to change the totality of the cells to start again with new ones.", 0, 'J', 0)
    pdf.ln(h=15)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.multi_cell(195, 5, "Warning: The age of the battery is also a parameter to take into account:", 0, 'J', 0)
    pdf.ln(h=6)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(195, 5,"- If the battery is less than 3 years old, all repairs are possible and can effectively improve the battery life.", 0, 'J', 0)
    pdf.ln(h=1)
    pdf.multi_cell(195, 5,"- Beyond 3 years, the gain of a rebalancing can be less, but repairs are still interesting to extend the life of the battery.", 0, 'J', 0)
    pdf.ln(h=1)
    pdf.multi_cell(195, 5,"- If the battery is more than 5 years old, a complete reconditioning may be preferable because a loss of autonomy is certainly due to cells at the end of their potential.", 0, 'J', 0)
    pdf.ln(h=5)

    #the pdf name is the client name and battery reference
    nomPdf = str(nomDuClient) + " " + str(referenceBatterie)

    #we create a directory named pdf in order to sore them inside
    if not os.path.exists('pdf'):
        os.mkdir('pdf')

    pdf.output('pdf/{}.pdf'.format(nomPdf))