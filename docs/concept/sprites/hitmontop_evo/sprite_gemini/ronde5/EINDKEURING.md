# Eindkeuring Hitmongroove: ronde 5 (`capoeira.png`, arm A)

Keurder: vers en onafhankelijk (8 nov). Ik heb `ronde3/EINDKEURING.md` en `NOTITIES.md` alleen als context gelezen en alles opnieuw gemeten (PIL op de geïndexeerde png).

**Armkeuze:** Jordi heeft al gekozen: "A uiteraard". Daarom is alleen `capoeira.png` gekeurd. B heeft geen reparaties nodig. Arm A was ook mijn keuze, om drie redenen:
- de rij huid op de schouder (rij 42) laat de torso in de arm overgaan, zoals in het model;
- in B zit de band direct tegen de torso, en dan leest de schouder als een ring;
- A heeft 2 px minder silhouetverschil met r3.

**Plaatje:** `eindkeuring.png`.
- Boven: r5 A op 8× met de reparaties omkaderd, een proef met reparaties 1–3 (alleen ter illustratie) en het model.
- Onder: alles op 1× (wit en donker) en 2× naast Hitmontop, Hitmonlee, Hitmonchan, Tyrogue, Breloom, Medicham, Blaziken, Hariyama en Machoke.

**Coördinaten** zijn (x,y), met 0 linksboven. **Tinten:**

| Index | Kleur |
|---|---|
| 1 | zwart |
| 2/3/4/5 | huid, licht → donker |
| 6 | wit |
| 7 | grijs |
| 8/9/A | geel |
| B/C/D | groen |
| E/F | blauw |

## Metingen

| | Kleuren | Vulling | Kader | Lichtkant zwart | Schaduwkant zwart | Vlakjes < 3 px |
|---|---|---|---|---|---|---|
| **r5 A** | 16 | 1217 | 50×61 | **72%** | 98% | 160 |
| r3 | 16 | 1205 | 50×61 | 78% | 100% | 157 |
| Hitmontop | 14 | 1257 | 53×50 | 21% | 50% | 201 |
| Hitmonlee / Hitmonchan | 13–14 | 1077–1149 | | 29–33% | 67–70% | 145–150 |
| Breloom / Medicham / Blaziken / Machoke | 13–16 | 1036–1579 | | 29–47% | 62–89% | 145–228 |
| Hariyama | 16 | 2409 | 64×64 | 71% | 91% | 179 |

- **Lichtkant zwart 72%:** dat komt nu bijna helemaal van de dunne delen: de diagonale benen, de 1 px-koorden, de bovenranden van de voeten en de onderkant van de kop.
  - Kop, vrije vuist, bovenarm, steunarm, manchet en bal-hand hebben aan de lichtkant hun selout (5 of 7).
  - De les uit r4 blijft staan: selout op 1 px-diagonalen maakt ze rafelig. Dit is dus geen reparatie.
- **Tintstappen**
  - Huid: 199/161/116/78, gelijkmatig.
  - Groen: 157/106/69, goed.
  - Geel: 232/207/142. De stappen 25/65 zijn ongelijk; dat is een paletkeuze (ter info).
  - Blauw: 134/85.
- **Vlakjes < 3 px:** 160. Dat is normaal voor deze grootte (de referenties zitten op 145–228). Ze zijn bedoeld: koordgroeven, glimpjes, ogen en binnenlijnen.

## Wat sinds ronde 3 verbeterd is (gecontroleerd)

- **Steunarm:**
  - geen totempaal meer: van de vier zwarte dwarslijnen zijn er nog twee over (pols en manchet), net als in het model;
  - de rechterrand van torso en arm is één lijn (x35);
  - de arm loopt taps van 5 naar 4, met een sikkel 1-2-2-2-1;
  - de lengte is gelijk gebleven (Jordi: "de arm mag niet langer").
- **Koordband:**
  - geen dambord meer: twee rijen gedraaid koord met regelmatige "/"-groeven (A op (30,43)→(29,44) en (33,43)→(32,44)), licht 8 links en 9 rechts;
  - hij steekt 1 px uit aan beide kanten, dus hij leest als een band om de arm;
  - op 1× en 2× leest hij nog als koord.
- **Reparaties 3–7 uit r3:**
  - selout op (17,26) en op de manchet (30,51–52);
  - de torso heeft geen schaduw meer aan de lichtkant;
  - de sikkel loopt taps;
  - de kruisnaad is 1 px;
  - de schaduwstrook van de kop loopt taps.
- **Hoorn:**
  - de ronde nop is nu een wig naar linksonder;
  - de lengte is als in het model: ±4 px, wat bij deze schaal overeenkomt met de spies in het model.

## 1. Eindkeuring: trouw aan het model en geloofwaardige evolutie: **PASS**

**Trouw:**
- Alle elementen van het model staan erin:
  - V-split;
  - kop omlaag met twee Hitmontop-ogen;
  - vrije arm met witte manchet en koordband;
  - grote koordriem met hangende koorden;
  - steunarm met manchet;
  - blauwe voeten met witte tenen.
- De toegestane afwijkingen zijn uitgevoerd:
  - de benen lezen als gekleurde benen, niet als broek;
  - de torso is bol door de kleur (keuze c);
  - de vuisten zijn volle ballen;
  - de steunarm is korter, met een koordband.
- Niets is toegevoegd wat niet in het model of de SPEC staat.
- Kop en vulling verhouden zich als in het model (de kop is ±40% van de breedte).

**Evolutie:**
- Naast Hitmontop, Hitmonlee, Hitmonchan en Tyrogue leest hij op 1× meteen als familie:
  - het Hitmontop-oog en de blauwe voeten;
  - de huidkleur van Hitmonlee;
  - de bokshand van Hitmonchan;
  - de kopspin wordt een handstand.
- De ontwerpkanttekening uit r3 blijft gelden: hij oogt niet zwaarder dan Hitmontop (vulling 1217 tegen 1257, dunne benen). Dat zit in het bevroren model en is niet in de sprite op te lossen; zie ter info.

## 2. Gen 3-spritekeuring: **PASS**

- **Formaat en vulling:** precies tussen Hitmontop, Hitmonchan en Breloom.
- **Detailniveau:** gelijk aan Hitmonlee en Medicham.
- **16 kleuren** inclusief transparant (index 0).
- **Leesbaar op 1×,** zowel op wit als op donker: V-benen, kop met twee ogen, bal-hand op de grond, gele riem.
- **Omlijning:** zwaarder dan Hitmonlee en Hitmontop, maar gelijk aan Hariyama en Medicham, en het komt door de dunne delen (zie metingen). Op 1× is hij niet merkbaar donkerder dan Machoke of Hariyama.
- **De hangende koorden** zijn de drukste pixels. Ze staan in het model, dus dit is toegestaan.

## 3. Dragonfly Cave-keuring: **BIJNA** (twee kleine reparaties, plus één optionele)

**Goed:**
- Licht komt overal van linksboven.
- Geen anti-aliasing en geen losse omlijningspixels.
- De beenranden zijn regelmatige 1:1-trappen.
- De bal-hand is een schone cirkel: glans linksboven, een sikkel rechtsonder en een slagschaduw onder de manchet.
- De binnenlijnen tussen kop en torso zijn in donker 5 en lopen taps.
- De torsosikkel volgt de vorm.
- Er zit geen dambord of ruis meer in de band.

**Nog fout:**
- **Mini-pillow op de schouder:** rij 42 is `1 4 3 3 3 4 1`, dus een schaduw 4 aan beide kanten van een rij van 3. De 4 op (30,42) zit aan de lichtkant, direct naast de selout van de arm.
- **Hoornpunt stomp:** de punt bestaat uit twee pixels boven elkaar: 5 op (8,48) en 1 op (8,49). Op 2× leest de hoorn daardoor als een hoekig nopje in plaats van een punt.

## Reparaties (belangrijkste eerst; diff 0 erbuiten)

**1. Schouder zonder pillow.** (30,42): 4 → 3. Rij 42 wordt `1 3 3 3 3 4 1`; de schaduw blijft alleen rechts.

**2. Hoornpunt scherp.** De hoorn wordt niet langer: de punt blijft op x8, het silhouet wordt 1 px kleiner. Dit past bij Jordi's "hoorn moet niet langer".
- (8,49): 1 → transparant (0).
- (8,48): 5 → 1.
- Resultaat: de punt is één zwarte pixel op (8,48), de onderrand is `111` op x9–11 en de bovenrand houdt zijn selout 5 op (9,47).

**3. (Optioneel) Selout torso in de oksel.** (20,32): 1 → 5. Dit is de enige zwarte lichtkantpixel van de torso tegen transparant, in het gaatje tussen de vrije arm en de kop. Het effect is klein.

Gecontroleerd op de proef: 16 kleuren, geen nieuwe tint, silhouet −1 px op (8,49).

Na reparatie 1–2 is de sprite **klaar voor af/**. Een nieuwe volledige keuring is niet nodig; een pixeldiff-controle (alleen deze 2–3 pixels) is genoeg.

## Ter info voor Jordi (ontwerpvragen, geen reparatie)

- **Hoorn:** hij leest als punt op 2× en 8× (na reparatie 2 duidelijker). Op 1× is hij een klein hoekje onderaan de kop, net zo klein als in het model. Langer maken is niet nodig en ook niet gevraagd ("hoorn moet niet langer").
- **Evolutie-gewicht:** hij oogt niet groter of zwaarder dan Hitmontop. Dat ligt aan het bevroren model (dunne benen, kleine romp), niet aan de vertaling.
- **Geel-palet:** de stappen 25/65 zijn ongelijk. Tint A iets lichter maken, bijvoorbeeld (200,156,56), maakt ze gelijkmatiger, maar dat raakt alle koorden en banden. Het is een paletkeuze en geen fout.
