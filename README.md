# matkakohteet

Sovellus johon käyttäjä voi lisätä arvosteluja matkakohteista, ja kommentoida toisten lisäämiä kohteita.

## Käynnistysohjeet

Luo tietokanta komennolla:

```
sqlite3 database.db < schema.sql
```

Käynnistä sovellus komennolla:

```
flask --app src/app.py run
```

## Sovelluksen toiminta suurella tietomäärällä

Kun tietokanta on luotu, sen voi alustaa suurella tietomäärällä komennolla:

```
python seed.py
```

Tämä lisää sovellukseen 1000 käyttäjää, satatuhatta matkakohdetta ja miljoona kommenttia.

Tietokanta käyttää indeksejä ja sovellus sivutusta, jonka seurauksena sovellus toimii tehokkaasti suurtakin tietomäärä käyttäen. Jos indeksejä ei ole käytössä niin sovelluksen etusivun lataamiseen menee noin 2.5-3.5 sekunttia, mutta kun ne otetaan käyttöön aika tippuu noin 0.01-0.05 sekunttiin.

## Sovelluksen toiminnallisuus

- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan matkakohteita.
- [x] Käyttäjä näkee sovellukseen lisätyt matkakohteet.
- [x] Käyttäjä pystyy etsimään matkakohteita hakusanalla.
- [x] Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät matkakohteet.
- [x] Käyttäjä pystyy valitsemaan matkakohteelle yhden tai useamman luokittelun (esim. hintaluokka ja arvostelu).
- [x] Käyttäjä pystyy kommentoimaan matkakohteita.
