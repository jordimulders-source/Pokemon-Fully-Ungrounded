# Icoon-gereedschap algemeen (proef 27 nov: Gumfish, Sunperor)

Volgt `docs/lessen/ICOON_WERKWIJZE.md`. Per soort één JSON (`<soort>/<soort>.json`); twee scripts (vereist `scipy`):
- `python3 icoon_bouw.py <soort>.json <map>` → `onderlaag.png`, `onderlaag_8x.png` (front | onderlaag | 3 echte Gen 3-iconen + 1×-strook), `rapport.txt`.
- `python3 icoon_af.py <soort>.json <map>` → past `poets` (per zone) en `frame2` toe → `icon.png` (32×64, P, index 0 transparant), `icon_anim.gif`, `icon_8x_vergelijk.png`.
- `toon.py icon.png [y0 y1]`: raster als tekst met kolomliniaal (coördinaten voor de poets-lijst).

## Wat het script nu zelf doet
- Onderdelen uit polygonen/vakken (+ optioneel alleen bepaalde frontkleuren, zoals de staf); voorste deel wint bij overlap.
- Doelhoogte uit de fronthoogte-tabel; kop ×1,25, lijf ×0,95 rond het halsgewricht; overige delen aan hun aanhechting; minimummaten (oog, oor, voorpoot, staart) vergroten een deel automatisch; hoogte/breedte (≤ 27) worden bijgestuurd.
- Kleur per pixel = de meest voorkomende frontkleur (geen gemiddelde, dus geen blur); wit/glans blijft wit.
- Palet: gemiddelde Delta E (Lab) per palet, in het rapport; bij een gelijkspel (≤ 3%) het palet met meer tinten. Gumfish → pal0, Sunperor → pal5.
- Tinten: dichtstbijzijnde, of `ramp` (vast) / `"auto"` (zelfde kleurtoon; 80% basistint, lichtste 20/5% en donkerste 15/5% een stap lichter/donkerder).
- Omlijning buiten het silhouet (boven 15, onder 14); binnenlijnen waar deel over deel ligt (ook "achter": lijn op het lijf naast een dunne staf); gaten dicht, uitsteeksels van 1 px weg, optioneel hoeken afronden.
- Oog/ogen als patroon op de omgerekende plek; lijnen/stippen uit de front (mond, vinstrepen, gouden stippen) met dezelfde transformatie.
- Frame 2: bovendeel 1 px omlaag, één rij vervalt, vaste vakken voor het gebaar (staartvin; vleugeltip + staf die op de grond blijft staan).

## Wat nog handwerk bleef
- JSON invullen: polygonen, anker, lijnkleuren, eventuele schaal (Sunperor: kroon ×0,85, vleugel ×1,25), ramp, ogen, stippen.
- Poetsen: Gumfish 33 px (dubbele lijn, glans, oog vrijmaken, rugdal + bult, hoeken staartvin/buik); Sunperor 21 px (paarse kroonrand rondom, twee pootstompjes, eivorm lijf, kroontop, snavellijn).
- Frame 2: de vaste vakken kiezen en zelf controleren op open randen (een vak dat een rand doorsnijdt laat een gat).
- Controle: Sunperor 17/17. Gumfish 15/17: binnenlijnen 0,069 en trapjes 41,5. Echte Gen 3-iconen van gladde vissen zitten daar ook (Wailord 0,07, Whiscash 0,067, Luvdisc 0; Wailmer 46,9 trapjes).
- Kleurgrens: geen enkel icoonpalet heeft karmijnrood (Gumfish wordt baksteenrood, zoals Octillery) of donkerbruin (Sunperor-lijf wordt grijs, zoals Honchkrow).

## Verwachting voor een batch
- JSON: ±10–15 min per soort (polygonen aflezen op een 12×-raster). Bouwen: 1 s.
- Poetsen + frame 2 + controle: 2–4 rondes, ±20–30 min per soort. Een eenvoudige vorm (vis, bol) gaat sneller dan een drukke vorm (kroon, staf, vleugel).
- Daarna nog een verse keurder en Jordi (stap 5–6): niet in deze proef gedaan.
