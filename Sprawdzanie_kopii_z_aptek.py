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

    def wyslij_email(self, tworz_komunikat, lp):
        komunikat = ""

        with open("wynik_do_wyslania.txt", "w") as plik:
            # Iterujemy przez elementy zbioru i zapisujemy je do pliku
            for element in tworz_komunikat:
                plik.write(
                    element + "\n"
                )  # Dodajemy znak nowej linii po każdym elemencie
            lp = str(lp)
            plik.write(lp + "\n")
        # Otwarcie pliku "wynik_do_wyslania.txt" i odczytanie jego zawartości
        with open("wynik_do_wyslania.txt", "r") as plik:
            komunikat = plik.read()

        # Dane konta e-mail nadawcy
        nadawca_email = "raporty_klient@poczta.pl"
        nadawca_haslo = "Practel123"

        # Dane konta e-mail odbiorcy
        odbiorca_email = "practel@gmail.com"

        # Tworzenie wiadomości e-mail
        wiadomosc = MIMEMultipart()
        wiadomosc["From"] = nadawca_email
        wiadomosc["To"] = odbiorca_email
        wiadomosc["Subject"] = "Raport poprawmosci kopii baz z aptek"

        tresc = komunikat
        wiadomosc.attach(MIMEText(tresc, "plain"))

        # Nawiązanie połączenia z serwerem SMTP
        serwer_smtp = smtplib.SMTP("smtp.poczta.pl", 587)
        serwer_smtp.starttls()
        serwer_smtp.login(nadawca_email, nadawca_haslo)

        # Wysłanie wiadomości e-mail
        serwer_smtp.sendmail(nadawca_email, odbiorca_email, wiadomosc.as_string())
        logowanie_zdarzen(zdarzenie=" - wyslano e-maila")
        # Zamknięcie połączenia
        serwer_smtp.quit()

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
        tworz_komunikat = set()
        lp = 0
        lista_aptek = self.wczytaj_liste_apteki()  # Tworzy listę aptek - lista_aptek
        for apteki in lista_aptek:
            #print(apteki)
            if apteki[2] != '':  # jeżeli jest wpisana ścieżka w trzecim polu to sprawdzaj plik
                wynik1 = self.sprawdz_plik(
                    sciezka_katalogu=apteki[2], szukany_plik=apteki[3],
                    nazwa_apteki=apteki[1],max_wielkosc_1=apteki[10])

            if wynik1.startswith(jaki):
                print(wynik1)
                lp = lp + 1
                tworz_komunikat.add(wynik1)
        #print(tworz_komunikat)
        self.wyslij_email(tworz_komunikat, lp)

def logowanie_zdarzen(zdarzenie):
    with open("logi.log", "a") as logi:
        teraz = datetime.datetime.now()
        teraz = str(teraz.strftime("%Y-%m-%d %H:%M:%S"))
        logi.write(teraz + zdarzenie + "\n")
def wczytaj_parametry(nazwa_pliku):
    try:
        with open(nazwa_pliku, "r") as plik:
            for linia in plik:
                czesci = linia.split(",")
                if len(czesci) == 2:
                    godzina_testu, dzien_tygodnia = czesci
        return godzina_testu, dzien_tygodnia
    except FileNotFoundError:
        print(f"Plik {nazwa_pliku} nie istnieje.")

def uruchom(start, dzien_tygodnia):
    logowanie_zdarzen(zdarzenie=" - uruchomienie")
    katalog = KatalogAptek()
    katalog.wczytaj_apteki_z_pliku()
    dzisiejsza_data_i_godzina = datetime.datetime.now()
    godzina = dzisiejsza_data_i_godzina.strftime("%H:%M")
    numer_dnia_tygodnia = dzisiejsza_data_i_godzina.weekday()

    if godzina == start:
        jaki = "Brak"
        logowanie_zdarzen(zdarzenie=" - uruchomienie testu")
        katalog.test_kopii_dziennej(jaki)
    time.sleep(30)


# Program do weryfikacji wysyłania kopii bazy
if __name__ == "__main__":
    parametry_pobrane = wczytaj_parametry("dane.ini")
    uruchom(parametry_pobrane[0], parametry_pobrane[1])


