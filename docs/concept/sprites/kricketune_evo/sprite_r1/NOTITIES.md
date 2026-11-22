# Kricketune-evolutie (Bug/Fairy, dirigent): frontsprite ronde 1

Bestanden: `kricketune_evo_r1.png` (hoofdversie, mét kledingaanpassing), `kricketune_evo_r1_zonder_kleding.png` (zelfde zonder stap 11),
`kaal.png` (kale reductie), `bouw.py`, `vel.png` (r1 | zonder kleding | kaal | model op 8×; close-ups 12× kop, vinger, andere hand,
hemd/lijf naast precies dezelfde modelpixels; 1× op wit/licht/donker naast Kricketune).
Alle drie 64×64, mode P, index 0 transparant. Hoofdversie 12 kleuren incl. transparant (zonder kleding 11); index 8 staat ongebruikt in het palet.
Bouwen: `cd kricketune_evo && python3 sprite_r1/bouw.py [kaal|toon]`. Gereedschap in `../gereedschap/` (van Alphyena, aangepast):
`pitch.py`, `natief.py` (→ `natief.png`), `gemeen.py`, `schrap.py`, `vel.py`, `controle.py`, `zones.py`, `kijk.py` (close-up 20× naast
dezelfde natieve modelpixels), `twee.py` (sprite 10× naast model), `vergelijk_methodes.py` (keuze schrapmethode).

## Metingen
- Rasterpitch **10,24** (fase 9,25 / 9,20), natief 99×99, figuur x10–84, y6–90 = **75×85**.
- Naar **56×64** (schaal 0,75, gelijk in x en y): 21 rijen en 19 kolommen geschrapt, één per gelijk stuk, de rij/kolom die het meest
  op zijn buur lijkt; oog-/hemdklassen en de gezichtszone wegen 10×, oogrijen (natief 18–22) nooit geschrapt.
  Rijen: 1 5 9 14 17 23 27 29 33 39 43 45 50 54 58 63 67 70 74 78 83 · kolommen: 2 4 8 13 16 20 24 28 34 36 41 44 50 54 57 60 66 68 73.
- **Samenvoegen i.p.v. weglaten** (`schrap_merge`): de geschrapte rij valt samen met de meest gelijkende buur; achtergrond verliest van
  figuur, oog/hemd winnen, verder wint de buur. Puur weglaten brak de 1-px antennes en randen op diagonalen; alles blijft een modelpixel.
- Plek: x4–59, y0–63 (vingertop boven, voeten onderaan). Niet gespiegeld. 1555 px.

## Wat niet uit het model komt (232 px t.o.v. kaal; zonder kleding 187)
Per zone (zonder kleding): vinger 25, hand 9, kop/snor 36, antennes 28, ogen 23, hemd 5, jasje/rokpanden/lijf 45, andere hand 1, benen 15.
1. **Buitenlijn 65:** randpixels → zwart; rood aan de lichtkant → donkerrood (model doet dat ook links langs kop/antennes). Dunne rode
   antennestreng (1 px rood tussen achtergrond en lijn): rood blijft, selout komt er 1 px buiten (de reductie maakte K|rood|K van 3 naar 2 px).
2. **Ogen 19** (toegestane afwijking 2): Kricketune-ogen pixel voor pixel uit `anim_front.png` frame 1: dichtbij kt x31–34,y17–22 → +1,−5
   (sprite x33–35, y12–17; glans en pupil vallen op die van het model), veraf kt x24–27,y20–23 → +1,−6 (x25–28, y14–17). Kt-donker (49,41,57)
   = pakdonker (52,48,62); grijsbruin (82,74,65) eigen index 12. Overgebleven modeloogpixels → kopkleur.
3. **Vinger 22** (toegestane afwijking 1): rechte lijn op de modellijn, per rij zwart | handtint midden | zwart, van x5 (y1) naar x13 (y13),
   tip zwart (4–5,0); helling 2:3 zoals het model. De reductie gaf knikken en onderbrekingen. Tweede vinger en hand = reductie.
4. **Rood naar 3 tinten + lijn 40:** modeltint r2 (140,40,40) samen met de lijntint donkerrood (106,31,31); r3/r4/r5 = schaduw/midden/licht.
5. **Snorkrul 2:** kolom 20 (opening hand|krul) viel weg; rij 18 x19 opening, x20–22 K m K (modelrij 23+24).
6. **Einde rechter antenne 4:** rood (56–57,17) uit modelrij 23 + selout erboven (+2 px silhouet).
7. **Ontkorrelen rood 25:** tintvlekjes <3 px schaduw/midden en losse 1-px hooglichtjes → buurtint (2-px glans blijft).
8. **Losse lijnpixels 3, geen selout om en om 7.**
9. **Rokpanden en been 18:** linker voering x22 y41–46 terug met zwarte rand x21 (y41–43 +3 px silhouet); rechter voering (53,53–54);
   linkerbeen y50–53 had alleen omlijning (vulkolom geschrapt) → K | pak | K zoals y54–57 (+3 px).
10. **Kleding 45** (toegestane afwijking 3, alleen in de hoofdversie): alleen kleur. Jasje over borst, schouders en mouwen krijgt volume
    van linksboven per jasdeel (pak donker → midden, midden → nieuwe lichttint (104,98,118), 7 px), zodat het jasje om het lijf zit;
    rokpanden (vanaf y44) blijven vlak (los hangende stof). Silhouet, zones en onderdelen gelijk.
Silhouet-diff t.o.v. kaal: 25 px (vinger 11, antenne 2–4, voering 3, been 3, rest selout buiten dunne streng).

## Bewust niet gedaan
- Zwarte binnenlijnen in het rood blijven zwart (model; Kricketune heeft ook zwarte lijnen). Proef met donkerrood (`bouw.py donkerrood`)
  maakte de lijfsegmenten modderig.

## Zwakke punten (eerlijk)
- **Zwart 34,5 %** van de figuur (Gen 3 ±12–19 %); het model zelf is 31 % zwart (pak, omlijning, segmentlijnen). Alleen op te lossen door
  van de modellijnen af te wijken.
- **Antennes rechts** (x42–59, y7–19): drie strengen op 0,75× liggen dicht op elkaar; leest als strengen, maar drukker dan het model.
- **Kledingstap** is subtiel (45 px); op 1× klein verschil. Sterker kan, maar dan wordt het meer dan "kleine ingrepen".
- **Ver oog** zit tegen de kopomlijning (zoals bij Kricketune) en leest als donkere verticale vlek; Jordi wil de ogen nog finetunen.
- Kop/gezicht is ±1 px breder dan exact proportioneel (oogkolommen weinig geschrapt).
- Lijf/buik: segmentlijnen zijn modellijnen maar op 64 px wat hoekig.
