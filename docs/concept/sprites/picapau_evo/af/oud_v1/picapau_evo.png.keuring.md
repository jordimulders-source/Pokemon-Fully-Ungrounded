# Keuring picapau_evo r16 (eindkeuring na de 2 reparaties uit r15, 7 nov)

Bron: Pidgeot Gen 3-front (frame 1; pose, vleugel, voeten), Staraptor Gen 3-front (frame 1; tenen en klauwen), Taillow Gen 3-front (frame 1; tinten, sikkels, oog), Picapau `docs/concept/sprites/picapau/af/picapau.png` (stippen, wang, steunstaart), Raichu Gen 1 `referenties/jordi_inspiratie_raichu_gen1.png` (slierten, lus, bliksem-Z, buikovaal). Keurvel: `keurvel.png` (deze map). Ik heb de pixeldiff tegen `../r15/picapau_evo.png` zelf nagerekend.

8×: precies 5 px anders dan r15:
- (19,7), (18,8) en (19,8) gingen van j naar f;
- (20,39) en (21,39) gingen van zwart naar f.

De kop heeft nu één glans, linksboven, en een sikkel rechts. De onderrand tussen de poten is niet meer recht: het kastanje lijf loopt door tot op de nabije tarsus, met zwart alleen op (18-19,39) en (22,39). Er komt geen lichte kleur op de buitenrand: (20-21,39) grenzen alleen aan het lijf, de tarsus en zwart. Verder is er niets veranderd, ook de omtrek niet.

1×: een complete Gen 3-vogel-Pokémon in 3/4 met het Raichu-motief. Slierten, lus en Z-bliksem zijn direct herkenbaar, de poten lezen als klauwtjes, de wang als wang en de stippen als stippen. De crème buik is de grootste lichte vlek; dat hoort bij het motief.

Hoofdvraag: ja. Op 1× een echte Gen 3-Pokémon-vogel in 3/4 met het gekozen motief.

Blind oordeel (stap 1 bij r14, ter vergelijking): een kastanje vogel, 3/4 naar links, achterover leunend, Pidgeot-achtige pose met Raichu-motief. Wat in r14 stoorde (ei-buik met banding, klem-poten, voorrand met strook, plusjes als stippen, zwakke bliksem) is in r15 en r16 opgelost.

Per reparatie uit r15:
1. Het j-restje op de kop is gelukt: (19,7), (18,8) en (19,8) zijn nu f, en de enige glans staat linksboven (x21-23, y3-5). De 2 px "snavel P5"-verschil op rij 8 in `diff_uitvoer.txt` zijn deze voorhoofdpixels; de snavel zelf (rij 9-13) heeft 0 px verschil.
2. De onderrand tussen de poten is gelukt: de rechte zwarte lijn van 5 px op (18-22,39) is gebroken door f op (20-21,39), en het lijf eindigt nu rond op de tarsus.

Per onderdeel:
- kop: lijkt op Taillow/Pidgeot (ronde kop, één glans linksboven, sikkel rechts) / wijkt nergens af.
- oog: lijkt op Picapau/Taillow (strak zwart, glanspixel op (24,6)) / wijkt nergens af.
- snavel: lijkt op Staravia (P5, bevroren) / wijkt nergens af.
- slierten: lijkt op Raichu Gen 1-oren (bevroren r14) / wijkt nergens af.
- wang: lijkt op Picapau (rode vlek, 2 tinten, 1 px los van de snavel) / wijkt nergens af.
- buik: lijkt op Raichu Gen 1 (crème ovaal) en Taillow (sikkel rechtsonder) / wijkt nergens af. Dat hij domineert is een ontwerpkenmerk.
- lijf/flank: lijkt op Pidgeot (schuin lijf, ronde onderkant tot op de poten) / wijkt nergens af.
- nabije vleugel: lijkt op Pidgeot (lichte dekverenband, glans bij de pols, gesloten handpennen) / wijkt alleen af in de rechte buitenrand van de voorrand. Die is bevroren en geen eis; hooguit een variant voor Jordi.
- verre vleugel: lijkt op Pidgeot (achter de kop, twee veertoppen) / wijkt nergens af binnen de bevroren pose.
- stippen: lijkt op Picapau (ronde lichte stippen) / wijkt nergens af.
- poten/klauwen: lijkt op Staraptor/Pidgeot (tenen en klauwen, de verre hoger en donkerder) / wijkt nergens af. Op 1× zijn ze klein, maar ze lezen als klauw.
- steunstaart: lijkt op Picapau (stijve spechtenstaart) / wijkt nergens af.
- staartlus: lijkt op Raichu Gen 1 (dunne zwarte lus) / wijkt nergens af.
- bliksem: lijkt op Raichu Gen 1 (schuine Z) / wijkt nergens af.
- belijning: lijkt op Gen 3 (zwart rechts/onder, gekleurde selout links/boven, geen lichte buitenrand) / wijkt nergens af.
- schaduw/volume: lijkt op Taillow (sikkels die de vorm volgen, contrast ±25-40 per stap) / wijkt nergens af.

Reparaties: geen. Optioneel, alleen als variant voor Jordi en geen eis: een bolle buitenrand van de voorrand rond x30-35, y17-21.

Oordeel: PASS
