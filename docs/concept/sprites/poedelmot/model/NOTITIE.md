# Poedelmot 3D-model, ronde 1 (5 nov)

Jordi: "maak maar eerst een model en dan draaien we die driekwart". Alleen het model en het rondom-vel; nog **geen
silhouet**. De 3/4-hoek kiezen we samen met Jordi op dit vel.

## Bestanden
- `poedelmot_model.py`: het model en de renderer. Blender (bpy) staat niet in deze container; zelfde principe als
  `kolibrie_pre.py` (huid = smooth union van afstandsvelden, één huid), maar direct in numpy gerenderd:
  orthografisch, licht linksboven-voor. Eén eenheid ≈ 1 spritepx, kader 64. Snelle proef: `python3 poedelmot_model.py 45 [pitch]`.
- `rondom_vel.png`: tak-foto + 8 hoeken (0°, 30°, 45°, 60°, 90°, achter-3/4 135°, 45° van boven +20°, 45° van onder −15°),
  elk op werkformaat (met dunne lijnen op de grenzen tussen onderdelen) en op 64×64 1× (licht/donker).
- `renders/`: elke hoek apart (`*_512.png` werk, `*_1x.png` verkleind).

## Vorm (punten 1–5 van de coördinator + SPEC)
1. **Vleugels**: per kant een voorvleugel (lang, bredere top) en een ronde achtervleugel die overlappen tot één paar; samen
   in een V omhoog en naar achteren. Geen punt recht boven de kop. In 3/4 links-voor staat het nabije paar (dier-links)
   groot rechts achter het lijf en het verre paar kleiner linksboven, deels achter de kop. Dat is ook hoe Venomoth en Butterfree het doen.
2. **Kop** is een eigen bol (r 9,6) op een wolkraag. De kop draait 30% van de lijfdraai terug naar de kijker (Gen 3-regel).
3. **Sprieten = oren**, platte bruine bladen opzij, bijna horizontaal. Ze breken de buitenomtrek tussen de V-armen door.
4. **Vier pompon-poten**: wollige bovenpoot, dun enkeltje en een pompon met plukken (voor r 4,3, achter r 3,6). Het
   achterste paar staat verder opzij en naar achteren, dus in 3/4 hoger en niet op één lijn.
5. **Grote ronde donkere ogen** (Venomoth-achtig, ±9 px breed) met een bruin snuitje ertussen.
Kleuren zijn alleen hulp bij het lezen (wit/bruin/zwart); de echte kleur komt in stap 4.

## Eigen zwakke punten
- **Voorpoten te ver naar voren.** In de zijkant (90°) liggen ze als bij een liggende hond. Op de foto staan ze meer onder
  de borst. In 3/4 valt het mee, maar het vraagt een kleine correctie vóór het silhouet.
- **Wolreliëf is golvende ruis**, geen echte plukken. Het geeft wel massa, maar de katoenlook moet in de pixelstap komen.
- **Kraag naar kop** leest in de 1×-renders nog zwak: de inkeping is klein (kleine smooth-k), vooral frontaal.
- **Oren zijn gladde paddels**: de kamvorm (bipectinaat) zit er niet in; dat wordt pixelwerk. Ze lijken nu wat op koala-/muizenoren.
- **De verre vleugel** komt bij 45–60° als punt linksboven naast de kop uit. Ik vind dat niet storend, maar het is te
  controleren tegen "geen vleugelpunt boven de kop".
- **Kader**: bij 0° en 30° raken de vleugels bijna de rand; bij 60° en meer schuift het dier naar rechts (vaste kadermidden).
- **Achter-3/4 en onder** zijn alleen ter controle (rondom); daar zijn de vleugelvlakken grijs door het licht.

## Voorstel voor de keuze
45° lijkt het meest op een Gen 3-3/4 (beide ogen zichtbaar, nabije vleugels groot, verre oor steekt uit). 30° is de
veilige variant als de verre vleugel bij 45° storend blijkt. Jordi kiest.
