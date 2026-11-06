# Poedelmot (Venezolaanse poedelmot): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md` + `docs/lessen/SPRITE_KERN.md`. Achtergrond: `docs/concept/IDEEEN.md` (Venezolaanse poedelmot, Gran Sabana) en `POKEMON.md` (Venomoth-regional form, nog niet bevestigd dat dit die vorm is).

## Jordi's woorden (6 nov, letterlijk)
- (bij afbeelding 1) "nieuwe poging voor de poodle moth. Dit is precies het design in de pose die ik wil in de game, maak hier een sprite van, zo true to form als mogelijk"
- (bij afbeelding 2) "hij is bijna perfect, maar hij heeft teveel poten toegevoegd. Pak anders deze, met de voelsprieten van de andere"

## Bronnen (`referenties/`)
- `jordi_2_lijf.png`: **de bron** voor lijf, vleugels, kop, ogen, pootjes, kleuren en pose.
- `jordi_1_voelsprieten.png`: alleen de **voelsprieten** (donkere, geveerde sprieten: zwartbruin met lichte middennerf en lichte dwarsstrepen), die vervangen de bruine sprieten van afbeelding 2.
- `samengesteld.png`: afbeelding 2 met de sprieten van afbeelding 1 erover (zelfde koppositie, ogen op dezelfde pixels).

## Besloten
- Ontwerp en pose = Jordi's afbeelding (bevroren); niets toevoegen of weglaten. Pootjes zoals in afbeelding 2 (niet meer).
- Silhouet: `silhouet/silhouet.png` (bron direct verkleind, `silhouet/sil.py`; 62×45, 1782 px). Rode omtrek over de bron: `silhouet/silhouet_over_bron.png`. Kleurgids (gemiddelde kleur per pixel, géén sprite): `silhouet/gids_gemiddeld.png`.

- (6 nov, letterlijk) "eigen soort, en een laatste evolutie idd, komt 1 vorm voor, een larve met poedel kenmerken"
  → **Eigen soort** (niet de Venomoth-regional form), **laatste evolutie** (fase 2 van 2; formaat 62×45, 1782 px is goed). Voorvorm: een **larve met poedelkenmerken** (ontwerp later, eigen SPEC).

## Open
- Naam, type en data komen later (Jordi, 5 nov). Ontwerp van de larve.
