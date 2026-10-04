# Vragen voor Jordi (ochtend 5 okt 2026)

**Antwoorden 1-10 (5 okt):** 1 kort (direct de arena in, iedereen klaar) · 2 ja · 3 later · 4 nee, Gyarados eruit · 5 blijft · 6 ok · 7 tong · 8 willekeurig · 9 ok · 10 Route 115. Verwerkt in v0.8.114–0.8.115.
**Antwoorden 11-17:** 11 Birth Island + ticket weg · 12 lv 70 · 13 eng en stil blijft · 14 Gothitelle weg · 15 zo laten, Toxic/Leech Seed zeldzaam · 16 relics naar 50 · 17 actlengte blijft; een run duurt voor een mens ±1 uur–1u20.
**Antwoorden 18-21:** 18 niks wijzigen (bewuste buffs, eerst testen; Desolate Land niet te sterk) · 19c (verborgen abilities zijn niet verkrijgbaar) · 20 Delibird, Lumineon, Plusle, Minun, Beautifly, Dustox, Kecleon, Huntail/Gorebyss, Sandslash; rest blijft · 21 ja. Verwerkt in v0.8.116.

Kort antwoorden mag ("1a, 2 ja, 3 Route 115"). Alles hieronder is al gebouwd of klaar om te bouwen; de vragen gaan over smaak en balans.

## Battle Stadium
1. **Arena per wedstrijd:** je loopt nu elke ronde de arena in (presentator, publiek, tegenstanders als overworld-sprite). Prettig, of wil je het sneller (alleen bij kwartfinale en hoger)?
2. **Kanto/Sinnoh in de arena** hebben nog generieke overworld-sprites (Misty = zwemster, Giovanni = gentleman ...). FRLG-sprites voor de Kanto-leiders en Giovanni/Blue importeren uit pokefirered (zoals Brock en Oak)?
3. **Johto en Unova** (Whitney, Morty, N, Ghetsis, Iris ...): er is geen schone GBA-bron bereikbaar. Heb jij trainersprites (bijv. Greenphx Gen 4+)? Zet ze in de repo, dan maak ik er toernooiteams bij.
4. **Ivan:** zijn grap is de Gyarados op lv 3; in het Stadium is alles lv 50. Uitzondering voor grap-trainers (levels houden), of zo laten?
5. **THE WEATHER** (Rayquaza, Kyogre, Groudon als compagnon): Rayquaza's Air Lock heft het weer van de andere twee op. Lore-grap houden of Rayquaza vervangen?
6. **Namen van collecties** zijn max. 10 tekens ("REGI SPIRIT" werd "REGIS"). Akkoord?
7. **Boo:** nu de Boo met uitgestoken tong; de verlegen Boo (handen voor het gezicht) kan ook.
8. **Doubles-duo's** worden willekeurig gekoppeld. Liever vaste iconische duo's waar dat kan (Archie+Maxie, Red+Blue, Tate+Liza, Dave+Mitch ...)?
9. **BP:** 1/1/2/3/5 per ronde (12 per titel). Te weinig/veel vergeleken met de Spire (±80 per gewonnen run)?

## Ditto
10. **Ditto in de overwereld:** voorstel Route 115: een Youngster naast een hengeltabel vol Ditto, zegt "...", na het gevecht ":)", daarna kun je Ditto vissen. Akkoord, of Ashfrost?

## Deoxys (ruimte-event)
11. Moeten **beide routes** blijven: het Aurora Ticket (Birth Island met puzzel) én de ruimte? Wie hem op één plek vangt, ziet hem nergens meer.
12. **Level:** ruimte-Deoxys is lv 70 (zoals de andere post-game-legendaries), Birth Island nog vanilla lv 30. Birth Island ook 70?
13. **Muziek** in de ruimte: nu `MUS_SEALED_CHAMBER` (eng en stil). Of liever Mt. Moon, of straks de Delta Emerald-muziek?
14. **Encounters:** Minior, Lunatone, Solrock, Elgyem, Clefairy, Metang, Beheeyem, Cleffa, Gothitelle, Clefable, Porygon-Z, Metagross. Andere soorten?

## The Spire (balans, zie onderaan `SPIRE_BALANS.md`)
15. **Gif, Leech Seed, weer en %-heals** negeren de ×HP-vermenigvuldiger: Toxic doodt elke baas in ±6 beurten, Recover heelt een halve balk. Delen door de vermenigvuldiger in de Spire, of zo laten en Toxic/Leech Seed zeldzaam maken?
16. **Relics:** er zijn er maar 8; in 28% van de runs raken ze op. Uitbreiden naar 20-25 (voorstel volgt bij ja)?
17. **Actlengte:** 7 verdiepingen per act (Slay: 15). Naar 9?

## Pokémon-balans (rapport: `POKEMON_BALANS.md`)
18. **OP-kandidaten** (voorstellen in het rapport): Volbeat/Illumise (Tail Glow lv 22, Volbeat al vóór Roxanne), Linoone (Extreme Speed lv 20, Belly Drum lv 39), Octillery (Protean + bijna elk type, Remoraid al na badge 1), Kricketune (wild lv 13 vóór Roxanne), Crawdaunt/Magcargo/Grumpig (vroege Shell Smash/Simple+Tail Glow). Welke aanpakken?
19. **Verborgen abilities zijn voor de speler onbereikbaar** (geen Ability Patch, DexNav uit): Kecleon Protean, Sharpedo Speed Boost, Feebas Adaptability ... Opties: (a) zo laten, (b) Ability Patch als beloning, (c) per soort het ability-slot verplaatsen.
20. **Buff-kandidaten** (18 stuks in het rapport, o.a. Delibird, Lumineon, Luvdisc, Plusle/Minun, Beautifly/Dustox, Swellow, Delcatty, Cacturne, Solrock/Lunatone, Pelipper, Hypno, Farfetch'd, Sandslash). Welke mag ik doorvoeren?
21. **Marill evolueert nu op lv 25** (stond zo in de changelog, code had 18). Daardoor zijn een wilde Azumarill (1%, lv 18–22, Route 117) en een trainer-Azumarill op lv 20 te vroeg. Aanpassen naar Marill?

## Backlog
22. Er staan nog open vragen in `BACKLOG_PLAN.md` (Jirachi, Giratina, Mewtwo, Genesect, Darkrai, Shaymin, Victini, Kubfu, nieuwe gebieden). Welke wil je als volgende?
23. **Archie en Maxie terug in de post-game** (open punt uit `TODO.md`): ja/nee, en waar?

## Uit de QA-ronde (`QA_RAPPORT.md`)
24. **Route 115:** wilde Pokémon lv 30–50, terwijl de trainers daar lv 13–33 zijn. Bedoeld (achter Surf) of verlagen?
25. **Dubbele soorten** in ±60 oudere wilde tabellen (lijst in het rapport). Mag ik die volgens de regel (dubbel slot vervangen, zeldzaamheidsvolgorde behouden) zelf invullen, met soorten die passen bij de plek?
26. **Route-transities** blijven aan het eind ±0,7 s stilstaan (10 frames vasthouden + fade). Korter maken?
