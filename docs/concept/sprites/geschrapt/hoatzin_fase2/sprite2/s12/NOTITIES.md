# Hoatzin fase 2, ontwerp 2, s12 (20 nov): tweede ronde hoofd, poten, verre vleugel

Op s11 vond Claude het niet duidelijk genoeg beter. Er kwamen keurderpunten A1–C3 bij (zie de opdracht). `sh alles.sh` draait bouw12.py op s10.
Silhouet = s10, 0 px anders (assert). Oog: zwart + 6 rood gelijk (assert). 194 px anders dan s10.
Pixels anders per zone (tegenover s10 / s11): verre vleugel 115/42, kop 42/14, poten 37/17, staart 9/9. Studie en voorbeelden: zie `../s11/NOTITIES.md`.

## Keurderpunten: wat ermee gebeurd is
- **A1/A2 onderkaak:** de kaak loopt door van punt tot mondhoek: (4–6,34) licht 8, (7–8,34) midden 7. Geen zwart meer in de kaak; de zwarte klont aan de punt is weg. De keel erachter is crème (6), dus kaak en keel komen los.
- **A3 bovensnavel:** bovenrug licht (rij 32). Onderkant aan de basis midden (4–5,33). Haakpunt (1,33) midden. De mondlijn (2–3,33) blijft zwart, zodat de open bek als twee kaken leest. (3,33) kreeg geen kleur: dan liep de bovenkaak zonder lijn in de mondopening over.
- **A4 gezicht:** volgens Mandibuzz een sikkel middentint (2) linksonder en onderaan om het masker: (6–8,31), (7–8,32). Diepe schaduw (3) rechtsonder: (11,30–31), (9–10,32). Boven het oog blijft licht (15). (5,30) bleef licht: dat is de lichtkant.
- **A5 streng:** (11,24) is nu midden. De streng loopt als trapje (10,24)-(10,25)-(11,25)-(11,26)-(12,26). Een zuivere 1-px-diagonaal gaf dambord.
- **A6 onderband:** (6–7,26) is nu midden. Er is één donkere rij boven de zwarte lijn.
- **A7 bovenband:** per lob onderbroken met midden op (9,23) en (12,23). Lobben: x7–8, x10–11, x13.
- **B1 verre poot:** geen navy meer. Grijs (7) met zwart aan beide kanten (Skarmory/Unfezant). Voet: bovenrij teen grijs, onderrij (33–35,59) zwart. Klauwen lichtgrijs ingesloten op (37,59), (33,60), (43,57).
- **B2:** (30,56) is nu 7; de achterteen is egaal midden.
- **B3:** de voorteen heeft een selout 7 bovenaan (18–22,56). Licht komt pas vanaf de enkel (23–26,56).
- **B4:** de klauw (18,57) staat los van het licht door een 7 op (19,57).
- **Nabije scheen, hele lengte:** elke rij heeft dezelfde volgorde: selout 7 aan de lichtkant, licht 8, zwart aan de schaduwkant. Bovenaan midden onder de veren.
- **C1 verre vleugel boven:**
  - De veertoppen (rij 8–10) zijn één aaneengesloten lichte rand, en de lichte linkerrand loopt door tot rij 19.
  - Er zijn nog twee veerscheidingen (4) vanuit de inkepingen, als trapje omlaag naar rechts. De rest is midden.
  - De lichte randen naast elke penlijn zijn weg.
- **C2 onderblok:** een donkere veerlijn langs de schuine bovengrens: (23–26,19) en (19–22,20). Daaronder een randje middentint: (23–26,20) en (18–23,21). Een veertop midden op (22–23,24).
- **C3:** de grens met de donkere sikkel rechts loopt nu schuin (rij 15–19) in plaats van horizontaal.
- **Staart:** de bovenste staartveer (x44–53, rij 42–45) heeft een lichte rand boven en midden eronder, waar per pixel 2/3 wisselde.
- **Navy uit elkaar:** 2 = (100,114,178), 3 = (64,60,104), 4 = (34,32,60). De vleugels zijn steviger.
- **Niet gedaan:** de penlijnstapjes in de nabije vleugel en ondervleugel. Dat is buiten hoofd en poten en geen paletkwestie.

## Paletbudget (15 + transparant)
| # | kleur | gebruik |
|---|---|---|
| 1 | (16,14,24) | lijn |
| 2 | (100,114,178) | navy licht, gezicht sikkel |
| 3 | (64,60,104) | navy midden, gezicht diepe schaduw, krop donker |
| 4 | (34,32,60) | navy donker: verre vleugel onder, penlijnen, sikkels |
| 5-6 | crème licht/midden | 5 ook klauwen nabije poot, 6 ook de keel |
| 7 | (146,144,136) | crèmeschaduw = grijs midden (snavel, poten, selout nabije poot) |
| 8 | (192,192,188) | grijs licht (snavel, nabije poot, klauwen verre poot) |
| 9-10 | krop | ongewijzigd |
| 11-13 | (200,126,78) (150,80,54) (96,42,32) | kuif |
| 14 | (196,60,52) | oogrood |
| 15 | (116,158,204) | gezicht licht |

## Controle
dambord 0 · om-en-om 0 · zwarte klonten 0 · barcode 0 · losse tintpixels 24 (klauwen, haakpunt, oude penlijnstapjes nabije vleugel).
`vel.png`: s12 | s10 | model op 8×, daaronder per onderdeel de voorbeelden naast s12 en s10.

## Eerlijk, wat nog zwak is
- **Kuif:** de bovenkant blijft vrij recht (silhouet bevroren). Het is wat haariger dan s10, maar geen rafelige kuif zoals in het model.
- **Gezicht:** heeft nu drie tinten, maar er is geen echt hooglicht. Het masker is maar ±20 px.
- **Snavel:** de twee kaken lezen op 8×; op 1× is het nog een kleine grijze haak.
- **Verre vleugel onder:** de structuur in 3 tegen 4 is subtiel; op 1× is het vooral een donker vlak achter de kop.
- **Tenen:** door de vorm heeft de nabije voet één voorteen (model: drie). De achterteen van de nabije poot staat aan de bovenkant open, omdat hij maar 2 px hoog is.
- Nog niet onafhankelijk gekeurd.
