# matkakohteet

## Käynnistysohjeet

Luo tietokanta komennolla:

```
sqlite3 database.db < schema.sql
```

Käynnistä sovellus komennolla:

```
flask --app src/app.py run
```

## Sovelluksen toiminnallisuus

- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan matkakohteita.
- [ ] Käyttäjä pystyy lisäämään kuvia matkakohteesta.
- [x] Käyttäjä näkee sovellukseen lisätyt matkakohteet.
- [x] Käyttäjä pystyy etsimään matkakohteita hakusanalla.
- [x] Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät matkakohteet.
- [ ] Käyttäjä pystyy valitsemaan matkakohteelle yhden tai useamman luokittelun (esim. hintaluokka, sijainti, turvallisuus).
- [ ] Käyttäjä pystyy kommentoimaan matkakohteita.
