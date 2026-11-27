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
- Jordi op r5: "de vorm van de plague mask snavel is verloren gegaan, de kuif mag het gifgroen wat verder gekleurd, zit het radioactieve teken nu goed?" Teken: staat als model B (midden van het zichtbare buikdeel, niet het echte midden); variant naar de buikrand voorgelegd.
- **r6** (`sprite/r6/`): snavel opnieuw uit het model (lichte kegel tegen donkere kop, ±5 px aan de basis, afhangende punt; dikker kan alleen door af te wijken van het model), kuifvarianten K1 volledig, K2 ⅓, K3 ½ (= r6), K4 ⅔ (`vel_kuif.png`); teken-variant in `hoatzin_r6_variant_teken.png`.
- Jordi op r6: "K1, snavel r6, maar de afwerking mag iets beter, onderkant is een horizontaal streepje. Het teken tussen de 2 voorbeeldne in". Naar r7.
- **r7** (`sprite/r7/`): K1 + snavelpunt rond afgesloten (onderste rij van de punt 2 px i.p.v. 4) + teken halverwege (−1,+1). Rechte lijn onder de kaak (y20, x14–20) staat er nog: het model is daar zelf recht.
- Jordi op r7: "poh uitstekend, eindelijk, toch de hoatzin gelukt. Linkerpoot moet je nog even naar kijken, de klauw is een beetje een rechthoek geworden". Naar r8 (alleen de linkervoet).
- **r8** (`sprite/r8/`): linkervoet met twee losse tenen uit het model (13 px, diff 0 erbuiten).
- **r9** (`sprite/r9/`): DC-eindkeuring op r8, 4 px (linkervoet 2, kuif 1, teken 1), alpha-diff 0. Naar Jordi.
- Jordi op r9: "het kleurgebruik, schaduw, tinten zijn nog niet top. Snavel is effen, kop die in de kuif overgaat lijkt gewoon bijna een vierkant vlak. Hij leest erg 2d, kan je dat nog fixen, kijk ook of die niet te donker is". Kleurronde r10 (verse maker).
- **r10** (`sprite/r10/`, verse maker): A (r9-donkerte) en B (Murkrow-bereik) met volume. Claude: vleugels kussenvlakken, snavel schuine banden; reparaties naar r11.
- **r11** (`sprite/r11/`): kussens weg (lichte randen per veergroep), snavel één rugstrook, kop lichte sikkel. Naar keurder.
- **r12** (`sprite/r12/`): B-lijn met keurderpunten (tintverdeling 31/39/26/4 %, blauwgrijs, achterhoofd rond, kuifnaad gebroken, één borstbolling, schouderhooglicht). Naar Jordi.
- **r13** (`sprite/r13/`): DC-eindkeuring op r12, 14 px (4 zwarte binnenlijnen → eigen tint, veerlijnen en voorrand in de opgeheven vleugel uit het model, borsthooglicht als druppel), alpha-diff 0. Naar Jordi.

## Fase 1 (kuiken), overleg 27 nov
- Inspiratie (Jordi): `referenties/kuiken_1_ai_uncanny.webp`, `kuiken_2_klauwtjes.png`, `kuiken_3_klimmend.webp`, `kuiken_4_tak.png`. Jordi: "Dit is de inspiratie. fotos als inspiratie maar dan iets meer uncanny, iets meer cryptid. Die eerste foto is namelijk een beetje AI geedit en die kant moeten we op".
- Antwoorden Jordi (27 nov): "geen plague doctor erin nee, hij is vooral zwart met wat gelige tinten"; "geen voorwerp" (geen tak).
- Pose (Jordi, 27 nov): "hij moet een beetje onhandig erbij staan".
- Pose (Jordi): "hij staat maar in een zodanige pose dat je de dunne gek uitziende poten en klauwtjes kan zien".
- Gelige tinten: "alleen in het dons". Snavel: kromme grijze snavel van foto 1 ("2 ja"). Oog: niet rood/blauw, "grijze ring" (foto 1). "nee, geen teken".
- Grootte: 700–900 px (voorstel Claude), Jordi: "grootte ok".
- Kuif: geen (Jordi: "geen kuif zoals ik al zei").
- **r1** (`gemini/fase1_r1.png`, prompt v1 met eigen toevoegingen van Claude: damp/scruffy down, pin feathers, half-spread wings). Jordi: "Dit ontwerp kunnen we niks mee, het is een slordige normale vogel, het uncanny zit niet in de vacht maar in de poot lengte, kijk goed naar deze. Hij hoort ook geen of bijna geen vleugel te hebben". Referentie: `referenties/kuiken_5_pootlengte.png`.
- **r2** (`gemini/fase1_r2.png`, prompt v2, nieuw gesprek: lange poten, geen vleugels, geen kuif). Jordi: "ietsje beter maar nu heeft die helemaal geen armen meer, zo moeten de armen eruit zien, soort vleugels zonder veren" (`referenties/kuiken_6_arm.png`).
  Jordi ook: "en hij is te blij".
- **r3** (`gemini/fase1_r3.png`, bijsturen r2: armen als kale vleugels met stekelrij + minder blij). Jordi: "ok maar het is nog geen vleugels zonder veren, dit zijn klauwen".
- **r4** (`gemini/fase1_r4.png`, bijsturen r3: armen als geplukte vleugel). Jordi: "vertaalt dit naar een sprite?". Kale verkleiningstest in `fase1_maat/` (`maten.py`, `maten_vel.png`): Gemini-raster 10,24 px (100×100), figuur natief 70×77 (2268 px); h56 1260 px, h50 1011 px, h44 787 px.
  Jordi: "dan moeten we bijsturen he" → bijsturen r4: stekels minder/dikker + nabije vleugel leesbaar als vleugel (voorstel Claude).
- **r5** (`gemini/fase1_r5.png`, bijsturen r4 met Claudes voorstel: 4–5 dikke stekels + nabije vleugel als driehoek). Jordi: "nee dit is niet langer wat ik bedoelde". Grote grijze vleugel bedekt nu het lijf, stekels als een stekelvarken.
  Jordi ook: "nu zijn de armen bijna messen".
  Jordi: "en de haren achterop zijn uberhaupt niet nodig" (stekels op de rug weg).

## Prompt fase 1 (v3, Engels; nieuw gesprek, zonder bijlage; Jordi: "nieuwe prompt he, goed gedetailleerd")
Eigen toevoegingen Claude (schrappen bij twijfel): "longer than the body and head together", "knees", "short black down", vleugel "folded at elbow and wrist, plucked chicken wing, soft and fleshy", klauwtjes aan de voorrand bij de pols, "small pupil", "beak closed".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

WHAT IT IS (most important): an uncanny, cryptid-like hoatzin chick (the chick of the Amazon "stinkbird"). It is NOT a normal bird. What makes it uncanny is its legs: they are far too long for its small body, longer than the body and head together. The legs are bare, thin and grey, with knobbly knees and big grasping clawed toes, like a real hoatzin chick's legs.

POSE: it stands a bit awkwardly and clumsily on those too-long legs, body turned 3/4 to the left. The pose clearly shows its thin, strange-looking legs and its little claws.

ARMS: it has two featherless wings that look like thin arms: bare grey skin over bone, folded at the elbow and wrist, like a plucked chicken wing, soft and fleshy. Each wing has two small claws on its front edge near the wrist bend. The wings hang down awkwardly from the shoulders. They are not hands, not blades, not sharp.

BODY: a small, hunched body covered in short, smooth black down, with some yellowish tints only in the down. The back and wings are smooth: no spines, no spikes, no quills, no feather shafts, no hair sticking out.

HEAD: a small round head with no crest. A hooked grey beak like a real hoatzin chick, closed. A dark round eye with a grey ring around it and a small pupil. The expression is not happy: a cold, blank stare, unsettling.

COLORS: mostly black, some yellowish tints only in the down, grey beak, wings, legs and claws. Few colors, clean simple shading.

MOOD: ugly in a Pokémon way, uncanny, a cryptid, something you don't trust. Simple, readable design, not complex.

AVOID: feathered wings; hands or fingers; blade-like or knife-like wings; spines, spikes, quills or hair on the back or wings; a crest; messy or scruffy feathers; a normal bird; a happy or cute face; a smile; a branch or any object; a mask; a red eye; brown or chestnut; a fat or round belly; a symbol or marking; glow.
```
- **r6** (`gemini/fase1_r6.png`, prompt v3). Jordi: "te blij en de vleugels kloppen nog steeds niet met wat ik bedoel". NB: Claude had "haren achterop" (rug) in v3 ook doorgetrokken naar de vleugels ("no feather shafts" op de vleugels); dat zei Jordi niet.
- Vleugel (Jordi, bij `referenties/kuiken_7_vleugel_kam.png`): "zonder dit erin is het design gefaald". = de waaier van lange donkere kale veerschachten (pennen in de schede, zonder vlag) aan de kale arm.
- Te blij (Jordi): "misschien die enorme glimlach?" (de snavellijn die naar het oog omhoog krult).
- **r7** (`gemini/fase1_r7.png`, bijsturen r6: kam-vleugels + glimlach weg). Jordi: "nee, niet wat ik bedoel". Pennen werden dunne lijntjes op de rug, glimlach bleef.
- Plan (Claude, Jordi: "doe maar"): eerst alleen de vleugel in een nieuw gesprek (bijlage `kuiken_7_vleugel_kam.png`), daarna plakken op het beste lijf (r2/r4/r6, Jordi kiest) met een kop zonder glimlach (voorstel r4).

## Prompt fase 1 vleugel (w1, Engels; nieuw gesprek, bijlage = foto kuiken_7)
Eigen toevoegingen Claude: "8 to 10 pin feathers", "seen from the side", "slightly lighter tips" niet opgenomen (open).

```
Pixel art in the style of an official Gen 3 Pokémon front sprite (Ruby/Sapphire/Emerald): draw ONLY one wing of a newly hatched hoatzin chick, as in the attached photo. White background, no body, no head, no ground, no shadow, no effects, max 16 colors.

The wing is a bare, thin arm with dark grey skin and no feathers on it, bent at the elbow and wrist, with one or two small claws on its front edge. From its back edge grows a fan of 8 to 10 long, thin pin feathers: dark bare shafts still in their sheaths, with no vanes at all. They stand clearly apart from each other with gaps between them and spread out like the teeth of a comb or a small hand fan, exactly like in the photo. Seen from the side, the fan fully spread so every pin feather is visible.

Size: as large as it would be on a 64x64 sprite of a small chick (about 20 pixels long), with clear dark outlines so every pin feather reads at that size.

AVOID: normal feathers with vanes, a hand or fingers, hair, fur, a body, any object or branch.
```
- **w1** (`gemini/fase1_vleugel_w1a.png`, `w1b.png`, vleugelprompt). Jordi: "ok heel leuk en aardig, maar wat ga je met 1 vleugel nu doen, verkeerd copy pasten?"

## Prompt fase 1 (v4, Engels; nieuw gesprek, Jordi voegt een bronfoto toe; Jordi: "doe gewoon een gehele prompt voor de pokemon")
Eigen toevoegingen Claude: zie v3, plus "far wing partly hidden behind the body".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

WHAT IT IS (most important): an uncanny, cryptid-like hoatzin chick (the chick of the Amazon "stinkbird"). It is NOT a normal bird. What makes it uncanny is its legs: they are far too long for its small body, longer than the body and head together. The legs are bare, thin and grey, with knobbly knees and big grasping clawed toes, like a real hoatzin chick's legs.

POSE: it stands a bit awkwardly and clumsily on those too-long legs, body turned 3/4 to the left. The pose clearly shows its thin, strange-looking legs, its little claws and its wings.

WINGS (very important, see the attached image): it has no normal wings. Each wing is a bare, thin grey arm, bent at the elbow and wrist, with one or two small claws on its front edge. From the back edge of each arm grows a fan of long, thin, dark pin feathers: bare shafts still in their sheaths, with no vanes at all. They stand clearly apart from each other and spread out like the teeth of a comb or a small hand fan. The near wing (right side of the image) is held out from the body with its fan fully spread and clearly visible; the far wing (left side) is partly hidden behind the body, with only part of its fan visible.

BODY: a small, hunched body covered in short, smooth black down, with some yellowish tints only in the down. No spines, hair or quills on the back.

HEAD: a small round head with no crest. A hooked grey beak like a real hoatzin chick, closed. The line between the upper and lower beak runs straight or slightly down and does NOT curve up toward the eye: no smile. A dark round eye with a grey ring around it. The expression is a cold, blank, unsettling stare, not happy.

COLORS: mostly black, some yellowish tints only in the down, grey beak, arms, legs and claws, dark pin feathers. Few colors, clean simple shading.

MOOD: ugly in a Pokémon way, uncanny, a cryptid, something you don't trust. Simple, readable design, not complex.

AVOID: feathered wings with vanes; hands or fingers; blade-like wings; spines, hair or quills on the back; a crest; messy or scruffy feathers; a normal bird; a smile, a grin or a happy or cute face; a branch or any object; a mask; a red eye; brown or chestnut; a fat or round belly; a symbol or marking; glow.
```
- Jordi over de losse vleugel w1: "hij snapt dit dus wel". Daarom v4 met bronfoto.
- **r8** (`gemini/fase1_r8.png`, prompt v4 + bronfoto). Jordi: "nee fout". Waaier los op de rug, armen als stokjes met handen: Gemini haalt arm en waaier uit elkaar.
- **r9** (`gemini/fase1_r9.png`, nieuw gesprek, w1a als bijlage + lijf eromheen). Jordi: "arm kuiken met maar 1 vleugel". Vleugel zit nu wel vast aan de schouder, maar poten weer kort en achterste vleugel weg.
- **r10** (`gemini/fase1_r10.png`, bijsturen r9: lange poten + achterste vleugel). Jordi: "de vorm klopt niet vgm".
  Jordi: "linkervleugel klopt toch niet, dat zie je toch" (achterste vleugel steekt als klauw voor de borst uit).
- **r11** (`gemini/fase1_r11.png`, bijsturen r10: linkervleugel achter het lijf). Jordi: "is ook niet wat ik bedoel".
- Jordi bij `referenties/kuiken_5_pootlengte.png`: "kijk die foto dan / dat is toch anders" (over de vleugels).
- Vleugels volgens foto 3 en 5 (Claude, na Jordi "kijk die foto dan"): lange kale arm, pennen als franje langs de achterrand die naar achteren/beneden wijst (geen waaier omhoog); voorste vleugel langs het lijf, achterste achter de rug omhoog.
- **r12** (`gemini/fase1_r12.png`, bijsturen r11 met die beschrijving). Jordi: "nieuwe prompt from scratch, gaat weer fout". Voorste vleugel werd een losse derde "poot".

## Prompt fase 1 (v5, Engels; nieuw gesprek from scratch, bijlage: foto 3 `kuiken_3_klimmend.webp`)
Eigen toevoegingen Claude: zie v3; vleugelbeschrijving naar foto 3/5; "lies flat against the side of the body", "not a third leg".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

WHAT IT IS (most important): an uncanny, cryptid-like hoatzin chick (the chick of the Amazon "stinkbird"), based on the attached photo. It is NOT a normal bird. What makes it uncanny is its legs: they are far too long for its small body, longer than the body and head together, bare, thin and grey, with big grasping clawed toes.

POSE: it stands a bit awkwardly and clumsily on those too-long legs, body turned 3/4 to the left, so the thin, strange-looking legs, the claws and the wings are clearly visible.

WINGS (very important, exactly like the wings in the attached photo): no normal feathers. Each wing is a bare, dark grey arm, folded at the elbow. Along the whole back edge of the arm grows a fringe of thin, dark pin feathers (bare shafts without vanes), close together like the teeth of a comb, all pointing backward and downward and following the line of the arm. They do NOT stand up like a fan, a crest or a mohawk.
- Near wing (right side of the image): folded and lying flat against the side of the body, its fringe hanging down over the lower body. It is part of the body's silhouette, not a separate limb, not a third leg.
- Far wing (left side of the image): raised up behind the back, only the bent arm and part of its fringe visible above the body.

BODY: a small, hunched body covered in short, smooth black down, with some yellowish tints only in the down. No spines or hair on the back.

HEAD: a small round head with no crest. A hooked grey beak like a real hoatzin chick, closed, with no smile: the line between the upper and lower beak does not curve up. A dark round eye with a grey ring around it, a cold blank stare.

COLORS: mostly black, some yellowish tints only in the down, grey beak, arms, legs and claws, dark pin feathers. Few colors, clean simple shading.

MOOD: ugly in a Pokémon way, uncanny, a cryptid, something you don't trust. Simple, readable design, not complex.

AVOID: feathered wings with vanes; pin feathers standing up like a fan or crest; a wing that looks like a third leg; hands or fingers; a crest; messy or scruffy feathers; a normal bird; a smile or a cute face; a branch or any object; a mask; a red eye; brown or chestnut; a fat or round belly; glow.
```
- **r13** (`gemini/fase1_r13.png`, prompt v5 + foto 3). Jordi: "deze is naast chernobyl geboren".
  Jordi: "nee dat bedoel ik sarcastisch omdat die er niet uit ziet".
- Jordi (beschrijving vleugels in eigen woorden): "vleugel zonder veren".

## Prompt fase 1 (v6, Engels; nieuw gesprek; vleugels letterlijk "wings without feathers", geen eigen vleugelbeschrijving van Claude meer)
```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

WHAT IT IS: an uncanny, cryptid-like hoatzin chick. Its legs are far too long for its body: thin, bare and grey, with claws. Its wings are wings without feathers, with small claws.

POSE: it stands a bit awkwardly, body turned 3/4 to the left, in a pose that shows its thin, strange-looking legs and its claws.

HEAD: no crest. A hooked grey beak, no smile. A dark eye with a grey ring around it. Not happy.

COLORS: mostly black, with some yellowish tints only in the down.

MOOD: ugly in a Pokémon way, something you don't trust.

AVOID: feathers on the wings; a crest; a smile; a branch or any object; a mask; a red eye; a normal bird.
```
  Jordi: "dat is het enige waar ik nog om vraag" / "al 4x gedaan" → alleen bijsturen op r13: vleugels zonder veren. (v6 hierboven vervalt.)
  Jordi: "als je de veren van een normale vogel plukt dan krijg je hetzelfde".
- **r14** (`gemini/fase1_r14.png`, bijsturen r13: "wings without feathers, like a plucked bird"). Jordi: "haha ja dat begreep gemini goed" (vleugels werden gladde vleermuisachtige platen).
- Kipvleugel-voorstel (Claude) afgewezen. Jordi: "nee / dat is niet zo" / "dat is een hele andere vorm".
- Referentie geplukte vleugel (Jordi): `referenties/kuiken_8_geplukte_vleugel_anatomie.webp` (anatomische schets).
  Jordi: "nee dit is een vleugel zonder veren" (Claudes lezing met schachten afgewezen). Bijsturen r13 met schets als bijlage, tekst alleen Jordi's woorden.
  Jordi: "de bovenste" / "dat bedoel ik" → bijlage `referenties/kuiken_8_bovenste_vleugel.png` (bijgesneden).

## Prompt fase 1 (v7, Engels; nieuw gesprek, bijlage `referenties/kuiken_8_bovenste_vleugel.png`; Jordi: "nieuwe prompt graag, gemini kan toch niet telkens editen")
Alleen Jordi's besluiten; geen eigen vleugelbeschrijving van Claude.

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

WHAT IT IS (most important): an uncanny, cryptid-like hoatzin chick. It is not a normal bird. What makes it uncanny is its legs: they are far too long for its small body, thin, bare and grey, with claws.

WINGS (very important): wings without feathers, exactly like the wing in the attached drawing. Each wing has small claws.

POSE: it stands a bit awkwardly, body turned 3/4 to the left, in a pose that shows its thin, strange-looking legs and its claws.

BODY: small, mostly black down with some yellowish tints only in the down.

HEAD: no crest. A hooked grey beak like a hoatzin chick, with no smile. A dark eye with a grey ring around it. Not happy.

MOOD: ugly in a Pokémon way, uncanny, a cryptid, something you don't trust. Simple, readable design, not complex.

AVOID: feathers on the wings; a crest; a smile or a cute face; a branch or any object; a mask; a red eye; brown or chestnut; a normal bird; glow.
```
- **r15** (`gemini/fase1_r15.png`, prompt v7 + bovenste vleugel). Jordi: "goede prompt weer" (sarcastisch; vleugels werden beige vleermuisvliezen met klauwen aan de punten, poten korter).
- Na r15: Jordi "ik ga wel krabbelen want dit is belachelijk". Volgende stap: Jordi's krabbel over r13 → Claude bouwt het model pixel voor pixel naar de krabbel (GEMINI.md: krabbel uitvoeren = kleuren meten).
- Jordi: "haal hier de handen weg" / "en de haren" / "op de rug en okselhaar links" (op r7). Krabbelbasis: `krabbelbasis/krabbelbasis_r7.png` (10×, natief `basis_natief.png`, `weghalen.py`; alleen weggehaald, gat dicht met lijfkleur + omlijning).
  Jordi op krabbelbasis_r7: "dat bedoelde ik niet" / "maar goed" / "wacht maar".
- **Krabbel Jordi** (`krabbelbasis/krabbel_jordi.png`, over r7): "zoiets bedoel ik" / "heel lelijk getekend want ik kan niet tekenen" / "daarom gebruik ik ai". Hand aan het eind van elke arm zwart overgetekend (langwerpige donkere vorm), met losse lange dunne lijnen die eruit naar achteren/beneden steken; kale grijze arm blijft.

## Prompt fase 1 (v8, Engels; nieuw gesprek, bijlage = Jordi's krabbel)
Eigen toevoegingen Claude: de lezing van de krabbel ("dark, elongated", "a few long, thin, bare shafts", "pointing backward and down"), "ignore the spikes on the back".

```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

The attached image is a rough hand-drawn sketch over an earlier version. Use it for the body, head, legs and pose, and above all for the WINGS: the black shapes and thin black lines were drawn by hand to show what the wings must look like. Redraw everything cleanly as a real Gen 3 sprite.

WINGS (most important, as in the sketch): wings without feathers. A thin bare grey arm; at the end, instead of a hand, a dark, elongated part of the wing, with a few long, thin, bare shafts sticking out of it, pointing backward and down. No hands, no fingers, no claws at the end.

WHAT IT IS: an uncanny, cryptid-like hoatzin chick. Its legs are far too long for its small body: thin, bare and grey, with claws. It stands a bit awkwardly, body turned 3/4 to the left.

BODY: small, mostly black down with some yellowish tints only in the down. Ignore the spikes on the back in the sketch: no spikes or hair on the back.

HEAD: no crest. A hooked grey beak, no smile. A dark eye with a grey ring around it. Not happy.

MOOD: ugly in a Pokémon way, uncanny, a cryptid, something you don't trust. Simple, readable design.

AVOID: hands or fingers; feathers with vanes; spikes or hair on the back; a crest; a smile or a cute face; a branch or any object; a red eye; a normal bird.
```
- **r16** (`gemini/fase1_r16.png`, prompt v8 + krabbel). Jordi: "zucht". Gemini plakte de krabbel letterlijk over r7 (gladde zwarte vlekken + vectorlijnen), niets hertekend.
  Jordi: "het moet niet letterlijk overgetekend worden".

## Prompt fase 1 (v9 = v8 met "idee, niet overtrekken"; nieuw gesprek, bijlage = krabbel)
```
Design an original Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, white background, no ground, no shadow, no effects, no objects. The whole creature fits inside the canvas with white margin on all sides; nothing is cut off.

The attached image is only a very rough idea sketch by someone who cannot draw. Do NOT copy, trace or paste anything from it. Only take the idea of the wings from it, and design the whole Pokémon yourself as a polished, real Gen 3 sprite with pixel outlines and Gen 3 shading everywhere.

WINGS (most important, the idea from the sketch): wings without feathers. A thin bare grey arm; at its end, instead of a hand, a dark, elongated, bare-skinned part of the wing, with a few long, thin, bare shafts sticking out of it, pointing backward and down. Drawn in pixels like the rest of the sprite. No hands, no fingers.

WHAT IT IS: an uncanny, cryptid-like hoatzin chick. Its legs are far too long for its small body: thin, bare and grey, with claws. It stands a bit awkwardly, body turned 3/4 to the left.

BODY: small, mostly black down with some yellowish tints only in the down. No spikes or hair on the back.

HEAD: no crest. A hooked grey beak, no smile. A dark eye with a grey ring around it. Not happy.

MOOD: ugly in a Pokémon way, uncanny, a cryptid, something you don't trust. Simple, readable design.

AVOID: copying or tracing the sketch; smooth vector shapes; hands or fingers; feathers with vanes; spikes or hair on the back; a crest; a smile or a cute face; a branch or any object; a red eye; a normal bird.
```
- **r17** (`gemini/fase1_r17.png`, prompt v9 + krabbel). Jordi: "weer niet".
- Jordi koos **r4** als model: "ga maar deze bouwen" (`model/fase1_model.png`). Makeropdracht `sprite_fase1/OPDRACHT.md` (44 px hoog).
  Jordi: "haren op de rug weg, en de haren rondom de vleugels haal je ook weg en vervang je door haren die beter passen bij een sprite" (aan de maker doorgegeven).
  Jordi (omcirkeld op r4, `sprite_fase1/jordi_omcirkeld.png`): "ik weet niet wat dit is wat ik omcirkeld heb, dus dat mag weg" (donkere wig in de nabije vleugel; donker strookje tussen poot en vleugel onder het lijf).
  Jordi: "gewoon de poot doortrekken en onder de vleugel is het lichaam" (wig = lijf, strookje = poot doorgetrokken).

## Sprite fase 1
- Jordi: "werk maar naar een hele goede eindfase toe want ik ga slapen".
- **r1** (`sprite_fase1/r1/`, maker): kale reductie 40×44 (735 px) + Jordi's wijzigingen op het natieve raster; oog 4×4; haren A (6×2 px) en B (7×3 px). Claude: vleugels gespikkeld (losse zwarte resten), lijf vlak, tenen onderbroken, onderkant rechts (poot/vleugel/staart) één grijze massa. Naar r2.
- **r2** (`sprite_fase1/r2/`): lijnronde (zwart 41→32 %), tenen, lijf 3 tinten + geelplukjes, haren B onregelmatig. Claude: veel schoner; rechtsonder (onderarm/dij/staart) nog vloeiend. Naar de keurder.
- Keurder op r2: FAIL (trouw = in orde; Gen 3: zwart 32 %, haren lezen als vuil, buikrand schaakbord, binnenlijnen zwart, staart/dij ruis, snavel vlak, verre voet balk). 8 punten naar r3.
- **r3** (`sprite_fase1/r3/`): 8 keurderpunten (zwart 32→28 %), haren vast aan de buitenlijn (A 3/vleugel, B 4/vleugel). Claude: duidelijk beter, staart/dij lezen. Naar DC-eindkeuring (r4).
- **r4** (`sprite_fase1/r4/`, DC-eindkeuring op r3: PASS): 63 px (selout lichtkant 48, binnenlijnen → eigen tint 16, gaatje (32,45) dicht), zwart 28→20 %, lichte hue shift, 11 kleuren; alpha-diff 0 behalve dat gaatje. Haren A en B allebei. Vergelijkvel met fase 2: `sprite_fase1/r4/voor_jordi.png`. Naar Jordi (kiest A/B).
- Jordi op r4 (`sprite_fase1/jordi_r4_omcirkeld.png`, rechterhelft omcirkeld): "niet goed te zien hier waar de ledematen los van elkaar zitten, verder prima versie". Naar r5.
- Haren: Jordi koos **B**.
- **r5** (`sprite_fase1/r5/`, haren B): 39 px in het omcirkelde gebied (scheidingslijnen onderarm/dij, dij/staart, verre poot/dij; staart een stap donkerder; schaduwrand dij); alpha-diff 0. Onderarm en dij nog dezelfde lichte tint. Naar Jordi.
  Jordi op r5: "je hebt nu gewoon maar wat rechte lijnen neergezet die niet kloppen" (`sprite_fase1/jordi_r5_lijnen.png`). Claude: de echte grenzen in het model lopen schuin (onderarm van elleboog schuin omlaag, onderrand vleugel naar de punt, poot eronder); r6 = terug naar r4 en de modellijnen in dat gebied 1-op-1 overnemen.
  Jordi (rode omtrek op r4/r5, screenshot niet op schijf): "vgm is dit de vorm en niet wat je van plan was": bovenarm + grijze band + lichte lob ("dij") + "staart" = één gevouwen vleugel die rechts uitpunt met een onderpunt; poot begint onder die onderpunt.
