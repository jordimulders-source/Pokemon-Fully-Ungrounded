# Hoatzin-lijn (Poison/Dark, 2 fases)

Alle citaten van Jordi (26 nov) staan in `docs/concept/IDEEEN.md` → "Originele Poison-lijn". Samengevat (citaten, niet aanvullen):

- Fase 1: "de hoatzin kuiken, die lelijke"; "heeft al wel een soort snavel"; "klauwtjes ja, zuur nog niet".
- Fase 2: snavelmasker = "de kop ja, want pokemon dragen geen accessoires"; "het oog is gewoon het kijkgat"; "op zijn minst 1 van de vleugels in een soort aanvallende pose".
- Beide: Poison/Dark; poison = "een soort zuur"; "Een beetje de vorm met de kuif"; "Belangrijk is het rode oog"; "misschien ... een blauw stuk gezicht ook in het masker"; "een kuif die goed leest in een gen 3 sprite".
- Zuur: geelgroen ("akkoord met geelgroen"); "gewoon de uiteindes van de veren die vlekken hebben in die kleur" (niet druipen).
- Kleur: "Zwartig is prima" (geen kastanjebruin: "werkte niet"); masker "kan zelfde kleur, maar dat we dat specifiek shaden".
- Lelijk "op een pokemon manier, dat je hem niet vertrouwt".
- Vorige keer mis: te veel tinten, te complex ontwerp, te stocky, buik te dik.
- Postuur en grootte: referentie `referenties/andermans_hoatzirit_postuur.webp` (ander concept, niet namaken; niet als bijlage aan Gemini).

## Prompt fase 2 (v1, Engels)

Eigen toevoegingen van Claude in deze prompt (schrappen bij twijfel): "slender, long S-curved neck, long tail, long legs" (uit de postuurreferentie), "few colors / flat", "not a crow".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects.

POSE (most important): a tall, slender bird standing upright, body turned 3/4 to the left. Exactly two wings: the near wing (right side of the image) is raised and spread wide in an attacking pose, the far wing (left) is folded or half open. Long S-curved neck, long tail, long thin legs. Not stocky, thin belly.

WHAT IT IS: an evolved hoatzin (the Amazon "stinkbird") whose whole head IS a plague doctor's beak mask. The mask is not worn: it is the head itself, the same feathered color as the body but shaded so it reads as a long curved beak mask. The eye is simply the eyehole of the mask: one bright red eye, with a patch of blue bare skin around it inside the mask, like a real hoatzin face. A spiky, messy hoatzin crest on top of the head, large and simple so it reads clearly at sprite size.

TYPE: Poison/Dark. Its poison is acid: the tips of its feathers (wing feathers and tail) have yellow-green acid-colored spots, which it uses to attack. The acid does not drip.

COLORS: blackish body and head (not brown, not chestnut). Few colors, clean simple shading: black-ish feathers, red eye, blue face patch, yellow-green acid feather tips.

MOOD: ugly in a Pokémon way, something you don't trust. Simple, readable design, not complex.

AVOID: clothing, hat, cloak or any accessory; brown or chestnut colors; a fat or round belly; a stocky body; many tones or gradients; dripping liquid; glow; not a crow or raven.
```

## Rondes fase 2
- **r1** (`gemini/fase2_r1.png`, prompt v1). Jordi: "postuur is best ok, maar ik lees hier geen poison uit, het hoofd is niet echt een plague mask en de kuif moeten we misschien een andere kleur geven. Het zijn vlekjes op de vleugel maar het ziet er niet uit alsof dat door zuur/poison komt"
- Keuzes na r1 (Jordi): kop = **1a** (lange rechte kegelsnavel die pas aan het eind omlaag buigt, zoals het echte masker); zuur = **3c** (geelgroen loopt als verloop van de veerpunten naar binnen, alsof het erin trekt); kuifkleur: "twijfel ik over, wat er mooi uit zou zijn". Voorstel Claude: kuif zwartig met dezelfde geelgroene punten als de veren (geen extra kleurgroep, kuif leest tegen wit).

## Prompt fase 2 (v2, Engels; nieuw gesprek, zonder bijlage)
Eigen toevoegingen Claude: kuif met zuurpunten (voorstel, Jordi twijfelde), "slender, long S-curved neck, long tail, long legs", "not a crow or raven".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects.

POSE (most important): a tall, slender bird standing upright, body turned 3/4 to the left. Exactly two wings: the near wing (right side of the image) is raised and spread wide in an attacking pose, the far wing (left) is folded or half open. Long S-curved neck, long tail, long thin legs. Not stocky, thin belly.

WHAT IT IS: an evolved hoatzin (the Amazon "stinkbird") whose whole head IS a plague doctor's beak mask. The mask is not worn: it is the head itself, the same blackish color as the body but shaded so it clearly reads as a plague doctor mask. The beak is long, straight and cone-shaped, and only bends downward at the very end, exactly like a real plague doctor mask (not a normal curved bird beak). The eye is simply the eyehole of the mask: one bright red eye, with a patch of blue bare skin around it, like a real hoatzin face. A spiky, messy hoatzin crest on top of the head, large and simple so it reads clearly at sprite size.

TYPE: Poison/Dark. Its poison is acid. The tips of its wing feathers, tail feathers and crest feathers are soaked in yellow-green acid: the color seeps from the tip inward into each feather as a gradient, as if the acid is soaking into it. No dots or spots, no dripping.

COLORS: blackish body and head (not brown, not chestnut). Few colors, clean simple shading: blackish feathers, red eye, blue face patch, yellow-green acid seeping into the feather tips.

MOOD: ugly in a Pokémon way, something you don't trust. Simple, readable design, not complex.

AVOID: clothing, hat, cloak or any accessory; brown or chestnut colors; a fat or round belly; a stocky body; polka dots or round spots; dripping liquid; glow; a normal curved bird beak; not a crow or raven.
```
- **r2** (`gemini/fase2_r2.png`, prompt v2). Jordi: "beter maar hij heeft nu geen poten meer, ik vind het ook nog net niet genoeg plague mask, de kroon mag wat meer gekleurd nog, de vleugels ook en misschien nog iets van een patroon op de buik, maar we zijn nu al verder dan we ooit warne". Volgende stap: bijsturen in hetzelfde gesprek, max. 2 wijzigingen per keer (GEMINI.md): eerst poten + meer zuurkleur op kroon/vleugels.
- **r3** (`gemini/fase2_r3.png`, bijsturen: poten + meer zuur). Jordi: "amper beter." Masker: "zit hem vooral in de vorm, hij is nog te scherp, het is echt een snavel doordat er een aansluitingslijn zit en dat moet niet". Buik: "eens wat betreft geelgroen, qua patroon op de buik misschien het radioactiviteit teken, weet niet of dat past". Volgende: nieuwe startprompt v3 in een nieuw gesprek (bijsturen werkt niet); buikpatroon eerst overleggen.

## Prompt fase 2 (v3, Engels; nieuw gesprek, zonder bijlage)
Eigen toevoegingen Claude: "rounded, blunt tip", "one smooth continuous shape", "the whole bird fits inside a square canvas with margin", kuif met zuurpunten, "not a crow or raven".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects. The whole creature, including both feet, fits inside a square canvas with white margin on all sides; nothing is cut off.

POSE (most important): a tall, slender bird standing upright on two long thin legs with clearly visible clawed feet, body turned 3/4 to the left. Exactly two wings: the near wing (right side of the image) is raised and spread wide in an attacking pose, the far wing (left) is half open. Long S-curved neck, long tail. Not stocky, thin belly.

HEAD (important): the head IS a plague doctor's mask, not a bird head with a beak. Head and beak are ONE smooth continuous shape with no line, seam or joint between them: the forehead flows straight into the long beak, like a stitched leather plague doctor mask. The beak is long, cone-shaped and soft in outline, with a rounded, blunt tip that bends slightly downward. Not sharp, not hooked, no separate bill. Same blackish color as the body, shaded smoothly like the mask. The eye is the eyehole of the mask: one bright red eye with a patch of blue bare skin around it, like a real hoatzin face. A spiky, messy hoatzin crest on top of the head, large and simple so it reads clearly at sprite size.

WHAT IT IS: an evolved hoatzin (the Amazon "stinkbird"). TYPE: Poison/Dark. Its poison is acid: about half of every wing feather, tail feather and crest feather is soaked in yellow-green acid, seeping from the tip inward as a gradient. No dots or spots, no dripping.

COLORS: blackish body and head (not brown, not chestnut). Few colors, clean simple shading: blackish feathers, red eye, blue face patch, yellow-green acid.

MOOD: ugly in a Pokémon way, something you don't trust. Simple, readable design, not complex.

AVOID: clothing, hat, cloak or any accessory; a seam or line where a beak meets a head; a sharp or hooked beak; brown or chestnut; a fat or round belly; a stocky body; polka dots; dripping liquid; glow; cut-off legs; not a crow or raven.
```
- **r4** (`gemini/fase2_r4.png`, prompt v3, nieuw gesprek). Jordi: "hij doet vrijwel niks anders, behalve dat we poten hebben, het teken op de buik hebben we nog niet en verder ook niks veranderd" + "behalve dat het gezicht nu wat beter klopt". Voorstel Claude (kop apart maken) afgewezen: Jordi "nee het hoofd is juist prima". Jordi daarna: "de rest moet beter". r4-hoofd = basis; buikteken: Jordi "waar is het radioactiviteits teken?" (Claude had het bewust uit v3 gelaten en a/b voorgelegd; nu radioactief, geelgroen).
- Buikteken = dit teken (Jordi: "deze"): `referenties/radioactief_teken.png` (zwart klaverblad met middenstip op een ronde schijf met zwarte rand); schijf in geelgroen (Jordi eerder: "eens wat betreft geelgroen").
- **r5** (`gemini/fase2_r5.png`, bijsturen r4 + teken als bijlage): teken klein op de dij geplakt, rest gelijk. Jordi: "manmanman" + "alleen die zwarte stukken hoeven erop" (dus geen schijf/rand, alleen de drie bladen en de stip).

## Prompt fase 2 (v4, Engels; nieuw gesprek, from scratch op Jordi's verzoek)
= v3 + buikteken (alleen de drie bladen + stip, zonder schijf/rand). Eigen toevoegingen Claude: teken in geelgroen (zwart valt weg op het zwarte lijf), "large, centered on the belly".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects. The whole creature, including both feet, fits inside a square canvas with white margin on all sides; nothing is cut off.

POSE (most important): a tall, slender bird standing upright on two long thin legs with clearly visible clawed feet, body turned 3/4 to the left. Exactly two wings: the near wing (right side of the image) is raised and spread wide in an attacking pose, the far wing (left) is half open. Long S-curved neck, long tail. Not stocky, thin belly.

HEAD (important): the head IS a plague doctor's mask, not a bird head with a beak. Head and beak are ONE smooth continuous shape with no line, seam or joint between them: the forehead flows straight into the long beak, like a stitched leather plague doctor mask. The beak is long, cone-shaped and soft in outline, with a rounded, blunt tip that bends slightly downward. Not sharp, not hooked, no separate bill. Same blackish color as the body, shaded smoothly like the mask. The eye is the eyehole of the mask: one bright red eye with a patch of blue bare skin around it, like a real hoatzin face. A spiky, messy hoatzin crest on top of the head, large and simple so it reads clearly at sprite size.

BELLY MARKING: a radiation trefoil grows as a natural feather marking on its belly: only the three blades and the center dot, in yellow-green, directly on the black feathers. No circle, no disc, no outline ring around it, not a sticker or badge. Large, centered on the belly.

WHAT IT IS: an evolved hoatzin (the Amazon "stinkbird"). TYPE: Poison/Dark. Its poison is acid: about half of every wing feather, tail feather and crest feather is soaked in yellow-green acid, seeping from the tip inward as a gradient. No dots or spots, no dripping.

COLORS: blackish body and head (not brown, not chestnut). Few colors, clean simple shading: blackish feathers, red eye, blue face patch, yellow-green acid and belly marking.

MOOD: ugly in a Pokémon way, something you don't trust. Simple, readable design, not complex.

AVOID: clothing, hat, cloak or any accessory; a seam or line where a beak meets a head; a sharp or hooked beak; brown or chestnut; a fat or round belly; a stocky body; polka dots; dripping liquid; glow; cut-off legs; a round badge or sticker; not a crow or raven.
```
- **r6** (`gemini/fase2_r6.png`, prompt v4). Jordi: "de vleugels zijn nu beter, het patroon prima alleen staat niet goed in perspectief, hoofd is nu een stuk minder". Voorstel Claude: model combineren (r6 lijf/vleugels + r4 hoofd, teken in perspectief zetten) in plaats van verder prompten.

## Model (combinatie, 26 nov; Jordi "akkoord")
- r6 (lijf, vleugels, staart, poten, teken) + r4-hoofd (incl. kuif met zuurpunten), naad bij de nek. Hoofdmaten: `model/comb_s1.0|1.1|1.2.png` (`comb_vel.png`), canvas 120 px hoger zodat de kuif past.
- Teken in perspectief (op s1.1): oud teken weggepoetst en opnieuw gezet, A smal 75 %, B 75 % + 15° links, C 75 % + 15° rechts, D 60 % (`model/teken_*.png`, `teken_vel.png`; `gereedschap/teken.py`). Jordi: "het radioactiviteits teken ga je in een ander perspectief dus niet helemaal zien, dat is niet erg, het is toch herkenbaar".
- Jordi: "het valt deels weg door de driekwart pose". Varianten E/F/G: teken naar de buikrand geschoven en door de omlijning afgesneden (E 20 px, F 35 px, G 35 px + linkerhelft samengedrukt als om een ronding); `teken_vel2.png`, `gereedschap/teken2.py`. Wegpoetsen nu met gladde invulling (A–D opnieuw gemaakt).
- Jordi: "B is het beste, maar stel hij draait zich naar ons toe, zou het teken dan midden op zijn buik staan?" Claude: nee, in driekwart naar links ligt het echte midden van de buik dichter bij de voorrand; B staat midden in het zichtbare deel. Varianten H/I = B 12/22 px naar de buikrand (`teken_vel3.png`, `gereedschap/teken3.py`).
- Jordi: "ga anders maar gewoon bouwen, dan fixen we dat in de sprite wel" / "want dat vertaalt ook weer anders". **Model = `model/model.png`** (= hoofdmaat 1,1 + teken B, Jordi's "B is het beste"); plek van het teken (midden op de buik, deels weg in driekwart) en hoofdmaat zo nodig in de sprite.

## Sprite fase 2
Opdracht: `sprite/OPDRACHT.md`.
- **r1** (`sprite/r1/`, maker): kale reductie + 371 px opschoning; Claude: te grijs/vlak t.o.v. het bijna zwarte model, veerlijnen in de vleugels weg; reparaties naar r2.
- **r2** (`sprite/r2/`): donkerder toonverdeling naar het model, veerlijnen uit het model, snavelrug. Naar de keurder.
- **r3** (`sprite/r3/`): 6 keurderpunten; Claude: oog nu te groot (7×7 met zwarte ring) en leest als blauw met een rode U.
- **r4** (`sprite/r4/`): oog terug op modelmaat (diff 0 buiten het oogvak). Naar de DC-eindkeuring.
- **r5** (`sprite/r5/`): DC-eindkeuring (133 px belijning: selout aan de lichtkant, hue shift in 6 tinten; alpha-diff 0). Ter info van de keurder: lijf donkerder dan Murkrow (meer volume = lichter), nabije vleugel vlak zoals het model, oog één roodtint. Naar Jordi.
