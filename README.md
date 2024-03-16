# Ostoslista-sovellus
Tekijä: Toma Lahtinen
### Kuvaus
Ostoslista-sovelluksella voi tehdä yksinkertaisia ostoslistoja ja jakaa niitä muiden käyttäjien kanssa. Käyttäjä voi myös tehdä omia reseptejä, joita se voi selata kätevästi ostoslistaa muokatessa.

### Tarkempi kuvaus
- Käyttäjätilin luominen/kirjautuminen/kirjautuminen ulos
- Uuden listan tai reseptin luominen
- Olemassa olevan oman ostoslistan, jaetun ostoslistan tai reseptin muokkaaminen
  - Ostoslistan/jaetun listan ominaisuudet
    - Listan tietojen tarkastelu
    - Tuotteiden lisääminen/postaminen
    - Jakaminen muille käyttäjille (vain listan omistaja)
    - Reseptien selaaminen
    - Listan poistaminen
        - Jos omistaja poistaa listan, se poistuu jokaiselta käyttäjältä
        - Jos jaettu käyttäjä poistaa listan, se poistuu vain häneltä itseltään.
  - Reseptin ominaisuudet:
    - Tuotteiden lisääminen ja poistaminen
    - Reseptin poistaminen 
  

## Sovelluksen paikallinen käynnistäminen:

### Kloonaa tämä repository omalle koneellesi ja siirry sen juurikansioon.
```
git clone https://github.com/latoma/Ostoslista-sovellus.git
cd Ostoslista-sovellus
```
### Luo virtuaaliympäristö
- Luo juurikansioon `.env`-tiedoso ja määritä sen sisälö seuraavanlaiseksi:
```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
- Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
- Määritä tietokannan skeema komennolla
```
psql < schema.sql
```

- Nyt voit käynnistää sovelluksen komennolla
```
flask run
```
## Sovelluksen käyttöesimerkki (vaihe vaiheelta)
- Rekisteröi käyttäjä (muista käyttäjänimi)
- Kirjaudu ulos
- Rekisteröi uusi käyttäjä
- Tee uusi resepti
  - Lisää muutama tuote
  - Palaa etusivulle
- Tee uusi ostoslista
  - Lisää muutama tuote
  - Paina "Jaa lista toiselle käyttäjä"
    - Syötä ensimmäisen käyttäjän nimi ja paina "lisää"
- Kirjaudu ulos
- Kirjaudu sisään ensimmäisellä käyttäjällä
- Jaettujen listojen kohdalla on nyt näkyvissä juuri jaettu lista.
- Paina "Näytä", niin voit katsella listaa ilman toiminnallisuuksia
  - (Voit halutessasi muokata sitä ja vaihtaa takaisin toiselle käyttäjälle niin näet muutokset)

## Käytetyt teknologiat
- Python
- Flask
- PostgreSQL
- HTML/CSS/JavaScript
