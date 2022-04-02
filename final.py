# -*- coding: utf-8 -*-
import serial
import matplotlib.pyplot as plt
import datetime
import pandas as pd

N = 1042*60*5

VoieV = 100
VoieA = 500

  
ser = serial.Serial('COM3', 781250, timeout=0,parity=serial.PARITY_ODD)    #ouvre le port COM. voir dans le gestionnaire de periphérique le port COM associé au FDTI

print(ser.isOpen())                                                       #Check si le port est ouvert (Reponse écran True)
i1=0
i2=0
i3=0
i4=0
i5=0
i6=0
cptEch = 0
CptError = 0
serialString = ""                                                           # Used to hold data coming over UART
cpt=0                                                                       #init compteur d'init
cptBUGS=0                                                              # Log une voie particulière, 0 sinon
cptHEXA=0
EchInt = 0

#Initialisation du buffer, suppression des artefacts
serialChar = b'1'                                                       #init Buffer de byte
serialString = bytearray()                                              #init buffer du message UART
while(serialChar!=b'\x0a'):                                             #Fin du mot et passage au suivant sur LF
    if(ser.in_waiting > 0):                                             #si au moins un byte recu
        # Read data out of the buffer until a carraige return / new line is found
        serialChar = ser.read(1)                                        #lecture du byte
        asciiChar = bytes(serialChar)
        try:    
            asciiChar.decode('ascii')
        except:
            serialString = serialString + bytes(b'\x28')                 #concatenation au mot en cours
        else:
            serialString = serialString + asciiChar                 #concatenation au mot en cours
if(ser.in_waiting>0):
    OldEchInt = EchInt
    EchInt = ord(ser.read(1))

Fin = EchInt + N
Data = 0                                                                    #futur data
Voie = 0                                                                    #futur selection de voies
cpt = 0                                                                     # permet de scanner N echantillons
demarrage = 0                                             #N echantillons

VoieNum1 = [None] * (N*2)
VoieNum2 = [None] * (N*2)
VoieNum3 = [None] * (N*2)
VoieNum4 = [None] * (N*2)
VoieNum5 = [None] * (N*2)
VoieNum6 = [None] * (N*2)
                     
VoieEch1 = [None] * (N*2)
VoieEch2 = [None] * (N*2)
VoieEch3 = [None] * (N*2)
VoieEch4 = [None] * (N*2)
VoieEch5 = [None] * (N*2)
VoieEch6 = [None] * (N*2)

                                     
#Demarrage de l'acquisition
while((cptEch * 256 + EchInt)<Fin-6):                                                               # remplacer LOG par 0 pour une boucle infini
    cpt = cpt + 1;
    # Wait until there is data waiting in the serial buffer
    serialChar = b'1'                                                       #init Buffer de byte
    serialString = bytearray()                                              #init buffer du message UART
    while(serialChar!=b'\x0a'):                                             #Fin du mot et passage au suivant sur LF
        if(ser.in_waiting > 0):                                             #si au moins un byte recu
            # Read data out of the buffer until a carraige return / new line is found
            serialChar = ser.read(1)                                        #lecture du byte
            asciiChar = bytes(serialChar)
            try:    
                asciiChar.decode('ascii')
            except:
                serialString = serialString + bytes(b'\x28')                 #concatenation au mot en cours
            else:
                serialString = serialString + asciiChar                 #concatenation au mot en cours
    if(ser.in_waiting>0):
        OldEchInt = EchInt
        EchInt = ord(ser.read(1))
        if OldEchInt>250 and EchInt<10 :
            cptEch = cptEch + 1
    try:
        DecodeString = serialString.decode('Ascii')                             #transforme le bytearray en string
    except:
        DecodeString = "BUG"+b'\x0a'.decode('Ascii')                           #transforme le bytearray en string
        cptBUGS=cptBUGS+1
    else:
        if len(DecodeString)==5 :                                               #si on a 5 caractères on est OK
            VoieChar = DecodeString[0]                                              #selection du byte de voie
            HexaData = DecodeString[1]+DecodeString[2]+DecodeString[3]              #selection du code Hexa 12 bits
                                                    #memo de voie courant pour comparaison au prochain coup
                                                      # passage en decimal de l'acquisition data en cours
            OldVoie = Voie;           
            Voie = ord(VoieChar)-32

            if Voie<1 or Voie>6 :
                if OldVoie<6 :
                    Voie = OldVoie+1
                else :
                    Voie = 6
                
            if Voie==1:  
                try :                                          # passage en decimal de l'acquisition voie en cours
                    VoieNum1[i1] = int(HexaData, 16)
                    VoieEch1[i1]= cptEch * 256 + EchInt
                except:
                    if i1 != 0 :
                        VoieNum1[i1] = VoieNum1[i1-1]  
                        VoieEch1[i1] = cptEch * 256 + EchInt
                    cptHEXA = cptHEXA+1
                    i1 = i1+1
                else:                
                    i1 = i1+1
            if Voie==2:                                            # passage en decimal de l'acquisition voie en cours
                try:
                    VoieNum2[i2] = int(HexaData, 16)
                    VoieEch2[i2]=cptEch * 256 + EchInt
                except:
                    if i2 != 0 :
                        VoieNum2[i2] = VoieNum2[i2-1]   
                        VoieEch2[i2] = cptEch * 256 + EchInt
                    cptHEXA = cptHEXA+1
                    i2=i2+1
                else:                
                    i2=i2+1
            if Voie==3:                                            # passage en decimal de l'acquisition voie en cours
                try:
                    VoieNum3[i3] = int(HexaData, 16)
                    VoieEch3[i3] = cptEch * 256 + EchInt
                except:
                    if i3 != 0 :
                        VoieNum3[i3] = VoieNum3[i3-1] 
                        VoieEch3[i3] = cptEch * 256 + EchInt
                    cptHEXA = cptHEXA+1
                    i3=i3+1
                else:
                    i3=i3+1
            if Voie==4:                                            # passage en decimal de l'acquisition voie en cours
                try:
                    VoieNum4[i4] = int(HexaData, 16)
                    VoieEch4[i4] = cptEch * 256 + EchInt
                except:
                    if i4 != 0 :
                        VoieNum4[i4] = VoieNum4[i4-1]  
                        VoieEch4[i4] = cptEch * 256 + EchInt
                    cptHEXA = cptHEXA+1
                    i4=i4+1
                else:
                    i4=i4+1
            if Voie==5:                                            # passage en decimal de l'acquisition voie en cours
                try:
                    VoieNum5[i5] = int(HexaData, 16)
                    VoieEch5[i5] = cptEch * 256 + EchInt
                except:
                    if i5 != 0 :
                        VoieNum5[i5] = VoieNum5[i5-1]   
                        VoieEch5[i5] = cptEch * 256 + EchInt
                    cptHEXA = cptHEXA+1
                    i5=i5+1
                else:
                    i5=i5+1
            if Voie==6:                                            # passage en decimal de l'acquisition voie en cours
                try:
                    VoieNum6[i6] = int(HexaData, 16)
                    VoieEch6[i6] = cptEch * 256 + EchInt
                except:
                    if i6 != 0 :
                        VoieNum6[i6] = VoieNum6[i6-1]  
                        VoieEch6[i6] = cptEch * 256 + EchInt
                    cptHEXA = cptHEXA+1
                    i6=i6+1
                else:
                    i6=i6+1
                                        #On log si LOG=1
        else :  
            VoieChar = DecodeString[0]                                              #selection du byte de voie

            OldVoie = Voie;           
            Voie = ord(VoieChar)-32  

            if Voie<1 or Voie>6 :
                try :
                    VoieChar = DecodeString[1]  
                except:
                    VoieChar = '\x38'                                             #selection du byte de voie        
                Voie = ord(VoieChar)-32  
                if Voie<1 or Voie>6 :               
                    CptError = CptError  + 1
                
            if Voie==1:  
                if i1 != 0 :
                    VoieNum1[i1] = VoieNum1[i1-1]  
                    VoieEch1[i1]= cptEch * 256 + EchInt
                cptHEXA = cptHEXA+1
                i1 = i1+1
            if Voie==2:                                            # passage en decimal de l'acquisition voie en cours
                if i2 != 0 :
                    VoieNum2[i2] = VoieNum2[i2-1]  
                    VoieEch2[i2]= cptEch * 256 + EchInt
                cptHEXA = cptHEXA+1
                i2 = i2+1
            if Voie==3:                                            # passage en decimal de l'acquisition voie en cours
                if i3 != 0 :
                    VoieNum3[i3] = VoieNum3[i3-1]      
                    VoieEch3[i3]= cptEch * 256 + EchInt
                cptHEXA = cptHEXA+1
                i3 = i3+1
            if Voie==4:                                            # passage en decimal de l'acquisition voie en cours
                if i4 != 0 :
                    VoieNum4[i4] = VoieNum4[i4-1]  
                    VoieEch4[i4]= cptEch * 256 + EchInt
                cptHEXA = cptHEXA+1
                i4 = i4+1
            if Voie==5:                                            # passage en decimal de l'acquisition voie en cours
                if i5 != 0 :
                    VoieNum5[i5] = VoieNum5[i5-1]   
                    VoieEch5[i5]= cptEch * 256 + EchInt
                cptHEXA = cptHEXA+1
                i5 = i5+1
            if Voie==6:                                            # passage en decimal de l'acquisition voie en cours
                if i6 != 0 :
                    VoieNum6[i6] = VoieNum6[i6-1]   
                    VoieEch6[i6]= cptEch * 256 + EchInt
                cptHEXA = cptHEXA+1
                i6 = i6+1




ser.close()    
print(ser.isOpen())                                                         #Check si le port est ouvert (Reponse écran False)

                                                              #fermeture du port COM

myDatetime = datetime.datetime.now()
myString = myDatetime.strftime('%Y-%m-%d-%H-%M-%S')


myDatetime1 = myString + "-Voie1_A.txt" 
myDatetime2 = myString + "-Voie2_A.txt" 
myDatetime3 = myString + "-Voie3_A.txt" 
myDatetime4 = myString + "-Voie4_V.txt" 
myDatetime5 = myString + "-Voie5_V.txt" 
myDatetime6 = myString + "-Voie6_V.txt" 

fichier1 = open(myDatetime1, "wt")
fichier2 = open(myDatetime2, "wt")
fichier3 = open(myDatetime3, "wt")
fichier4 = open(myDatetime4, "wt")
fichier5 = open(myDatetime5, "wt")
fichier6 = open(myDatetime6, "wt")
                                                      #fermeture du fichier si LOG=1
print("erreur Comm ",CptError)
print("erreur BUGS ",cptBUGS)  
print("erreur HEXA ",cptHEXA)    
ErrEch = i1+i2+i3+i4+i5+i6
print("Nb ech",N)
print("ech perdu ",6*N-6-ErrEch)

plt.plot(VoieEch1,VoieNum1)
plt.show()
  
plt.plot(VoieEch2,VoieNum2)
plt.show()
  
plt.plot(VoieEch3,VoieNum3)
plt.show()
   
plt.plot(VoieEch4,VoieNum4)
plt.show()
   
plt.plot(VoieEch5,VoieNum5)
plt.show()
  
plt.plot(VoieEch6,VoieNum6)
plt.show()

print("i1 ",i1)  
print("i2 ",i2)  
print("i3 ",i3)  
print("i4 ",i4)  
print("i5 ",i5)  
print("i6 ",i6)  


a1=0
a2=0
a3=0
a4=0
a5=0
a6=0
print("Debut d'ecriture fichier : traitement des echantillons")
cont = True
ErrEch=0
while(cont):
    V= [VoieEch1[a1],VoieEch2[a2],VoieEch3[a3],VoieEch4[a4],VoieEch5[a5],VoieEch6[a6]]
    df=pd.DataFrame(V,index=[1,2,3,4,5,6],columns=['x'])
    if not (None in V) :
        if (df.max()["x"]==df.min()["x"])  :
            str1 = str(VoieEch1[a1]/1024.0)
            str2 = " "
            str3 = str((VoieNum1[a1]-1966)/2130*VoieA)
            str4 = str1 + str2 + str3 + "\n"
            fichier1.write(str4)
            str1 = str(VoieEch2[a2]/1024.0)
            str2 = "s "
            str3 = str((VoieNum2[a2]-1966)/2130*VoieA)
            str4 = str1 + str2 + str3 + "\n"
            fichier2.write(str4)    
            str1 = str(VoieEch3[a3]/1024.0)
            str2 = " "
            str3 = str((VoieNum3[a3]-1966)/2130*VoieA)
            str4 = str1 + str2 + str3 + "\n"
            fichier3.write(str4)  
            str1 = str(VoieEch4[a4]/1024.0)
            str2 = " "
            str3 = str((VoieNum4[a4]-2048)/2048*VoieV)
            str4 = str1 + str2 + str3 + "\n"
            fichier4.write(str4)
            str1 = str(VoieEch5[a5]/1024.0)
            str2 = " "
            str3 = str((VoieNum5[a5]-2048)/2048*VoieV)
            str4 = str1 + str2 + str3 + "\n"
            fichier5.write(str4)
            str1 = str(VoieEch6[a6]/1024.0)
            str2 = " "
            str3 = str((VoieNum6[a6])/4096*VoieV)
            str4 = str1 + str2 + str3 + "\n"
            fichier6.write(str4)   
            ErrEch+=1
            a1+=1
            a2+=1
            a3+=1
            a4+=1
            a5+=1
            a6+=1
        else :
            f = df.idxmin()
            ap= f["x"]
            if ap == 1 :
                a1 +=1
            elif ap==2:
                a2 +=1
            elif ap==3:
                a3+=1
            elif ap==4:
                a4+=1
            elif ap==5:
                a5+=1
            else :
                a6+=1
    if (a1==N) or (a2==N) or (a3==N) or (a4==N) or (a5==N) or (a6==N) or (None in V): 
        cont = False

print("Fermeture des fichiers: Fin de l'enregistrement")

print("Nb ech",N)
print("ech perdu au final ",N-1-ErrEch)
    
fichier1.close()  
fichier2.close()  
fichier3.close()  
fichier4.close()  
fichier5.close()  
fichier6.close()  
