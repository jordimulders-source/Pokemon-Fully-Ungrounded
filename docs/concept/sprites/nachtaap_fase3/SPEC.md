# Nachtaap fase 3 (Psychic-starter, eindvorm): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`. Opdrachten aan agents altijd met `SPRITE_NORM.md` + `SPRITE_OPDRACHT.md` + deze SPEC. Vorige fasen: `../nachtaap/ronde12/variant_spiraal/anim_front.png` (fase 1), `../nachtaap_evo/af/nachtaap_evo.png` (fase 2, SPEC in `../nachtaap_evo/SPEC.md`).

## Lijn (uit `docs/concept/POKEMON.md`)
- Tarsier-achtige baby → nachtaap (nachtwaker met maangezicht) → **muriqui** met de grote ogen van de eerdere fasen. Lijkt gevaarlijk, maar is zachtaardig en een healer. Healer-outfit (kallawaya/yatiri) uit de anatomie, geen Inca-god; subtiel zilveren maanmotief (Mama Killa). Volle Nazca-spiraal in de staart.
- Type: nog niet besloten (voorstel Claude: Psychic/Fairy). Geen data in deze stap.

## Jordi's woorden (letterlijk)
- 3 nov (op het brainstormvoorstel A–E): "Ik zie een muriqui zitten, hebben we oranguru in onze dex gezet? Ben ik even vergeten, dat is geen zuid amerikaans dier. Hier wat fotos ter inspiratie. Het gezicht vind ik erg belangrijk, evenals de lange armen en benen. Daar gaan we wat mee doen. Hij kan idd weer meer rechtop en groot. Zijn wel meerdere pokemon lijnen waar ze van zittend naar kruipend naar rechtop gaan vgm. We houden het kleurpatroon aan, hooguit donkerder of lichter dan de rest van de lijn. Ook wil ik de sinistere ogen blijven vasthouden, al mogen die nu best kleiner gezien de muriqui kop, even kijken hoe we dat kunnen doen. Kleur mag anders dan Oranguru wel. Andere tint iig. Spiraalstaart is belangrijk. De bladeren in de staart is wel een leuk idee, mits dat te doen is in onze spriet. Zweven vind ik eigenlijk nog geniaal. Dan moeten we zorgen dat die niet te hoog zweeft, zijn genoeg pokemon die als voorbeeld kunnen dienen hiervoor. Mega Alakazam zweeft bijv."
  - Oranguru staat niet in de dex (`P_FAMILY_ORANGURU FALSE`; zijn rol ging naar de oeakari, `DEX_NOMINATIES.md`).
  - **Besloten:** muriqui; gezicht, lange armen en lange benen zijn de kern; **rechtop en groot** (lijn zittend → kruipend → rechtop); **kleurpatroon van de lijn blijft** (violet, witte maan, rode ogen, lichte tekening), hooguit donkerder/lichter; **sinistere ogen blijven**, mogen kleiner (muriqui-kop); tint anders dan Oranguru; **spiraalstaart belangrijk**; **bladeren in de staart** als het op de sprite kan; **zweven**, maar laag (voorbeeld Mega Alakazam).
  - Kleuromkering (lichte vacht, donker gezicht) dus níet; de lijnkleuren blijven.

- 3 nov: "P1, maak het poppetje maar" → **pose P1 zwevend hangen**: één lange arm omhoog (hangt aan een onzichtbare tak), de andere reikt (helend gebaar), benen los, volle spiraalstaart met bladbundel in de krul, zweefhoogte ±6–7 px.
- 3 nov (bij het eerste poppetje): "de benen zijn ook te recht" + "mogen veel relaxter" → knieën gebogen naar voren en uit elkaar, onderbenen hangen slap, voeten bungelen (zitten in de lucht).
- 3 nov (bij raster P1): "nee dit lijkt echt nog nergens op. De hand aan het einde van de arm moet echt een healer gebaar maken. Verder is dit nog niet psychic/zwevend genoeg" + "Lijkt gewoon alsof die staat" → P1 afgekeurd; studie `referenties/psychic_gebaren.png` (Mega Alakazam, Medicham, Meditite, Mr. Mime, Deoxys, Mewtwo …): open handpalm naar de kijker met gespreide vingers; benen niet onder het lijf.
- 3 nov: "Ik zou bijna zeggen om het echt uniek te maken zou je bijna de benen nog hoger willen hebben alsof die in een soort van vlucht staat zit" + foto 2 ("wat meer zon soort idee") → **benen omhoog** zoals op foto 2: hangt aan de benen, lijf eronder, kop onderaan rechtop, armen vrij.
- 3 nov, **lore**: "met als lore dat hij planten en takken met psychische krachten kan channelen, onzichtbare of zichtbare" → hij hangt aan een onzichtbare (of zichtbare, psychische) tak; bladeren in de staart passen hierbij.
- 3 nov, krabbel `referenties/jordi_krabbel_pose.png`: "ik dacht meer aan zoiets, heel slecht getekend" → **lijf horizontaal in de lucht**, kop vooraan links; één arm omhoog-voor en één been recht omhoog; ander been sleept naar achteren-omlaag; staart rechtsboven als spiraal; onderste arm reikt naar voren-omlaag.
- 3 nov: "misschien dat 1 arm en 1 been takken vasthouden" + foto 2 ("zoals hier") → geheven arm en geheven been houden elk een (psychische) tak vast.
- 3 nov: "nee de onderste hand houdt geen plant vast" / "die maakt een healer gebaar" / "zoals in films en anime met magiers" / "open hand" → onderste hand: **open hand, palm naar buiten, vingers gespreid** (spreukgebaar); geen voorwerp.
- 3 nov: "40-80 akkoord, maar we tonen geen takken en de hand moet nogmaals open zijn zoals bij healers in films en anime, of snap je niet wat ik bedoel?" → **hoek lijf 40° / kop 80° akkoord**; **geen takken** (handen en voet gekruld om een onzichtbare tak); onderste hand = arm lang gestrekt naar voren, voorbij de kop, hand rechtop met de palm naar de kijker en de vingers omhoog, duim opzij (A gesloten, B iets gespreid; `pop3d/pose_40_80_hand.png`).
- 3 nov: "ja nu moet het alleen nog meer in verhouding, ziet er niet uit zo. Daarnaast wil ik het rechts van het hoofd en niet links" + anime-still medisch ninjutsu (niet als bestand binnengekomen: twee platte handen, vingers wijd gespreid, palm drukt naar het doel, groen licht) "dit bedoel ik met healing pose" / "maar dan doet deze het met 1 hand".
- 3 nov: "je hebt nu ook het rechterbeen afgekapt", "hahaha wat doe je nou", "dit lijkt nergens op", "waarom schiet die hele arm naar boven", "volg mijn schets" → terug naar de schets: onderste arm van onder de nek schuin naar linksonder, hand onder de kop.
- 3 nov: "en kijk ook naar andere pokemon sprites want dit ziet er nog erg onnatuurlijk uit" → studie `referenties/dynamische_poses.png` (Mew, Deoxys Speed, Celebi, Zeraora, Ambipom, Infernape, Primeape, Simipour …): compact, ledematen gebogen en dicht bij het lijf, grote handen/voeten, kop groot op de schouders, taps (dikke dij/bovenarm), geen zeester.
- 3 nov: "waar is de healing hand?" + **"als er geen healing hand met de palm richting de tegenstander is dan mag je het altijd afkeuren"** → **harde eis:** open hand, vingers gespreid, palm naar de tegenstander (= naar de kijker bij een frontsprite), groot genoeg om op 1× te lezen.
- 3 nov, handkrabbel `referenties/jordi_krabbel_hand.png` ("zie hier mijn lelijke sketch", "dit is toch niet zo moeilijk"): hand aan het eind van de onderste arm, linksonder de kop; pols knikt naar achteren, **vingers omhoog, duim links, palm naar de tegenstander**. Render: `pop3d/pose_40_80_healerhand.png` (groot + 1×).
- 3 nov: "ja dit is veel beter al is de hand nu overdreven groot" → hand kleiner (schaal 1,6 → 1,25, ongeveer de maat van de voeten).

## 3D-poppetje
- `pop3d/muriqui3d.py` (renderer `pop3d/pop3d.py`, kopie van fase 2). Kleuren alleen ter oriëntatie (lijnkleuren van fase 2).
- Raster `pop3d/hoeken.png` (P1, afgekeurd). Raster `pop3d/poses.png`: 'benen omhoog' (lijf 30/40/50°) naast kleermakerszit, zweven en in vlucht (voorbij).
- Raster `pop3d/poses_krabbel.png`: pose naar de krabbel, lijf 20/30/40°, kop +40/+55°.

## Referenties
- Foto's van Jordi (3 nov): `referenties/foto1_gezicht_closeup.jpg` (donker kaal gezicht, lichte vachtrand, kleine diepe ogen, brede snuit), `foto2_hangend_lange_armen.jpg` (hangt aan twee armen, benen los, heel lange ledematen), `foto3_klimmend_tak.jpg` (rechtop aan een tak, lange arm omlaag), `foto4_moeder_met_jong.jpg` (gezicht met roze gespikkelde snuit, omhelzing), `foto5_zittend_hand_op_kop.jpg` (zittend, armen om zich heen, roze snuit).
- Zweefhoogte: `referenties/zweven_hoogte.png`: sprites op hun `enemyMonElevation` uit de repo (Mega Alakazam 7, Dusknoir 6, Uxie 6, Victini 7, Reuniclus 8, Meloetta 8, Gardevoir 10, Mew 11, Gothitelle 14; Medicham 1 als staand).

## Open
- Pose (zwevend, rechtop), kop/gezicht (muriqui-masker in lijnkleuren + maan), ogen kleiner maar sinister, bladeren in de staart, outfit uit de anatomie, kené ja/nee, type.

## Afgekeurd (niet herhalen)
- Elke versie zonder healerhand met de palm naar de tegenstander (Jordi: 'mag je het altijd afkeuren'); zeesterpose met gestrekte buizen; hand die het gezicht bedekt of op zijn kant staat; takken in beeld.
- Pose P1 met de voeten onder het lijf ('lijkt gewoon alsof die staat'), een arm omhoog aan een tak zonder healergebaar, gestrekte stokbenen.
- Alles uit `../nachtaap_evo/SPEC.md` (Afgekeurd) en `../FEEDBACK.md`: o.a. kené als dunne lijntjes of ribbels, borstvlak, bleke gezichtsschijf, maanfasen/sterren, ondersteboven hangen.
- Kleuromkering naar muriqui-kleuren (lichte vacht, donker gezicht): de kleuren van de lijn blijven (Jordi, 3 nov).
