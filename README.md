# ET5410 discharge battery software

This project was realized within the context of an internship in the company OZO, from June to August 2022. The goal of the project is to create an executable software allowing to communicate with two models of test bench: the ET5410 and the ET5410+. These machines allow among other things to discharge batteries. The software can then generate a PDF with the important information of the battery and a discharge curve. At the end, it can give a first opinion on the (non) conformity of the battery.

## Structure of the project :

This project consists of four main programs:

![Image text](/Users/guilhem/Desktop/CaptureLog.png)

- LogicielBancDeTestOZO.py is the main program. It allows to generate the interface. It is divided into four major parts:

    - In the first part, it is possible to choose the right COM port and the baudrate. The latter depends on the device used: 9600 if it is the ET5410+ and 115200 if it is the ET5410 ;
    - The second part is used to enter the various information concerning the battery.  It is important to enter the theoretical voltage and capacity of the battery because these are the parameters which will participate in the determination of the (no) conformity of the battery ;
    - The third part allows to launch the test, but the button will only work when the battery is connected to the test bench and the latter is connected to a PC ;
    - The fourth part allows to generate the PDF but the test must be finished first ;
- dcLoad.py allows the communication with the machine. It contains functions in which are SCPI commands. It is thanks to this protocol that the communication is possible ;
- genererPDF.py allows to generate the PDF ;
- drawCorube allows to draw the battery discharge graph ;

A last program, named setup.py is used to transform the programs into an executable file.

## Installation :

The project has been realized with Python 3.10.6.  The whole project has been made in Python but some databases (made with sqlite) are required.
Here is the list of necessary libraries: tkinter, fpdf, fpdf2, pyvisa, pyvisa-py, sqlite3, pyserial, datetime, time, matplotlib, os, sys, cx_Freeze.

The project is functional: it could however be improved by making a cross-platform executable, improving the interface to make it more aesthetic or adding more languages.

