# Olinguito fase 1: herbouw op Zigzagoon

Basis: `graphics/pokemon/zigzagoon/anim_front.png`, in zijn geheel als onderlaag gebruikt (kopconstructie, romp, vier poten, pose, 3/4-hoek). Ik heb er met de hand overheen getekend als tekst-raster (`bron/bouw.py`, per onderdeel rijen `(y, x, tekens)` op de coördinaten van de basis). Palet: `ronde23/normal.pal`, byte voor byte gelijk.

Bestanden: `anim_front.png` (64×128, 2 frames, transparency 0), `normal.pal`, `onderlaag.png` (basis | overtekening over halfdoorzichtige basis | resultaat, 8×), `compare.png` (herbouw | Zigzagoon | ronde 23 | Galar-Linoone, 3× en 1×, licht en donker), `zelfcheck.png` (kop, elke poot en de staart op 12×), `bron/` (bouw, check, preview, crop, vergelijk, zelfcheck; `check_uitvoer.txt`).

## Wat er van de basis bleef en wat er anders is
| Onderdeel | Basis (Zigzagoon) | Herbouw |
|---|---|---|
| Kop | lange snuit naar links, één oog, neus x8–10 y34–38, masker rond het oog | dezelfde plek en hoek. Neus x6–9 y32–34. **Masker** loopt over de neusbrug door tot boven de neus en heeft een golvende onder- en bovenrand. **Licht boogje** (7) direct op de maskerrand boven het oog (x15–19 y27–28). Crème snuit en kaak, **scheve grijns** (mondlijn y37, mondhoek omhoog op x12 y36), geen tong. **Oog** amandelvormig in de stijl van ronde 16 (bovenlid 1, iris E boven en D onder, glans C). **Kleine ronde oren** met crème binnenkant: het nabije oor rechts is groter en heeft licht crème, het verre oor links is kleiner en donkerder. Het achterhoofd bolt 1 px uit (x29, y29–33). |
| Romp | stekelvacht, rug x20–48 | glad olinguitolijf. Rug als boog op de basislijn van de stekels (top y24, x35–37), bil x48. Dij als bolling met hooglicht (x38–41 y36–38). |
| Nabije voorpoot | x19–27, voet laagst (y51) | x20–28, voet y48–49, licht aan de voorkant (5), schaduw achter. Voet licht gekanteld (hiel omhoog). |
| Verre voorpoot | x13–18, onder de kin naar voren, voet hoger | x13–21, schaduwtint, onder de kin naar voren (zoals Galar-Linoone), voet y46–47 (2 px hoger dan de nabije). |
| Nabije achterpoot | x35–42 onder de heup | x33–40, uit de dij, hak naar achteren (x40 y44), twee tenen (y48). |
| Verre achterpoot | (bij Zigzagoon nauwelijks zichtbaar) | stompje x41–45, donker, voet y46 (hoger dan de nabije y48), deels achter de nabije (zoals Linoone). |
| Klauwen | geen | 2 per voorpoot in **Sandslash-stijl**: wit blad (B/C) met grijze bovenrand (9) en donkere onderrand (1), punt buigt omlaag. Elke klauw is 4 px lang. Bij de verre poot zijn ze grijzer (A/B). |
| Staart | pluim omhoog aan de bovenkant van de bil | **hangende J** vanaf dezelfde aansluiting (bovenkant van de bil, x44–48 y25–30). Hij gaat in een boog naar achteren, hangt omlaag (x51–57), krult onderaan terug omhoog en eindigt in een **ronde lichte punt** (6/5, x48–49 y41–43). Hij raakt de grond niet, zodat de steel niet als poot leest (de les uit ronde 23). Lucht tussen bil en steel (x49–51 y36–40) en in de haak (x51–52). |

Frame 2: de kop zakt 1 px (ademhaling). De staartvoet blijft aan de bil en het hangende deel zwaait 1 px na (rij 35 rekt). Romp en poten staan stil.

## Bewijs (`bron/check.py`, `check_uitvoer.txt`)
- Palet gelijk aan ronde 23; transparency 0; mode P, 64×128.
- Open randen: 0 in beide frames.
- Rechte omtrekruns ≥ 4 px (horizontaal of verticaal, met lucht aan dezelfde kant): 0 in beide frames.
- Ingesloten gaatjes: 0. Het gaatje x20 y45 tussen de voorpoten is gedicht met omlijning.
- Formaat: **1057 / 1051 px**, box 52×31 (Zigzagoon 1127 px, 50×35; ronde 23 1045). Dat is 7 px boven 1050; ik heb het niet ingekort ten koste van de vorm.
- Vormmeting (`vormstudie/tools`): symmetrie 0,676 (< 0,80 ok), soliditeit 0,815 (Zigzagoon 0,833; norm 0,65–0,80, 0,015 erboven door de lage, gesloten Zigzagoon-romp), donker aandeel 0,47 (Dark mag; ronde 23 0,52).

## Zelfcheck per onderdeel (`zelfcheck.png`, 8–12×)
| Onderdeel | Vast aan lijf? | Rechte lijn? | Dikte vs tegenhanger | Opmerking |
|---|---|---|---|---|
| Kop | overlapt de borst, omlijnd tegen de romp | nee (achterhoofd bolt uit, kin in treden 2-3-3) | n.v.t. | natuurlijk 3/4 zoals de basis: één oog, snuit wijst links-voor, neus is het meest linkse punt |
| Nabije voorpoot | ja, de bovenkant loopt onder de kaak door in de borst | nee (voorrand x23,22,22,21,21,21,20,20,20; max. run 3) | 6–7 px (nabije achterpoot 6–7) | ok |
| Verre voorpoot | ja, de bovenkant zit onder de kin in de borst | nee | 5–6 px, donkerder (verre kant) | ok, voet 2 px hoger dan de nabije |
| Nabije achterpoot | ja, groeit uit de dij (vouwlijn x36–38) | nee (voet als twee tenen) | 6–7 px (nabije voorpoot 6–7) | hak naar achteren |
| Verre achterpoot | ja, onder de bil | nee | 4–5 px, donker | klein, zoals bij Linoone; deels achter de nabije |
| Telgang? | — | — | — | **diagonaal**: verre voor + nabije achter staan vóór, nabije voor + verre achter staan achter |

## Checklist
**SPRITING §0:** (1) lijf en blik 3/4 naar links-voor, zoals de basis: ok. (2) 4 poten, 2 oren, 1 oog (het verre oog zit achter de neusbrug), neus, mond, staart: alles verbonden, ok. (3) geen rechte lijnen ≥ 4 in de omtrek (gemeten), ok. (4) oog geïntegreerd in het masker, bovenlid, tweekleurige iris, glans: ok. (5) silhouet op 1× leest als een kleine gemaskerde roofdier-viervoeter: ok (zie hieronder). (6) formaat 1057, binnen het doel van ±900–1050 (7 px erboven). (7) pose: lopend, voeten op 3–4 hoogtes, ok.

**FAKEMON_CHECKLIST:** A1 ok · A2 ok: masker + J-staart, de staart breekt de omtrek rechts · A3 ok: kop linksboven, staart als tegenwicht rechts · A4 bijna: soliditeit 0,815 (basis 0,833) · A5 ok 0,676 · A6 ok · B1 ok: kop iets meer naar de kijker dan het lijf (zoals de basis) · B2 ok: lange snuit, één oog · B3 n.v.t. · B4 ok · B5 ok: de oren verschillen in grootte en kleur · B6 ok · B7 ok · C1 ok · C2 ok: 4 kolommen, voeten op y49/47/48/46 · C3 ok · C4 ok: hak achter, voorpoot met knik naar voren bij de pols · C5 ok · C6 ok · C7 ok · C8 ok: de staart sluit aan de bovenkant van de heup aan en buigt (J) · C9 ok: laag sluipend (Dark) · D1 iets boven de band 700–950, binnen de opdracht (±900–1050) · **D2 afwijking:** de kop is ±70% van de hoogte; dat komt van de lage Zigzagoon-bouw (Zigzagoon zelf ook ±70%) · D3 ok: compacte romp, korte poten · D4 afwijking: 52 breed (Zigzagoon 50–56, "laag dier") · E1 ok · E2 ok · E3 Dark: 0,47.

**AFGEKEURD.md:** geen beige vlak uit het niets (het crème zit alleen in snuit en kaak, oorbinnenkant en boogje), masker rond het oog groot en doorlopend over de neusbrug, geen telgang, geen dunne of rechte poten, geen tong.

## Eerlijk oordeel
- **Leest als een echte Pokémon:** ja, op 1× en 3×. Het is duidelijk een klein, laag, gemaskerd dier dat sluipt, met de constructie van Zigzagoon: één samenhangend lijf, poten onder schouder en heup, geen Escher. Naast ronde 23 is het rustiger en "echter", vooral de poten en de staart.
- **Zwakke punten:**
  - Door de Zigzagoon-bouw is het lijf lang en laag met korte pootjes. Het leest meer als "wasbeer/wezel" dan als compacte starter, en de kop is relatief groot (D2).
  - De romp heeft weinig vachtdetail (egaal 4 met schaduw 3); het lijf kan nog iets meer vorm krijgen (schouderbolling, gekartelde schaduwgrens).
  - De klauwen zijn op 1× witte streepjes: herkenbaar, maar nog niet zo sprekend als bij Sandslash. Langer maken gaat richting "too much".
  - De verre achterpoot is maar een stompje (zoals bij Linoone).
  - De kop is opnieuw getekend in de stijl van ronde 16, geen pixelkopie: masker, oog en oren volgen de Zigzagoon-kop, niet de bevroren ronde-16-pixels. Jordi moet dus zelf kijken of het gezicht "hetzelfde dier" blijft.

## Lessen
- Een volledige basis-sprite als onderlaag werkt snel: na 8 iteraties staat de constructie (poten, hoek), omdat er niets te verzinnen valt. De tijd gaat naar uitlijnen en omlijnen.
- Rijen met een vaste x-offset (of segmenten `(y, x, tekens)`) houden de kolommen controleerbaar. Rijen die op wisselende x beginnen, gaven direct een verspringend oog en een gat tussen oor en rug.
- `src.index('ACHTER = [')` vindt ook `VER_ACHTER = [`: zoek met een regelbegin (`'\nACHTER = ['`).
- Een hangende staart die niet tot de grond komt, leest niet als extra poot (de vervolgvraag van ronde 23).
- Staartanimatie: laat de staartvoet staan en rek het hangende deel. Een staart die in zijn geheel zakt, maakt een rechte rugrand.
- Meet ook ingesloten gaatjes (holes) en niet alleen open randen: tussen twee overlappende poten bleef 1 pixel lucht ingesloten.
