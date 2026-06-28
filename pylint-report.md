# Pylint raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
******\******* Module config
src/config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
******\******* Module destinations
src/destinations.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/destinations.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:70:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:99:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:113:0: C0116: Missing function or method docstring (missing-function-docstring)
src/destinations.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
******\******* Module db
src/db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
src/db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
******\******* Module app
src/app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:64:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:119:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:131:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:131:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
src/app.py:152:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:152:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
src/app.py:172:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:178:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:190:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:207:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:207:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
src/app.py:235:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:239:0: C0116: Missing function or method docstring (missing-function-docstring)
src/app.py:245:0: C0116: Missing function or method docstring (missing-function-docstring)
******\******* Module comments
src/comments.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/comments.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
src/comments.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
src/comments.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
src/comments.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
******\******* Module users
src/users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/users.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:37:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)

---

Your code has been rated at 8.38/10 (previous run: 8.22/10, +0.17)
```

## Docstring ilmoitukset

Pylint antaa paljon ilmoituksia docstringien eli dokumentaation puutteesta:

`src/users.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)`

Sovelluksessa päätettiin kuitenkin että näitä ei käytetä.

## Vaarallinen oletusarvo

Pylint kertoo että jotkin funktiota käyttävät vaarallista oletusarvoa:

`src/db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)`

Parametri ottaa oletusarvokseen tyhjän listan `[]`, tässä ongelma voisi olla jos moni funktion kutsu muuttaisi listaa samaan aikaan. Tämä ei kuitenkaan ole ongelma sovelluksessa koska listaa ei muuteta.

## Puuttuvat palautusarvot

Joissain tapauksissa funktion eri haarat käsittelevät palautuksen eri tavoin:

`src/app.py:207:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)`

Tämä on kuitenkin liittyy tapaukseen jossa funktio käsittelee metodeita GET ja POST. Jos funktio kutsuttaisiin jollain muulla metodilla niin se ei palauttaisi arvoa. Tämä ei kuitenkaan ole mahdollista sillä funktion dekoraattori määrittää että funktiota on mahdollista kutsua vain näillä arvoilla.
