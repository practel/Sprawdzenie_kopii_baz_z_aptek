import os
import time
import datetime
import smtplib
import fnmatch
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class Apteka:
    def __init__(self, id_kamsoft, nazwa, sciezka_1dzienna, plik_1dzienna, sciezka_2dzienna, plik_2dzienna, sciezka_1godzinowa, plik_1godzinowa, sciezka_2godzinowa, plik_2godzinowa, max_wielkosc_1):
        self.id_kamsoft = id_kamsoft
        self.nazwa = nazwa
        self.sciezka_1dzienna = sciezka_1dzienna
        self.plik_1dzienna = plik_1dzienna
        self.sciezka_2dzienna = sciezka_2dzienna
        self.plik_2dzienna = plik_2dzienna
        self.sciezka_1godzinowa = sciezka_1godzinowa
        self.plik_1godzinowa = plik_1godzinowa
        self.sciezka_2godzinowa = sciezka_2godzinowa
        self.plik_2godzinowa = plik_2godzinowa
        self.max_wielkosc_1 = max_wielkosc_1

    def __str__(self):
        return f"Apteka: ID Kamsoft - {self.id_kamsoft}, Nazwa - {self.nazwa}, Plik1 - {self.sciezka_1dzienna}"
class KatalogAptek:
    def __init__(self):
        self.apteki = []
    def wczytaj_apteki_z_pliku(self, nazwa_pliku = 'ListaAptek.txt'):
        self.apteki = []  # Wyczyść istniejącą listę aptek
        try:
            with open(nazwa_pliku, "r") as plik:
                for linia in plik:
                    dane_apteki = linia.strip().split(',')
                    if len(dane_apteki) == 11:
                        id_kamsoft, nazwa, sciezka_1dzienna, plik_1dzienna, sciezka_2dzienna, plik_2dzienna, sciezka_1godzinowa, plik_1godzinowa, sciezka_2godzinowa, plik_2godzinowa, max_wielkosc_1 = map(str.strip, dane_apteki)
                        apteka = Apteka(int(id_kamsoft), nazwa, sciezka_1dzienna, plik_1dzienna, sciezka_2dzienna, plik_2dzienna, sciezka_1godzinowa, plik_1godzinowa, sciezka_2godzinowa, plik_2godzinowa, max_wielkosc_1)
                        self.apteki.append(apteka)
                    else:
                        print(f"Błąd w linii: {linia}. Pomijanie tej linii.")
        except FileNotFoundError:
            print(f"Plik {nazwa_pliku} nie istnieje.")

    def sprawdz_plik(self, sciezka_katalogu,szukany_plik,nazwa_apteki,max_wielkosc_1):
        dzisiejsza_data = datetime.date.today()
        wynikjest = []
        wynikbrak = []
        wiek_pliku = 0
        rozmiar1 = 0.01
        plik_poprzedni = ""
        max_wielposc_pliku = max_wielkosc_1
        rodzaj_bledu ='Brak pliku'
        lista_plikow_apteki = [] # lista plików do analizy
        for plik in os.listdir(sciezka_katalogu):
            if fnmatch.fnmatch(plik, szukany_plik):
                pelna_sciezka_pliku = os.path.join(sciezka_katalogu, plik)
                if os.path.isfile(pelna_sciezka_pliku):
                    data_modyfikacji = datetime.date.fromtimestamp(os.path.getmtime(pelna_sciezka_pliku))
                    rozmiar_pliku = os.path.getsize(pelna_sciezka_pliku)
                    wiek = (dzisiejsza_data - data_modyfikacji).days
                    #print(f'Wynik testu {wiek} {nazwa_apteki} {plik} {rozmiar_pliku}')
                    wynik = nazwa_apteki, wiek, plik, rozmiar_pliku
                    #print(wynik)
                    lista_plikow_apteki.append(wynik) #, szukany_plik, wiek_pliku max_wielposc_pliku)
        posortowana_lista = sorted(lista_plikow_apteki, key=lambda x: x[1])
        #print(posortowana_lista)

        najmlodszy = (posortowana_lista[0]) # pierwszy element listy posortowanej
        wielkosc_najlodszego = najmlodszy[3]
        najmlodszy_1 = (posortowana_lista[1]) # kolejny z najmlodszych element listy posortowanej
        wielkosc_najmlodszego_1 = najmlodszy_1[3]
        wiek_najmlodszego = najmlodszy[1]
        procent_wielkosci_pliku = round(((wielkosc_najlodszego - wielkosc_najmlodszego_1) / wielkosc_najmlodszego_1) * 100, 2)

        if wiek_najmlodszego >0:
            wynikbrak = (f'Brak kopii {najmlodszy[0]} plik: {najmlodszy[2]} ma {wiek_najmlodszego} dni ')
            return wynikbrak
        if procent_wielkosci_pliku >= 7 or procent_wielkosci_pliku <= -7 :
            wynikbrak = (
                f'Brak Blad wieklosci pliku {najmlodszy[0]}'
                f' plik: {najmlodszy[2]} ma {wielkosc_najlodszego}'
                f' poprzedni mial {wielkosc_najmlodszego_1} {procent_wielkosci_pliku}')
            return wynikbrak
        if procent_wielkosci_pliku < 10 and wiek_najmlodszego == 0 and wielkosc_najlodszego < int(max_wielposc_pliku):
            wynikjest = (f'OK {najmlodszy[0]}, plik: {najmlodszy[2]}, wielkosc: {round(najmlodszy[3]/ 1024**3, 2)} GB, procent: {procent_wielkosci_pliku}% ')
            return wynikjest

    def wczytaj_liste_apteki(self):
        lista_aptek = []
        for apteka in self.apteki:
            pojedyncza_apteka = (
                apteka.id_kamsoft, apteka.nazwa, apteka.sciezka_1dzienna, apteka.plik_1dzienna, apteka.sciezka_2dzienna,
                apteka.plik_2dzienna, apteka.sciezka_1godzinowa, apteka.plik_1godzinowa, apteka.sciezka_2godzinowa, apteka.plik_2godzinowa, apteka.max_wielkosc_1)
            lista_aptek.append(pojedyncza_apteka)
        return lista_aptek
    def test_kopii_dziennej(self, jaki):
        lista_aptek = katalog.wczytaj_liste_apteki()  # Tworzy listę aptek - lista_aptek
        for apteki in lista_aptek:
            #print(apteki)
            if apteki[2] != '':  # jeżeli jest wpisana ścieżka w trzecim polu to sprawdzaj plik
                wynik1 = katalog.sprawdz_plik(
                    sciezka_katalogu=apteki[2], szukany_plik=apteki[3],
                    nazwa_apteki=apteki[1],max_wielkosc_1=apteki[10])

            if wynik1.startswith(jaki):
                print(wynik1)
                pass

    def start(self):
        katalog.wczytaj_apteki_z_pliku()
        #lista_aptek = katalog.wczytaj_liste_apteki()  # Tworzy listę aptek - lista_aptek
        while True:
            print('1 - Pokaż apteki bez kopii dziennej')
            print('2 - Pokaż apteki z poprawną kopią')
            wybor = input(f'Podaj opcje: ')
            if wybor == "0":
                break
            elif wybor == "1":
                jaki = "Brak"
                katalog.test_kopii_dziennej(jaki)
            elif wybor == '2':
                jaki = "OK"
                katalog.test_kopii_dziennej(jaki)

# Program do weryfikacji wysyłania kopii bazy
if __name__ == "__main__":
    katalog = KatalogAptek()
    katalog.start()

