# Projekt_3: Elections scraper

### Popis projektu
Projekt slouží k extrahování výsledků voleb do Poslanecké sněmovny Parlamentu České republiky v roce 2017.  <br>
Odkaz: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ. <br>
Program vyscrapuje výsledky hlasování pro všechny obce z vybraného okresu.

### Instalace knihoven
Soupis všech potřebných knihoven a jejich verzí je uložen v souboru requirements.txt.

### Spuštění projektu
Spuštění souboru Election_scraper.txt vyžaduje zadání 2 argumentů. <br>
První argument obsahuje odkaz, který územní celek chceme scrapovat, druhý argument obsahuje jméno výstupního souboru.  <br>
Nebo přímo z příkazového řádku  <br>
python Elections_scraper.py “https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102“ “volby_vysledky_Frydek_Mistek.csv“

### Příklad spuštění
import Elections_scraper <br>
Elections_scraper.volby_celkem_fce('https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102', 'volby_vysledky_Frydek_Mistek.csv')

### Částečný výstup
obec_kod,obec_nazev,volici_pocet,obalky_vydane,hlasy_platne,strana_1,strana_2, ...
598011,Baška,3093,2065,2053,175,1,1,124,1,49,192,21,12,21,1,0,216,0,0,44,665,2,9,194,1,16,7,3,293,5
598020,Bílá,285,178,178,19,0,0,14,0,10,21,3,1,0,1,0,12,1,0,3,52,0,0,15,0,3,0,0,23,0
511633,Bocanovice,358,197,197,20,0,0,32,0,3,13,3,1,0,0,0,18,0,1,1,45,0,0,43,0,0,0,0,17,0 <br>
...
