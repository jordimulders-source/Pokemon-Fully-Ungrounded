# DJ Rotom (Electric/Steel, Rotom-vorm): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`.

**Bevroren (Jordi, 5 nov "prima! ga maar in kleuren. Bliksem noot mag idd dikker dan"):** `silhouet_af/silhouet.png` = silhouet 2 variant B (k 0,18) + bliksem-noot met de hand dikker (15 px, zone x 19–30, y 19–32; script `silhouet_af/hand_bliksem.py`). Onderlaag voor kleur: `silhouet_af/onderlaag.png` (64×64) en `silhouet_af/bron_vervormd.png` (groot). Alpha-diff 0 in alle volgende rondes.

**Stijl (Jordi, 5 nov):** "gebruik vooral de stijl van de rotom sprites die al in de game zitten he" → `graphics/pokemon/rotom/{heat,wash,frost,fan,mow}/anim_front.png` en `graphics/pokemon/rotom/anim_front.png` zijn de stijlnorm (gloedrand, oranje tinten, ogen, shading). Type uit de concepten (Jordi, 22 okt): Electric/Steel.

**Bron (Jordi, 5 nov):** "Begin met de DJ Rotom sprite. Dit is de bron" → `referenties/pokopia_dj_rotom_bron.webp` (render van DJ Rotom uit *Pokémon Pokopia*, 1920×1920). Eerder (23 okt): "duidelijk een Rotom-vorm, maar niet DJ Rotom; je hebt het niet goed nagebouwd"; het ontwerp moet **trouw zijn aan DJ Rotom uit Pokopia**, alleen de pixels zijn eigen werk in Gen 3-stijl.

## Onderdelen
| onderdeel | bron / referentie | Jordi's woorden | status |
|---|---|---|---|
| pose en massa | silhouet 2 (`silhouet2/vel_perspectief.png`): het 3/4 van de bron sterker, varianten A/B/C (k 0,10/0,18/0,26; nabij groter, veraf kleiner, boven- en onderlijn kantelen); silhouet 1 = `silhouet1/silhouet.png` = de bron verkleind tot 60 px breed (script `silhouet1/maak_silhouet.py`) | "Dit is de bron"; "misschien iets meer perspectief als in pronounced vormen?"; "ik vind de bron juist driekwart" | bevroren (variant B) |
| linker speaker | bron: lage kast, twee conussen (boven klein, onder groot), zwart front | — | open |
| middendeel = Rotom-kop | bron: oranje kubus met spits, Rotom-ogen, grijns met tandjes, zwart display met groene equalizer als mond; zwart snoertje naar beide speakers | — | open |
| rechter speaker | bron: hogere kast, twee grote conussen | — | open |
| bliksem met noot | bron: mintgroene bliksem uit de spits, witte muzieknoot erin; handreparatie zone x 20–34, y 18–36 (32 px, rest 0 px gewijzigd) | — | open |
| gloed | bron: mintgroene rand rond het hele silhouet (de Gen 3-Rotom-vormen hebben ook een gekleurde gloed i.p.v. zwarte lijn) | — | open |

## Afgekeurd (niet herhalen)
- Ronde 1 (23 okt, `ronde1/`): boombox met handvat, cassettedek en speakers ín één kast. "een hele andere vorm, kom op, je kan beter"; "niet DJ Rotom".
