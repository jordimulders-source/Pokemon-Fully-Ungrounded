# TODO – Pokémon Fully Ungrounded

## Fase 0: skelet (bezig)
1. ~~Fork + repo opruimen~~ (bronbestanden weg, Ungrounded-docs naar `docs/ungrounded/`).
2. ~~Spire, Battle Stadium en Battle Casino eruit~~ (v0.0.2).
3. (deels gedaan in v0.0.3: kaarten/code van Spacetime en Ultra Space; muziek nog, zie docs/concept/STAND_TECHNIEK.md) Overige Ungrounded-content eruit (**behalve Keccles**: transitie, thema, trainer; hij keert terug): Spacetime (+ Area Zero-muziek), Yoshi's Island, Rainbow Road/Bowser Castle, Ultra Space, legendary-/gym-/klasse-intro's en films (tools blijven), overgenomen muziek uit andere games, Battle Frontier/Tents/Trick House.
4. Expansion bijwerken: 1.14.4 → 1.17.1 (proefmerge 22 okt: 192 bestanden met conflicten, waarvan veel in `src/data/graphics/pokemon.h`/`cry_tables.inc` door onze Mega/Gmax-verwijzingen; die kant van upstream nemen en opnieuw toepassen).
5. Nieuwe start: nieuw spel begint in een plaatshouder-startstad (La Paz-achtig) in een eigen kaartgroep; titel "Pokémon Fully Ungrounded".
6. Hoenn-kaarten, -scripts en -trainers eruit (805 `MAP_*`-verwijzingen in de C-code; generieke interieurs als Pokémon Center/Mart/huizen houden).
7. Dex halveren (±400–500 soorten + Zuid-Amerikaanse lijnen, zie `docs/concept/IDEEEN.md`); families uitzetten via de expansion-config.
8. Vanilla-systemen die niet bij de QoL-filosofie passen: contests/Pokéblocks, Berry Blender en andere minigames, secret bases, Mystery Gift/e-Reader, Record Mixing/Union Room (eerst aan Jordi voorleggen).

## Fase 1: concept
- `docs/concept/CONCEPT.md`: regiokaart, steden, gyms, E4, verhaal, starters (Fighting → Dark → Psychic), dex-lijst, fakemon-lijst.
- Proefronde fakemon-sprites (±5 soorten) om het spritewerk te oefenen.
