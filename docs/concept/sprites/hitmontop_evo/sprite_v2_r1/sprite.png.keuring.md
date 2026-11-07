# Keuring sprite_v2_r1/sprite.png (Hitmontop-evolutie, capoeira)

Bron: `docs/concept/sprites/hitmontop_evo/sprite_v2_r1/sprite.png` (8× en 1× bekeken, plus 14× uitsnede van kop/romp); daarna `docs/lessen/SPRITE_KERN.md`, `docs/concept/sprites/hitmontop_evo/SPEC.md`, `referenties/pose_eenhandsstand.webp` (gespiegeld), `graphics/pokemon/hitmontop/anim_front.png`, `graphics/pokemon/hitmonlee/anim_front.png`, `graphics/pokemon/medicham/anim_front.png`, `graphics/pokemon/machop/anim_front.png` (bovenste 64×64, naast elkaar op 4×). NOTITIES en eerdere keuringen niet gelezen.

## Blinde indruk (vóór context)
- Wezen: een **mensje/chibi-meisje** met bruin haar in een zijstaart/bob, blauwe maillot en blauwe wanten aan de voeten, dat een eenarmige handstand doet. Geen Pokémon-indruk; leest als fanart/anime-chibi.
- Houding: V-split omhoog en één steunarm omlaag zijn herkenbaar. Maar de **kop staat rechtop bovenop/naast een vormeloze lichte klomp** (de romp), los ervan, met een witte spleet ertussen: het lijkt een los hoofdje dat naast het lijf zweeft.
- Raar/fout: romp is een ondefinieerbare bobbel met krasstrepen (geen borst, heup of vrije arm te lezen); benen zijn dunne rechte blauwe buizen zonder knie; huid is bleek perzik i.p.v. Hitmon-bruin; ogen anime-achtig; omlijning van de benen wisselt zwart en paarsblauw.

## Per onderdeel
**(a) Hitmon-familie / pose / verhoudingen**
- Lijkt op: het grove Y-silhouet (twee voeten bovenaan, hand onderaan) uit de pose-foto; ronde hand; blauwe voeten.
- Wijkt af in: leest op 1× niet als Hitmontop-evolutie maar als mensje. Romp leest niet; de kop hangt niet laag naast de steunarm met een hals erheen, maar zweeft los (geen nek). Vrije arm "over de heup" is niet te vinden. Benen zijn spillebeentjes van 3–4 px zonder knie/dij-volume, terwijl Hitmonlee/Hitmontop stevige, getekende ledematen hebben. Huidkleur (222,189,131 / 255,222,156) is veel lichter dan Hitmontops bruin; het familiegevoel valt weg.

**(b) Haar**
- Lijkt op: bruine strepen in het haar (verwijzing naar Hitmontops geribbelde top), klein puntje bovenop.
- Wijkt af in: het is **een nieuw kapsel**, geen gerestyled Hitmontop-haar. Het leest als pony + zijstaart/bob naar links (meisjeskapsel), niet als afro/dreads à la Eddy Gordo en niet als Hitmontops puntige rand. Het hoorntje leest als een haarpluk of pet-knopje.

**(c) Anatomie**
- Geen nek: witte kolom tussen kop (x≈26–27) en romp. Kop en lijf zijn twee losse vormen.
- Vrije arm onleesbaar (rood koordje zweeft in de romp, x≈29–32, y≈29–34).
- Benen sluiten bovenaan de romp aan als buizen; geen heup/billen; enkels als 1–2 lichte pixels; voeten zijn kleine wanten met zwarte puntjes als klauwen.
- Steunarm: stok van 3 px met rood bandje en balhand; acceptabel als idee, maar te dun naast de dikke kop.

**(d) SPEC-punten**
- Eenarmige handstand, V-split: ja, in grote lijnen.
- Kop laag naast de steunarm en kijkt de kijker aan: half (kijkt aan, maar zweeft en staat rechtop i.p.v. aan een hals).
- Vrije arm gebogen over buik/heup: nee.
- Cordão van de heup omlaag: ja (rode strook rechts, x≈47–49, y≈31–40), leest wel als koord.
- Koordjes om de bovenarmen: alleen een bandje op de steunarm; leest.
- Bruine huid, langer lijf: nee (huid bleek, lijf een klomp).
- Lange aansluitende blauwe broek: ja, maar te dun/buisvormig.
- Kleine hoorn: nauwelijks herkenbaar.
- Haar = Hitmontop-haar gerestyled: nee.

**(e) Netheid**
- 15 kleuren, groepen binnen 3 tinten: ok.
- Romp: krasachtige donkere strepen en diagonale banding (tinten parallel aan elkaar), glans rechts (x≈42–44, y≈25–27) terwijl licht linksboven moet komen: pillow/inconsistent licht.
- Benen: buitenrand wisselt **zwart en donkerlila (82,90,148) om en om** op dezelfde rand: harde regel geschonden.
- Ogen zelf getekend (wit glimpje, groot zwart), geen overgenomen Gen 3-oog; leest anime.
- Kop/haar: omlijning ok, maar haar heeft strepen als harde verticale lijnen (banding).

## NODIG
1. **Haar** (zone x≈4–28, y≈18–42 op 1×): weg met pony/zijstaart. Neem Hitmontops eigen bruine puntige rand met strepen als basis en restyle die tot afro-Braziliaanse dreads/opgebonden (Eddy Gordo), alleen vastzittend aan de schedel; hoorntje klein maar herkenbaar ertussen.
2. **Nek + kop-aansluiting** (x≈24–30, y≈24–40): kop moet met een hals aan de romp vast, laag naast de steunarm; geen witte spleet.
3. **Romp opnieuw** (x≈27–48, y≈24–42): leesbare borst→heup-diagonaal (heup hoogste punt), Hitmon-bruin, met de **vrije arm gebogen over buik/heup** als eigen vorm met binnenlijn.
4. **Huidkleur** naar Hitmontops bruin (kop, armen, romp) zodat de familie leest.
5. **Benen** (x≈5–60, y≈2–26): dikker, met dij/knie-volume en een zachte curve, aansluitend aan een heup; geen rechte 3 px-buizen.
6. **Omlijning benen**: geen zwart/donkerlila om en om; zwart aan schaduwkant, selout aan lichtkant.
7. **Ogen**: pixel voor pixel van een echte Gen 3-vechter (Hitmontop/Hitmonlee/Machop), geen anime-glimoog.
8. **Licht linksboven** op romp en kop; krasstrepen en rechter glans op de romp weg.

## POLIJSTEN
- Voeten iets groter en klauwen als echte 2-px-klauwen (zoals Hitmontop), enkels zichtbaar bruin.
- Steunarm 1 px dikker zodat hij de kop draagt; hand plat-rond op de grond.
- Cordão iets meer slinger (geen rechte strook).

## Reparatie of opnieuw?
De opbouw moet opnieuw voor kop/haar, nek, romp en benen: het is geen kwestie van kleur of losse pixels maar van vorm en leesbaarheid (pose-probleem los je niet op met kleurrondes). Alleen de grove pose (Y, steunarm, voeten, cordão) is herbruikbaar als schets.

Oordeel: FAIL
