# Studie: waarom Dundragoon, Princadee, Zapacha en Skinguin "uit een Pokémon-game" lijken (24 nov)

Jordi: "dundragoon doet dat het beste van alle sprites die we gemaakt hebben, princadee en zapacha ook" · "skinguin is trouwens ook uitstekend, die 4 lijken het meest alsof ze uit een pokemon game komen" · "dus doe een studie naar wat het kleurgebruik zo goed maakt in die sprites en pas het toe op de bibarel evo".
Vel: `beste4.png` (de vier + onze r17 en r18 op 4×, paletladders met tint h, verzadiging s, luminantie L en aandeel). Script: `beste4.py`.

## Metingen
| | buitenlijn | aandeel buitenlijn | lijn per vlak (L lijn / L basis) | tintverschuiving licht → schaduw |
|---|---|---|---|---|
| Dundragoon | (16,16,24) blauwzwart | 14% | geel 109/218 = 0,50; blauw 73/148 = 0,49 | geel h56→52→50→49; blauw 199→202→200→204 |
| Princadee | (35,18,17) roodzwart | 14% | bruin 51/107 = 0,48; rood 60/106 = 0,57 | rood/oranje h22→10→0→0; geel 50→36→37 |
| Zapacha | (40,20,12) bruinzwart | 18% | oranjebruin 85/190 = 0,45 | h44 (crème)→40→36→31→21→20 |
| Skinguin | (24,16,32) paarszwart | 14% | rood 52/110 = 0,47; geel 71/204 = 0,35; wit 122/248 = 0,49 | rood h7→2→352→349; geel 46→42→38→32 |
| **ons r17** | (16,16,16) neutraal zwart | **7%**, lichtkant bruine b | bruin 59/146 = 0,40; crème: geen eigen lijn | bruin h39→30→28→28 (bijna vlak) |

## Vijf regels (wat het "game"-gevoel geeft)
1. **De hele buitenrand is een getint bijna-zwart** (L 16–25), ongeveer 14–18% van de pixels, in de kleur van de soort (bruinzwart, roodzwart enz.), dus geen neutraal zwart en geen lichte lijn op de lichtkant. Dat is wat ze "af" laat ogen. Wij hadden half zo veel buitenlijn, deels in middenbruin.
2. **Elke kleurgroep heeft een eigen lijntint, niet zwart**, op ±0,35–0,5 van de basistint en sterk verzadigd (s 65–90). Die lijn staat waar vorm over vorm valt en rondom elk vlak van een andere kleur (Dundragoons gele vlakken hebben een olijflijn, Zapacha's crème buik een bruine).
3. **Duidelijke tintverschuiving over de ladder**: het licht is geler en minder verzadigd, de schaduw roder en verzadigder (10–25° over de hele ladder). Ons bruin was bijna één tint, dus vlak en "bruin uit een pot".
4. **Verzadigde middentinten, een klein, licht en bleek hooglicht**: de basistint en de schaduw zijn s 55–80; het hooglicht is 4–10% van de pixels, s 20–40.
5. **Harde overgangen tussen kleurgroepen**: een vlak stoot met zijn lijntint of schaduwtint op het andere vlak; nergens mengtinten die tussen twee groepen in zitten.

## Toegepast in `sprite_r18/` (zie `bouw.py`)
1. Buitenlijn: bruine b op de silhouetrand → K (43 px); K wordt bruinzwart (40,20,12), zoals bij Zapacha.
2. Lijnen per vlak: bruin b (92,40,16), lijn/basis = 0,35 (Jordi: "iets harder, iets donkerder"); crème krijgt een gouden lijn D (152,100,40), 0,45, rondom de tuinbroek (38 px, Jordi: "zelfs het buikvlak").
3. Tintverschuiving bruin: f h36, d h29, c h20, b h19 (was 34/30/29/28); crème C h50 → M h44 → S h36 → D h32.
4. Verzadiging: d s63, c s69, f s49 (hooglicht minder verzadigd dan de basistint).
5. Harde overgangen: al in r17 (geen mengband D meer tussen crème en bruin); de oogrand-D gaat naar d.
