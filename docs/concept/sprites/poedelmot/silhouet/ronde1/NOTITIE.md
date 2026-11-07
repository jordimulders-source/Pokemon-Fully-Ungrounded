# Poedelmot silhouet, ronde 1 (5 nov)

Bron: `referenties/foto_tak_katoen.webp` (pose P1). Script: `silhouet.py` (omtrek punt voor punt in fotocoördinaten,
wasbeer-/kolibriemethode; per onderdeel een eigen laag). Schaal: 18,7 fotopx per spritepx, onderkant op y=62.

## Bestanden
- `silhouet_1x.png`, `silhouet_8x.png`: het silhouet (één kleur).
- `delen_1x.png`, `delen_8x.png`: zelfde silhouet per onderdeel (achtervleugel lichtgrijs, voorvleugel grijs, lijf zwart,
  oren bruin, ogen rood = alleen plek en maat), met een witte "luchtlijn" waar lijf en oren over de vleugels vallen.
- `controle_foto.png`: omtrek van elk onderdeel over de foto (zelfde kader als de sprite).
- `vel.png`: foto, omtrek-over-foto, silhouet en delen naast Venomoth, Butterfree, Dustox (Gen 3) en Frosmoth (Gen 8) op 4× en 1×.

## Uit de foto
- Lijf + kop (wolmassa) en de vier poten: omtrek van de foto, met een plukjesrand (rondjes langs de omtrek) voor de katoenlook.
- Voorrand en hoek van beide voorvleugels (links schuin omhoog, rechts recht omhoog = de V); kop iets naar links.
- Plek en maat van de ogen (links groot, rechts kleiner en deels weggedraaid), snuitje ertussen.

## Met de hand (uit de SPEC)
- **Voorvleugels verbreed** (achterrand naar buiten) en iets korter (links 0,72, rechts 0,80 vanaf de wortel): op de foto
  zie je ze bijna op de kant en lazen ze op 1× als stekels; zo is er ook meer ruimte voor lijf en kop.
- **Achtervleugels toegevoegd** (niet op de foto): rond zoals bij de vilt-mot, links onder de voorvleugel, rechts naast het lijf.
- **Sprieten als oren** naar de zijkant (bolle kambladen, ±17 px lang, ±6 px breed), achter de kop en vóór de vleugels.
- **Pompons**: bovenpoot wollig (foto), dan een dunner "geschoren" enkeltje, dan een ronde pompon met plukken
  (voor 8–9 px, achter 6 px).
- Gaatjes < 4 px (afrondingsruis tussen poten) dichtgezet.

## Eigen zwakke punten (eerlijk)
1. **Kop leest niet als eigen vorm**: kop en lijf zijn één wolkoepel (zoals op de foto), zonder hals of inkeping. Bij een
   Gen 3-sprite hoort een ronde kop als eigen vorm; mogelijk in kleur oplossen (kraag onder de ogen) of de kop iets
   groter/breder dan het lijf maken. Graag een oordeel.
2. **Linkeroor valt op de linkervoorvleugel**: in het pure silhouet verdwijnt het; alleen in kleur/delen leest het. Rechts
   steekt het oor wel uit. De vleugelhoek is de pose (niet gedraaid), dus het oor moest daar overheen.
3. **Rechtervoorvleugel** staat als een spits blad recht boven de kop en kan op 1× als hoed/vlam lezen i.p.v. vleugel.
4. **Het geheel leest als ster/bloem** (vier vleugels rondom), minder als mot dan Venomoth/Butterfree; past misschien bij
   "wow wat een vaag dier", maar dat is een keuze voor Jordi/keurder.
5. **Pompons links** (ver + voor) raken elkaar bijna; de dunne enkeltjes zijn op 1× maar 2 px.
6. Ogen zijn groot (7 en 5 px), maar het rechteroog is door de kopdraai klein; Venomoth-achtig "groot rond" aan beide
   kanten vraagt misschien het rechteroog iets groter.
7. Plukjesrand is op 8× nog trappig (geen vloeiende curve); in de kleurstap glad maken.
