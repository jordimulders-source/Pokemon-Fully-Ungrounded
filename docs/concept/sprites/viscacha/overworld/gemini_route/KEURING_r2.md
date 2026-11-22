# Keuring overworld viscacha, ronde 2 (19 nov)

Gekeurd: `af/overworld.png` (+ `overworld_normal.pal`, `overworld_8x.png`) tegen model `../gemini_r2_A.png`. Verse keurder; eerst blind naast eevee, rattata, sentret, minccino, pachirisu (1× en 4×), daarna per onderdeel op dezelfde schaal (model per aanzicht verkleind tot de figuurhoogte van de sprite, onder uitgelijnd, silhouet-overlay).

## Stap 1, blind
- **Voor:** leest als een net, af figuurtje; recht van voren, symmetrisch, oren/pluim/wangplukken duidelijk. Geen losse pixels of blur. Iets drukker dan de HGSS-buren (veel geel en donkere accenten), maar binnen wat pachirisu doet.
- **Achter:** leest goed (twee billen + middenlijn + oren). De gele wangplukken zijn op 1× bijna weg (1 gele pixel per kant).
- **Opzij:** leest goed als profiel; de staart oogt zwaarder dan de rest van de figuur (dikker dan bij de buren en dan het model).
- Geen open randen, geen hoekige trapjes die opvallen.

## Stap 2a, techniek
| eis | voor | achter | opzij | oordeel |
|---|---|---|---|---|
| hoogte (±21 / ±19, p75 23) | 22 | 19 | 22 (lijf+kop 18, met pluim 22) | ok |
| onderkant y29 | 29 | 29 | 29 | ok |
| midden x15–16 | 15,0 | 15,0 | 15,5 | ok |
| symmetrie (spiegel om x15) | 2 px verschil (zigzag van de pluim, zoals model) | 0 | – | ok |
| kleuren (9–15) | 11 | 8 | 10; palet 12, alle uit `af/normal.pal` | ok |
| loopframe | alleen rij 28–29 (voeten), 11/11/14 px | | | ok |
| omlijning | overal index 1 (28140c) | | | zie reparatie 4 |

## Stap 2b, trouw aan het model (zelfde schaal)
Silhouetverschil na schalen: voor 24/5 px (model/sprite-only, vooral 1 kolom rechts door afronding), achter 13/4, opzij 17/30 (vrijwel allemaal staart).

| aanzicht | oordeel |
|---|---|
| **Voor** | **PASS**. Oren, pluim met bruine voet, wangplukken, slabbetje, poten kloppen. Ogen volgens toegestane afwijking. |
| **Achter** | **FAIL (klein)**: wangplukken te klein t.o.v. model. |
| **Opzij** | **FAIL (klein)**: staart te dik; oor 1 rij te laag. |

## Reparaties (neem over uit het model, niet hertekenen)
1. **Opzij, staart** (rij 13–27, x21–28, frames 4 en 5): model is aan de staart 3–4,5 px breed incl. omlijning (gemeten op 22 px hoogte), sprite 5–6 px (bijv. rij 19–23: x23–28). Staart aan de buitenkant (rechts) 1 px smaller maken, rond de bocht onderaan (rij 24–27) mee; pluim bovenaan (rij 8–12) blijft.
2. **Opzij, oor** (x7–12): modeloortop ligt op rij 11, sprite op rij 12. Oor 1 rij hoger, vorm uit het model (ronde top, ver oor `c` erachter).
3. **Achter, wangplukken** (rij 18–19, x7–8 en x22–23, frames 2 en 3): model toont per kant een gele pluk van ±2–3 px breed met spikes; sprite heeft 1 gele pixel (x8/x22, rij 19). Uit het model overnemen: 2 gele pixels per kant, omlijning erbuiten, symmetrisch.
4. **Omlijning boven** (alle frames, techniek): boven en onder zijn nu dezelfde bijna-zwarte 28140c; de norm is onder zwart, boven een donkere tint (HGSS 33/45 frames). Oortoppen, kruin, pluim- en staartbovenkant naar een donkere tint uit `normal.pal` (alleen index 2, 80482a, komt in de buurt; lichter dan HGSS-tinten als 584018). Lijkt dat te licht: voorleggen, niet zelf een kleur toevoegen.
5. *(controle, geen FAIL)* **Voor, ogen** (rij 20–21, x12–13 en x17–18): glans zit linksonder-binnen; meetregel 6 zegt glans boven. Klopt dat met de front (zwaar bovenlid), dan laten staan.
