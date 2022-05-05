#Vybereme libovolný okres z
#https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ .
#Zadáme jeho url a požadované jméno výsledného csv souboru.
#Program vyscrapuje výsledky hlasování pro všechny obce z vybraného okresu.

import requests
from bs4 import BeautifulSoup
import csv

#Funkce zjišťující názvy obcí vybraného okresu

def nazvy_obci_fce(url_okres):
    odpoved = requests.get(url_okres)
    soup = BeautifulSoup(odpoved.text, 'html.parser')
    obec_nazev_pom = soup.find_all("td", {"class": "overflow_name"})
    obec_nazev = []
    for i in range(0, len(obec_nazev_pom)):
        obec_nazev.append(obec_nazev_pom[i].get_text())
    return obec_nazev

#Funkce zjišťující čísla kódů obcí vybraného okresu

def cisla_obci_fce(url_okres):
    odpoved = requests.get(url_okres)
    soup = BeautifulSoup(odpoved.text, 'html.parser')
    obec_kod_pom = soup.find_all("td", {"class": "cislo"})
    obec_kod = []
    for i in range(0, len(obec_kod_pom)):
        obec_kod.append(obec_kod_pom[i].get_text())
    return obec_kod

#Funkce zjišťující url výsledků hlasování obcí vybraného okresu

def url_okrsku_fce(url_okres):
    odpoved = requests.get(url_okres)
    soup = BeautifulSoup(odpoved.text, 'html.parser')
    obec_kod_pom = soup.find_all("td", {"class": "cislo"})
    url_obec = []
    for i in range(0, len(obec_kod_pom)):
        for a in obec_kod_pom[i].find_all('a'):
            url_obec.append('https://volby.cz/pls/ps2017nss/' + a['href'])
    return url_obec

#Funkce zjišťující počet voličů v obcích vybraného okresu

def volici_fce(url_obec):
    odpoved_obec = []
    soup_obec = []
    for i in range(0, len(url_obec)):
        odpoved_obec.append(requests.get(url_obec[i]))
        soup_obec.append(BeautifulSoup(odpoved_obec[i].text, 'html.parser'))
    volici_pocet = []
    for i in range(0, len(url_obec)):
        volici_pocet.append(soup_obec[i].find("td", {"headers": "sa2"}).get_text())
    #Vyhození mezery mezi tisicemi a jednotkami
    volici_pocet = [r.replace("\xa0", "") for r in volici_pocet]
    return volici_pocet

#Funkce zjišťující počet vydaných obálek v obcích vybraného okresu

def obalky_fce(url_obec):
    odpoved_obec = []
    soup_obec = []
    for i in range(0, len(url_obec)):
        odpoved_obec.append(requests.get(url_obec[i]))
        soup_obec.append(BeautifulSoup(odpoved_obec[i].text, 'html.parser'))
    obalky_vydane = []
    for i in range(0, len(url_obec)):
        obalky_vydane.append(soup_obec[i].find("td", {"headers": "sa3"}).get_text())
    obalky_vydane = [r.replace("\xa0", "") for r in obalky_vydane]
    return obalky_vydane

#Funkce zjišťující počet platných hlasů v obcích vybraného okresu

def hlasy_fce(url_obec):
    odpoved_obec = []
    soup_obec = []
    for i in range(0, len(url_obec)):
        odpoved_obec.append(requests.get(url_obec[i]))
        soup_obec.append(BeautifulSoup(odpoved_obec[i].text, 'html.parser'))
    hlasy_platne = []
    for i in range(0, len(url_obec)):
        hlasy_platne.append(soup_obec[i].find("td", {"headers": "sa6"}).get_text())
    hlasy_platne = [r.replace("\xa0", "") for r in hlasy_platne]
    return hlasy_platne

#Funkce zjišťující počty platných hlasů jednotlivých stran v obcích vybraného okresu

def strany_obec_fce(url_zadej_jedno):
    odpoved = requests.get(url_zadej_jedno)
    soup = BeautifulSoup(odpoved.text, 'html.parser')
    strany_sloupec1 = soup.find_all("td", {"headers": "t1sa2 t1sb3"})
    strany_sloupec2 = soup.find_all("td", {"headers": "t2sa2 t2sb3"})
    strany_hlasy1 = []
    strany_hlasy2 = []
    for j in range(0, len(strany_sloupec1)):
        strany_hlasy1.append(strany_sloupec1[j].get_text())
    for k in range(0, len(strany_sloupec2)):
        strany_hlasy2.append(strany_sloupec2[k].get_text())
    strany_hlasy = strany_hlasy1 + strany_hlasy2
    strany_hlasy = [r.replace("\xa0", "") for r in strany_hlasy]
    return strany_hlasy

#Funkce zjišťující čísla jednotlivých stran v obcích vybraného okresu

def cislo_strany(url_zadej_jedno):
    odpoved = requests.get(url_zadej_jedno)
    soup = BeautifulSoup(odpoved.text, 'html.parser')
    cislostrany_sloupec1 = soup.find_all("td", {"headers": "t1sa1 t1sb1"})
    cislostrany_sloupec2 = soup.find_all("td", {"headers": "t2sa1 t2sb1"})
    cislostrany_cast1 = []
    cislostrany_cast2 = []
    for j in range(0, len(cislostrany_sloupec1)):
        cislostrany_cast1.append(cislostrany_sloupec1[j].get_text())
    for k in range(0, len(cislostrany_sloupec2)):
        cislostrany_cast2.append(cislostrany_sloupec2[k].get_text())
    cislostrany_cast1a2 = cislostrany_cast1 + cislostrany_cast2
    cislostrany_cast1a2 = [r.replace("\xa0", "") for r in cislostrany_cast1a2]
    strana_1azn = []
    for cislo in range(0, len(cislostrany_cast1a2)):
        strana_1azn.append('strana_' + cislostrany_cast1a2[cislo])
    return strana_1azn

#Výsledná funkce

def volby_celkem_fce(url, vystup_csv):

    if ".csv" not in vystup_csv:
        print("Není zadán .csv soubor")

    else:
        if "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ" not in url:
            print("Špatně zadaný odkaz")
        else:

            obec_nazev = nazvy_obci_fce(url)
            obec_kod = cisla_obci_fce(url)
            url_obec = url_okrsku_fce(url)
            volici_pocet = volici_fce(url_obec)
            obalky_vydane = obalky_fce(url_obec)
            hlasy_platne = hlasy_fce(url_obec)

            obsah_prvnicast = []

            for i in range(0, len(volici_pocet)):
                obsah_prvnicast.append([obec_kod[i], obec_nazev[i], volici_pocet[i], obalky_vydane[i], hlasy_platne[i]])

            obsah_strany = []

            for i in range(0, len(volici_pocet)):
                obsah_strany.append(strany_obec_fce(url_obec[i]))

            obsah_celkem = []

            for i in range(0, len(obsah_prvnicast)):
                obsah_celkem.append(obsah_prvnicast[i] + obsah_strany[i])

            hlavicka = ['obec_kod', 'obec_nazev', 'volici_pocet', 'obalky_vydane', 'hlasy_platne'] + cislo_strany(url_obec[0])

            f = open(vystup_csv, 'w', newline='')
            f_writer = csv.writer(f)
            f_writer.writerow(hlavicka)
            f_writer.writerows(obsah_celkem)
            f.close()



