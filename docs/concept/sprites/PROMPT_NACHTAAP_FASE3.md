# Prompt voor een nieuw gesprek: nachtaap fase 3 (eindvorm Psychic-starter)

Plak de tekst hieronder in een nieuw gesprek.

---

We gaan beginnen aan **fase 3 (de eindvorm) van de Psychic-starter**, de nachtaap-lijn. Fase 1 en fase 2 zijn af. Volg de werkwijze die bij de kolibrie, de olinguito v2 en nachtaap fase 2 werkte, met de lessen die we daarbij leerden. **Begin met brainstormen over het ontwerp met mij; geen pixels, geen poppetje voordat de richting staat.**

**Eerst lezen (gericht, niet alles volledig):**
- `CLAUDE.md` (werkafspraken, Stand van zaken).
- `docs/lessen/SPRITE_WERKWIJZE.md`, helemaal, inclusief de lessen onderaan (o.a. unieke labels op rastervellen, motieven als bolkappen in 3D, patronen in 3D ontwerpen en projecteren, krabbels uitlezen, retro nachtaap fase 2).
- `docs/lessen/SPRITE_NORM.md` (incl. de patroonregels van Game Freak onderaan) en `docs/lessen/SPRITE_OPDRACHT.md`.
- `docs/lessen/FAKEMON_DESIGN.md` en `docs/lessen/FAKEMON_CHECKLIST.md` (ontwerpregels, Dragonfly Cave).
- `docs/concept/POKEMON.md`, sectie "Psychic: nachtaap-lijn" en "Ontwerpkeuze starters".
- `docs/concept/sprites/nachtaap_evo/SPEC.md`: alle besluiten en mijn letterlijke woorden van fase 2, plus wat is afgekeurd.

**Waar de lijn staat:**
- **Fase 1** (goedgekeurd): `docs/concept/sprites/nachtaap/ronde12/variant_spiraal/anim_front.png`. Een violette tarsier-achtige jonge nachtaap: grote roze ogen, crème gezicht, een krulletje als staart.
- **Fase 2** (af): `docs/concept/sprites/nachtaap_evo/af/nachtaap_evo.png`. De "nachtwaker met maangezicht": gehurkt in de Lairon-pose, de kop laag en recht in de camera, de rug hoger, donkerder violet. Eén witte sikkelmaan op de kop met de punten omlaag, rode Espurr-achtige ringogen met een vlak bovenlid, drie lichte tapse wiggen (maanzilver) vanaf de ruggengraat, violette handen met crème vingertoppen, de staart omhoog met een spiraal.
- **Fase 3, wat al besloten is** (POKEMON.md): een **muriqui** (de grootste aap van Zuid-Amerika, Atlantisch Woud, de "hippie-aap": geen rangorde, begroet met omhelzingen, grijpstaart) **met de grote ogen van de eerdere fasen**. Hij lijkt gevaarlijk maar is zachtaardig, een **healer**. Een **healer-outfit** (Andes-genezer: de kallawaya met de geweven kruidentas, de yatiri die cocabladeren leest), **geen Inca-god**. Een **subtiel zilveren maanmotief** (Mama Killa). De **volle Nazca-spiraal** in de staart (krulletje → spiraal → volle spiraal). Ideeën: Psychic/Fairy, helende moves, een signature move die het team geneest en 's nachts sterker is.
- **Open punten om met mij te bespreken:**
  - Wat neemt fase 3 mee van fase 2 (sikkelmaan, ringogen, wiggen, violet)?
  - Hoe wordt de outfit Pokémon-achtig, dus uit de anatomie en niet "dier met kostuum"?
  - Wordt de kené het patroon op het geweven deel (tas, poncho)? Bij fase 2 werd die voor later bewaard.
  - Het type.
  - De pose.
  - De stap van nachtaap naar muriqui: muriqui-bouw met nachtaap-gezicht, of meer nachtaap?
  - Het formaat: eindvorm ±2,4× fase 1 (±2200–2300 px; fase 2 is 1459 px).

**Werkwijze (stap voor stap, zoals in SPRITE_WERKWIJZE):**
1. **Brainstorm.** Geef 4–6 duidelijk verschillende richtingen in tekst, met je eigen voorkeur. Ik kies, en daarna vraag ik om foto's van het echte dier.
2. **Foto's** die ik stuur meteen in `docs/concept/sprites/nachtaap_fase3/referenties/` zetten, plus een `SPEC.md` met mijn woorden letterlijk.
3. **Pose zoeken** met echte sprites als voorbeeld (vellen met vergelijkbare poses), dan een **3D-poppetje** (`docs/concept/sprites/nachtaap_evo/pop3d/` als basis, `pop3d.py` en `nachtaap3d.py`). Daarvan een raster met hoeken waarin **elk label de hoek zelf noemt**. Ik kies.
4. **Kenmerken en motieven op het poppetje**: maan, outfit, patroon. Tekeningen op de kop als bolkappen, symmetrisch om het middenvlak, gecontroleerd van voren en van opzij. Patronen in 3D en met een 1×-preview, getoetst aan de patroonregels van Game Freak; leg me 2–3 opties voor vóór de pixels.
5. **Silhouet** = de render direct verkleind (de massa is heilig). Alleen dunne delen met de hand, in benoemde zones, met een diff-bewijs. Ik keur, daarna bevroren.
6. **Kleur** door één maker-agent die doorwerkt (eerst een Game Freak-studie). Claude kijkt elke ronde zelf. Daarna een onafhankelijke keurder die vergelijkt met ≥ 10 echte sprites en met de Dragonfly Cave-gids, en kleine reparaties benoemt in een pixeltabel; die voert Claude zelf uit. Pas dan krijg ik hem te zien.
7. **Af** in `af/`: SPEC, POKEMON.md, CHANGELOG (nieuwe sectie), Stand van zaken in CLAUDE.md, lessen. Commit en push na elke ronde.

**Wat ik eerder zei en nog steeds geldt:**
- "Pokémon designen is geen cirkels en driehoeken werk"
- "gebruik de fotos echt als inspiratie"
- "een patroon zou altijd dikker moeten"
- "de ogen zijn het belangrijkst"
- Lijkt gevaarlijk maar is zachtaardig.
- Simpel houden.
- Immersie: alleen wat in de wereld klopt.
- Fase 3 moet duidelijk de volgende fase zijn, niet "fase 2 met ander lijf" (dat zei ik bij fase 2 over fase 1).

Antwoord in het Nederlands, kort en zonder lange samenvattingen.
