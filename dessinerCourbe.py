#################################################################
# This is the programe used to draw the battery discharge graph #
#################################################################

import matplotlib.pyplot as plt
import sqlite3


#fonction permettant de tracer la capacite de la tension en fonction de la batterie à partir d'une bdd. La figure est ensuite enregistrée dans le même dossier que les programme
def dessinerGraph(capaciteTh, tensionTh):

    #we fetch the datas in the db
    conn = sqlite3.connect("bdd.db")
    cur = conn.cursor()
    cur.execute('SELECT capacite, tensionCoupure from COURBE')
    data = cur.fetchall()
    capaciteTh = capaciteTh+0.5
    tensionTh = tensionTh+4
    capacite = []
    tensionCoupure = []

    for row in data:
        capacite.append(row[0])
        tensionCoupure.append(row[1])
    plt.plot(capacite, tensionCoupure, color = (1.0, 0.4, 0.0), linewidth=4)
    plt.xlabel('Capacity (Ah)')
    plt.ylabel('Voltage (V)')
    plt.grid(b = True, linestyle = 'dashed')
    plt.xlim(0,capaciteTh)
    plt.ylim(0,tensionTh)
    cur.close()
    conn.close()
    plt.savefig('courbe.png')

#(1.0, 0.4, 0.0)