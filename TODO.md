# TODO – Pokémon Fully Ungrounded

## Fase 0: skelet (bezig)
1. ~~Fork + repo opruimen~~ (bronbestanden weg, Ungrounded-docs naar `docs/ungrounded/`).
2. ~~Spire, Battle Stadium en Battle Casino eruit~~ (v0.0.2).
3. (deels gedaan in v0.0.3: kaarten/code van Spacetime en Ultra Space; muziek nog, zie docs/concept/STAND_TECHNIEK.md) Overige Ungrounded-content eruit (**behalve Keccles**: transitie, thema, trainer; hij keert terug): Spacetime (+ Area Zero-muziek), Yoshi's Island, Rainbow Road/Bowser Castle, Ultra Space, legendary-/gym-/klasse-intro's en films (tools blijven), overgenomen muziek uit andere games, Battle Frontier/Tents/Trick House.
4. Expansion bijwerken: 1.14.4 → 1.17.1 (proefmerge 22 okt: 192 bestanden met conflicten, waarvan veel in `src/data/graphics/pokemon.h`/`cry_tables.inc` door onze Mega/Gmax-verwijzingen; die kant van upstream nemen en opnieuw toepassen).
5. Nieuwe start: nieuw spel begint in een plaatshouder-startstad (La Paz-achtig) in een eigen kaartgroep; titel "Pokémon Fully Ungrounded".
6. Hele Hoenn-wereld eruit: kaarten, trainers, teams, dialogen, scripts, Battle Frontier/Tents/Trick House (805 `MAP_*`-verwijzingen in de C-code). **Blijven (Jordi, 22 okt):** tilesets en alle assets; Pokémon Center en Mart precies zoals ze zijn (layouts + scripts); een set stock-gebouwen (generieke huis-interieurs, gebouwen in verschillende maten) als bouwstenen; een minimale startkaart + testkaart zodat het opstart.
7. Dex halveren (±400–500 soorten + Zuid-Amerikaanse lijnen, zie `docs/concept/IDEEEN.md`); families uitzetten via de expansion-config.
8. Vanilla-systemen die niet bij de QoL-filosofie passen: contests/Pokéblocks, Berry Blender en andere minigames, secret bases, Mystery Gift/e-Reader, Record Mixing/Union Room (eerst aan Jordi voorleggen).

## Fase 1: concept
- **Cosmic-type uitwerken** (besloten 12 nov, zie `docs/concept/CONCEPT.md`): welke soorten Cosmic worden (kandidaten van Jordi definitief, 21 nov; Elgyem-lijn puur Cosmic), Cosmic-moves, welke gym of welk E4-lid, Minior in de dex?, Fairy-nerf; daarna in de code (typetabel, icoon, Hidden Power/Gem/berry). Jordi gaat hiermee verder in een nieuw gesprek.
- `docs/concept/CONCEPT.md`: regiokaart, steden, gyms, E4, verhaal, starters (Fighting → Dark → Psychic), dex-lijst, fakemon-lijst.
- Proefronde fakemon-sprites (±5 soorten) om het spritewerk te oefenen.
- **Afronding goedgekeurde frontsprites** (kolibrie, olinguito v2, Coathief, wasbeer): frame 2, rugsprite, icoon, shiny-palet (skins-regel), naam/data. Coathief daarnaast: A/B-test kleine kleurreparaties (zie `docs/concept/sprites/coathief/SPEC.md`). Frame 2/icoon/shiny bouwen op het goedgekeurde frame 1; de rugsprite is een nieuwe pose (overtrekvel gebruiken).

## Ontwerpen (overzicht 20 nov; bron: `docs/concept/POKEMON.md` en `IDEEEN.md`)
Originele Poison-lijn = hoatzin-lijn (Poison/Dark, 2 fases): beide fases af (fase 2 26 nov, kuiken 28 nov). Aanleiding: een originele Poison-lijn (Jordi, 26 nov: "ik denk dat ik nog een originele poison lijn wil toevoegen"); bestaande ideeën (pijlstaartrog, pijlgifkikker, koraalslang, Amazone-insecten, açaí, ozongat) "niet overtuigend genoeg". Af: vlieg → mug (21 nov), harpij-arend + regionale Rufflet, vuurwerk-, spooktrein- en koningstiran-lijn (met namen).
- **Nieuwe evoluties:** Kecleon → leguaan (Galápagos), Pinsir → tor/kaiju, Flamigo-evolutie.
- **Regional forms:** Tiwanaku-Golett/Golurk, Venomoth-vuurvlieg (Electric/Fire), Heliamphora-Bellsprout-lijn, Oricorio samba/tango/cumbia, onderwater-Oddish-lijn (bron + anemonen; kokerworm geschrapt), Combee als carpenter bee, Poliwag/Poliwhirl/Poliwrath Ice/Poison (Politoed blijft gewoon; alle drie frontsprite af 25 nov), bokser-Mr. Mime → Mr. Prime (Mr. Prime frontsprite af, 24 nov), Yanma/Yanmega Dragon, Lotad-lijn (*Victoria amazonica* en/of gaucho met hoed), yareta/Copiapoa (Rock-Cacnea?), Spheal/Sealeo + zeeleeuw-eindvorm (neiging), Natu/Xatu Nazca-kolibrie (genomineerd), Galápagos-vormen.
- **Nieuwe Pokémon:** Rock/Water-lijn fontein ↔ gargoyle (Jordi, 16 nov; richting open, uitwerking niet forceren), Steel/Cosmic satelliet-lijn (alle drie de fases af: Spoetnik 23 nov, satelliet 25 nov, ruimtestation 26 nov; namen open), Nazca-astronaut, Golofa-kever, aardappel/maïs-lijn, guácharo, rode oeakari + witgezichtsaki, capibara, Norowara en Kyonpan, zandloper-lijn (Ground/Psychic, origineel; fase 1 en 3 af 27 nov, fase 2 open).
- **Regionale fossielen (Jordi, 26 nov: "sowieso nog gaan komen"):** terreurvogel en glyptodon.
- **Legendaries:** trio Hanan Pacha (condor, de enige condor), Kay Pacha (poema), Uku Pacha (slang); Pachamama (Ground/Fairy).
- **Brainstorm:** evoluties voor Sunflora, Shuckle, Ninjask, Sableye, Mawile, Manectric, Absol, Glalie; regionale Tropius; nog een Mr. Mime-vorm.
- Geschrapt (Jordi, 23 nov): vicuña → guanaco, carnavalspauw; Fire/Water-Pokémon is gedaan (onderwater-Oddish-lijn). Geschrapt (Jordi, 20 nov): regionale vogel die eindigt als condor, Lanturn-evolutie, brandweerhond-Growlithe, opossum (verwerkt in Abra).

## Sprites opknappen (Jordi, 24 nov)
- "dundragoon doet dat het beste van alle sprites die we gemaakt hebben, princadee en zapacha ook, zijn helaas nog wel wat meer sprites waar we het niet goed gedaan hebben en die mogelijk verbeterd moeten worden, maar dat is voor een ander moment." Jordi: "skinguin is trouwens ook uitstekend, die 4 lijken het meest alsof ze uit een pokemon game komen". Maatstaf: Dundragoon, Princadee, Zapacha, Skinguin + echte Gen 3 (`anim_front_gba.png`). Ook de Bibarel-evolutie (r19) gaat mee; regels uit `sprites/bibarel_evo/stijl_gen123/STUDIE_BESTE4.md` (alleen overgangen en lijntinten, palet en lijnposities blijven).
