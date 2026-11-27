# Makeropdracht hoatzin fase 2 (Poison/Dark), ronde 1

Lees EERST `docs/lessen/SPRITE_KERN.md` helemaal en volg het. Daarna `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken" en de Dundragoon-methode (`docs/concept/sprites/dundragoon/sprite_r1/NOTITIES.md`, `bouw.py`). Eisen en citaten van Jordi: `docs/concept/sprites/hoatzin/SPEC.md`.

**MODEL OVERNEMEN, NOOIT HERTEKENEN.** De sprite is de verkleining van het model zelf: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde kleur uit het model → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten per kleurgroep) en per pixel repareren wat de reductie kapotmaakt (oog, kuifpunten, tenen), steeds naar het model. Gezicht, vlakken, schaduw en poten komen uit het model. Meld per zone hoeveel pixels afwijken van de kale reductie. Kleur mag van het model afwijken (Gen 3 + maatstaf-sprites), vorm niet.

- Model: `docs/concept/sprites/hoatzin/model/model.png` (1024×1144, witte achtergrond; samengesteld uit Gemini r6 + hoofd van r4). Het is een Gemini-pixelbeeld: haal eerst het natieve raster terug.
- Doel: 64×64, max 15 kleuren + transparant, de figuur zo groot mogelijk binnen het vak (breedte bepaalt de maat; ±62 px breed), voeten onderaan.
- Gezicht is het belangrijkste: rood oog met de blauwe ring precies zoals het model; de kop is een pestmasker (doorlopende snavel). Kuif: zwarte stekels met geelgroene punten; moet op 1× lezen.
- Kleurgroepen (Jordi): zwartig lijf/kop (kop = zelfde kleur, eigen shading), blauw om het oog, rood oog, geelgroen zuur (verloop van de veerpunten naar binnen) en het geelgroene stralingsteken op de buik (alleen de 3 bladen + stip). Niet bruin. Weinig tinten.
- Stralingsteken: neem het over zoals in het model; Jordi wil dat het in driekwart "deels wegvalt" en midden op de buik staat. Lever naast de hoofdversie een variant met het teken iets naar de buikrand (voorrand linksonder) geschoven, deels achter de ronding. Niet hertekenen: dezelfde pixels verschuiven/afsnijden.
- Maatstaf-sprites voor kleur en lijnen: `docs/concept/sprites/{skinguin,dundragoon,awki}/af/` en `viscacha/af/`; Gen 3-vergelijking alleen `graphics/pokemon/<naam>/anim_front_gba.png` + `normal_gba.pal` (bijv. Honchkrow bestaat niet in Gen 3: gebruik Murkrow, Xatu, Skarmory, Swellow).
- Werk in `docs/concept/sprites/hoatzin/sprite/r1/`: scripts, `kaal.png` (kale reductie), `hoatzin_r1.png` (64×64 geïndexeerd, index 0 transparant), `hoatzin_r1_variant_teken.png`, `vel.png` (r1 | model verkleind op 1× en 8× | close-ups kop en teken). Noem zelf je zwakke punten en repareer ze eerst.
- Niet committen; Claude doet git. Rapporteer kort: bestanden, afwijkingen per zone t.o.v. de kale reductie, zwakke punten.
