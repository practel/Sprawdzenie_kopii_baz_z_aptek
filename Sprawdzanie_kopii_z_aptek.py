import os
import time
import datetime
import smtplib
import fnmatch
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
        procent_wielkosci_pliku = 0
        max_wielposc_pliku = max_wielkosc_1
        rodzaj_bledu ='Brak pliku'
        for plik in os.listdir(sciezka_katalogu):
            if fnmatch.fnmatch(plik, szukany_plik):
                pelna_sciezka_pliku = os.path.join(sciezka_katalogu, plik)
                if os.path.isfile(pelna_sciezka_pliku):
                    data_modyfikacji = datetime.date.fromtimestamp(os.path.getmtime(pelna_sciezka_pliku))
                    rozmiar_pliku = os.path.getsize(pelna_sciezka_pliku)
                    wiek = (dzisiejsza_data - data_modyfikacji).days
                    if wiek == wiek_pliku + 1 and rozmiar_pliku > 500 and plik == szukany_plik: # pobieram wielkość pliku starszego o 1 dzień
                        rozmiar1 = rozmiar_pliku
                    if wiek == wiek_pliku and rozmiar_pliku > 500: # Jeżeli są pliki dzisiejsze > 500
                        procent_wielkosci_pliku = round(((rozmiar_pliku - rozmiar1) / rozmiar1) * 100, 2)
                        if rozmiar1 == 0.01:
                            procent_wielkosci_pliku = 0.01
                        if int(rozmiar_pliku) < int(max_wielposc_pliku):
                            if -2.9 <= procent_wielkosci_pliku <= 2.9:
                                wynikjest.append(
                                    f"OK: {nazwa_apteki} {data_modyfikacji} Rozmiar: {round(rozmiar_pliku/ 1024**3, 2)} GB   proc {procent_wielkosci_pliku}")
                            else:
                                rodzaj_bledu = 'błąd wielkości '
                        else:
                            rodzaj_bledu = 'Plik za duży '
                    else:
                        wynikbrak.append(f"{nazwa_apteki} Rozmiar: {rozmiar_pliku} Jest {data_modyfikacji} ")
        if wynikjest:  # Jeśli wynik zawiera elementy, to zwracamy listę z wynikami
            return wynikjest
        else:
            return [f'Blad: {rodzaj_bledu} {wynikbrak[0]}  {szukany_plik}']

    def wczytaj_liste_apteki(self):
        lista_aptek = []
        for apteka in self.apteki:
            pojedyncza_apteka = (
                apteka.id_kamsoft, apteka.nazwa, apteka.sciezka_1dzienna, apteka.plik_1dzienna, apteka.sciezka_2dzienna,
                apteka.plik_2dzienna, apteka.sciezka_1godzinowa, apteka.plik_1godzinowa, apteka.sciezka_2godzinowa, apteka.plik_2godzinowa, apteka.max_wielkosc_1)
            lista_aptek.append(pojedyncza_apteka)
        return lista_aptek

    def sprawdz_pliki(self):
        katalog.wczytaj_apteki_z_pliku()
        lista_aptek = katalog.wczytaj_liste_apteki()  # Tworzy listę aptek - lista_aptek
        for apteki in lista_aptek:
            if apteki[2] != '':  # jeżeli jest wpisana ścieżka w trzecim polu to sprawdzaj plik
                wynik1 = katalog.sprawdz_plik(sciezka_katalogu=apteki[2], szukany_plik=apteki[3], nazwa_apteki=apteki[1],
                                              max_wielkosc_1=apteki[10])
                # print(wynik1)
            if apteki[4] != '':  # jeżeli jest wpisana ścieżka w piątym polu to sprawdzaj plik
                wynik2 = katalog.sprawdz_plik(sciezka_katalogu=apteki[4], szukany_plik=apteki[5], nazwa_apteki=apteki[1],
                                              max_wielkosc_1=apteki[10])
                # print(wynik2)
            if apteki[6] != '':  # jeżeli jest wpisana ścieżka w piątym polu to sprawdzaj plik
                wynik3 = katalog.sprawdz_plik(sciezka_katalogu=apteki[6], szukany_plik=apteki[7], nazwa_apteki=apteki[1],
                                              max_wielkosc_1=apteki[10])
            if apteki[8] != '':  # jeżeli jest wpisana ścieżka w piątym polu to sprawdzaj plik
                wynik4 = katalog.sprawdz_plik(sciezka_katalogu=apteki[8], szukany_plik=apteki[9], nazwa_apteki=apteki[1],
                                              max_wielkosc_1=apteki[10])

            for element in wynik1:
                if element.startswith("Blad"):
                    print(element)
                    pass
                elif element.startswith('OK'):
                    print(element)
                    pass
            for element in wynik2:
                if element.startswith("Blad"):
                    # print(element)
                    pass
                elif element.startswith('OK'):
                    # print(element)
                    pass
            # for element in wynik3:
            #    if element.startswith("Blad"):
            #        #print(element)
            #        pass
            # for element in wynik4:
            #    if element.startswith("Blad"):
            #        #print(element)
            #        pass

# Program do weryfikacji wysyłania kopii bazy
if __name__ == "__main__":
    katalog = KatalogAptek()
    katalog.sprawdz_pliki()

