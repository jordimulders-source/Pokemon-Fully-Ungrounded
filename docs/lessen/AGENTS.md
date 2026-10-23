# Lessen: Agents, git en merges

Lees vóór het starten of samenvoegen van agents en bij git-werk. Opgesplitst uit CLAUDE.md (23 okt); nieuwe lessen hier toevoegen.

- **Subagents in worktrees:** laat ze eerst `git reset --hard <werkbranch>` doen (worktrees starten soms op een oude commit) en CHANGELOG/CLAUDE.md níet aanraken; zelf samenvoegen, gegenereerde bestanden (stadium_pool.h, battle_partners-blok) na een conflict opnieuw genereren i.p.v. met de hand mergen.
- **Agent-branches samenvoegen:** conflicten achteraan enums/tabellen/map_groups zijn "beide houden"; let op een `}` of komma die op de grens wegvalt. Vlecht git twee nieuwe functieblokken door elkaar (battle_transition.c), bouw het bestand dan op uit onze versie + hun blok.
- **Max. 3–4 agents tegelijk** (4 cores, krappe schijf, gedeelde gebruikslimiet: met 7 tegelijk stopten ze allemaal op de limiet en moesten ze hervat worden). Ruim gemergde worktrees en grote wav/gba-bestanden in de scratchpad direct op.
- **Subagents en de scratchpad:** die wordt gedeeld; laat elke agent een eigen submap gebruiken (een `test.gba` van een ander proces gaf een Bus error).
- **Agent-branches met conflicten:** `graft.py`-aanpak: onze versie + de pure toevoegingen van de agent (diff base→agent), wijzigingen met de hand; trainernummers en gegenereerde bestanden (pool.py) daarna opnieuw.
- **Agent-merges van tileset-headers** (`graphics.h`/`headers.h`/`metatiles.h`): git splitst de blokken verkeerd (gedeelde staart `};` valt weg). Neem onze versie en plak de toevoegingen van de agent (diff merge-base → agent) erachter. Bij JSON-conflicten (layouts, mapsecs) controleren op weggevallen velden (`width`/`height`).
- **Werkbranch kiezen:** kijk bij een nieuwe sessie met `git ls-remote origin` naar de nieuwste `claude/*`-branch; `master` kan tientallen versies achterlopen (8 okt: v0.9.89 vs v0.9.140).
- **Agents in worktrees:** shellregels met `$VAR`, `for` of `cd` worden daar geweigerd; laat ze hulpscripts in hun scratchpad schrijven. Object verbergen na een trainergevecht: `"flag": "TRAINER_FLAGS_START+TRAINER_X"` (map_events.s include `constants/opponents.h`).
- **Graft van tileset-headers:** voeg ALLE regels van de agent toe (geen filter op "staat al in ons bestand": `.isCompressed = TRUE,` e.d. kwamen al voor en vielen weg → Yoshi's Island toonde vuilnis). Altijd een emulatorbeeld van een nieuwe tileset na een merge.
- **Merge met veel conflicten:** na het oplossen altijd controleren dat elke toegevoegde regel van de agent (diff merge-base → agent) in het resultaat staat (difflib-script); regex-oplossingen verloren bij National Park stilletjes flags en trainerconstanten. Twee agents die allebei het volgende `OBJ_EVENT_GFX`-nummer pakken: hernummeren en `NUM_OBJ_EVENT_GFX` ophogen; partnernummers verschuiven → `pool.py` + `announcer.py` opnieuw.
- **Nooit `git stash` in de hoofdcheckout met eigen onopgeslagen werk** om een testrun terug te zetten (stash + drop gooide scriptwijzigingen weg; terug via `git fsck --no-reflog`). Gebruik `git checkout -- data include src`.
- **Audit vóór elke grote merge/release:** `python3 tools/grounded/audit.py` (open lijst in `AUDIT.md`). Coord-scripts die op `end` eindigen geven de besturing terug; alleen `lock`/`lockall` zonder `release` laat je vastzitten. Snel naar elke kaart in emulatortests: debugscript 1 (`warp`) en daarna `sWarpDestination` overschrijven (zie `nm`).
- **Schijf vol** (8 okt–10 okt): oude agent-worktrees (±585 MB elk) na het samenvoegen weghalen (`git worktree remove --force`, branch blijft); controleer eerst `git status` en `merge-base --is-ancestor`. **Nooit de worktree van een agent die nog (of weer) aan het werk is** (v0.9.292: een agent die na v1 een v2-opdracht kreeg, verloor zijn worktree; `-f -f` negeert het slot). Alleen agents die klaar zijn én geen vervolgopdracht hebben.
- **Parallelle sessies:** check bij een nieuwe opdracht eerst of een andere `claude/*`-branch dezelfde punten al deed (`TESTRUN.md`, `git log HEAD..origin/<branch>`); anders dubbel werk en conflicten (Leftovers, Johnson, Colress-levels op 15 okt).
- **Nooit `cd <map>; rm *`** in één Bash-regel: de veiligheidscheck blokkeert het hele commando (ook de commits ervoor). Gebruik volledige paden.
- **Controleer de basis vóór je begint:** `master` liep ver achter op de echte werkbranch (1.0 op `funny-edison`); vergelijk de laatste changelogversie van de remote branches (`git branch -r` + `git show <b>:CHANGELOG.md`) met wat Jordi speelt, anders reproduceer je bugs op oude code.

## Upstream-merge (expansion 1.14.4 → 1.17.1, 23 okt)
- Zet eerst hernoemde API's mechanisch om; los pas daarna conflicten op. Bij sterk herschreven bestanden upstream als basis nemen en onze blokken erin porten ('ours' geeft oude API in nieuwe code).
- Na de merge per bestand een accoladecheck (git liet gedeelde staarten `}`/`};` vallen) en controleren dat eigen blokken niet in een `#if IS_FRLG`-blok belandden.
- Naast de regelvergelijking een identifier-check: regels verhuizen naar andere bestanden.
- Battlescripts draaien in 1.17 per geraakt doelwit, na de schade: 'één keer per zet'-effecten hebben een eigen markering nodig.
- Een volledige `make check` hangt hier ('Illegal opcode'); draai eigen tests per bestand met een filter (`gTestRunnerArgv` = bestandsnaam), met `tools/` als symlink in de map waar je de test draait.
- Een agent die uren draait: laat hem tussenstanden committen en push een back-upbranch (`backup/...` in Pokemon-Fully-Ungrounded) als de limiet nadert.
- **Parallelle sprite-agents en SPRITING.md:** elke agent voegt "§N" onderaan toe, dus elke merge geeft een conflict op hetzelfde nummer. Oplossen: beide secties houden, de binnenkomende hernummeren; of agents laten schrijven in hun eigen NOTITIES.md en de lessen zelf overzetten.
