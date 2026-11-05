# Picapau kleur r2: notities (maker, 5 nov)

Opdracht (Claude): A op het bevroren silhouet (vleugel als duidelijke schubben + schouder ronder/lichter, punt donkerder; kuiftoppen als zwarte kap 2–3 px; snavel als één vorm met de kop, aanzet lichter/dikker, punt donker). B = A + voorstel-silhouetwijziging (snavelbasis dikker, pootjes uit elkaar, ronde buik), max. 30 px.

Bestanden: `maak_A.py` / `maak_B.py` (de handgekozen wijzigingen op r1 → `raster_A.txt` / `raster_B.txt`), `bouw.py` (→ `picapau_A.png`, `picapau_B.png`, `normal.pal`), `controle.py A|B` → `controle_A.txt`, `controle_B.txt`, `vel.py` → `vel.png` (1x boven, 8x onder: Taillow, r1, A, B, Pikachu). r1 onaangeroerd.

Palet: index 11 is nu **l lichtbruin (168,114,62)** voor de vleugelschouder; de snavel gebruikt voortaan 1/3/4/k (de aparte snavelkleur p is vervallen, 15 kleuren vol).

## Wat er veranderde (A)
- **Kuiftoppen**: zwarte kap 1–2–3–4 px breed met donkergrijze binnentint (`k / kk / kek / keek`), beide punten; 6 px extra, alle in de kuiftoppen-zone.
- **Snavel**: punt donker (k + goudbruin), lichte bovenhelft (1) loopt door tot in het gezicht, onderhelft schaduw (3); de goudbruine scheidingslijn tussen snavel en kop is weg, dus snavel en kop zijn één vorm.
- **Vleugel**: schouder lichtbruin (l, rond vlak linksboven); drie rijen schubben (was vier), elk een u-rand in room met een donkere onderkant: rij 1 licht (1), rij 2 basis (2), rij 3 schaduw (3), dus naar de punt donkerder; slagpennen bovenaan roodbruin, naar de punt bruin/donkerbruin (contrast met de roodbruine staart).

## Controle
- **A**: silhouet buiten de zones 0. In de zones 7: kuiftoppen (33,4) (32,5) (31,6) (39,5) (36,6) (39,6), snavelpunt (16,17), alle +. Open randen: alleen de 2 lichte teenpixels (29,46) (28,47) (tenen-zone, zoals r1). Losse pixels 0, clusters < 3 px 0. 825 px.
- **B**: 21 silhouetwijzigingen (budget 30): de 7 van A + snavelbasis (18,18) (17,22) (18,23) + poten/buik: weg (33,46) (33,47) (34,47) (34,48) (42,46) (43,46), erbij (35,46) (36,47) (37,47) (39,47) (40,47). Verre poot staat 1 px hoger (onderkant rij 47 i.p.v. 48) en naar achteren (x34–37), kolom 33 is lucht. Buikonderkant: rij 47 x39–40, rij 46 x38/41, rij 45 x42–43, dus een boog i.p.v. 8 px recht. Open randen idem 2 teenpixels; losse pixels 0; clusters 0. 827 px.

## Checklist
| punt | A | B |
|---|---|---|
| Leest op 1x als Pikachu-achtige specht | ok, kuiftoppen lezen nu als Pikachu-oortoppen | ok |
| Vleugelschubben leesbaar op 1x | ok: drie roomkleurige rijen op de bovenvleugel, schouder lichter | idem |
| Pootjes los van elkaar, verre hoger/achter | nee (silhouet) | ok |
| Buikonderkant rond | nee (rechte lijn, silhouet) | ok |
| Omlijning, licht linksboven, clusters, randen | ok | ok |

## Zwakke punten (eerlijk)
1. **Snavel (A en B)**: als vorm sluit hij nu wel aan op de kop, maar op 1x leest hij **minder als snavel dan in r1**. Hij heeft dezelfde tinten als de kop (de bleke hoorntint is weg om plek te maken voor de vleugelschouder) en vooral de goudbruine bovenrand is zichtbaar. Mogelijke oplossing: één tint teruggeven aan de snavel (bijv. iris e → k, dan komt er een plek vrij voor een bleke hoorntint), of de lichte aanzet lichter dan de kop maken. **Terug naar de maker, niet naar Jordi.**
2. **Vleugel**: nog steeds een lange strook langs de rug (modelvorm); de derde schubbenrij (in 3) is op 1x zwak.
3. **B, verre poot**: de tenen wijzen naar achteren als een grijs streepje van 3 px; op 1x leest het als "pootje achter", maar het is klein.
4. A: pootjes als één plukje en de rechte buiklijn blijven (silhouet; opgelost in B).

## Lessen
- Een tint schrappen om een andere toe te voegen heeft een prijs elders: de snavel verloor zijn eigen kleur toen p plaats maakte voor l. Bij een vol palet eerst kijken welke tint het minst zichtbaar is (hier e, 3 px).
- Een scheidingslijn tussen snavel en kop maakt een los staafje; zonder die lijn gaat de snavel op in de kop. Het verschil moet uit de tint komen, niet uit de lijn.
- Het variantenscript (`maak_B.py` op raster_A) houdt A en B identiek buiten de wijziging; de controle telt de silhouetwijzigingen zelf.
