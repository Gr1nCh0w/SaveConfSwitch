
*Pour un meilleur affichage, Ouvrir avec Visual Studio Code et en haut à droite de la fenêtre, sélectionner l'icone avec une loupe.*

---

# Sauvegarde des configs des Switchs

Ce script **Python** permet de sauvegarder la configuration actuelle de chaque switch présent dans le fichier "Liste.txt" (à créer et à completer).

Les sauvegardes sont placées dans un dossier **SAVE**.
Le nom du fichier est l'IP du Switch en question.
Le fichier n'a pas d'extension par sécurité, il est possible d'en mettre un comme ".txt", pour ca il suffit de rentrer dans le code du script et de modifier la variable : **formatconfig**. Il est cependant possible d'ouvrir le fichier de conf via un éditeur de texte.
Pour ouvrir le fichier sans extension, il suffit de l'ouvrir avec Visual Studio Code. (Ou NotePad ++)

## Prèrequis

---
Exécuter sous **Linux**

**Python 3**

```bash
sudo apt-get install python3
```
**Pip Python3**

```bash
sudo apt-get install python3-pip
```
**Netmiko**

```bash
python3 -m pip install netmiko
```
---

Exécuter sous **Windows**

Installer Python : [LIEN](https://www.python.org/downloads/)

Ouvrir un CMD et exécuté les commandes suivantes

```bash
pip install netmiko
pip3 install netmiko
```
---

## Netmiko

[GitHub](https://github.com/ktbyers/netmiko)

Bibliothèque multi-fournisseur pour simplifier les connexions SSH aux périphériques réseaux.

---

## Fichier : Liste.txt

```bash
typeSwitch|ipSwitch|identifiantSSH|mdpSSH
```
Le fichier doit absolument être complété comme ci-dessus.

Liste des différents : ["typeSwitch"](https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py#L104)

Exemples de typeSwitch :

- aruba_os
- dell_os10
- mikrotik_routeros
- hp_comware
- hp_procurve

---

## Exécution

Sous Linux ou macOS

```bash
python3 save_conf.py
```

Sous Windows

```bash
python save_conf.py
```
---

Une Tâche Windows a été mise en place pour éxécuté le script tout les Lundis. 
La Tâche est visible dans le "Planificateur de Tâches" de Windows.
Tout les Lundis, il lance donc le "start.bat" qui s'occupe de lancer le script Python. 
