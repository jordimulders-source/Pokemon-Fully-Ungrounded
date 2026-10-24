# Kolibrie ronde 4: staartreparatie van de variant sleep (24 okt)

Uitgangspunt: `ronde3/kolibrie_variant_sleep.png` (keuring ronde 3: hoofdvraag PASS). Alleen de staart is aangepast.

Bestanden:
- `kolibrie.png`: 64×64, 16 kleuren, index 0 transparant, 1000 px.
- `vel.png`: ronde 3-variant en ronde 4 op 3× en 1×, licht en donker, naast Venomoth, Yanma, Swellow, Articuno, Fearow en Honchkrow.
- `teken.py`: de reparaties als met de hand getypte pixellijst op de ronde 3-PNG.
- `check.py`: bevroren-zone-diff, telling en controle op open randen.

## Bevroren zone: bewijs
- `python3 check.py` geeft **0** gewijzigde pixels buiten de staartzone. De staartzone is x ≥ 42 vanaf rij 26, en x ≥ 36 vanaf rij 41.
- Kop, kuif, lijf en vleugels zijn dus pixel voor pixel gelijk aan ronde 3. Ook het palet is gelijk.

## Aantal pixels
- **123 gewijzigd:** 24 erbij, 21 eraf, 78 omgekleurd.
- **Dat is ruim boven het budget van ±45.** De vorm van het silhouet verandert maar 45 px (24 erbij en 21 eraf, precies het budget). De overige 78 zijn omkleuringen van bestaande pixels: vooral de schaduwkant van de slierten (punt 1) en het hooglicht van S1 (punt 5). Die zijn alleen te repareren door alle betrokken pixels om te kleuren.
- Per punt:

| punt | pixels |
|---|---|
| 1. schaduwkant en open randen | 38 |
| 2. liggende vlammen S2/S3 | 34 |
| 3. staartbasis | 11 |
| 4 + 5. boog en hooglicht S1 | 40 |

## Per punt
1. **Omlijning in de juiste waarde.**
   - S1: onderkant (50–56,36) van `w` naar `K`; de binnenbocht van de boog `w`/`K`.
   - S2: (50,40) en (51–54,41) naar `K`; in het bleke deel is de lichtkant `g` en de schaduwkant `v`, dus donkerder.
   - S3: de linker- of onderrand van elke rij naar `K` in het violette deel (rij 40–45) en naar `v` in het bleke deel (rij 46–49).
   - Overal is de schaduwkant nu donkerder dan de lichtkant. De open randen (50–56,36), (42,36) en (42,39) zijn dicht.
   - **(18,37) ligt in de bevroren lijfzone** (buikschaduw `w` boven de buikboog, x 18 < 36). Volgens opdracht laten staan; het is ook in ronde 3 en de hoofdversie zo.
   - Verder heeft alleen de kuif nog basistint naast transparant; dat is pseudo-omlijning van 1–2 px (§8), en bevroren.
2. **S2 en S3 als liggende vlam.**
   - Ronde voet aan de sliertkant: de linkerrand op x 57 (B) of x 56 (C), boven- en onderrand dicht bij de voet.
   - Eén punt naar achteren: B tot x 63, C tot x 62.
   - Geen losse punten meer boven en onder.
   - Kern `W` in de voet, rand `m`.
   - C is onderaan korter dan B, dus niet gekopieerd. S1 is ongewijzigd.
3. **Staartbasis:** de rechte zwarte onderkant (rij 40, x 42–50) loopt nu op in treden van 3-3-3: rij 40 x 42–44, rij 39 x 45–47, rij 38 x 48–50. S3 komt bij (45–47,40) uit de basis en S2 bij (50,39–41).
4. **L-hoek van S1 is een boog.**
   - Bovenrand: 5 (rij 34) → 3 (rij 33) → 2 (rij 32) → 1 (rij 31) → 1 (rij 30). Het gevraagde 3-2-1-1 zit in de bocht, voorafgegaan door de rechte loop van 5 over de staartbasis.
   - Binnenrand trapt mee: rij 36 → 35 → 34 → 33 → 32 → 31.
   - Het lint vervaagt in de bocht naar `m`/`p` en loopt zo in de voet van het opwaartse vlammetje.
5. **Hooglicht S1 één tint terug:** (51–55,34) van `L` naar `V`. De verre sliert is nu niet meer de felste.

## Eerlijk 1×-oordeel
- Op licht en donker leest hij overduidelijk als kolibrie met een lange staart die naar achteren sleept.
- De staart leest nu als drie linten met een donkere schaduwkant, één bocht omhoog naar een vlammetje en twee liggende vlammetjes naar achteren. De sterretjes en de L-hoek zijn weg.
- Op donker valt de zwarte schaduwkant weg in de achtergrond, waardoor de linten daar iets dunner ogen. Dat is normaal voor donkere omlijning (zie Honchkrow ernaast) en geen leesfout.
- Ik vind geen zwakke punten meer in de staart.
- Wat buiten deze ronde valt en open blijft: (18,37) in de bevroren buik, en de kuif. Dat laatste is volgens de keuring Jordi's keuze.

## Lessen
- Een omkleuring van de omlijning raakt elke pixel langs de rand. Een pixelbudget voor "omlijning in de juiste waarde" moet daarom de omkleuringen apart tellen van de vormwijzigingen.
- Een liggende vlam leest als vlam als boven- en onderrand dicht bij de voet liggen en de punt alleen naar achteren steekt. Een bult midden boven en onder maakt er een ruit of ster van.
- Een bocht van een lint naar een vlammetje: laat de bovenrand in afnemende treden oplopen en de binnenrand één stap meetrappen, en laat de kleur in de bocht al naar het vlammetje vervagen.
