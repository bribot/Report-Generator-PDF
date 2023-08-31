# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 13:46:07 2023

@author: Bri
"""

from fpdf import FPDF
from datetime import datetime, timedelta
import time
import configparser
import sys


spacing = 10
tab = 100
normalFSize = 15
pageW = 200
pageH = 220
marginX = 10
marginY = 40
varsFilename = "./visionSystemVars.ini"
configFile = "config.ini"
outputPath = "./"


def getVarsFromVisionSystem(var):
    config = configparser.ConfigParser()
    config.read(varsFilename)
    configVar = config.get("vision", var)
    return configVar


def timeSplit(timeStr):
    #string = "8:30:20"
    now = datetime.now().replace(microsecond=0)
    startStamp = datetime.strptime(timeStr,"%H:%M:%S")
    startStamp = timedelta(hours=startStamp.hour,minutes=startStamp.minute,seconds=startStamp.second)
    start = now - startStamp
    #datetime.time()
    currentTime = now.strftime("%Y/%m/%d, %H:%M:%S")
    startTime = start.strftime("%Y/%m/%d, %H:%M:%S")
    
    #print(currentTime)
    #print(startTime)
    return currentTime, startTime
    


class PDF(FPDF):
    def header(self):
        # Logo
        
        self.image("logoL.png", pageW/20, 6, 0,28)
        self.image("logoR.png", 17*pageW/20, 6, 0,28)
        # Arial bold 15
        self.set_font('Arial', '', 22)
        # Move to the right
        self.cell(50)
        self.set_text_color(100)
        self.cell(pageW/2, 20, 'REPORTE DE LOTE', 0, 0, 'C')
        
        self.rect(10,5,200,30,'f')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        
        #reportGen.py varsFilename
def main():
    # global configFile
    # configFile = sys.argv[1]
    global varsFilename
    config = configparser.ConfigParser()
    config.read(configFile)
    outputPath = config.get("config", "output")
    varsFilename = config.get("config", "varsFile")
    
    #Vars from txt
    nLote = getVarsFromVisionSystem("nLote")
    nameLote = getVarsFromVisionSystem("nameLote")
    model = getVarsFromVisionSystem("model")
    userI = getVarsFromVisionSystem("userI")
    userF = getVarsFromVisionSystem("userF")
    # tProduction = getVarsFromVisionSystem("tProduction")
    nInspection = getVarsFromVisionSystem("nInspection")
    inspOK = getVarsFromVisionSystem("inspOk")
    inspNOK = getVarsFromVisionSystem("inspNOK")
    startTime = getVarsFromVisionSystem("startTime")
    stopTime = getVarsFromVisionSystem("stopTime")
    
    
    # Instantiation of inherited class
    pdf = PDF(format="Letter")
    
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', normalFSize)
    pdf.ln()
    #pdf.line(10, 40, 200, 40)
    pdf.rect(marginX, marginY, pageW, pageH)
    pdf.cell(tab,spacing,"Número de Lote:",0,0)
    pdf.cell(0,spacing,str(nLote),0,1)
    
    pdf.cell(tab,spacing,"Nombre de Lote:",0,0)
    pdf.cell(0,spacing,str(nameLote),0,1)
    
    pdf.cell(tab,spacing,"Nombre de Receta: ",0,0)
    pdf.cell(0,spacing,str(model),0,1)
    
    #currentTime,startTime = timeSplit(tProduction)
    
    
    pdf.cell(tab,spacing,"Inicio de Lote:",0,0)
    pdf.cell(0,spacing,startTime,0,1)
    
    
    pdf.cell(tab,spacing,"Final de Lote:",0,0)
    pdf.cell(0,spacing,stopTime,0,1)
    
    pdf.cell(tab,spacing,"Usuario Inicio:",0,0)
    pdf.cell(0,spacing,str(userI),0,1)
    
    pdf.cell(tab,spacing,"Usuario Final:",0,0)
    pdf.cell(0,spacing,str(userF),0,1)
    
    startTime = datetime.strptime(startTime,"%H:%M:%S")
    stopTime = datetime.strptime(stopTime,"%H:%M:%S")
    tProduction = stopTime - startTime
    pdf.cell(tab,spacing,"Tiempo de Producción:",0,0)
    pdf.cell(0,spacing,str(tProduction) + " hrs",0,1)
    
    pdf.ln()
    #////////////////////////////////////////////////////////
    pdf.set_font('Arial', 'B', normalFSize)
    pdf.cell(0,spacing,"Contadores:",0,1)
    pdf.set_font('Arial', '', normalFSize-3)
    pdf.set_fill_color(200)
    pdf.cell(60,spacing,"NOMBRE DE CONTADOR",1,0,"L",1)
    pdf.cell(60,spacing,"VALOR DE CONTADOR",1,0,"L",1)
    pdf.cell(60,spacing,"PORCENTAJE",1,1,"L",1)
    
    pdf.cell(60,spacing,"Total Inspeccionado (A)+(R)",1,0,"L",0)
    pdf.cell(60,spacing,str(nInspection),1,0,"L",0)
    pdf.cell(60,spacing,"",1,1,"L",0)
    
    
    pdf.cell(60,spacing,"Total Aceptado (A)",1,0,"L",0)
    pdf.cell(60,spacing,str(inspOK),1,0,"L",0)
    pdf.cell(60,spacing,str(100*float(inspOK)/float(nInspection) if float(nInspection) != 0 else 0)+ " %",1,1,"L",0)
    
    pdf.cell(60,spacing,"Total Rechazado (R)",1,0,"L",0)
    pdf.cell(60,spacing,str(inspNOK),1,0,"L",0)
    pdf.cell(60,spacing,str(100*float(inspOK)/float(nInspection) if float(nInspection) != 0 else 0) + " %",1,1,"L",0)
    
    
    #pdf.image("plot.png",x=20,w=180)
    outputFilename = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    
    pdf.output(outputPath + outputFilename + '.pdf', 'F')

if __name__ == "__main__":
    main()

