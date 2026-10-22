# Changelog – Pokémon Fully Ungrounded

De changelog van Pokémon Ungrounded staat in `docs/ungrounded/CHANGELOG_UNGROUNDED.md` (inclusief alle Pokémon-revisies, die in dit project gelden).

### [v0.0.1] - Fork van Pokémon Ungrounded
- Nieuwe repo `Pokemon-Fully-Ungrounded` met de volledige geschiedenis van Ungrounded (basis: `claude/dazzling-babbage-ud6oxr`, 22 okt) en daarmee van pokeemerald-expansion 1.14.4.
- Opgeruimd: 72 bronbestanden in de hoofdmap (mp3's, zips, gsf-rips, losse plaatjes en MIDI's); 35 plannings-/ontwerpdocumenten van Ungrounded naar `docs/ungrounded/`.
- Nieuw: `docs/concept/IDEEEN.md` (brainstorm), `TODO.md` (fases van het skelet), CLAUDE.md bijgewerkt voor het nieuwe project.

### [v0.0.2] - Spire, Battle Stadium en Battle Casino eruit; concept en regiokaart
- **Verwijderd:** The Spire (code, kaart, graphics, save-blok, alle gevechtshooks), het Battle Stadium (72 Stadium-trainers, 130 partners, 49 ongebruikte trainerfoto's, kaarten, slides) en het Battle Casino (kaart, specials, flags). Gewone gevechten werken zoals voorheen; gimmicks blijven uit. `VAR_STADIUM_STATE`/`VAR_CASINO_BETS` zijn weer vrij (`VAR_UNUSED_0x40B8`/`0x40BB`). ROM: 492 KB → 814 KB vrij.
- Bewust blijven staan: 7 ongebruikte Kanto/N-overworldsprites (hernummeren is riskant), Stadium-trainerklassen, de trainerfoto-generatoren (maken ook nog gebruikte foto's), de Frontier-kaarten (gaan mee met Hoenn).
- **Concept:** `docs/concept/CONCEPT.md` (besloten: starters Fighting → Dark → Psychic, gym 1 Ground in Uyuni, gym 2 Ice, gymtypes en E4, Inca-trio + Pachamama, toon) en `docs/concept/IDEEEN.md`.
- **Regiokaart, schets 1:** `docs/concept/regiokaart_namen.png`, met `tools/concept/regiokaart.py` in de stijl van de Emerald-kaart (kleuren en stadsiconen uit `graphics/pokenav/region_map`).
