# Ostoslista-sovellus

## Sovelluksen paikallinen käynnistäminen:

### Kloonaa tämä repository omalle koneellesi ja siirry sen juurikansioon.
```
git clone <repository-url>
cd shopping-list-app
```
### Luo virtuaaliympäristö
- Luo juurikansioon `.env`-tiedoso ja määritä sen sisälö seuraavanlaiseksi:
`DATABASE_URL=<tietokannan-paikallinen-osoite>`
`SECRET_KEY=<salainen-avain>`
- Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
- Määritä tietokannan skeema komennolla
` psql < schema.sql`

- Nyt voit käynnistää sovelluksen komennolla
flask run

