# Shopping list app

- [Suomekielinen versiol](#ostoslista-sovellus)

Author: Toma Lahtinen

### Description
The shopping list app allows you to make simple shopping lists and share them with other users. Users can also create their own recipes, which they can conveniently browse while editing the shopping list.

### More detailed description
- Create/login/logout user account
- Create a new list or recipe
- Edit an existing personal shopping list, shared shopping list or recipe
  - Shopping list/shared list properties
    - Viewing list information
    - Adding/posting products
    - Sharing with other users (list owner only)
    - Browsing recipes
    - Deleting a list
        - If the list is deleted by the owner, it will be deleted for each user
        - If a shared user deletes a list, it will only be deleted by the shared user.
  - Recipe properties:
    - Adding and deleting products
    - Adding and adding new recipes, adding or deleting a recipe 
  

## Start the application locally (requires PostgreSQL):

### Clone this repository on your machine and navigate to its root folder.
```
git clone https://github.com/latoma/Ostoslista-sovellus.git
cd Shopping list application
```
### Create a virtual environment
- Create a `.env` file in the root folder and configure its contents as follows:
```
DATABASE_URL=<<database-local-address>
SECRET_KEY=<secret-key>
```
- Activate the virtual environment and install the application dependencies using the commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
- Specify the database schema with the command
```
psql < schema.sql
```

- Now you can start the application with the command
```
flask run
```
## Application example (step by step)
- Register a user (remember the username)
- Log out
- Register a new user
- Create a new recipe
  - Add a few more products
  - Return to home page
- Create a new shopping list
  - Add a few products
  - Press "Share list with another user"
    - Enter the name of the first user and press "add"
- Log out
- Log in with the first user
- Under shared listings, the list you just shared is now displayed.
- Press "Show" to view the list without any functionality
  - (You can edit it if you wish and switch back to another user to see the changes)
 
## About the structure of the application database
- Users are stored in the users table with hashed passwords
- Shopping lists are in the shopping_list table and their items are in the list_items table by list_id reference
- The items are like lists but with less data. They are in the recipe_lists table and their products are in a separate recipe_items table with a recipe_id reference.
- Shared_lists keeps information about shared lists by referencing the list_id of the shopping lists and the username of the users

## Technologies used
- Python
- Flask
- PostgreSQL
- HTML/CSS/JavaScript

Translated with DeepL.com (free version)

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
  

## Sovelluksen paikallinen käynnistäminen (vaatii PostgreSQL):

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
 
## Sovelluksen tietokannan rakenteesta
- Käyttäjät tallennetaan users-taulukkoon hashatuilla salasanoilla
- Ostoslistat ovat shopping_list taulukossa ja niiden tuotteet ovat list_items taulukossa list_id viittauksella
- Rseptit ovat kuten listoja mutta vähemmillä tiedoilla. Ne ovat recipe_lists taulukossa ja niiden tuotteet ovat omassa recipe_items taulukossa recipe_id viittauksella.
- Shared_lists säilyttää tiedon jaetuista listoista viittaamalla  ostoslistojen list_id:iin ja käyttäjien username:ihin

## Käytetyt teknologiat
- Python
- Flask
- PostgreSQL
- HTML/CSS/JavaScript
