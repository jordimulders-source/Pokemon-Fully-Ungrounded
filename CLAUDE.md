# Pokémon Fully Ungrounded – werkafspraken voor Claude

Vervolg op **Pokémon Ungrounded** (Project Grounded), gebouwd als fork daarvan op pokeemerald-expansion: alle revisies van Pokémon, moves en abilities, de nieuwe moves/abilities en de QoL blijven. Nieuwe, originele regio gebaseerd op **Zuid-Amerika** (geïnspireerd, niet nagemeten, zoals Hoenn op Kyushu). In code en tools heten veel dingen nog "Grounded" (`tools/grounded/`, `FLAG_GROUNDED`); dat blijft zo. De eigenaar (Jordi) communiceert in het Nederlands; antwoord en schrijf de changelog in het Nederlands.

- **Repo:** `jordimulders-source/Pokemon-Fully-Ungrounded` (branch `main`, volledige geschiedenis van Ungrounded + expansion, dus upstream mergen kan). Het oude project staat in `jordimulders-source/projectgrounded`; de Ungrounded-documenten (changelog, plannen) staan als naslag in `docs/ungrounded/`.
- **Concept:** ideeën van Jordi verzamelen in `docs/concept/IDEEEN.md`; besloten punten in `docs/concept/` (overzicht `CONCEPT.md`, verder `REGIO.md`, `VERHAAL.md`, `POKEMON.md` met per Pokémon de inspiratie, `SPRITE_PLAN.md`). Alles wat we doen goed documenteren, verdeeld over deze documenten (Jordi). Jordi gooit hersenspinsels; Claude maakt er een geheel van.
- **Lessen hieronder** komen grotendeels uit Ungrounded en gelden technisch nog steeds; regels over Hoenn-kaarten, het Stadium, de Spire en Spacetime zijn naslag tot die content weer terugkomt.

## Zuinig met tokens
- **Humor herhaalt niet:** de "X: YES."-grap is op (Jordi, 9 okt); varieer grappen en check met grep of een vorm al vaak voorkomt.
- **Autonoom (Jordi, 9 okt):** ga zelf door met taken uit `TODO.md` die geen input van Jordi vereisen (volgorde: de prioriteitsregel bovenaan TODO); vraag alleen bij echte ontwerpkeuzes.
- **Werkregel (Jordi, 9 okt): zo weinig mogelijk moeite, zo veel mogelijk bereiken.** Hergebruik kaarten/tilesets/scripts/teams, placeholders voor intro's en thema's tot de muziekfase, alleen het riskante testen, dure onderdelen uitstellen en melden.
- **Geen ROM opleveren** (zippen/versturen) tenzij Jordi erom vraagt. `make -j4` om te controleren dat het bouwt mag altijd; filter de uitvoer met `make -j8 2>&1 | grep -i error` (`grep "rror:"` mist linkerfouten zoals een onbekend geluid of symbool).
- Emulatortests en screenshots alleen voor wat echt nieuw of riskant is (warps, scripts, nieuwe mechanics); niet voor elke kleine kaartwijziging. Eén render van de hele kaart aan het eind is genoeg; stuur die zonder ze zelf eerst vaak te bekijken.
- Gebruik de bestaande tools (`tools/grounded/maptools/`, o.a. `testrom.py`, `render_map.py`) in plaats van ze opnieuw te schrijven. Lees grote bestanden gericht (grep, offset/limit), niet in zijn geheel.
- Korte statusberichten; geen samenvattingen van wat al in de changelog staat.
- **Stand van zaken** hieronder kort houden: alleen wat een volgende sessie moet weten. Details horen in `CHANGELOG.md`.

## Vaste regels
- **Niet interpreteren (Jordi, 5 nov: "vanaf nu ga je niet meer dingen interpreteren die ik niet zeg"):** geef Jordi's woorden letterlijk door; vul niets in wat hij niet zei (geen eigen kenmerken, geen versmalde of verbrede lezing). Is iets onduidelijk: vragen, niet invullen.
- **Changelog:** zet elke wijziging onderaan in `CHANGELOG.md`, als een nieuwe `### [v.x.y.z] - ...`-sectie. Versies: 0.8.x tot de laatste fase vóór de beta; 0.9 = die laatste fase; 1.0 = de beta. Dit is Jordi's eigen logboek; het mag "vervuild" zijn (codeblokken, learnsets). Niet opschonen of herstructureren.
- **Debugmenu blijft aan** (`DEBUG_OVERWORLD_MENU` en `DEBUG_BATTLE_MENU` in `include/config/debug.h`).
- **Mail en Magikarp-levels** niet aanpassen.
- **Grap-trainers blijven een grap:** extreem lage levels op sterke Pokémon zijn bewust (bijv. Ivan's Gyarados lv 3, Lyle's Scizor/Yanmega lv 6). Ze moeten schrikken, niet onverslaanbaar zijn. Alleen **vroeg in de game** (Jordi, 6 okt: "die Gyarados zo laag aan het begin is omdat die anders niet te verslaan is"); laat in de game is een laag level tijdverspilling: daar krijgen grap-trainers een echt team.
- **Toon (Jordi, 22 okt):** het verhaal van Fully Ungrounded is **serieuzer** dan Ungrounded (dat was 100% humor). Humor mag, maar is geen gimmick meer: droog en op zijn plek (NPC's, zijpaden), niet in elke regel en niet ten koste van het hoofdverhaal. Niet zwart-wit, mag filosofisch zijn, nooit edgelord. Show, don't tell: via personen en situaties, niet via uitleg of preken. Bestaande Ungrounded-teksten die meekomen niet "netjes maken"; wel tekstregels afbreken zodat ze passen (`\n`, `\l`, `\p`).
- **Intro kort houden:** geen truck-intro, geen tv-scène. Mom houdt haar humoristische standaardtekst; healen, PokéNav-registratie en post-game-dialoog werken wel.
- **Elemental monkeys** (Pansage/Pansear/Panpour-lijnen) mogen sinds 9 okt op routes waar ze passen (Jordi).
- **National Dex** is vanaf het begin beschikbaar. **Alle Pokémon zijn te krijgen** (Jordi, 9 okt): geen versie-exclusieve keuzes waarbij een soort voorgoed verdwijnt (Glastrier én Spectrier).
- **Ruimte is na de 1.0 geen hoofdzaak meer** (Jordi 11 okt: "veel content hoeft en kan er ook niet meer bij, maps, trainers etc"): kies bij klank/beeld voor kwaliteit; de grens hieronder blijft wel gelden.
- **ROM-ruimte bij de 1.0 (Jordi, 10 okt):** doel ≥ 512 KB vrij, nooit minder dan 256 KB (na de 1.0 komen er alleen nog moves/abilities bij, en eventueel extra shinies). Meld bij elke grote toevoeging de resterende ruimte zodra we onder 1 MB komen. Meten: `grep "__rom_end = " pokeemerald.map`, vrij = 0x0A000000 − dat.
- **Kleurvarianten zijn skins** (Jordi, 15 okt): herkenbaar anders, passend bij de soort, hoe zeldzamer hoe opvallender. Nooit een variant die nauwelijks van normaal verschilt; geen vloekende kleuren tenzij het een grap is. Recepten en filosofie: `TODO.md` (Kleurvarianten).
- **BELANGRIJKSTE SPRITEREGEL (Jordi, 6 nov): een model van Jordi namaken = alleen twee eisen:** (1) heel accuraat op het origineel (niets toevoegen/weglaten/herinterpreteren), (2) een Gen 3-sprite volgens al onze eisen. Keurders toetsen alleen die twee. Zie bovenaan `docs/lessen/SPRITE_KERN.md`. **Zegt Jordi dat hij een model (van Gemini) heeft om na te maken: volg `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken".**
- **Werkwijze is verplicht, Coathief is het voorbeeld (Jordi, 2 nov: "zorg er voor dat alle volgende sessies dit wel doen").** Claude bouwt zelf géén silhouetten uit buizen/collages van bestaande sprites en kleurt nooit per script; silhouet (als één geheel, van een echte bron) en kleur (met de hand, na een Game Freak-studie) maakt **één maker-agent**; Claude coördineert, vergelijkt elke ronde zelf met de bronfoto's en een keurder vóór Jordi. Mis het na 2 rondes: stoppen en terug naar de werkwijze, niet doorpatchen (wasbeer, 2 nov: 3 poppetje- en 11 silhouetrondes zonder resultaat). **Ontwerp uit Gemini** (Jordi, 7 nov): dan gelden de aangepaste regels in `docs/lessen/GEMINI.md` (Jordi's Gemini-keuze is het bevroren ontwerp, de sprite is een trouwe vertaling, kwantiseren als onderlaag mag).
- **SPRITES: lees eerst `docs/lessen/SPRITE_KERN.md` (één pagina, alle lessen samengevat) en geef dat bestand aan elke sprite-agent mee.** De andere spritebestanden zijn naslag. "Pokémon designen is geen cirkels en driehoeken werk."
- **Volgorde sprites (Jordi, 5 nov):** "frame 2, rugsprite, icoon, shiny, naam en data allemaal later, ook in het vervolg, we bouwen eerst designs met sprites". Per nieuwe Pokémon eerst alleen ontwerp + frontsprite tot af; de rest pas in een latere, aparte fase voor alle soorten samen.
- **Pokémon ontwerpen (Jordi, 23 okt):** elk ontwerp van een nieuwe Pokémon (fakemon, regional form, sprite) gebeurt met de Dragonfly Cave-gidsen in het achterhoofd: `docs/lessen/FAKEMON_DESIGN.md`, `docs/lessen/SPRITING.md` en de bronnen in `docs/lessen/bronnen/` (*Making Fake Pokémon* en *Spriting Guide*). Geef ze aan elke ontwerp- of sprite-agent mee. Maatstaf: **Cuyby** (ronde 3) is een geslaagde fakemon; referenties in `docs/concept/ontwerp/referenties/`. **Volg de vaste werkwijze bovenaan FAKEMON_DESIGN.md** (ontwerp → silhouet op echt skelet → sprite + checklist → onafhankelijke keuring vóór Jordi → alleen benoemde reparaties; doel ≤ ±5 rondes).
- Merk je een nieuw designprincipe op, stel het eerst aan Jordi voor en voeg het pas na bevestiging toe aan dit bestand.

## Speelervaring
- Filosofie à la Shin Megami Tensei / Slay the Spire: gevechten mogen pittig zijn, maar de speler krijgt veel tools en mogelijkheden om ze op te lossen.
- Move-aanpassingen gebeuren per move; er is geen algemene regel (zoals "altijd 100% bijeffect").

## Quality of life
- **De game respecteert de tijd van de speler.** Pokémon is een JRPG vol herhaling; schrap die herhaling zodat speed-up-knoppen niet nodig zijn. Animaties (aanvallen, schermtransities) zijn tof en blijven; wachttijden, overbodige teksten, ja/nee-vragen en minigames gaan eruit.
- **Nooit grinden** (Jordi, 9 okt): de EXP-opbrengst moet het hoofdpad haalbaar maken zonder grinden; de extra content (sidequests, zijgebieden) is het alternatief voor grinden en geeft marge; variatie in teams aanmoedigen (completionists met meerdere parties mogen niet ver boven de curve uitkomen). Meten met `tools/grounded/levelcurve.py`.
- Wat al gedaan is (lijst): `docs/QOL.md`.
- Bewust níet: Exp. Share als Key Item, pc in het menu, type-effectiviteit altijd tonen, zwakke encounters ontlopen (zwakkere routes afzoeken kan een bewuste keuze zijn), uitleg van de laatst-gebruikte-bal-knop, een echte levelcap.

## Zelflerend werken
- Leer van elke sessie en word steeds beter in het meebouwen aan deze rom. Voeg **zelf, zonder het te vragen**, aan het eind van een stuk werk nieuwe lessen toe in het passende bestand in `docs/lessen/` (zie hieronder): fouten die je maakte, feedback van Jordi, valkuilen in de code/tools en testtrucs die werkten. Kort, één regel per les; verouderde lessen bijwerken of schrappen.
- Alleen **designprincipes** (smaak, spelregels, humor) eerst aan Jordi voorleggen (zie Vaste regels). Technische en werkwijze-lessen mag je direct opschrijven.

## Lessen
Algemene lessen staan hieronder; de rest is per onderwerp opgesplitst. **Lees het passende bestand vóór je aan dat onderwerp begint** (niet allemaal tegelijk):
| Onderwerp | Bestand |
|---|---|
| Kaarten, tilesets, events, routes/grotten/steden bouwen | `docs/lessen/KAARTEN.md` |
| Sprites, trainerfoto's, vormen, kleurvarianten | `docs/lessen/GRAPHICS.md` |
| Stappen + commando's / naslag sprites | `SPRITE_WERKWIJZE.md` (compact: Checklist, stappentabel en commando's); naslag alleen bij twijfel: `SPRITE_NORM.md`, `SPRITE_OPDRACHT.md`, `SPRITING.md`, `FAKEMON_DESIGN.md`, `FAKEMON_CHECKLIST.md`, `RETRO_*.md`, `SPRITE_REVIEW.md`, `naslag/SPRITE_WERKWIJZE_oud.md` |
| **Pokémon-sprites en -ontwerp (ALTIJD EERST)** | **`docs/lessen/SPRITE_KERN.md`** (één pagina; meegeven aan elke sprite-agent); ontwerp uit Gemini: ook `GEMINI.md` |
| C-code: gevechten, UI, eigen schermen, scripts | `docs/lessen/CODE.md` |
| Transities, klasse-intro's, films | `docs/lessen/INTROS.md` |
| Muziek en samples | `docs/lessen/MUZIEK.md` (+ `tools/grounded/MUZIEK.md`) |
| Emulatortests, saves | `docs/lessen/TESTEN.md` |
| Agents, git, merges | `docs/lessen/AGENTS.md` |
| Trainers, wilde Pokémon, revisies, moves, flags, levelcurve | `docs/lessen/TRAINERS.md` |
| Ungrounded-systemen die eruit zijn (Spire, Stadium, Spacetime) | `docs/lessen/NAASLAG.md` |

- **Immersie telt voor Jordi:** alleen dingen die in de wereld kloppen (geen Reshiram-beeld als Reshiram niet in de game zit; dieren die echt in koud zoet water leven; bloemen alleen waar het plausibel is). Bij twijfel kort uitleggen of voorleggen.
- **ROM-ruimte (v0.9.234: 3,46 MB vrij; ongebruikte Mega/Gmax-vormen wijzen naar de basisvorm (cry_tables.inc, graphics/pokemon.h); verdeling: samples 12,8 MB waarvan kreten 8,2 MB (al gecomprimeerd), Pokémon-sprites ±2,3 MB, films ±1,1 MB, tilesets 1,4 MB; graphics zijn al `smol`).** Was 3,25 MB vrij in v0.9.105 (meten: `grep "__rom_end = " pokeemerald.map`, vrij = 0x0A000000 − dat); gebieden kosten 5–15 KB per kaart, muziek op stock-instrumenten 20–50 KB, met eigen samples 100–400 KB; een filmintro kost ±180–220 KB (20 fps). Grover (STEP 4–6, lagere `budget`) of eerst ongebruikte samples opruimen. INCBIN-paden voluit schrijven (geen stringconcatenatie in macro's).
- **Types, abilities en evoluties altijd uit de repo** (`src/data/pokemon/species_info/`, `types_info.h`), nooit uit het geheugen of van internet: veel soorten zijn herzien (Parasect is Ghost/Grass, Toxicroak evolueert tot Lumineon, Ludicolo heeft geen Swift Swim). Jordi 18 okt: "gebruik de repo-documentatie".
- **Compat-voorstellen van agents** controleren tegen de repo-types vóór je ze aan Jordi voorlegt (Gyarados "Dark", Clefable "Flying" waren fout).
- **Max. 3–4 agents tegelijk** en geef agents het relevante lessenbestand mee in hun opdracht (zie AGENTS.md).

## Bouwen en testen
- Bouwen: `make -j4` (moet zonder fouten slagen vóór elke push).
- `make check` (CI-job `build`) faalt ook op `master`, met honderd-en-zoveel tests die de bewust gewijzigde mechanics en soorten niet meer verwachten. Nieuwe failures ten opzichte van master zijn wel een probleem; meld de bekende failures niet aan Jordi.
- Werk op een branch en open een PR naar `master`.
- Testen: `python3 tools/grounded/maptools/testrom.py` (zie `docs/lessen/TESTEN.md`); testkaart `warp MAP_TEST_MAP, x, y`; testmon Mewtwo lv 100 met Dark Pulse/Psychic/Thunderbolt/Ice Beam en alle badges. `data/scripts/debug.inc` nooit committen.
- Afronden: `make -j4` slaagt → changelogsectie → Stand van zaken bijwerken (kort) → commit en push. Geen ROM tenzij gevraagd.

## Dialogen (Dialoogstudio)
- Jordi's Dialoogstudio: https://claude.ai/artifact/LP3qyGyvhaj6p5GS32Gjxz. Werkwijze ('verwerk de dialogen', import/export): `docs/lessen/NAASLAG.md` (onderaan). Na de Hoenn-opruiming verwijst hij naar verdwenen labels; niet automatisch bijwerken.

## Sessies en overdracht
- **Takenlijst:** `TODO.md` (fases van het skelet en daarna). Afgeronde taken daar weghalen en in de changelog zetten.
- Elke sessie begint vers; dit bestand is het geheugen. Werk **Stand van zaken** bij aan het eind van elk afgerond stuk werk (in dezelfde commit).
- Commit en push na elk afgerond stuk, met een changelogsectie in `CHANGELOG.md` (nieuw project: versies 0.0.x tijdens het skelet).

## Stand van zaken
- **Fase: concept + skelet** (23 okt). Repo `Pokemon-Fully-Ungrounded` (branch `main`); dezelfde commits ook op `projectgrounded`, branch `claude/vibrant-wright-j33xkl`. Push naar beide (`git push fu HEAD:main` en `git push origin HEAD`).
- **Concept:** `docs/concept/` (CONCEPT met index, REGIO, ROUTEPLAN, DUNGEONS, MYTHOLOGIE, VERHAAL, POKEMON, FAKEMON_PITCH, MUZIEK, IDEEEN, DEX_NOMINATIES, DEX_IN_ROM, SPRITE_PLAN). Regiokaart: variant 3 (gekozen). Dex ±445 soorten + Mew/Mewtwo/Zarude.
- **Sprites:** werkwijze in `docs/lessen/SPRITE_KERN.md` + `SPRITE_WERKWIJZE.md` (Checklist; keurslot-hook verwijderd, Jordi 6 nov); Gemini-model namaken: `docs/lessen/GEMINI.md` + SPRITE_WERKWIJZE "Gemini-model namaken" (poedelmot = voorbeeld). Ontwerpkeuzes in POKEMON.md. **Eerst de hele dex alleen frontsprites (Jordi, 5 nov); frame 2, rug, icoon, shiny, naam/data later voor alle soorten samen.** **22 frontsprites af:** Cuyby, Cuychu, nachtaap (`nachtaap ronde12/variant_spiraal`), alpaca (`ronde17/variant_kop`), kolibrie (`kolibrie/af/`), kolibrie pre-evo (`kolibrie_pre/af/`), olinguito v2 (`olinguito_v2/af/`), Coathief (`coathief/af/`, nog A/B kleurreparaties), wasbeer (`wasbeer/af/`), nachtaap fase 2 (`nachtaap_evo/af/`) en fase 3 (`nachtaap_fase3/af/`), lama fase 2 (`lama/fase2/af/`) en fase 3 (`lama/fase3/af/`), Uyuni-Silicobra (`silicobra_uyuni/af/`) en Salticonda (`salticonda/af/`; Ground/Electric; ability immuun voor Ice én Water, naam/effect open), DJ Rotom (`dj_rotom/af/`), Picapau (`picapau/af/`, Electric/Flying) en evolutie (`picapau_evo/af/`, naam open), poedelmot (`poedelmot/af/`, Bug/Fairy) en poedellarve (`poedellarve/af/`), Sapa Inca (`koningstiran/af/`, eindvorm koningstiran-lijn, Normal/Flying → Fire/Flying → Fire/Psychic; retro `docs/lessen/RETRO_SAPA_INCA.md`), hatun runa (`hatun_runa/af/`, fase 1 van die lijn, kiskadie, naar Gemini-model). Alle paden onder `docs/concept/sprites/`.
- **Koningstiran fase 2 (awki, Fire/Flying), volgende:** fase 1 (hatun runa) en 3 (Sapa Inca) af; awki = koningstiran met gesloten kuif; model-kandidaat = Gemini r4 met Claude's kleuraccenten (`koningstiran/gemini/awki_r4_accenten.png`, rondes in `gemini/README.md`); wacht op Jordi's akkoord, dan SPEC + frontsprite. Sapa Inca = late evolutie (Bisharp-idee).
- **Great potoo (één stage), bezig:** kandidaat r6 + oog C4, eindkeuring 2 gerepareerd; zie `docs/concept/sprites/potoo/OVERDRACHT.md` en SPEC.
- **Hitmontop-evolutie (capoeira, Fighting/Ground), gepauzeerd:** bron = `hitmontop_evo/referenties/model_gemini_pose_v3.png`, silhouet D gekozen; sprite ronde 1 (per script) afgekeurd; volgende: met de hand op silhouet D, zo ACCURAAT mogelijk t.o.v. het model (Jordi). SPEC in die map.
- **Viscacha (Electric, één stage):** Gemini-ronde 6 gekozen als ontwerp (`viscacha/referenties/gemini_gekozen_ronde6.png`); frontsprite nog te doen.
- Feedback: `docs/concept/sprites/FEEDBACK.md`. **Zuinig:** één sprite-agent tegelijk.
- **Muziek staat op pauze** (feedback in `docs/concept/MUZIEK.md`; instrumentenset `fu_samples.py`, schetsen songs 611–616).
- **Tilesets:** `tilesets/` (assetbibliotheek); La Paz + altiplano ronde 2 wacht op Jordi.
- **Techniek (v0.0.9, ±18,4 MB vrij):** Ungrounded-muziek, intro's/films, Hoenn-wereld en Pokémon buiten de dex zijn eruit (`docs/concept/STAND_TECHNIEK.md`, `PLAN_HOENN_ERUIT.md`). Skelet: StartTown, Pokémon Center, Mart, stock-huizen, TestMap; overgangsheader `map_compat.h` + stubs. **Stap 8 (Frontier/Union Room/Contests/Secret Bases/Trainer Hill weg?) wacht op Jordi.** Expansion is bijgewerkt naar **1.17.1** (v0.0.10; nieuwe gevechtsmotor, zie STAND_TECHNIEK stap 4). Soorten aan/uit: `include/config/species_enabled.h`.
- **Save-data:** nieuwe velden alleen achteraan SaveBlock1 (na `bagItems`). Oude saves werken niet meer.
- **Grenzen:** flags via `FLAG_GROUNDED(n)`, trainer-id's max 1199, max 128 kaarten per kaartgroep (zie `docs/lessen/TRAINERS.md`, `KAARTEN.md`). Emulator: `python3.11` (mgba).
