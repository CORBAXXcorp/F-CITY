# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:15:28 2022

@author: corbe
"""
import numpy as np
import json
import time 
from time import sleep


#
#tab=np.genfromtxt(filenames,deletechars='s')

"""
Pensez à utilisez mydatetime ou fichier pour crée
les tableaux associé aux documents

"""
#tabX=np.loadtxt(myDatetimeX)
"""
tab0=np.loadtxt("/var/www/html/PROJET/myDatetime1")
tab2=np.loadtxt("/var/www/html/PROJET/myDatetime3")
tab3=np.loadtxt("/var/www/html/PROJET/myDatetime4")
tab4=np.loadtxt("/var/www/html/PROJET/myDatetime5")
tab5=np.loadtxt("/var/www/html/PROJET/myDatetime6")

tab1=np.genfromtxt("myDatetime2",deletechars='s')

"""

tab0=np.loadtxt("/var/www/html/PROJET/2021-04-26-17-16-58-Voie1_A.txt")
tab2=np.loadtxt("/var/www/html/PROJET/2021-04-26-17-16-58-Voie3_A.txt")
tab3=np.loadtxt("/var/www/html/PROJET/2021-04-26-17-16-58-Voie4_V.txt")
tab4=np.loadtxt("/var/www/html/PROJET/2021-04-26-17-16-58-Voie5_V.txt")
tab5=np.loadtxt("/var/www/html/PROJET/2021-04-26-17-16-58-Voie6_V.txt")

tab1=np.genfromtxt("/var/www/html/PROJET/2021-04-26-17-16-58-Voie2_A.txt",deletechars='s')

"""BAT"""

T=tab0[:,0]

A1=tab0[0:2000,1]
V6=tab5[0:2000,1]

Puissance=round(np.mean(A1*V6),2)


"""
A2=tab1[:,1]
V4=tab3[:,1]
"""

"""BOUCLE TEMPS"""
i=0
cpt=0
n=0

while(cpt==n):
    A3=tab2[n:n+2000,1]
    V5=tab4[n:n+2000,1]
    Puissance_1=round(np.mean(A3*V5),2)
    T=tab0[n:n+2000,0]
    
    E=round(np.mean(Puissance_1*T),2)
    
    #print(Puissance_1)
    n+=2001
    cpt+=2001
    
    """FICHIER"""
  
    Param={
            "Puissance" : Puissance,
            "Puissance_1" : Puissance_1,
            "Energie" : E
        }


    
    Puissance_json=json.dumps(Param)

    print(Puissance_json)
    
    time.sleep(2)

    fichier=open('/var/www/html/PROJET/data.json','w+')
    fichier.write(Puissance_json)
    fichier.close()

  
    



#timestamp
#crée fichier
#code json
#gps



"""
Puissance_2=A2*V4
"""



    
