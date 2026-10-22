# Tilesetplan: Andes-tegels in Hoenn/Emerald-stijl

Korte studie van de Hoenn-tilesets (22 okt, na Jordi's feedback op ronde 1: "kaal, niet Pokémon-achtig, EarthBound").
Gemeten op gerenderde kaarten (Lavaridge, Mauville, Fallarbor, Petalburg, Slateport, Route 111/113/114) met
`tools/concept/tiles/tilelib.render_repo_map`.

## Wat Hoenn anders doet dan ronde 1
| | Hoenn | ronde 1 (fout) |
|---|---|---|
| Grond | basis + **15–25% textuur**: korte streepjes en puntjes van 1–2 px, één lichtere en één donkerdere tint (gras: lichte 2x2-vlekjes en donkere puntjes; Fallarbor-pad: lichte streepjes; zand: golvende ditherrijen) | grote egale vlakken met ±5% stipjes |
| Overgangen | **dither (dambord) van 2–3 px** met een tussenkleur, plus een lichte rand op paden en kliffen | omlijnde, gladde randen |
| Omlijning | gebouwen in **navy** (65,74,106)/(41,49,90); natuur in de donkerste tint van zijn eigen kleur | zwart-achtig of geen |
| Tinten | 4 per materiaal (licht/basis/schaduw/donker) + de gedeelde grijs/navy-ramp | 2–3, plat |
| Gebouwen | groot **dak = de helft van het gebouw** (2 rijen), met patroon (ribbels, pannen), lichte nokband en donkere dakrand; muur 1,5–2 rijen met planken/pilaren; ramen met lichtblauw glas, witte glans en kozijn; deur met paneel | dunne daken, kale muren, kleine ramen |
| Schaduw | onder dakranden (donkere band), onder bomen (donkere grondvlek), voet van kliffen; geen slagschaduw van gebouwen op de grond | bijna geen |
| Decor | overal: bloemen, struikjes, bordjes, brievenbussen, hekjes, rotsjes, bomenranden | spaarzaam |
| Kleur | licht en verzadigd, warm; elke palet-index 15 is de grondkleur (randen sluiten zo naadloos aan) | donkerder, droger |
| Kliffen | gelaagde rotswand (rijen "rotsbakstenen" met lichte bovenrand, Route 113/114) of rotsbergen (Route 111) | zelfbedachte brokken |

## Regels
- **Bouw op Hoenn-tegels.** Neem tegels 1-op-1 over op indexniveau en kleur alleen het palet om (`r2lib.import_region`,
  `import_mt`). Pas pixels alleen aan waar het materiaal anders is (baksteen, adobe) en houd dan de indexindeling aan.
- **Teken zelf alleen wat Hoenn niet heeft** (cholet, kabelbaan, pirca, apacheta, bofedal, Illimani), en dan in
  de kleuren van een bestaand Hoenn-palet: navy omlijning, licht linksboven, 4 tinten, glas zoals het Pokémon Center.
- **Index 15 = grond.** In elk eigen palet is index 15 de puna-grond (216,192,112), zoals Hoenn daar het gras heeft.
- **Kleurvarianten via paletten**, niet via nieuwe tegels (huizen in drie kleuren kosten 0 tegels extra).
- **Decor hoort erbij**: elke mock-up heeft bloemen, struikjes, bordjes, lantaarns of hekjes, zoals een Hoenn-kaart.
- Doel is Emerald-niveau, niet meer: weinig varianten, veel hergebruik (Jordi: "het hoeft geen GTA 6 te worden").

## Nooit
- Grote egale vlakken zonder textuur, of textuur met ruis (willekeurige pixels): Hoenn-textuur is regelmatig.
- Zwarte omlijning, of een lijn als overgang tussen twee grondsoorten (gebruik dither).
- Een nieuw palet als een Hoenn-palet het al kan; een eigen palet zonder de grijs/navy-ramp.
- Dingen die niet in de wereld kloppen (immersie): geen dieren in tegels, bloemen die er echt groeien (kantuta).

## Opbouw: Andes-primary + secondaries (door Jordi bevestigd, 22 okt)
- **Andes-primary** (`tilesets/eigen/andes_primary/`, `tools/concept/tiles/andes_primary.py`): een omgebouwde kopie
  van General. Zelfde tegelnummers, metatiles, gedrag en animaties (water, bloemen, watervallen), dus alle
  Hoenn-secondaries passen erop. Paletten 0–5: gras → goudgele puna, hoog gras → ichu (alleen via het palet),
  Hoenn-zand → lichte onverharde weg, mauve rotsbergen → rode klei, bomen olijfgroener. Nieuw in ongebruikte
  General-metatiles: verre bergketen + lucht, lantaarn, bank, kantuta. Budget: 512 tegels (44 vrij), 512 metatiles
  (48 vrij, alleen slots die op geen enkele kaart en niet in `metatile_labels.h` staan).
- **La Paz-secondary** (paletten 6–12): huizen (Mauville), markt en kasseien (Slateport), cholets, kabelbaan,
  Illimani. **Altiplano-secondary** (6–12): Fallarbor-tegels (adobe-huis, queñua, kliffen, akker, droge puna,
  paja brava, richels, pad) + pirca, apacheta, voorraadhuisje, bofedal. Budgetten in de NOTITIES per set.
- Later naar dezelfde opbouw: andere Andes-gebieden (Uyuni, Lípez, Cuzco) als eigen secondary op deze primary.
- Bij inbouw in de game ook het **grasdeeltje** omkleuren (de field effects in `graphics/field_effects/pics/`: o.a.
  `tall_grass`, `jump_tall_grass`, `cut_grass` zijn groen), anders loopt de speler door ichu met groene sprietjes.
