# Poedelmot: kleur r14

Gebouwd vanaf r13. Alleen de 5 punten uit de keuring van r13 zijn aangepast; de rest is bevroren. Kop, ogen, sprieten, linkervleugel en middenstuk zijn niet geraakt. Alle wijzigingen staan met de hand in `stappen/r14.py`.

## Gedaan
1. **Voorvleugel-onderrand:** 3 schulpbogen in lijn 3, met het dal op y36 (x40–42, 45–47, 50–53) en knikken op y35 (x43–44, 48–49). De laatste boog loopt via (54–55,37) naar de inkeping. Binnen de bogen zit de vlaktint van de voorvleugel (tan aan de voet, crème, wit). Onder de knikken komt de witte bovenrand van de achtervleugel door.
2. **Achtervleugel/pluim E:** 2 bogen met het dal op y47 (x47–48, x51–52) en de knik op (49–50,46) in plaats van een rechte lijn van 9 px.
3. **Pluimen en binnenlijnen:**
   - C heeft bovenop een koepel: (37–39,52) en de schouders (36,53)/(40,53).
   - De grens tussen B en de kraag is rafelig: lijn afwisselend op y47/y48, met witte donspunten (25,48) en (27,48).
   - Binnenlijnen lopen taps uit: de bovenkant van de overlaplijn A/B (21,51) is 7, de bovenkant van de grenslijn x40 (y45–46) is 6.
4. **Voorvleugelpatroon:** de grote tan vlek is vervangen door schubjes van 3 px in 6 met een bruine onderrand (4): (51–53,23–24), (47–49,31–32) en (51–53,31–32). Daartussen staan de bestaande C-krul en boogkrul (y26–30).
5. **Klauwtjes:**
   - De buitenrand is overal lijntint 2; geen 2/3 meer om en om.
   - Teentjes in 4 binnenin: A (19,55), B (23,55), B2 (26,58), C (36,60) en (38,60) gescheiden door 2, D (44,58).

## Controle
Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0.

## Zwakke punten
- **Rij schubjes:** de twee schubjes op y31–32 staan naast elkaar op één rij. Op 1× kunnen ze weer als patroon gaan lezen.
- **Oorspronkelijke opdracht:** die vroeg juist om minder, grotere vormen. De keuring wil nu schulpen zoals het model. Ik heb het bij 3 schubjes + 2 krullen gehouden.
- **Pluimen:** de naden tussen de pluimen zijn verder nog volle 3-lijnen (alleen de uiteinden lopen taps). De toppen van D en E zijn niet herzien.
- **Klauwtjes:** blijven op 1× kleine stipjes. D heeft maar één teentje, want er is geen ruimte binnen het silhouet.
- **Keuring:** niet onafhankelijk gekeurd.
