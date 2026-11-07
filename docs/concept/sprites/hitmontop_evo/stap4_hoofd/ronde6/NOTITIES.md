# Stap 4 hoofd, ronde 6 (6 nov): Hitmontops eigen kop bewerkt, niet getekend

Jordi zei over ronde 5b: "ik heb liever dat je hitmontops hoofd pakt en daarmee gaat spelen". Daarom begint deze ronde bij Hitmontops pixels (`graphics/pokemon/hitmontop/anim_front.png`), en elke stap is een bewerking op de vorige stap. Script: `stap4_r6.py`, met de hulpbestanden `hulp.py` en `stap12.py`. Het telwerk staat in `controle.txt`.

| Stap | Wat er gebeurt | Bestand |
|---|---|---|
| 1 | Uitsnede met de regel van stap3b `KOP`: geen blauw lijf, handen, polsbanden of armstokjes. | `stap1_uitsnede.png` |
| 2 | 180° gedraaid, zodat de hoorn boven zit. Elk oog is in zijn eigen 4×4-vak teruggedraaid, zodat het witte puntje weer linksboven zit. De lichtvlek is naar linksboven gespiegeld en de flappen zijn een toon omgezet. De hoorn is links licht gemaakt. | `stap2_gedraaid_licht.png` |
| 3 | De neerhangende zijflappen zijn weg. Hun binnenrand werd de omtrek van wang en kaak. De afgeronde bovenhoek van de linkerflap is de knot geworden; de plooien (5) zijn eruit. De hoorn heeft hier nog zijn volle grootte. | `stap3A/B_flappen_knot.png` |
| 4 | Hoorn kleiner: de middelste 3 rijen zijn eruit en de tip is gezakt (tip `ff`, dan `f34f`). | `stap4A/B_hoorn_klein.png` |
| 5 | Hitmontops rand boven de ogen staat 1 rij hoger en is zachter: f werd 5, met de uiteinden in 4, los van de omtrek. De flapschaduw is van de lichte linkerwang. De mond is een streepje van 5 px met de hoeken 1 hoger. | `stap5A/B_fade_mond.png` |
| 6 | Maat: A is rechtop 23 px breed (gedraaid 26), B 23 px. Er hoefde niets weg. | `stap6A/B_maat.png` |
| 7 | 27° tegen de klok in. De omtrek volgt het gedraaide masker en is daarna per pixel als pad gelegd. De ogen zijn 1:1 Hitmontops oog. Licht (linksboven), mond en fade zijn opnieuw gelegd. | `stap7A/B_gedraaid.png` |

- **Losse hoofden:** `hoofd_A.png` en `hoofd_B.png` (64×64). Ze staan op de plek van ronde 5b (midden ongeveer (14,35)).
- **Vellen:** `vel_hoofd.png` (8×/2×/1× naast Hitmontop en de anime) en `vel_stappen_A.png`/`vel_stappen_B.png` (alle stappen naast elkaar).
- **Varianten:** A heeft de knot achterop (linksboven, achter de kruin; gedraaid wijst hij naar achteren). B heeft de knot bovenop, rond de kleine punt.

## Hoeveel is nog Hitmontop
"Exact" betekent: zelfde plek én zelfde tint als in stap 2. "Plek" betekent: een pixel waar Hitmontop huid had.

| Stap | Exact | Plek |
|---|---|---|
| Stap 3 | 58–60% | 85–89% |
| Stap 4 | 61–64% | 88–93% |
| Stap 5 | 41–45% | 88–93% |

In stap 5 daalt "exact" omdat de flapschaduw is omgekleurd. In stap 7 is alles opnieuw gelegd na het draaien; alleen de ogen zijn 1:1 Hitmontop.

Controle: geen open randen, en alles ligt binnen 64×64.

## Eerlijke zwakke punten
- **Stap 5 verliest karakter.** Stap 3/4, met Hitmontops oude rand, frons en schaduw, leest het sterkst als "Hitmontops kop". Na het weghalen van de flapschaduw en de frons wordt het gezicht vlak en lief; dat was ook de kritiek op 5b. Wellicht moet meer van Hitmontops eigen schaduw blijven staan (alleen gespiegeld).
- **De knot leest niet duidelijk als knot.** Het is een bult met inkepingen. A leest gedraaid als oortje of kattenkop, B als ui of peer. Een "naar achteren gekamd" idee is er niet zonder haarlijnen, en die mogen niet.
- **Stap 3A:** de volle hoorn staat los naast de knot. Dat is een tussenstap; het klopt pas in stap 4.
- **Stap 7:** de schaduw is met een regel (rand rechts/onder = 4) gelegd en daarna niet pixel voor pixel bijgewerkt. De onderrand heeft een brede 4-band en een paar losse 5-pixels. De fade is op 1× bijna onzichtbaar, en de mond is op 1× maar een vlekje.
- **Omtrek gedraaid:** de rechterkant heeft een kleine bult naast het rechteroog (x41–42, y16–18). Onderaan zitten trapjes.
- Geen onafhankelijke keuring gedaan.
