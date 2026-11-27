# Uku Pacha r4: notitie van de maker

**Bestand:** `uku_pacha_r4.png` (64×64, geïndexeerd, index 0 = transparant, **16 kleuren incl. transparant**, palet = r2/r3). Vel: `vel.png` (r4 | r3 | model op 8×; 12× naast het model: linkerkop, rechterkop, borst/buik van beide nekken, kronkels links en rechts; r4 op 1×/2× op licht en donker).
**Silhouet:** alpha-diff met r1–r3 = **0**. **Lijnen: alle r3-lijnen blijven** (enige r3-lijnpixels die nu geen lijn zijn: (39,5) en (11,16), beide werden oog/pupil, zie 1). Lijnpixels K+n: r3 585 → r4 643; plus nieuwe dunne borstlijnen in d/l. Pixeldiff r3 → r4: 197.

Opdracht (Jordi via coördinator, letterlijk): "beide ogen hebben geen pupillen", "de borst mist lijnen, maar die kan je prima namaken van het model", "hier en daar nog wat blurry, maar dat is kleur, schaduw en lijnen". Alle lijnen blijven, niets weghalen.

## Scripts (volgorde, reproduceerbaar)
`koppen.py` (op `raster_auto.txt`) → `kronkel_lijnen.py` → `banden.py 2.0` → `borst.py` (nieuw) → `afwerk.py` → `check.py`, `lijnfreq.py`, `vel.py`.

## 1. Pupillen (gemeten op het natieve model)
- **Linkeroog** (modelcellen x 17–22, y 26–29): wit (20,27–29) met links ervan een zwarte spleet (19,26–29, sluit aan op de wenkbrauw) en een klein licht vlekje (18,29). Bij 0,70 vallen spleet en wit op dezelfde spritekolom, dus 1 px verbreed: licht (9,17) | **pupil/spleet K (10,16), (10,17)**, aansluitend op de wenkbrauw (10–11,15) zoals in het model | wit (11,16), (11,17) | zwart (12,16).
- **Rechteroog** (modelcellen x 60–65, y 10–13): geel (61,12), (63–64,11–12), (62–63,13), zwarte spleet (62,11–12), donkere hoek (64,13). Sprite: geel (39,5) | **pupil K (40,5)** | geel (41,5); geel (39,6), (40,6); donkere hoek n (41,6); zwarte rand (38,5), (42,5); wenkbrauw (40–41,4).

## 2. Borst/buik van beide nekken (`borst.py`)
- Zone: pixels rij 16–60 buiten koppen/geest/vleugels/buitenrand waar het model overwegend lichte vlakklassen heeft (12–15): 496 px.
- Lijnen uit het model, drie soorten, elk geprojecteerd en doorlopend 1 px getekend, met alle bestaande lijnen vast (alleen nieuwe dubbele dikte gedund):
  - donkere modellijnen (klasse 1–4) → **n**;
  - dunne grijsblauwe dwarslijnen in het witte vlak (klasse 5–11 met ≥ 4 lichte buren), die het model met sprongetjes van 2 cellen tekent → per lijnstuk langs de hoofdas als polylijn verbonden;
  - plaatgrenzen: een cel ≥ 20 donkerder dan twee tegenoverliggende lichte buren (L ≥ 190).
  - Kleur naar de gemeten modelhelderheid van de lijncellen: < 95 → n, 95–150 → d, > 150 → l.
- Vlakken in de zone: meerderheid van de lichte modelklassen (b/l/p/w), harde toongrenzen op de modelplek in plaats van gemiddelde middentonen.
- Resultaat: 89 lijnpixels in de zone (70 nieuw t.o.v. r3).

## 3. Blur
- Borst: vlakken per pixel naar de modelklasse (geen gemiddelden meer).
- Hele sprite (buiten koppen/geest): tintclusters van 1–2 px (losse middentonen) naar de vlaktoon eromheen (`afwerk.py`). Geen lijn aangeraakt, niets egaler dan het model: alleen losse middentonen weg.

## Zelfgenoemde zwakke punten
1. **Borst: de lijnen staan er nu op de modelplekken, maar de plaatverdeling leest nog minder regelmatig dan in het model op 8×.** Gemeten op het natieve model: veel plaatgrenzen in het witte vlak zijn maar 1 cel dik en bestaan uit lichte cellen (klasse 13–14, lum 150–190), ±1 tint donkerder dan wit. Die heb ik als l/d gezet. Wil Jordi ze steviger (n), dan is dat één regel in `borst.py` (kleurdrempel).
2. **Linkeroog is 1 px verbreed** (de pupil past anders niet: spleet en wit vallen bij 0,70 op dezelfde kolom).
3. **Nieuwe 2×2-lijnklonten** waar een nieuwe borstlijn tegen een bestaande lijn komt: (18–19,43), (26,42), (7,58). Ik heb ze laten staan omdat Jordi "alle lijnen blijven" zei en dunnen een lijn zou inkorten.
4. Restpunten uit r3: (15,53)/(16,54) 1-px pocket tussen twee lijnen; vleugelklauw (41–42,39–40); (5,22) donker mondbinnenwerk.
5. De spiraal van de rechterkronkel is ongewijzigd t.o.v. r3 (Jordi vond r3 "vrij goed"); niet aangeraakt.
