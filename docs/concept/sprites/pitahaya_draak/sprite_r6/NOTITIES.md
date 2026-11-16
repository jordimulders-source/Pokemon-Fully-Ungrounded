# Pitahaya-draak r6 (op af/pitahaya_draak.png)

Jordi: "rechterarm zit vast aan het lichaam, kijk nog beter naar schaduw, kleur, belijning".

## Opzet
- **Bevroren (gemeten):** alles boven y 37 (diff 0, dus ook het ooggebied, de mond en het tandje). De buitenomtrek verandert alleen bij het armgat (4 px).
- **Script:** `maak_r6.py` (aanroep `python3 maak_r6.py 1.5 pitahaya_r6.png tint`). Wijzigingen per pixel in `afwijkingen_af.txt`.
- **Vel:** `vel.png` (r6 | af | model op 8×, arm op 12× naast het natieve model, 1× en 2× op licht en donker).

## Gen 3-studie (Treecko, Cacnea, Bagon, Oddish, bovenste 64×64 op 8×)
- **Groen:** Gen 3 heeft een verzadiging van 0,42–0,86 (Treecko 0,42–0,79, Cacnea 0,44–1,0, Oddish 0,47–0,72); onze groentinten hadden 0,27–0,40 en lazen grijzig. Roze (0,59–0,68, licht 0,38) zit al in de Gen 3-band (Treecko-rood 0,60–0,68).
- **Schaduw:** Gen 3 legt grote doorlopende tintvlakken die de vorm volgen. Ons lijf had een grote donkergroene massa in het midden en links van de romp (x 23–37, y 37–51). Die kwam uit de reductieregel "≥ 3 px van de donkerste toon → donkerste toon", die schaduw als lijn behandelde, en was donkerder en vlekkeriger dan het model.
- **Lijn:** het zwartaandeel (17 %) zit binnen de Gen 3-band (Bagon 14 %, Treecko 30 %). Tussen arm en romp ontbrak de scheiding.

## 1. Rechterarm los van het lijf (13 stappen, 9 px blijven na stap 2)
In het model zit tussen arm en romp een gat met achtergrondkleur, ingesloten door zwart. Het staat in `groepen.py` als 'wit' (niet met de rand verbonden). Elk blok met ≥ 3/9 van zulke pixels wordt transparant.
- **Gat:** (38,41), (38,42), (38,43), (39,43).
- **Lijn rond het gat:**
  - zwart waar het model ≥ 1 zwarte px heeft: (38,40), (39,41);
  - donkerste groen waar dat niet zo is: (39,40), (39,44), (37,44), (40,42), (40,43), (40,44).
  - Een deel van die diagonale buren is daarna door stap 2 opnieuw gekwantiseerd. De 4-buren van het gat zijn randpixels en blijven lijn.
- **Lijnstuk (38,45):** donkerste groen. Het model heeft daar donkergroene pixels (lum < 85) tussen (38,44) en (39,46); daarmee loopt de scheiding door tot de onderlijn van de arm (39–41,46). Het gat onder de klauwen, (40,47), (41,48) en (42,48), stond al.

## 2. Groene toonkaart (72 px)
- Binnenpixels van romp, armen en poten (groen, geen rand, geen echte modellijn) komen opnieuw uit de gladgestreken groene luminantie van het model (σ 1,5), naar de dichtstbijzijnde modeltoon (73/98/123/158).
- "Echte lijn" = een blok met ≥ 3 donkere modelpixels (lum < 62 of zwart). Die blijven: de ribbels en naden.
- Daardoor verdwijnt de te donkere middenmassa: donkergroen 161 → 111 px, dat is ongeveer wat het model heeft. Licht blijft op dijen en armen, schaduw onder de kop en rechts.
- **Verworpen:** drempels volgens de oude toonverdeling ("kwantiel"). Die hield de te grote donkere massa in stand.

## 3. Palet groen (alleen waarden, helderheid en tint gelijk)
| idx | af | r6 | verzadiging |
|---|---|---|---|
| 8 | (48,80,52) | (43,83,48) | 0,40 → 0,48 |
| 9 | (80,113,76) | (72,119,66) | 0,33 → 0,45 |
| 10 | (115,147,101) | (108,153,89) | 0,31 → 0,42 |
| 11 | (155,183,134) | (150,188,121) | 0,27 → 0,36 |

Bewust onder in de Gen 3-band gehouden, omdat het model zelf gedempt saliegroen is.

## Afwijkingen t.o.v. af (81 px; per pixel de laatste stap)
| Stap | kop (y ≤ 36) | romp | linkerarm | rechterarm | poten | totaal |
|---|---|---|---|---|---|---|
| 1 gat | 0 | 0 | 0 | 4 | 0 | 4 |
| 1 lijn rond het gat + (38,45) | 0 | 0 | 0 | 5 | 0 | 5 |
| 2 toonkaart groen | 0 | 27 | 8 | 17 | 20 | 72 |
| 3 palet | 0 | 0 | 0 | 0 | 0 | 0 |

## Zelf vergeleken (r6 naast af op 1×, 2×, 8×)
- **Beter:** de arm leest op 2× los (wit gaatje met lijn eromheen). Het lijf is rustiger en minder donker, met meer vorm (lichte dijen en arm, schaduw onder de kop). Het groen leest als plant in plaats van grijs.
- **Niet aangepakt (bevroren of buiten de opdracht):** de kop (y ≤ 36) is ongewijzigd, ook de zwaardere zwarte schubranden rechts. Het gat is maar 4 px; het model toont daar weinig meer. De bovenkant van de arm sluit aan de schouder nog zonder lijn aan op de romp, want het model heeft daar ook geen lijn.
