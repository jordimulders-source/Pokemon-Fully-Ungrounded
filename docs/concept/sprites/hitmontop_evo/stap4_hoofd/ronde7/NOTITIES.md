# Stap 4 hoofd, ronde 7 (6 nov): Jordi's recept, op Hitmontops eigen pixels

Jordi (letterlijk): "De V-vorm tussen zijn ogen, die lijn gaan we naar achter trekken, die haren komen samen in een soort knot, dat mag gewoon een rondje zijn met een witte band, bijna zoals zijn handen. en de stekel bovenop mag kleiner, makkelijker kan ik het echt neit maken". Referentie: `../../referenties/hitmontop_3d.webp`.

Basis: ronde 6, stap 2. Dat is Hitmontops kop rechtop: ogen terug in hun vak, licht linksboven, en de neerhangende zijflappen weg (hun binnenrand is de wang- en kaaklijn).

## Stappen
Bestanden: `stap0_…png` t/m `stap4_…png`, samen in `vel_stappen.png`.

1. **V naar achteren** (`stap1_V_naar_achteren.png`).
   - Hitmontops eigen V-lijn (de voorrand van de flappen, met de punt tussen de ogen) staat 2 rijen hoger. De pixels en tinten zijn dezelfde.
   - Het voorhoofd tussen en boven de ogen is vrij gezicht. De flapschaduw op wang en voorhoofd is weg.
   - Eén aanvulling: de V-punt is dichtgezet met 2 px (`(33,17)` 4 en `(34,17)` 5). In het origineel stond die 2 px open.
2. **Knot** (`stap2_knot_variant1/2.png`).
   - De knot is Hitmontops linkerhand (`anim_front.png`, x9–16, y28–35), 1:1 overgenomen zonder het armstokje.
   - De band is zijn polsband in zijn eigen kleuren: wit `1` in het midden, grijs `c`/`d` aan de randen, omlijnd. Hij zit tussen knot en kop, zoals bij hand en arm.
   - Variant 1: knot achter op de kruin, met een liggende band op de kruin.
   - Variant 2: knot achterop/opzij, met een staande band precies waar de V-lijn naar achteren uitkomt.
3. **Stekel kleiner** (`stap3_…png`). Het is zijn eigen stekel; de 3 middelste rijen zijn eruit en de tip is gezakt. Er blijven 3 rijen plus de voet over.
4. **Gedraaid** (`stap4_gedraaid_…png`).
   - Licht tegen de klok in, 15°. Het draaien gebeurt met rotsprite als gids. Daarna gaan de ogen 1:1 terug, worden losse pixels weggehaald en wordt de omtrek dichtgezet.
   - Dit is nog niet per pixel nagewerkt.

De ogen en de mond zijn Hitmontops eigen pixels en zijn niet veranderd: de frons-streep is gebleven.

## Opgeleverd
- `hoofd_1_rechtop.png`, `hoofd_1_gedraaid.png`, `hoofd_2_rechtop.png`, `hoofd_2_gedraaid.png`: elk 64×64.
- `vel_hoofd.png`: 8×, 2× en 1×, rechtop én gedraaid, naast de sprite en `hitmontop_3d.webp`.
- Telling in `controle.txt`: variant 1 heeft 59% eigen Hitmontop-pixels en variant 2 60% (zelfde plek en tint als stap 2, of de hand 1:1).

## Zwakke punten
- **Variant 1:** de knot staat met zijn smallere band boven de kruin. Op 1× leest dat als een bolletje op een steeltje (antenne), niet als een knot die óp het hoofd ligt.
- **Variant 2 leest beter als knot met band achterop**, maar kan ook als oor of hand gelezen worden.
- **Het "naar achteren kammen" zie je alleen aan de hogere V-lijn.** De schedel boven de V is smal (2–3 rijen). Er is geen massa die zichtbaar naar de knot toe loopt; dat zou nieuwe pixels vragen.
- **De gedraaide versies zijn rotsprite plus een automatische schoonmaak.** Er zitten trapjes in de omtrek, en de V en de mond zijn wat rafelig. Ze zijn niet met de hand nagewerkt.
- Niet onafhankelijk gekeurd.
