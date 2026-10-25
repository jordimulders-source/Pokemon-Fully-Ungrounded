# Retrospectief: de kolibrie naast de olinguito (25 okt)

Kolibrie (Ghost/Flying, eindvorm), 24–25 okt. Jordi: "dit is een smooth proces geweest, veel beter dan sommige andere sprites". Ter vergelijking: `RETRO_OLINGUITO.md` (23+ rondes, finale met 33 fails, ontwerp geschrapt) en `docs/concept/sprites/KEURING_RONDE5.md`.

## De cijfers
| | olinguito | kolibrie |
|---|---|---|
| ontwerp/vorm | concept → pixels; vorm werd tijdens het pixelen gezocht (23 rondes, 3 herbouwen) | 8 modeltekeningen (mislukt) + 6 silhouetten, **daarna stond de vorm vast** |
| pixelrondes | 23+ en een finale, nooit goedgekeurd | 5 (r1–r4 intern, r5 na Jordi's 2 punten) |
| rondes die Jordi zag | bijna allemaal | silhouetten + 2 sprites (eind, r5) |
| fouten gevonden door | vooral Jordi | vooral de onafhankelijke keurder ("leest als mug"), daarna Claude |
| bouwtype | viervoeter met klauwen (moeilijk) | vogel zonder poten, zwevend (makkelijker) |

## Wat werkte (overnemen)
1. **Een foto van het echte dier in de gewenste pose als skelet.** De doorbraak kwam toen Jordi een foto stuurde van een drinkende kolibrie in precies de pose; de omtrek is overgenomen en geschaald. Andere Pokémon als skelet (Talonflame) gaven de pose maar de verkeerde anatomie (vleugel vóór de kop).
2. **Silhouet eerst, in één kleur, goedgekeurd vóór de eerste kleurpixel.** Daarna ging het niet meer over vorm maar over kleur en volume.
3. **Jordi's eigen krabbels** (correctie over silhouet v3, eerste posetekening) gaven per stuk meer vooruitgang dan elke tekstuele uitleg.
4. **Onafhankelijke keurder vóór Jordi**, dezelfde agent die rondes onthoudt, met zijn eigen meetscripts (pixeldiff, open randen, vulling/kernmassa). Hij vond de grootste fout (slierten lazen als poten) die Claude miste, en trok een onterechte fail (formaat) in na meten.
5. **Eén maker die doorwerkt** (SendMessage), SPEC.md met Jordi's letterlijke woorden en wat afgekeurd is, en "zelfgenoemd zwak punt = fail".
6. **Kleine, gerichte opdrachten** na goedkeuring: r5 alleen volume + oog, silhouet bevroren (alpha-diff 0).

## Wat misging (niet herhalen)
1. **Modeltekeningen uit cirkels en driehoeken** (v1–v8): stijf, horizontaal, vleugels fout; "Pokémon designen is geen cirkels en driehoeken werk". Kostte de meeste beurten met Jordi.
2. **Gokken in plaats van vragen**: vleugelvorm drie keer fout tot Jordi een close-up stuurde; zijn krabbel verkeerd gelezen.
3. **Claude voegde zelf een fout toe aan het silhouet**: drie slierten die onder het lijf hingen. Goedgekeurd als silhouet, maar in kleur lazen ze als poten → 2 extra rondes en een variant.
4. **Claude stuurde versies die hij zelf nog niet goed vond** (schets v1–v6).

## Waar de tokens heen gingen
- Ontwerp/silhouet: veel korte beurten met Jordi, weinig tokens per beurt, maar frustrerend.
- Pixelrondes: per ronde ±150–400k agenttokens (inlezen van richtlijnen, vellen maken, met de hand typen van rasters). De keurder ±150–220k per keuring.
- Grootste besparing zat in **geen herbouw**: na het silhouet alleen nog gerichte rondes.

## Aanbevelingen voor de sprite-editor (Jordi bouwt er een)
Doel: Jordi doet waar mensen goed in zijn (vorm, pose, smaak), agents doen wat saai en meetbaar is (kleur, volume, opschonen), en de editor meet de harde regels zodat niemand daar tokens aan uitgeeft.
1. **Foto als onderlaag + silhouet trekken op 64×64** (pen/gum, één kleur). Dit is de stap die het meeste scheelde en die Claude het slechtst kan.
2. **Lagen per onderdeel met een slot** (kop, lijf, vleugel, staart…): "bevroren" wordt een knop in plaats van een pixeldiff-afspraak.
3. **Annotatielaag**: Jordi krabbelt op de sprite, de editor slaat het op als PNG naast de sprite in de repo; agents lezen het zonder uitleg.
4. **Palet vast op 16 kleuren** met index 0 transparant, export als geïndexeerde PNG + JASC `.pal` zoals `graphics/pokemon/`.
5. **Ingebouwde checks** (gratis i.p.v. agenttokens): aantal kleuren, open randen (schaduw/basis naast transparant), losse pixels, rechte stukken ≥ 4 px in curven, alpha-diff tegen een bevroren versie, vulling/kernmassa naast referenties.
6. **Voorbeeld op 1×/3× op licht en donker naast gekozen echte sprites** (Venomoth, Swellow…), want "leest het op 1×" was de vraag die het meeste opleverde.
7. **Export/import als tekst-raster** (één teken per paletindex): agents bewerken dat het goedkoopst en het past in een prompt; de editor rendert het terug.
8. **Werkwijze met de editor:** foto → Jordi trekt silhouet → agent kleurt + volume via tekst-raster → editor-checks → één keurderagent alleen op "leest het op 1× als X, past het tussen Gen 3" → Jordi.
