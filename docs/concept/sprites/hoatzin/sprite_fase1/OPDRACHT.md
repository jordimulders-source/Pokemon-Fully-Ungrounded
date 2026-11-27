# Makeropdracht hoatzin fase 1 (kuiken), ronde 1

Lees EERST `docs/lessen/SPRITE_KERN.md` helemaal en volg het. Daarna `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken" en `docs/lessen/GEMINI.md` (vooral pitahaya fase 1 en "Spritegrootte eerst tonen"). Citaten van Jordi: `docs/concept/sprites/hoatzin/SPEC.md` → "Fase 1 (kuiken)". Fase 2 (zelfde lijn, voor palet-gevoel): `docs/concept/sprites/hoatzin/af/hoatzin_fase2.png` en `sprite/r13/`.

**MODEL OVERNEMEN, NOOIT HERTEKENEN.** Jordi koos dit model letterlijk ("ga maar deze bouwen"). De sprite is de verkleining van het model zelf: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde modelkleur → alleen technisch opschonen (buitenlijn, ruis, ≤3–4 tinten per kleurgroep) en per pixel repareren wat de reductie kapotmaakt (oog, tenen, klauwtjes), steeds naar het model. Niets toevoegen, niets weglaten (ook de stekeltjes op rug/vleugel horen erbij zoals in het model). Meld per zone hoeveel pixels afwijken van de kale reductie.

- Model: `docs/concept/sprites/hoatzin/model/fase1_model.png` (= Gemini r4, 1024×1024). Natief raster: pitch 10,24 px (100×100), figuur natief 70×77. Maattest: `docs/concept/sprites/hoatzin/fase1_maat/maten.py` en `maten_vel.png`.
- Maat: figuur **44 px hoog** (±787 px gevuld; Jordi akkoord met 700–900 px), in een 64×64-vak, voeten onderaan, horizontaal gecentreerd.
- Max 15 kleuren + transparant. Kleurgroepen: zwartig dons (lijf/kop), gelige tinten alleen in het dons, grijs (snavel, kale vleugels, poten, klauwen), donker oog met grijze ring. Niet bruin. Weinig tinten.
- Belangrijk voor Jordi: de te lange dunne poten met grote tenen, de kale veerloze vleugels (geen handen), kromme grijze snavel zonder glimlach, koude lege blik (oog met grijze ring moet op 1× leesbaar blijven).
- Bekende risico's uit de maattest: stekeltjes worden een schaakbordraster (maak er de modelstekels van, niet meer en niet minder dan de reductie toelaat, geen eigen vorm); de nabije vleugel over het lijf moet als vleugel blijven lezen (grijs tegen zwart, omlijning uit het model).
- Gen 3-vergelijking: `graphics/pokemon/<naam>/anim_front_gba.png` + `normal_gba.pal` (bijv. Murkrow, Natu, Doduo, Taillow). Maatstaf-sprites: `docs/concept/sprites/{skinguin,dundragoon,awki,viscacha}/af/`.
- Werk in `docs/concept/sprites/hoatzin/sprite_fase1/r1/`: scripts, `kaal.png` (kale reductie), `kuiken_r1.png` (64×64 geïndexeerd, index 0 transparant), `vel.png` (r1 op 1× en 8× | kale reductie | model verkleind | close-up kop). Noem zelf je zwakke punten en repareer ze eerst.
- Niet committen; Claude doet git. Rapporteer kort: bestanden, afwijkingen per zone, zwakke punten.
