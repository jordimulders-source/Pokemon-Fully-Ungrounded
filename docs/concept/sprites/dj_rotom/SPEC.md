# DJ Rotom (Electric/Steel, Rotom-vorm): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`. Type uit de concepten (Jordi, 22 okt): Electric/Steel.

**Bron (Jordi, 5 nov):** "Begin met de DJ Rotom sprite. Dit is de bron" → `referenties/pokopia_dj_rotom_bron.webp` (render van DJ Rotom uit *Pokémon Pokopia*, 1920×1920). Eerder (23 okt): "duidelijk een Rotom-vorm, maar niet DJ Rotom; je hebt het niet goed nagebouwd"; het ontwerp moet **trouw zijn aan DJ Rotom uit Pokopia**, alleen de pixels zijn eigen werk in Gen 3-stijl.

## Onderdelen
| onderdeel | bron / referentie | Jordi's woorden | status |
|---|---|---|---|
| pose en massa | silhouet 2 (`silhouet2/vel_perspectief.png`): het 3/4 van de bron sterker, varianten A/B/C (k 0,10/0,18/0,26; nabij groter, veraf kleiner, boven- en onderlijn kantelen); silhouet 1 = `silhouet1/silhouet.png` = de bron verkleind tot 60 px breed (script `silhouet1/maak_silhouet.py`) | "Dit is de bron"; "misschien iets meer perspectief als in pronounced vormen?"; "ik vind de bron juist driekwart" | open (Jordi kiest A/B/C) |
| linker speaker | bron: lage kast, twee conussen (boven klein, onder groot), zwart front | — | open |
| middendeel = Rotom-kop | bron: oranje kubus met spits, Rotom-ogen, grijns met tandjes, zwart display met groene equalizer als mond; zwart snoertje naar beide speakers | — | open |
| rechter speaker | bron: hogere kast, twee grote conussen | — | open |
| bliksem met noot | bron: mintgroene bliksem uit de spits, witte muzieknoot erin; handreparatie zone x 20–34, y 18–36 (32 px, rest 0 px gewijzigd) | — | open |
| gloed | bron: mintgroene rand rond het hele silhouet (de Gen 3-Rotom-vormen hebben ook een gekleurde gloed i.p.v. zwarte lijn) | — | open |

## Afgekeurd (niet herhalen)
- Ronde 1 (23 okt, `ronde1/`): boombox met handvat, cassettedek en speakers ín één kast. "een hele andere vorm, kom op, je kan beter"; "niet DJ Rotom".
