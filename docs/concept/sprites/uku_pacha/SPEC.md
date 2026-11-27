# Uku Pacha – slang-legendary (Water/Ghost)

Pacha-kwartet (zie `docs/concept/POKEMON.md` → Legendaries; condor `../hanan_pacha/SPEC.md`). Wezen, geen godenbeeld (Jordi: "net als dat groudon een behemoth is en kyogre een leviathan"). Moet ogen als een box legendary. Geen Cosmic ("ze zijn juist aards").

## Jordi (27 nov, letterlijk)
- Type: "Water/Ghost goed".
- Basis: "anaconda, met 2 koppen en kleine vleugels klinkt tof en uniek".
- Koppen: "Twee koppen aan de nek" (gevorkte nek, twee koppen naast elkaar).
- Ghost: "Lijf loopt uit in geest" (achterlijf/staart vervaagt in geestachtig water, alsof hij uit de onderwereld oprijst).
- Kleur: "diepblauw en grijs tinten, die water en geest goed samenbrengen, maar geen grijze brei".

## Ingevuld door Claude (niet door Jordi gezegd; schrappen als het niet klopt)
- Pose: voorlijf rijst op uit een kronkel, past in een vierkant (Gen 3-compositie).
- Plaats van de kleine vleugels: achter de koppen, waar de nek zich splitst.
- Anaconda-anatomie (ogen en neusgaten bovenop de kop, zware dikke romp, vlekken) = echte soort.

## Rondes
- **r1** (`gemini/r1.png`, prompt v1). Jordi: "ok het is nog iets teveel een normale slang denk ik, de hoofden moeten naar verhouding wat groter en beide een andere pose/blik. Plus de staart is normaal met een beeetje rook eromheen, was niet het idee vgm, vleugel zit ook te hoog en is er maar 1". (Gemini: twee kleine koppen met dezelfde blik, één vleermuisvleugel hoog op de rug, gewone staart met wat rookslierten.)
- **r2** (`gemini/r2.png`, prompt v2). Jordi: "deze is tof, prima legendary vorm, de staart loopt logisch, koppen wijken af. Vertaalt die goed naar een sprite?"
- Check r2 (Claude): natief raster 100×100 (pixel 10,24 px), figuur ±92×89; voor een legendary die het vak vult reductie ±0,70 (zoals zandloper fase 1), geen exacte 2× (dat wordt 46 px). Silhouet, koppen, tong, vleugels en geest blijven leesbaar in een kale testreductie; risico = de vele schubbenlijnen worden bij 0,70 druk. ±20 tinten in het model, terug te brengen naar ≤16.
- Vergelijkingsvel met alle slang-Pokémon: `vergelijk_slangen.png`. Jordi: "doe het zoals arbok het doet", "qua lijn frequentie". Bijsturen in het r2-gesprek: `gemini/BIJSTUUR_r2_lijnen.md`.
