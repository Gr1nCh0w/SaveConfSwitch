# =================================================
#        Script de Sauvegarde pour Switchs 
# =================================================

# Pour plus d'info, lire "README.txt"

import os
import platform
import datetime
import sys
import time
from netmiko import ConnectHandler
import netmiko


# ======================================
# Variable Global
# ======================================
fichierListe = "./Liste.txt"
DossierSave = "./SAVE"
nbLignes = 0
formatConfig = ""
Date = datetime.datetime.now()
textBleu = '\033[94m'
textVert = '\033[92m'
textJaune = '\033[93m'
textRouge = '\033[91m'
textGras = '\033[1m'
textClassique = '\033[0m'
log = open("./log.txt", "w+")
# ======================================

if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")


# Verification si le Dossier "SAVE", ou sera stocker les configs, existe, sinon, le creer
if not os.path.exists(DossierSave):
    os.system("mkdir " + DossierSave)

print(textBleu + "\n===================================================")
print(textBleu + "=     Sauvegarde Automatique des Switchs v1       =")
print(textBleu + "===================================================\n" + textClassique)

# Ouverture du fichier contenant les infos de tout les switchs (Ouverture en mode Lecture --> "r")
try:
    fichier = open(fichierListe, "r")
except:
    print(textRouge + "Le Fichier n'a pas l'air d'exister.." + textClassique)
    log.write("[" + str(Date) + "] Erreur : Le Fichier " + str(fichierListe) + " n'existe pas, le programme a quitter sans s'executer.\n")
    os.system("pause")
    sys.exit(1)

# Obtention de toutes les lignes du fichier
lignes = fichier.readlines()
nbLignesTotal = len(lignes)
print("[ ... ] Nombre de switchs a sauvegarder : " + textGras + str(nbLignesTotal) + "\n" + textClassique)

if nbLignesTotal != 0:
    print(textBleu + "[ ... ] Sauvegarde des configs en cours... \n" + textClassique)

    for line in lignes:
        nbLignes = nbLignes + 1

        ligne = line.rstrip('\n')
    
        infoSwitch = ligne.split('|')
        
        # Recuperation de chaque donnee : type, IP, Identifiant et MDP
        typeSwitch = infoSwitch[0]
        ipSwitch = infoSwitch[1]
        identifiantSwitch = infoSwitch[2]
        mdpSwitch = infoSwitch[3]

        # Debut de la sauvegarde
        print("[" + str(nbLignes) + "] " + str(ipSwitch) + " .. ", end="", flush=True)

        # Connexion sur le Switch
        try:
            net_connect = ConnectHandler(device_type=typeSwitch, host=ipSwitch, username=identifiantSwitch, password=mdpSwitch)

            # Verification OS et du modele car certains ajustement sont necessaires
            if typeSwitch == "mikrotik_routeros":
                
                config = net_connect.send_command_timing("export", delay_factor=2)
            
            elif typeSwitch == "hp_comware":
                
                if ipSwitch == "10.1.1.101" or ipSwitch == "10.1.1.202":
                    
                    # Les switchs HPE 1910 non pas acces a toute les commandes lors d'un login.
                    # Du coup, un fichier "1910Config.txt" dans le dossier "ConfigFile" est utilise pour envoyer les commandes
                    # qui permettent d'avoir acces a toutes les commandes

                    ConfigFile = open("./ConfigFile/1910Config.txt")
                    ConfigSet = ConfigFile.read()
                    ConfigFile.close()
                    net_connect.send_command_timing(ConfigSet)

                    config = net_connect.send_command_timing("display current-configuration")

                else:

                    config = net_connect.send_command_timing("display current-configuration")

            elif ipSwitch == "10.1.1.254":

                # Le MSM760 demande aussi des commandes intermediaires pour pouvoir executer la commande de save.
                # Son fichier de config est 'MSM760.txt'

                ConfigFile = open("./ConfigFile/MSM760.txt")
                ConfigSet = ConfigFile.read()
                ConfigFile.close()
                net_connect.send_command_timing(ConfigSet)
                
                config = net_connect.send_command_timing("show all config")

            else:
                
                # Les switchs qui n'ont pas besoin de commande speciales passent par la commande "universelle" :
                config = net_connect.send_command_timing("show running-config")

            # Ouverture du fichier qui va contenir la config du Switch (PS : Son nom = ipSwitch)
            name = str(ipSwitch)

            # Creation ou Ouverture du fichier correspondant au switch. 
            # Le fichier n'a pas d'extension. Pour en configurer une, il faut completer la variable "formatConfig"
            txtConfig = open("./SAVE/" + name + formatConfig, "w+")

            # Ecriture de la config du Switch dans son fichier de sauvegarde
            txtConfig.write(str(config))

            # Fermeture fichier
            txtConfig.close()

            print(textVert + "OK" + textClassique)

        except:

            print("\n" + textRouge + "[ ERREUR ] Impossible de se connecter au switch " + str(ipSwitch) + "! Erreur probable dans le fichier Liste.txt" + textClassique)
            log.write("[" + str(Date) + "] [ ERREUR ] Impossible de se connecter au switch " + str(ipSwitch) + "! Erreur probable dans le fichier Liste.txt\n")
            pass

    # Fermeture de la liste des switch
    fichier.close()

    print(textVert + "\n[ OK ] Sauvegarde terminee !\n" + textClassique)
else:

    print(textRouge + "Aucune ligne trouvee dans le fichier Liste. Le Programme est finis." + textClassique)
    log.write("[" + str(Date) + "] Aucune ligne trouvee dans le fichier Liste. Le Programme est finis.")
    sys.exit(1)
