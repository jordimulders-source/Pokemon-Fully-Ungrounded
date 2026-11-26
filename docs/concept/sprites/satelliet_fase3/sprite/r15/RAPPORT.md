# Ruimtestation sprite r15 (25 nov): twee afkappingen weg

Jordi over r14 (met `r14/jordi_afkappingen.png`): "hier kappen de twee panelen onnodig af toch?"

**Werkwijze:** `herstel15.py` werkt vanaf `r14/sprite.png` en verandert alleen de twee aangewezen plekken. De recepten komen uit `recept.py`.

**Wat er veranderd is:**
- 53 pixels anders, allemaal binnen x 26–42 en y 23–48.
- De ogen zijn niet aangeraakt: 0 px verschil.
- 16 kleuren incl. transparant (transparency=0).
- Elke pixel staat met zijn reden in `log.txt`; zie ook `diff_r14.png`.

**Uitvoer:**
- `sprite.png` en `sprite_8x.png`
- `vel.png`: r14 en r15 op 8×, close-ups van beide plekken (r14 | r15 | modeluitsnede), 1×/2× naast fase 2.

## Plek 1: rechts van mast PB
**Wat het model laat zien:** het linkerachterpaneel PA komt rechts van de mast weer tevoorschijn en loopt door tot tegen de achterarm (model_r10 en model_gekozen). In r14 eindigde PA op zijn ingekorte binnenrand (x 38,7), achter PB.

**Wat er veranderd is:**
- PA is aan het binnen-einde ×1,4 verlengd. De vakgrenzen blijven op dezelfde plek; alleen het laatste vak loopt door.
- Alleen lege pixels rechts van PB (x ≥ 38) zijn gevuld. Achter de arm en romp verdwijnt PA.

**Nieuw PA (11 px):**

| plek | pixels | kleur |
|---|---|---|
| bovenrand | (38,23), (39,23), (40,24), (41,24) | navy |
| bovenrand | (42,24) | zwart |
| lichte rand | (38,24), (39,24) | |
| vak | (38,25), (39,25), (38,26) | |
| onderrand | (39,26) | zwart |

**Gevolg:** (33,26) is van rand vak geworden, omdat PA daar nu onder de romp doorloopt.

## Plek 2: links van PF, boven PE
**Wat er mis was:** de witte driehoek (x 27–33, y 42–46) was geen voorbuis. Het was ingesloten modelachtergrond tussen de voorbuis, PF en PE. De achtergrond-floodfill bereikte hem niet, dus de kale reductie maakte er witte romp van.

**Waar de buis echt ligt:** in model_gekozen loopt de onderrand van de voorbuis van (28,1; 45,6) naar (34,1; 41,1), in spritecoordinaten. Alleen daarboven ligt de buis echt vóór PF.

**PF zichtbaar (10 px), recept zoals r14:**
- (32,42)–(32,46): linkerrand navy
- (33,42)–(33,45): lichte rand
- (33,46): vak

Daarbij is (34,42)–(34,45) van navy rand weer vak geworden (4 px). PF heeft nu boven PE zijn volle breedte van 6 px.

**Onderrand voorbuis (8 px, zwart):** (32,41), (33,41), (31,42), (30,43), (28,44), (29,44), (27,45), (26,46).

**Driehoek:**
- Transparant, zoals de witte achtergrond in het model: (30,44), (31,44), (30,45), (31,45).
- Losse gaatjes van 1 px buisrand gemaakt (zwart, anders ruis): (27,46), (31,46), (31,43), (28,45), (29,45).

**PE-rand (10 px):** de punt van PE grenst nu aan de lege driehoek en krijgt daarom zijn eigen rand. Het gaat om (28–30,46), (27,47), (31,47) (navy) en de lichte rand eronder.

## Let op
Er blijft een transparant gaatje van 2×2 tussen buis, PE en PF. Dat zit ook in het model, maar op 1× kan het als een gaatje lezen. Dichtmaken met buisrand is een kleine wijziging.
