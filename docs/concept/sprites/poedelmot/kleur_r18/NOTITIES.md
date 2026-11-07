# Poedelmot: kleur r18

Vanaf r17 (`stappen/basis.txt`). Stap: `python3 apply.py basis.txt ../raster.txt r18a` (in `stappen/`), daarna `palet.py`, `controle.py` en `vel.py`. Er zijn 56 px gewijzigd, allemaal in x36–53 / y33–51.

## Gedaan (de twee zelfgenoemde zwakke punten uit r17)
1. **Golflijn onder de witte rand van de achtervleugel:**
   - Gemeten op het model: één lijn op y46 met dalen naar y47 op x47 en x49–50. Dat is een periode van ±2,5 px, geen blokjes van 2.
   - Nu: (45–46,46), (47,47), (48,46), (49–50,47), (51–53,46), daarna omhoog naar (53–54,45).
   - De rand boven de lijn (y45, x45–52) staat in 7, zoals de grijswitte rand in het model. Daaronder ligt wit dons.
2. **Tan plaatje:**
   - Bovenlijn op y44 (x40–43), waar de rand van de achtervleugel en de plaatrand samenkomen.
   - Linkerrand diagonaal: (40,45), (39,46–47), (37,48–50).
   - Rechterrand op x44 (y46–48) en x43 (y49–50), zoals het model. In r17 stond die 1 px te ver rechts.
   - De losse lijn (39–41,48), die niet in het model staat, is weg.
   - Lichte stippen in D op (42–43,47–48), zoals het geblokte lichte vlak in het model.
3. **Eindtoets (lijnkaart_r18.png + 1× naast het model):** de wortel van de vleugelnaad (39–41,34) en (40,35) is zwart, zoals in het model. Verder vond ik geen afwijkingen.
   - Wat de lijnkaart nog laat zien: de sprietstrepen (de periode van het model, ±1,5 px, is te fijn voor 64 px), selout 4 op de lichtkant en de klauwteentjes in 4. Dat zijn bewuste Gen 3-keuzes.

## Controle
Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0, 13 kleuren.

## Zwakke punten
Geen nieuwe gezien.
