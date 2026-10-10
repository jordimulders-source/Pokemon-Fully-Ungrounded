# Muziek componeren en arrangeren voor Project Grounded

Dit is het geheugen voor muziekwerk. **Lees dit vóór elk nieuw nummer, en vul het aan na elke feedbackronde van Jordi**
(wat fout ging, wat hij mooi vond, welke controle het had kunnen vangen). Een nieuwe fout die automatisch te
herkennen is, komt ook als controle in `music_lint.py`.

## Werkwijze (verplicht, in deze volgorde)
1. Componeren/arrangeren met een script (`zarude_theme.py`, `wally_theme.py`), nooit met de hand in de MIDI.
2. `python3 tools/grounded/music_lint.py sound/songs/midi/<nummer>.mid`: moet **OK** zijn.
3. **Controleren in batches** (Jordi): `python3 tools/grounded/maptools/batchrec.py <uitmap> MUS_A:90 MUS_B:120 ...` bouwt per 8 nummers één test-ROM en geeft per nummer overlopen/piek/audiocheck + preview-mp3. Een agent bouwt alleen zelf een test-ROM als een meting echt de game nodig heeft. Losse test-ROM: `python3 tools/grounded/maptools/testrom.py <map> "playbgm MUS_X, FALSE"`.
4. Opnemen: **`recpcm.py`** (uit de mixbuffer van de game, exact wat de GBA speelt; alleen DirectSound):
   `PYTHONPATH=tools/grounded/maptools python3 tools/grounded/maptools/recpcm.py <rom> <intro.bin> <k> <sec> <uit.wav>`.
   Heeft het nummer PSG-sporen, dan `recaudio.py` (emulator-audio, met glitch-reparatie).
   **Altijd ook recpcm over de hele lengte (+10 s): `overlopen: 0`.** De 8-bit-mixer klemt niet maar slaat om
   (-93 -> 123) = knapperen; dat zie je níet in recaudio/audiocheck (Zinnia, v0.9.60). Piek ≤ ±120/127 houden.
5. `python3 tools/grounded/maptools/audiocheck.py <uit.wav>`: geen pieken/clipping na de eerste 0,1 s, geen
   onverwachte constante tonen, RMS rond 700–2700 (Zarude ≈ 2700 = bovengrens).
6. mp3 maken (`ffmpeg -ss 0.1 ... -af afade=...`), `volumedetect`: max_volume onder −1 dB.
7. Pas dan naar Jordi (regel van Jordi: geen zoemtonen of andere dingen die gehoorschade kunnen geven).

## De engine (m4a)
- **Max. sporen per nummer = `NUM_TRACKS_BGM`** in `sound/music_player_table.inc` (vanilla 10, nu 16). Sporen
  daarboven worden stilletjes NIET gespeeld. Dat kostte Regigigas (16 sporen: koor/tuba/taiko/pauken/crash/klokken
  speelden nooit) en Mewtwo v3 (14: de drums vielen weg) veel tijd. De lint controleert dit nu.
- **Mixer op 21.024 Hz** (`src/m4a.c`, was 13.379): ±40% minder 8-bit-ruis ('vinyl'), door Jordi gekozen na A/B.
  Gemeten: geen extra lag in de overworld, 1–5 frames per 900 tijdens gevechtsintro's. Previews en metingen dus
  altijd met deze mixer; `recpcm.py` leest de frequentie uit de game.
- **12 DirectSound-kanalen** (`src/m4a.c`, was 5 in vanilla; elk kanaal kost ±1% CPU per frame). Muziek krijgt
  er max. **10** (`MAX_VOICES`/`MAX_CHANS`), zodat geluidseffecten (aanvallen, cries) geen muzieknoten afkappen. Meer noten tegelijk = kanaalroof: een nieuwe noot
  kapt een andere af. Dat hoort Jordi als **snips** / "overhaast eindigende maat". Ook uitklinkende noten (release)
  en lange drumnoten houden een kanaal bezet. PSG-sporen (vierkant/ruis/golf) tellen niet mee.
- **Uitklinktijd per instrument** = de release-byte in de voicegroup (envelope × rel/256 per frame; keysplits:
  zie `sound/voicegroups/keysplits/*.inc`). `musiclib.releases()` + `release_ticks()` rekenen het uit. Lange
  releases (overdrive 226) laten elke riffnoot ±250 ticks naklinken: geef zware gitaren een kortere release
  (160–170, strak en metal).
- Laat het arrangeerscript melden hoeveel noten per spoor wegvallen; > 3% bij een hoofdpartij = "instrumenten
  verdwijnen opeens" (Jordi over Wally 5). Dun eerst akkoorden uit (bas 1, cello 1, melodie 2, riff 2).
- Arrangeer met een **stemverdeler** (zie `wally_theme.py`: `MAX_VOICES`, `PRIORITY`, `thin()`): melodie > riff >
  drums > bas > harmonie. Akkoorden in bas/cello uitdunnen (bas = laagste noot, melodie = hoogste). Check het
  hele interval van een noot, niet alleen het startmoment.
- **Dubbele noten** (zelfde spoor, noot en tick) komen voor in aangeleverde MIDI's (Wally) en ontstaan ook als je
  drumnoten omzet (snare → tamboerijn). Altijd ontdubbelen, ook ná het omzetten: ze geven een volumepiek en kapen
  een kanaal.
- `voicegroup_grounded_gm`: programma's 24–31 zijn PSG-vierkanten (piepjes); `grounded_wally` heeft daar echte
  gitaren (24–27 nylon, 28–29 overdrive, 30 distortion hoog, 31 distortion laag) en op 78 een fluitje.
- `rs_drumset` begint op noot 36; PSG-drumnoten (piepjes): 37, 44, 49, 51, 52, 56, 58, 61, 63. Snare = 38,
  crash = 57, tamboerijn = 54, kick = 36, clap = 39.
- Noten onder E1 (28) op DirectSound klinken als een vervormde dreun; bas liefst E1–E3.
- **8-bit afronding per kanaal = de "overload"** (v0.9.240, gemeten): de mixer telt elk kanaal op in de 8-bit-buffer
  (`(vol*sample)>>8`, afgekapt), dus elk kanaal brengt eigen afrondingsruis mee: ruisvloer ±−32 dB onder het signaal,
  die met de noten mee aan- en uitgaat. Bij heldere nummers (Athletic) gemaskeerd, bij donkere/zachte (YI Overworld,
  Castle: origineel −53 dB) hoort Jordi "alsof mn speakers eraan gaan". Kanaalvolumes zijn ook in vanilla laag
  (mediaan 12–35 van 255). Tegengif: zo hard mixen als veilig kan (piek ±110), zachte zuivere partijen en bassen op
  PSG, of een 16-bit-mixer (HQ-mixer van ipatix: voorstel, wacht op Jordi). Meten: solo per spoor uit de mixbuffer
  (`scratchpad/ovl/solo2.py`-aanpak; de mGBA-audiobuffer heeft bursts die metingen vertekenen).
- **HQ-mixer (v0.9.245, op proef):** 16-bit mixen, één afronding met noise shaping, klemt i.p.v. omslaan.
  Gemeten: ruisvloer 1–8 kHz 4–6 dB lager (YI), kreten/geluidseffecten identiek, minder vertraagde frames (Rayquaza-
  gevecht 34 i.p.v. 46 per 2400). Volumes en pieken onveranderd, dus de mixregels (piek ±110) blijven gelden.
- **`voice_directsound_no_resample` speelt op de mixersnelheid (21.024 Hz)**, niet op de rate van de sample: een
  drum van 13.379 Hz (alle vanilla-kits) klinkt sinds v0.9.32 ±7,8 halve tonen hoger en 36% korter, een van 16 kHz
  +4,7. Eigen kits: `voice_directsound 60, ...` (speelt op toets 60 met de eigen rate).

- **Eigen samples max. 11 kHz** (v0.9.232, Jordi: A/B SickBlik "prima"): de mixer draait op 21 kHz/8 bit, hogere rates kosten alleen ROM. Drums (drumsets/) blijven; grondtoon ≥ C6 → 16 kHz. Na elke `*_samples.py`/`gm_samples.py` en elke merge: `python3 tools/grounded/resample_wav.py --all`. Akkoorden als één sample (SickBlik) klinken voller maar kosten ±30 KB per akkoord.

- **Rips (SPC/MP2K) op volume brengen (v0.9.240, gecorrigeerd):** de mixbuffer slaat pas om bij 128 (meet met `recpcm.py`, nu links én rechts). Richtwaarde: piek ±100–112 in batchrec. Lager laat de afrondingsruis van de mixer horen ("overload", zie De engine). SNES-samples eerst Gauss-filteren (`soften` in spc2gba.py) en de velocity schalen op de piek **ná** dat filter (drums verliezen tot 12 dB piek). Korte loops nooit rekken of verlagen (valse toon, zoem). Vergelijk met de GBA-versie uit een minigsf (gsflib = hele ROM, nummer op het adres uit de minigsf).

## Opnemen (valkuilen)
- De audiobuffer van mGBA moet **elke frame** worden uitgelezen, ook tijdens menu-navigatie; anders loopt hij over
  en neem je 16 kHz-ruis op (eerste Wally-previews: "gehoorschade simulator", terwijl de game in orde was).
- Het korrelige/"vinyl"-geluid is de GBA zelf (8 bit, 13.379 Hz mix). Zachte nummers laten die ruis meer horen:
  houd de RMS rond 1000+ (Wally 1 was 750 → "vinyl").
- mGBA (python-binding) geeft af en toe een burst van ~10 samples (0 / 15136 / 32520 om en om). In de game zit
  dat niet. `recaudio.py` overbrugt elke sprong > 12000 en controleert daarna dat er geen meer over zijn. Jordi hoorde ze als
  snips op 3 s en 12 s in álle versies; het tijdstip verschuift met de samplerate (48 kHz: 7,7 s), dus niet de game.
  **Snips op hetzelfde tijdstip in verschillende nummers = opname, niet muziek.**
- **Drumnoten niet inkorten** in de MIDI: een crash duurt in de bron 2 tellen, een snare ±¾ tel. Wally kortte ze in tot
  een 16e ('tweede beat kapt te snel af', Jordi op 7 s). Voor de stemverdeler telt de echte lengte.
- **Mixniveau:** de GBA mixt 8 bit; Wally gebruikte op -V090 maar RMS 6–11 van 128, waardoor de ruis opviel ('vinyl').
  Zet eigen nummers op -V110–127 en controleer met recpcm (geen samples op ±127).
- De eerste 0,03 s bevat een klik van het starten: knip 0,1 s weg.

## Smaak van Jordi
- **Catchy > veilig.** Een piepje oplossen door hele sporen weg te halen verloor in Zarude v2 de catchiness;
  zoek de ene foute noot (v10 = intro van v9 + loop van v1).
- Legendary-intro's: opbouw in sync met de gevechtstransitie (10–20 s), percussie die episch opbouwt, blazers pas
  na de transitie.
- Wally groeit mee: dezelfde iconische melodie, steeds zwaardere instrumenten. 1 = fluitje + akoestisch, traag,
  "wimpy"; 5 = heavy metal ("balls to the wall"). De "piano" in de ORAS-MIDI is eigenlijk een elektrische gitaar.
- Mewtwo (idee Jordi): euforische trance, melancholisch én evil (een onvrijwillige, imperfecte kloon); intro
  passend bij de Mewtwo-transitie; wisselt high-tempo stukken af met trance-stukken.
- Regigigas: het bestaande Regi-thema bombastisch remixen, met **Slow Start**: traag beginnen en versnellen naar
  het normale tempo, halverwege nog één keer afzwakken en vertragen ("bijkomen") en dan vol gas.
- Jordi geeft feedback met tijdstempels; gebruik die om noten op te zoeken (tick = s × 1e6 / tempo × tpb).

## Status per nummer
| Nummer | Script | Status | Waar in de log |
|---|---|---|---|
| Zarude | `zarude_theme.py` | goedgekeurd (v10) | "Zarude" |
| Wally 1–5 | `wally_theme.py` | goedgekeurd | "Wally" |
| Regigigas | `regigigas_theme.py` | wacht op Jordi (v5) | "Regigigas" |
| Mewtwo | `mewtwo_theme.py` | v3 | "Mewtwo" |
| Mew (remix van Mewtwo) | `mew_theme.py` | v3 wacht op Jordi (Mewtwo-arrangement, minder dreigend) | "Mew v1", "Mew v2", "Mew v3" |
| Dave (Freed From Desire) | `freed_theme.py` | goedgekeurd | "Dave" |
| Beasts (Raikou/Entei/Suicune) | `beasts_theme.py` | goedgekeurd | "Raikou", "Beasts" |
| Zinnia, Ghetsis, PSG-drumfixes | `midi_songs.py` | goedgekeurd | "Zinnia", "Ghetsis", "PSG-drums" |
| Keccles | `keccles_theme.py` | goedgekeurd (v3) | "Keccles" |
| Shaymin | `shaymin_theme.py` | goedgekeurd (v2) | "Shaymin" |
| Magikarp | `magikarp_theme.py` | goedgekeurd (v3) | "Magikarp" |
| Jirachi | `jirachi_theme.py` | goedgekeurd (v4) | "Jirachi" |
| Rayquaza (gamelan) | `rayquaza_theme.py` | goedgekeurd (v4) | "Rayquaza" |
| SickBlik | `sickblik_theme.py` | goedgekeurd (v2) | "SickBlik" |
| Ashfrost (winter) | `ashfrost_theme.py` | goedgekeurd | "Ashfrost" |
| Heatran | `heatran_theme.py` | v5 in de maak (Kyuss "Odyssey" x GBA) | "Heatran" |
| Mitch (DnB) | `mitch_theme.py` | v4 in de maak (v3-ritme/vorm 'spot-on'; luidere wobble, keiharde kit) | "Mitch" |
| Neo Plasma (BW2-remake) | `neo_plasma_theme.py` | v8 in de maak (noten/timing v7 'perfect'; GBA-soundfont-instrumenten) | "Neo Plasma" |
| Heatran | `heatran_theme.py` | v7 wacht op opname (v6 'saai': meerdere riffs, 74/130 bpm, palm-mutes/slides) | "Heatran" |
| Mitch (DnB) | `mitch_theme.py` | v7 wacht op Mitch (v6 'nog te goedkoop, ander instrument dan de horn'; alleen klanken: lead-synth A supersaw / B screech (standaard) / C vocal chop, `LEAD` bovenin) | "Mitch" |
| Neo Plasma (BW2-remake) | `neo_plasma_theme.py` | v9 in de maak (vette opening-run, valse noten B-sectie, brug) | "Neo Plasma" |
| Neo Plasma (BW2-remake) | `neo_plasma_theme.py` | v10 wacht op opname (glissando-intro, octaaffix orgeldeel, dikke bas, hats in de break) | "Neo Plasma" |
| Neo Plasma (BW2-remake) | `neo_plasma_theme.py` | v12 wacht op Jordi (noten v11, alleen stock-Emerald-instrumenten: trompet-lead, fingered bass, organ2, PSG, rs-kit) | "Neo Plasma" |
| Heatran | `heatran_theme.py` | v6 in de maak (from scratch, gemeten aan Jordi's Kyuss-mp3's) | "Heatran" |
| Mitch (DnB) | `mitch_theme.py` | v3 in de maak (duistere DnB) | "Mitch" |
| Neo Plasma (BW2-remake) | `neo_plasma_theme.py` | v7 in de maak (vol, gelaagd) | "Neo Plasma" |
| Victini, Darkrai, Genesect | `victini_theme.py`, `darkrai_theme.py`, `genesect_theme.py` | v3 (ronde 7), wacht op opname | "Victini", "Darkrai", "Genesect" |
| Gymleiders 1-4 (Roxanne, Brawly, Wattson, Flannery) | `gym_remixes.py` | Wattson goedgekeurd; Roxanne/Brawly/Flannery v2 (GBA-instructies), wacht op opname | "Gymleiders" |
| Victini, Darkrai, Genesect | `victini_theme.py`, `darkrai_theme.py`, `genesect_theme.py` | v2 (ronde 6), wacht op opname | "Victini", "Darkrai", "Genesect" |
| Gymleiders 1-4 (Roxanne, Brawly, Wattson, Flannery) | `gym_remixes.py` | Wattson goedgekeurd; Roxanne/Brawly/Flannery v3 (anti-kermis, half-time), wacht op opname | "Gymleiders" |
| Gymleiders 1-4 (Roxanne, Brawly, Wattson, Flannery) | `gym_remixes.py` | v1 in de maak | "Gymleiders" |
| Gymleiders 5-8 (Norman, Winona, Tate & Liza, Wallace) | `gym_remixes2.py` | Wallace, Norman goedgekeurd; Winona/Tate & Liza v3 (anti-kermis), wacht op opname | "Gymleiders" |
| Burglar (SIMON) | `burglar_theme.py` | v1 wacht op opname (noir-jazz-sluipen -> alarm -> achtervolging) | "Burglar" |
| Battle! Tapu | `tapu_theme.py`, `tapu_samples.py` | v6 GOEDGEKEURD en gekoppeld (Jordi, 6 okt) | "Tapu" |
| Ho-Oh (658) | `hooh_theme.py`, `hooh_samples.py` | v2 VOLDOENDE VOOR DE BETA (Jordi: "niet perfect maar voldoende"; na de beta evt. helderder/percussie). Was: (v1 'te vrolijk, trompet/fluit schel': E-klein hirajoshi, shakuhachi/koto/shamisen/taiko als eigen samples, geen trompet/whistle) | "Ho-Oh" |
| Forces of Nature (Tornadus, Thundurus, Landorus) | `forces_theme.py` | v2 GOEDGEKEURD (v1 'Megaman/SNES'; v2 volle GBA-orkestratie, Landorus 132 bpm battle-groove) | "Forces" |
| Lugia | `lugia_theme.py` | v2 GOEDGEKEURD (v1 'bijna helemaal goed'; v2 = accelerando 144->164 met drumopbouw op 30-33 s) | "Lugia" |
| Treasures of Ruin (683) | `ruinous_theme.py`, `ruinous_samples.py` | v6 wacht op Jordi (v4: intro goed maar 70 KB; v6: roep maat 5-12, hoge lijn 13-20, eigen strijkerknipsel legato; 367 KB samples) | "Ruinous" |
| Zacian & Zamazenta (684), Xerneas & Yveltal (685), Uxie/Mesprit/Azelf (686) | `legends3_theme.py` | v1 wacht op opname (eigen composities, alleen stock-samples) | "Legends3" |
| Area Zero (681) + Battle! Area Zero (682) | `areazero_theme.py`, `areazero_samples.py`; 682: `vs_areazero_theme.py`, `vs_areazero_samples.py` | 681 v10: begeleiding m1-64 + koor + aria uit het origineel; 682 v1: het origineel in 10 knippen (11025 Hz, DPCM) | "Area Zero" |
| Battle! Pokémon Tower (687) | `tower_theme.py` | v1 wacht op Jordi (Lavender-remix, 160 bpm, alleen stock-samples, alle gevechten in MAPSEC_POKEMON_TOWER) | "Tower" |
| Battle! Legendary Pokémon (670) | `legendary_theme.py` | v1 wacht op Jordi (generiek legendary-thema, Hoenn-stijl: Weather Trio-pauken, E4-koper, 176 bpm, alleen stock-samples) | "Legendary" |
| Battle! Arceus (676) | `arceus_theme.py` | v1 wacht op Jordi (noten 1-op-1 uit zijn DPPt-MIDI, alleen stock-samples, gekoppeld in de Hall of Origin) | "Arceus" |
| Battle! Dialga/Palkia (678) | `dialga_theme.py` | v1 wacht op Jordi (uit zijn MIDI, alleen stock-samples, ±9 KB) | "Dialga" |
| Battle! Ultra Beast (677) | `ub_theme.py`, `ub_samples.py` | v1 wacht op Jordi (eigen compositie, octatonisch/heeltoons, 7/8, glazen FM-lead met microtonale bends; alle UB-gevechten in Ultra Space) | "Ultra Beast" |
| Area Zero (681) + Battle! Area Zero (682) | `areazero_theme.py`, `areazero_samples.py` | v8: begeleiding m5-39 + koor + aria uit het origineel geknipt, 682 geschrapt (Jordi) | "Area Zero" |

Goedgekeurde nummers niet meer aanraken. Volgende kandidaten: `MUZIEK_KANDIDATEN.md` (repo-root).

## Kernlessen (samenvatting van `MUZIEK_LOG.md`)
**Meten i.p.v. gokken**
- Een geluid zoeken (puup, snip, brom): neem **sporen solo** op (volX = 0 op de rest, `balance.py` `gba()`, vensters
  0,25 s). Ghetsis' puup zat twee keer in een ander spoor dan gedacht.
- Balans/"klinkt niet als de bron": `solo_rms.py` (RMS per sectie per groep), `balance.py` (FluidR3-referentie),
  `balance_orig.py` + Spleeter-stems (tegen een opname van het origineel; beter dan een GM-render).
- "Schel": aandeel energie > 2 kHz / > 4 kHz per sectie én per partij (het zit vaak in één partij, niet in de mix).
  "Donker/vrolijk": chroma/Krumhansl per sectie. "Traag/recht": aanslag per 16e per band (spectrale flux).
- Sync met een transitie: `gMPlayInfo_BGM.clock` per frame naast de helderheid van het beeld meten.
- audiocheck-"constante tonen" verklaren: 59,7/119,5/179 Hz = framesnelheid (veelvouden); anders vaak een grondtoon
  (bas/kick/kendang). Controleer met een solo-opname.
- `recaudio` neemt twee keer op en vervangt mGBA-glitches; snips op hetzelfde tijdstip in verschillende nummers = opname.

**Stemverdeler en kanalen**
- Max. 10 DS-noten (11 legendaries) inclusief uitklinktijd; `allocate()` is gretig per partij in volgorde: belangrijkste
  partij eerst, nieuwe lagen áchteraan (dan blijven bestaande partijen identiek).
- Legato/staccato: `detach()` (vorige noot een uitklinktijd eerder los); nootlengte + release ≤ de afstand tot de
  volgende aanslag; lange pads/koren in stukken van 2 tellen. Dezelfde toonhoogte mag in één spoor niet overlappen.
- Eén sample voor een akkoord/voicing/unisono (powerchord, Rhodes-akkoord, trompet+sax, supersaw, ombak) = 1 kanaal.
- PSG (2 blokgolven, golf, ruis) kost geen DS-kanaal: arpeggio's, sub (golf: Data_8 klinkt een octaaf lager,
  niet onder ±32,7 Hz), hihat/shaker/riser/wind (ruis), delay-echo's. Niet als drumnoot in rs_drumset (PSG-puup):
  `drum_map`. Drumnoten buiten 36–64 lezen buren in het geheugen.

**Klank en register**
- Geen noten onder E1; koper (ook synth-brass) niet onder C3 (puuup). Bas een octaaf lager = sample een octaaf te hoog labelen.
- Liever het juiste instrument als eigen sample (FluidR3 via een eigen `<thema>_samples.py`) dan een "verwante" sample.
  Meet de helderheid van een GM-programma vóór je het kiest (klarinet 71 en muted trumpet 59 zijn schel).
- Eén sample per riffnoot als het spectrum moet kloppen (transponeren schuift alles mee). Drumkit-regels spelen de sample
  op de eigen toonhoogte. Gen 3-klank = lage samplerate, weinig hoog, gecomprimeerd.
- Pitch bend werkt (BENDR via CC20; BENDR 4 = 16 stappen per halve toon, zuiver). Bend terugzetten bij de volgende
  noot, niet bij de note-off. CC7 per sectie werkt (CC11 niet). Tempo: alleen even bpm, en de GBA speelt 0,45% te traag.

**Mix**
- recpcm: `overlopen: 0`, piek ≤ 120/127 (de 8-bit-mixer slaat om = knapperen). -V is niet lineair: altijd opnieuw
  meten. RMS via recaudio ±2000–3000; per sectie meten voor dynamiek.

**Vorm en smaak (Jordi)**
- Een genre = een vorm en een ritme, niet alleen een klank (Heatran v2/v3, Shaymin battle-waardig = ritme).
- Remix van een bestaand nummer: origineel 1-op-1 (sporen, volgorde, tempo), alleen instrumenten wisselen en lagen
  tóévoegen; nooit herschikken of inkorten. Melodie voorop en herkenbaar. Climax = structureel (extra sectie, toonsoort omhoog).
- Wat Jordi goedkeurde of "zo houden" noemt: niet aanraken, controleren met een diff per MIDI-spoor.
- Jordi geeft briefings punt voor punt (vaak via Gemini): volg ze letterlijk, maar controleer feiten (Neo Plasma-tempo
  is gemeten 176 bpm). Bij een vaag idee: doorvragen of twee varianten.
- Legendary-intro's in sync met de transitie; de cry van een wilde Pokémon klinkt ±2,3–3 s na de start (geen drop daar).
- Hoorveiligheid: geen constante zoemtonen, geen schelle pieken.

**Samenvoegen (voor de hoofdsessie)**
- Gedeelde samplehulpjes alleen uit `sample_utils.py`; nooit samples/functies van een ander thema gebruiken.
- Na elke merge alle `*_samples.py` en `*_theme.py` opnieuw draaien (byte-identiek) en labels/wav's controleren.

## Log (nieuw)
Nieuwe lessen kort hieronder, met de naam van het nummer vooraan. De hoofdsessie verplaatst ze geregeld naar `MUZIEK_LOG.md` en werkt de kernlessen bij.

### Feedback ronde 5 (Jordi, 5 okt middag)
- **Goedgekeurd:** Jirachi v4 ("geweldig, done"), SickBlik v2, Rayquaza v4 ("perfect"). Niet meer aanraken.
- **Heatran → v5:** gebaseerd op Kyuss' "Odyssey": traag sludge-stuk (~75 bpm) wisselt met snelle desert-pump (~135 bpm). Moet klinken alsof Kyuss de originele R/S-Heatran-baasmuziek op de GBA inspeelde: crunchy low-bitrate gitaarsamples (C-standard), doffe fuzz-synthbas die de gitaar volgt, doffe Gen 3-drums (doffe snare, blikkerige crashes). Geen moderne studioklank.
- **Mitch → v3:** v2 klonk als drukke chiptune/happy hardcore; alleen het stuk rond 1:00 had de juiste sfeer. Duister, minder pieperig (leads 1–2 octaven lager), less is more, two-step 172 bpm met keiharde droge snare + ducking, lage reese met portamento, intro → build-up → 1 tel stilte → drop.
- **Neo Plasma → v7:** te kaal/dun. Octaafverdubbeling van de lead, sub onder de bas, gesplitste arpeggio's L/R, staccato off-beat-akkoordstoten, four-on-the-floor met ghost-snares en 16e-hats met accenten (tempo blijft 176, bevestigd door Jordi).
- Heatran v4 (Jordi over v3: 'nog te netjes, helder en vrolijk; 100% Kyuss', met productieregels per punt): de regels
  letterlijk als keten in `heatran_samples.py`: nek-pickup + toonknop dicht (lowpass 900 Hz vóór de fuzz) ->
  asymmetrische fuzz -> **cocked wah** (bandpass 800 Hz, Q 4, +8 dB) -> SVT (shelf +11 dB < 220 Hz, +6 dB rond 700 Hz,
  2x 8-polige lowpass 3,6/4 kHz). **Een sample per riffnoot** (keysplit `keysplit_heatran`, 21.024 Hz = mixfrequentie):
  één C2-sample op Bb2 schuift het hele spectrum x1,8 omhoog (4 kHz -> 7 kHz); zo blijft 'niets boven 4 kHz' ook in
  de game waar. Gemeten (sample, aandeel energie): v3-powerchord 500-1k 7%, piek 281 Hz -> v4 42-68%, piek 707-891 Hz,
  > 4 kHz 0,0%. In de game per sectie (recpcm): refrein v3 500-1k 12-15%, > 2 kHz 7-10% -> v4 35-40%, 1,7-1,9%.
  Bas = exact dezelfde MIDI-noten als de gitaar, de bassample een octaaf te hoog gelabeld (klinkt C1 bij C2).
  **Samples van een ander thema kunnen gedeeld zijn**: SickBlik gebruikt de v3-drums (heatran_kick/snare/crash/
  floor_tom/open_hat/side_stick); niet hergenereren of weggooien (linkerfout), v4 heeft eigen `heatran_ky_*`.
  audiocheck 'constante tonen' 62-133 Hz = de riffgrondtonen C2/F2/G2/Bb2/C3 (pedaal op C), geen brom.
  -V086: 0 overlopen, piek 97/127, RMS 2862.
- Jirachi v4 (Jordi over het v3-tussenstuk: 'te donker/spookachtig, wil euforische uplifting trance'): **'donker' meten met
  chroma**: Krumhansl-toonsoort van het tussenstuk v3 = Bm (0,66), v4 = D (0,85); de drieklank per maat volgt nu de
  geschreven progressie (D-A-Bm-G, G-A-F#m-Bm). Lange glijdende vocals = spookachtig; korte stoten (3+3+2 achtsten) in
  stijgende akkoordtonen + een diatonische terts eronder = euforisch. Gated vocals in achtsten: gate 0,25 tel + release
  150 (= 23 ticks bij 164 bpm), anders bezet elke stem 2 kanalen (tsaw 25% -> 3% weggevallen). Heldere lead-arpeggio's
  op de PSG-vierkanten (sporen van fonkel-echo/speeldoos die dan zwijgen) kosten geen kanalen; delay-echo = dezelfde
  noten 3 16en later op vierkant 1. Laag minder dominant (kick-velocity -8, PSG-sub 56 -> 40): < 150 Hz 59% -> 48%,
  zwaartepunt 480 -> 653 Hz. -V100: 0 overlopen, piek 107/127.
- SickBlik v2 (Jordi: 'hybride van battle-urgentie en Steely Dan-jazzfunk; de slap bass zoveel mogelijk intact'): de
  v1-secties blijven noot voor noot staan (diff per basspoor per sectie: 0 verschillen, ook de bends) en er komen
  secties tússen (refrein 1 na de hook, virtuoos slap-deel + refrein 2 vóór de laatste hook). **Steely Dan-akkoorden
  als één sample per voicing** (rootless close voicings: Cmaj9, B7#9b13, Am9, D13, G-'mu', Fmaj7#11, F#m7b5, C-'Mu
  Major' C-D-E-G), gespeeld op de grondtoon uit de smpl-chunk (geen transpositie) = 1 kanaal per Rhodes-/blazersakkoord;
  de bas speelt de grondtoon. Pushes (akkoord op de '&' van 4) laten de eerste aanslag van de volgende maat vervallen,
  anders overlapt dezelfde noot in één spoor. Naadloze overgang = dezelfde drumgroove als A1 + de bestaande stop/basfill
  (Bb-B) die naar C oplost (bedrieglijke slot B7 -> Cmaj9). Jazzgitaar-octaven als één sample (GM 26, twee noten).
  FluidR3 Muted Trumpet (GM 59) heeft 20-30% energie > 5 kHz (harmon-zoem): lowpass 3,8 kHz. Partijen die een spoor
  delen (flageolet op deadP, jazzgitaar op talkbox) krijgen hun eigen CC7 bij elke wissel (`part_vol_fx`). Solo-RMS:
  tegenstem-trompet (1675) stond luider dan de gitaarmelodie (1307) -> CC7 55%. Geen samples van andere thema's: de
  Heatran-drums zijn als sb_* gekopieerd. -V112: 0 overlopen, piek 115/127, RMS 2431. audiocheck '81 Hz' = E2, de
  grondtoon die de bas het hele nummer pompt (zat ook in v1), geen brom.
- Rayquaza v4 (Jordi: 'balans trompet/melodie v3 precies zo; fellere kebyar-intro, breaks, gong ageng op de laatste tel
  van elke frase'): **breaks zonder de melodie aan te raken = in de rusten van de melodie** (rasterkaart per spoor per
  zestiende: in maat 8-19 rust de trompet van tel 4+ tot tel 2 van de oneven maat; maat 32-39 heeft geen melodie) en een
  `stop()` die alleen niet-beschermde partijen afkapt. Controle: diff per MIDI-spoor (lead/suling/PSG noot voor noot
  identiek) + solo_rms v3 vs v4 (melodie 893 vs 892, kotekan 565 vs 562). Een stemverdeler die gretig per partij werkt
  houdt de melodiepartijen exact gelijk zolang ze vóór alle nieuwe partijen in de volgorde staan; check met een
  `RQ_AT=<tick>`-dump wie de kanalen op een gat bezet (bar 8: vijf pauken tegelijk door uitklinktijden). Snelle
  unisono-figuren op de gedempte gangsa (release 140), niet op de gangsa (226): 8 zestienden in octaven = 12 kanalen.
  Gong ageng meten: RMS < 150 Hz in de eerste 0,2 s van elke tel, opname uitlijnen op de eerste aanslag (±0,04 s) en de
  tijdas x 60/59,73 (GBA-framerate; zonder dat schuift het na 30 s een halve tel). Onset-kruiscorrelatie over alle
  noten koos twee keer een andere offset (0,125/0,285 s): niet betrouwbaar bij een dicht 16e-raster.
  -V070: 0 overlopen, piek 112/127, RMS 2814; ageng +4,4..+7,7 dB (F/Eb-secties het zwakst), audiocheck 196 Hz = kendang G3.
- Mitch v2 (Jordi: 'ECHTE HYBRIDE episch Pokémon-baasgevecht x Chase & Status; de beat klinkt te recht/langzaam, mist de
  agressieve DnB-fundering; geen wandelende bas'). **Diagnose eerst meten:** het v1-patroon wás two-step (K 1, S 2,
  K 3-en, S 4), maar in de opname (aanslag per 16e per band, `diag_audio.py`-achtig: spectrale flux op het 16e-raster,
  gemiddeld over 8 maten) zaten de PSG-hihats 14 dB onder de kick, waren de 16den onhoorbaar (alleen de achtste 'en'),
  was de snare-aanslag 2-3x zwakker dan de reese-aanslagen in 150-1500 Hz en verdwenen de ghosts in de ruis. Je hoorde
  de lange basnoten op de kicks = halve snelheid. **Een DnB-beat staat of valt met hoorbare 16den en een snare met
  crack**: hihats als DirectSound-sample (FluidR3 + ruis > 6 kHz, 60 ms, accent 127/84/108/88, kost ±1 kanaal),
  snare = FluidR3 38+40 + ruisstoot 1,8-6,5 kHz door tanh x4 (de crack moet boven de trompet uit, die in dezelfde band
  zit), kick x0,85. Resultaat drop: hihats > 6 kHz +5 dB, snare-aanslag 2x de rest in 1,5-5 kHz, aandeel > 2 kHz van
  < 2% naar ±30%. Bas: 'bad-da-DAN' (16de, 16de, lang op de kick van 3-en) + pitch-bend-dives/-scoops (BENDR 12,
  terugzetten bij de volgende noot). Lead = de sc88pro-trompet-keysplit (de echte Pokémon-trompet) + een zaagtand-
  sample unisono (DirectSound, spoorvolume 84) + PSG-blokgolf unisono: solo gemeten t.o.v. de rest in 0,6-5 kHz van
  -1,4 dB (alleen trompet) naar ±+2 dB. Een hete snare liet de mixer omslaan (-V090: 100x overlopen, -V078: 6x) ->
  -V070: 0, piek 103/127. Crash vóór de leadlaag in de stemverdeler (anders viel 36% van de drop-crashes weg).
- Neo Plasma v6 (Jordi over v5: 'te ver doorgeslagen naar kale, schelle 8-bit; hoge tonen snijden, geen dynamiek/
  gelaagdheid'): **'schel' zat niet in het totaalspectrum** (v5 had boven 2 kHz zelfs iets mínder dan het origineel),
  maar in wélke partij het hoog draagt: bij v5 de PSG-lead (25%-blokgolf, > 3 kHz 5%, luidste groep) en vrijwel geen
  hihats/snare (drums 4-8 kHz 7-10 dB te zwak). Meet per solo-groep de banden (`bands.py`-achtig) naast de Spleeter-
  stems van het origineel. Fix: lead een octaaf lager op een warme DS-sample (puls 25% + 50% ontstemd, lowpass 3 kHz
  op C4; > 3 kHz 5,2% -> 0,6%), drums volledig DirectSound (909-clap, `unknown_close_hihat` op 16en, kick 7 halve
  tonen hoger) -> drums 4-8 kHz zoals de drumstem. **Een kitregel `voice_directsound 60` speelt de sample op de
  eigen toonhoogte**; rnd_kick (51 Hz, 55 ms) was een subdreun, de kick van het origineel zit op 65-200 Hz.
- 'Koper niet onder C3' geldt ook voor eigen synth-brass: de lage gitaarpartij (E1-B2) op een C2-brass-sample gaf
  30-60 Hz +5 dB t.o.v. het origineel; per octaaf omhoog tot >= C3 (en weg als het akkoord die toon al speelt).
- NNLS-gewichten (balance_orig) tegen een origineel met een ander leadtimbre zeggen 'lead -11 dB te luid': negeren
  als de opdracht 'melodie voorop' is; gebruik dan de solo-RMS t.o.v. de mix (lead -6,6, drums -4,8 ≈ drumstem -3,8).
- Genesect v1 (`genesect_theme.py`, industrial/big beat à la The Prodigy + hard techno, 144 bpm, E-frygisch; samples
  `genesect_samples.py`): motief = baslijn-riff (E E G E Bb A E E D | ... F F G E) in elk deel + een hook-lead erboven.
  Kanon (Techno Blast) op het witte scherm van de transitie (maat 1 = 4 tellen na de start: muziek ±25 frames vóór het
  beeld, wit op frame ±71 van de transitie), de cry valt in een riffmaat zonder drop. Hard-techno-rumble = kick door
  een ruisgalm, vervormd, lowpass 420 Hz, als losse kitnoot op de 16den ná elke kick (k-r-r-r, velocity aflopend).
  303 = zaagtand door een Chamberlin-SVF met cutoff per sample + tanh, twee samples (gewoon/accent) en een
  programmawissel per noot. Gemeten (recaudio, -V090): 0 overlopen, piek 114/127, maar RMS 3500-3900 en < 150 Hz 46-65%
  (kick + rumble + sub-octaaf in de bassample): sub-octaaf in de bas 0,8 -> 0,35, PSG-sub 52 -> 38, hats 92 -> 120,
  kick x0,88 en -V074. Alles boven 4 kHz bleef < 4,5%: met lowpass 7-8 kHz in de samples is industrial niet schel.
- Victini v1 (`victini_theme.py`, anime-overwinningsfanfare, 172 bpm, D-groot -> climax E-groot; samples
  `victini_samples.py`): intro op de transitie via een **tempokaart binnen maat 0** (tel 0-2 op 174, tel 2-4 op 224 bpm)
  zodat inslag (t = 32) en explosie (t = 48) precies op tel 3 en maat 1 vallen (aanname: route-transitie start ±25
  frames na de muziek, gemeten bij Jirachi; nog niet in de game nagemeten). **Powerchord als één sample** (FluidR3 GM 30,
  A2+E3+A3, auto-loop) + palm-mute (GM 28) = 1 kanaal per akkoord. Spiccato-keysplit met release 130 (16en = 1 kanaal),
  pauken release 200 (226 klonk door de stilte-tel vóór de climax). **De lint rekent uitklinktijden met de eerste
  tempo van het bestand** (hier 174): reken de tails in de stemverdeler met dezelfde bpm (+2 ticks), anders meldt de lint
  overlap van 1 tick bij gedetachte partijen. Geen test-ROM-opname (coördinator neemt samen op met batchrec.py).
- Darkrai v1 (`darkrai_theme.py`, eigen compositie, 7/8 (2+2+3) en in B 9-7-9-5, 150 bpm, E-klein; samples
  `darkrai_samples.py`): **ongewone maatsoorten = gewoon een tijdlijn van maten in achtsten** (`BARS`), mid2agb kent geen
  maatsoort. **Ontstemd = in de sample + pitch bend**: speeldoos met een kopie +22 cent gebakken (zweving) en per noot een
  bend van 10-40 cent (BENDR 2, 64 = 2 halve tonen, vaste seed); lange noten zakken weg (kromme band). Bends op een
  drone-spoor aan het eind van een sectie terugzetten (anders blijft de loop vals). **Achterstevoren klanken als samples**:
  `x[::-1]` van een FluidR3-noot/cluster/bekken (aanslag aan het eind = zuigt naar de tel; de noot een samplelengte vóór
  de tel starten), het hele wiegelied achterstevoren in één sample (op exact 4 maten geresampled = 1 kanaal), de Gen 3-cry
  achterstevoren op 0,8x. Ritardando via de tempokaart per achtste (even bpm). Opname door de coördinator (batchrec.py).

### Feedback ronde 5 (Jordi, 5 okt middag)
- **Goedgekeurd:** Jirachi v4 ("geweldig, done"), SickBlik v2, Rayquaza v4 ("perfect"). Niet meer aanraken.
- **Heatran → v5:** gebaseerd op Kyuss' "Odyssey": traag sludge-stuk (~75 bpm) wisselt met snelle desert-pump (~135 bpm). Moet klinken alsof Kyuss de originele R/S-Heatran-baasmuziek op de GBA inspeelde: crunchy low-bitrate gitaarsamples (C-standard), doffe fuzz-synthbas die de gitaar volgt, doffe Gen 3-drums (doffe snare, blikkerige crashes). Geen moderne studioklank.
- **Mitch → v3:** v2 klonk als drukke chiptune/happy hardcore; alleen het stuk rond 1:00 had de juiste sfeer. Duister, minder pieperig (leads 1–2 octaven lager), less is more, two-step 172 bpm met keiharde droge snare + ducking, lage reese met portamento, intro → build-up → 1 tel stilte → drop.
- **Neo Plasma → v7:** te kaal/dun. Octaafverdubbeling van de lead, sub onder de bas, gesplitste arpeggio's L/R, staccato off-beat-akkoordstoten, four-on-the-floor met ghost-snares en 16e-hats met accenten.
- Mitch v3 (Jordi over v2: 'drukke chiptune/happy hardcore; alleen rond 1:00 de juiste sfeer'): 1:00 in v2 = maat 44 =
  de wobble-sectie (two-step + lange wobble + thema). **Less is more = schrappen, niet dempen**: geen PSG-lead, geen
  16den-loopjes, geen stinger/luchthoorn/rewind; PSG alleen nog sub (golf) en riser (ruis). 172 bpm, koperstoten in
  octaven als één sample (`mitch3_brass_lo/hi`, F3-C5), melodienoten nooit op de snaretellen (4 en 12), anders
  verdwijnen ze in de ducking. **Ducking op de GBA** = CC7-dip per spoor op elke hoofdsnare (30 -> 55 -> 80 -> 100%
  in een 16de; VOL werkt ook op al klinkende noten en op PSG). **Portamento** = pitch bend op de starttick van elke
  reese-noot vanaf de vorige toonhoogte (max. ±12 bij BENDR 12) en in 6 stappen naar 0; de rise van de build-up
  eindigt een octaaf hoger, zodat de drop er (ook na de loopsprong) uit omlaag duikt. Meten van 'snare snijdt door':
  RMS in 40 ms na elke 16de, gemiddeld over de drop (`lvl.py`-achtig): v3-eerste mix snare 1,5-5 kHz +5..7 dB boven de
  rest, maar breedband maar 1-2 dB boven de off-beat-basstoten/koper -> reese 92 -> 80, koper 118 -> 100, stoten
  vel 120 -> 110, -V070 -> 080 (eerste meting -V070: 0 overlopen, piek 85/127).
- Heatran v5 (Kyuss' 'Odyssey' op de GBA; sludge 76 bpm met swing <-> desert pump 136 bpm): **'Gen 3-klank' = de echte
  Gen 3-samples** waar ze bestaan: lead `sd90_classical_distortion_guitar_high` (C4), feedback `sd90_classical_overdrive_guitar`,
  bas `sc88pro_synth_bass`, drums uit rs_drumset zónder de PSG-noten in een eigen kit (rnd_kick, rnd_snare = doffe snare,
  orchestra/trinity crash = blikkerig, sc55-toms). De Gen 3-gitaren liggen op C3/C4 (`distortion_guitar_low` = C3, de
  'power_chord'-sample rond C4); voor C-standard (C2) eigen samples gemaakt zoals een Gen 3-sample: hard gecomprimeerd
  (crest 1,8), 13.379 Hz, 8 bit, korte loop; spectrum gemeten tegen `distortion_guitar_low` (zwaartepunt 900-1300 vs 946 Hz,
  > 2 kHz 18-30% vs 16%). **Tempowissels:** mid2agb zet een TEMPO op de tick van het loopeinde ná de GOTO (wordt nooit
  gespeeld): zet het tempo van het loopbegin op de looptick zelf (dan staat het direct na het label). De lint rekent
  uitklinktijden met het eerste tempo; de stemverdeler in het script rekent met het snelste (meeste ticks).
- Neo Plasma v7 (Jordi over v6: 'kaal, dun, los zand'; GBA-lagen): lead op bronhoogte (DS) + octaaf lager op PSG-
  vierkant 1 (vel 96), sub op de PSG-golf, arpeggio B op PSG-vierkant 2 (16 ticks later, pan 85), off-beat-tweeklanken
  (np_stab) alleen uit brontonen (gitaar is meestal 16e-octaven = alleen grondtoon -> arpeggiotonen van die tel; geen
  secundes, niet in unisono-riffs), four-on-the-floor, snare 2/4 + ghosts, 16e-hats met accent op de kwart.
  **PSG-noten onder C2 (36) klinken allemaal als C2** (`MidiKeyToCgbFreq` klemt key <= 35): een sub-bas op de golf kan
  niet onder 65 Hz. **De game staat standaard op mono** (`optionsSound`): panning hoor je alleen in stereo; maak een
  L/R-splitsing ook in mono zinvol (ander timbre/kleine vertraging). Lagen op PSG kosten geen DS-kanalen: daarmee bleef
  de stemverdeler binnen 10 (melodie/bas/drums 0% weg). Tempo-check op de mp3 (fold-scherpte): 175,96 scherp, 150-155 vlak.

### Feedback ronde 6 (Jordi, 5 okt avond)
- **Heatran v5: "klinkt als vrolijke Mario Kart / ska-punk".** Vijfde keer dat het stoner-genre mis gaat zonder audioreferentie. Regels: alleen mineur/pentatonisch/blues, geen huppelritmes of vrolijke blazers; traag 75 bpm loodzware chug, snel ±130 bpm als stompende stoner-metal-trein (Green Machine / snelle deel Odyssey), níet ska/punk. Basis = het R/S Regi-gevechtsthema (`mus_vs_regi`) "door de shredder" met Kyuss-riffs. Volgende poging pas met een audioreferentie (mp3 van Jordi) en meetbare anti-ska-controles.
- **Mitch v3: "ECHT spot-on Chase & Status"**, ritme en structuur goed. v4: wobble ('wowowow') veel luider/agressiever, hardere kick/snare-transients, ducking op kick én snare.
- **Neo Plasma v7: ritme en timing perfect.** v8: alleen instrumenten (pulse-lead met lange release, strakke synth/slap bass, zachte pulse-arpeggio's, synth brass/orgelstabs, standaard GBA-kit).
- **Victini v1:** basis goed, maar nog niet euforisch/triomfantelijk genoeg → v2: jubelender koper met grote stijgende intervallen, key change in het tweede deel, buitelende arpeggio's/bells, octaafbas en snare-rolls naar de drops.
- **Darkrai v1: "heel goed, 80%".** v2: duisterder, Giratina-achtig: asymmetrische/wisselende maten, schurender (tritonus, ijzige akkoordwendingen), rauwe brass-stabs en lage drones; het wiegelied blijft als contrast.
- **Genesect v1:** klonk als een funk-groove → v2: keiharde snelle Prodigy-breakbeat, distorted bas/synths, industriële stabs, hoekige riffs, korte risers en harde drops.
- Gymleiders 5-8 v1 (`gym_remixes2.py`, samples `gym2_samples.py`, één voicegroup `grounded_gym2` + vier kits
  `drumsets/gym2_*.inc`): **het vanilla-gymleiderthema haalt de lint zelf niet** (tot 17 noten: pianotriller release 239,
  strijkers-16en 196, pauken 226 in maat 0-1). Fix zonder noten te schrappen: alle niet-drumpartijen `detach`en
  (aanslag/toonhoogte gelijk, lengte max. een uitklinktijd korter; het script controleert dat tegen het origineel) +
  eigen korte intro-varianten (piano1_84 rel 150, strings_72 rel 140, piano1_60 rel 200) -> 0% weg in alle vier.
  Akkoordlagen bij een remix: grondtoon = **laagste** basnoot per halve maat (de C-G-bas begint soms op G) en per halve
  maat checken op kleine secunden met de melodie; voicings zonder terts (G-A-Bb-D op C) passen bij zowel E als F.
  Trainermuziek op trainerId: niet in Frontier/Trainer Hill (eigen nummering botst met TRAINER_NORMAN_1 = 269).
- Gymleiders v1 (`gym_remixes.py`, remixes van `mus_vs_gym_leader.mid`; Roxanne power ballad 188, Brawly nu-metal 196,
  Wattson gabber 176, Flannery flamenco 196; samples `gym_samples.py`): **één script ontleedt het origineel één keer**
  (noten per spoor mét het programma op dat moment, grondtonen per halve maat uit de bas, ritme van pauken/snare) en per
  leider bepaalt een routeringsfunctie per noot het nieuwe instrument; de pauken worden kick/cajón, de snare blijft op
  zijn plek. **Riff-dyaden eerst analyseren**: de riff in maat 2-9 is afwisselend kwarten (C5-Db5-C5 = powerchord) en
  tertsen/tritonus (E-G, F-Ab, Bb-Db in maat 3/5/7); een powerchord op 'de bovenste noot' gaf daar G5 over C. Alleen
  kwart/kwint -> powerchord/rasgueado, de rest losse noten. **De vanilla Gen 3-piano (release 221-239) klinkt ±50 ticks
  na**: de intro-loop in zestienden bezette 10 kanalen; als losse samples (sc88pro_piano1_*) met release 150 opnieuw
  in de voicegroup. `fit()` (noot + uitklinktijd eindigt vóór de volgende aanslag) op bas/kick/chugs/rasgueado bracht
  alle hoofdpartijen op 0% weg. Controle: elke noot van spoor 1-3 komt met dezelfde toonhoogte (of toonklasse, bij
  powerchords/hoover) op dezelfde tick terug. Geen test-ROM (coördinator neemt op met batchrec.py).
- Mitch v4 (Jordi over v3: 'ritme/structuur spot-on; wobble luider/agressiever, kick/snare keihard + sidechain'): alleen
  klank/volume/CC's (diff per spoor: noten, programma's en bends identiek). **Diepe wobble ondanks distortion: eerst
  vervormen, dán het tijdvariante resonante filter** (Chamberlin-SVF, twee rondes over de periodieke loop = naadloos);
  filter vóór de tanh (v3) laat de LFO-diepte wegvallen. Pitch-LFO in een exacte loop: fase = cyc x (ph + D), D = integraal
  van (ratio - gemiddelde). Luid zonder pieken: tanh op het 99,7e percentiel + periodiek FFT-lowpass, 2x (crest 5,6 -> 2,1).
  Volume per sectie via de basis van de duck-curve (`reese_base`: CC7 118 zolang een wobble-programma klinkt). Ducking op
  kick én snare: dips eindigen waar de volgende begint. Solo in de game: wobble -1,3 dB t.o.v. alle rest, kick+snare +10,5 dB
  in 30 ms. -V070 -> 088 (piek 72 -> 92); -V100 liep over op de roffel-einden van de build-up (9,9/43,9/77,5 s).
- Neo Plasma v8 (Jordi: 'noten/timing perfect, alleen de instrumenten aan het GBA-soundfont koppelen'): **noten exact
  houden terwijl releases wisselen = de stemverdeler (en detach) laten rekenen met de oude releases**, de nieuwe releases
  niet langer dan de oude (anders faalt de lint), en pas daarna de lead legato maken (`trim_legato`: tot de volgende aanslag,
  maar ingekort waar anders > 10 kanalen klinken, uitklinktijden en de andere leadnoten meegerekend; 96% gelukt).
  m4a steelt bij te weinig kanalen eerst een kanaal in release (`ply_note`), maar de lint rekent conservatief: houd hem OK.
  Een vanilla-sample een octaaf lager = byte-kopie met root +12 (`gba_copy`, np_synth_bass). Gedeelde keysplit met een
  andere release = eigen voicegroup op dezelfde tabel (`keysplits/np_trumpet.inc` + keysplit_trumpet). Drumkit in
  GM-indeling (36/38/39/40/42/46/49/55) met stille DS-vulregels. recpcm -V092: 0 overlopen, piek 109/127.
- Heatran v6 (from scratch na 'Mario Kart/Bowser's Castle'; eerste versie mét audioreferentie): **eerst de referentie
  meten** (Spleeter 4 stems + librosa-autocorrelatie per stem + basic-pitch op de basstem). Odyssey: traag intro 77 bpm,
  daarna 94-96 bpm (snare om de 0,64 s, 8e-puls 188/min; 'snel' = de 8en, níet 130 bpm), Green Machine 90 bpm; gitaar-
  sustain (P20/P90 van de envelop) 0,55-0,63, gitaarstem < 250 Hz 49-72 %, hihat-accent 69-81 % op de tel, C-klein /
  G-frygisch, bas 56-78 % op de pedaaltoon. v5: 136 bpm (8e-puls 272/min = +45 %), riff gem. 0,36 tel (stoten), open hihat
  op de 'en', chromatische riffloopjes, gitaar < 250 Hz 12-19 % / > 2 kHz 18-27 %. **Die getallen zijn nu harde controles**
  (`stoner_checks()` in het script, generiek `music_lint.py --genre stoner --tonic C`; v5 faalt op 20 punten). Kyuss-
  sustain op de GBA: riffs níet detachen (legato, release 150) en de 2e gitaar als 'muur' (herhaalde chugs = één noot).
- Victini v2 (Jordi: 'euforischer, triomfantelijker'): thema met open sprongen (kwart+kwint = octaaf, octaafsprongen,
  top D6), hoorn in decimen (terts eronder - 12) i.p.v. tertsen = opener koper. **Key change midden in de melodie** =
  `SHIFT` per maat (E +2 -> F +3) + één scharniermaat met absolute akkoorden (B -> C7) en een dalende aanloop die via de
  leidtoon (E) op F oplost; terug naar D via stijgende hele tonen F-G-A. Buitelende bellen op de PSG-golf
  (`ProgrammableWaveData_5`, env 0/2/6/1) alleen in lange melodienoten (>= 6 zestienden), stijgende arpeggio's (8 16den
  over twee octaven) op vierkant 2, 32sten-risers en snare-roffels (16den -> 32sten) naar elke drop, octaafbas in
  achtsten: alles PSG of drums, dus de stemverdeler bleef gelijk (alleen pauken 17% weg, zoals v1).
- Darkrai v2 (Jordi: '80%, duisterder, Giratina-achtig'): bijwerken = lagen wisselen, de C-sectie (ritardando,
  achterstevoren wiegelied) onaangeroerd. Maten A 7-7-6-7-5-9-7-8, B 9-7-10-5-9-6-11-5, D 7-6-8-5-7-10-5-7; `fit()`
  kort een wiegeliedmaat nu van achteren in (de oude versie gaf bij 5 achtsten een maat van 6). **Rauwe koperstoten als
  één sample per voicing** (FluidR3 61+62, verminderd E-G-Bb-E en cluster E-Bb-E-F, tanh x3, 13.379 Hz) op één spoor
  met een programmawissel per noot (`ccs` 'prog'); een orgeldrone E1-Bb1-E2 (GM 19, gelust) verving de strijkerspads:
  strijkers 43% -> 4% weg, koper/drone 0%. 16 sporen = het maximum.
- Genesect v2 (Jordi: 'klonk als funk'): **`funk_meter()` meet waarom** (loop, MIDI): v1 kick op oneven 16den 18%,
  bas op oneven 16den 23%, ghost-snares 1,6 per maat, hat-accentspreiding 0,44 (118/70/96/74), octaaf-'pops' in de bas
  6,5% (E2 -> D3). v2: 0,027 (alleen de 16den-kicks van de build-up) / 0 / 0 / 0,097 / 0; het script weigert te
  schrijven als het weer 'funk' wordt. Recht achtstenraster, geen ghosts, roffels alleen als felle 16den/32sten
  (`genesect_roll2`), 152 bpm (maat 0 blijft 144 voor de transitiesync), overstuurde bas `genesect_dbass` (tanh x6),
  tritonusstoot `genesect_istab`, kick2/snare2 (tanh x5/x7; de 909-clap zit ín de snare: los clappen kostte een kanaal),
  risers (ruis + sirene-bend) en een 16de stilte vóór elke drop (`stop()`).
- **Gymleider-remixes ronde 1 (Jordi):** Wattson en Wallace "fenomenaal, done" (niet meer aanraken). Roxanne, Brawly, Flannery, Norman, Winona, Tate & Liza: tweede ronde met concrete GBA-instructies per leider (tekst in de agent-opdracht): echte Emerald-samples (rock-snare, overdrive/slap bass, distortion/nylon/finger bass, pizzicato, synth bass, dance-kick), PSG-ruis als aanvulling (gated snare, double kick, castagnetten), dual-guitar-tertsen + vibrato (Roxanne), off-beat-staccato-chugs + scratches (Brawly), rasgueado-arpeggio's (Flannery), walking bass + ride + brass-stoten (Norman), geen brass (Winona), psy-bas op de PSG-golf in 16en + melodie als 16e-arpeggio's met sweeps op 138–145 bpm (Tate & Liza).
- Gymleiders ronde 2 (Roxanne, Brawly, Flannery; `gym_remixes.py`, Wattson byte-identiek: md5 van MIDI/voicegroup/kit/
  samples vóór en na): **'echte GBA-samples' = de vanilla-labels, maar let op de opgenomen toonhoogte** (autocorrelatie):
  distortion_high/overdrive/slap_bass/fingered_bass = C4 op toets 60 (klopt), distortion_low en nylon_str_guitar = C3
  op toets 60 (klinken een octaaf lager dan geschreven) -> byte-kopie met label 48 (`COPIES` in `gym_samples.py`).
  Emerald-kit: kick `drum_and_percussion_kick` (96% < 150 Hz; `trinity_big_boned` is een bas), rock-snare
  `sd90_solo_snare` (na 9 ticks afgekapt = gated), side stick/rimshot = dezelfde snare hoog (kitregel
  `voice_directsound 70/77`, decay 200/170, sustain 0). Geen castagnetten/seashore/scratch in de bank: PSG-ruis.
  **Dual lead**: terts onder de melodie, maar de sext eronder als de terts een kleine secunde/none/grote septiem maakt
  met de rest van het origineel op dat moment (69 noten: 57 tertsen, 12 sexten). **Arpeggio-rasgueado**: `fit()` per
  noot kapt een slag (noten 1 tick na elkaar) na 3 ticks af; fit per slag (`group`). Rasgueado-release 50, voorslagen
  2 noten van 1 tick, palmas-ghosts als aparte partij áchter de gitaar in de stemverdeler (accenten 0%, ghosts 11% weg
  onder de rasgueado's). Staccato-chugs (2 ticks, release 70) haalden Brawly's bekkens van 12% naar 1% weg.
  PSG-ruis-sweeps = één `voice_noise`-noot (sustain 15, release 0) met BENDR 24 en een bend-curve (de ruistoets
  telt mee: 21-80).

- Gymleiders ronde 2: Norman, Winona, Tate & Liza v2 (`gym_remixes2.py`, samples `gym2_samples.py`). **Een
  goedgekeurd nummer dat een voicegroup deelt: niet die voicegroup aanpassen maar de anderen een eigen geven**
  (`grounded_gym2_norman/_winona/_tate`, zelfde basis 0-91, eigen instrumenten 92-126, kit op 127); Wallace' MIDI,
  `grounded_gym2.inc` en `gym2_wallace.inc` bleven byte-identiek (git diff leeg). **'Gelaagde akkoorden op de echte
  Emerald-samples' = de vanilla-wav per toon transponeren en optellen** (`layer()`: smpl-chunk lezen, toon m klinkt
  bij rate x 2^((m-key)/12), loop uitrekken voor sustain): brass section = hoorn-grondtoon + 3 trompetten, pizzicato-
  akkoorden, één kanaal per stoot. Walking bass = kwarten uit de grondtonen per halve maat + chromatische nadering
  van de volgende grondtoon. **PSG-golfbas onder C2**: eigen golf met één periode per 32 stappen
  (`ProgrammableWaveData_gym2_saw`) klinkt een octaaf lager dan genoteerd; noteer +12 (m4a klemt PSG-toetsen < 36).
  PSG-lead op blokgolf 1 = alle tegenstemmen op blokgolf 1 naar DirectSound (anders stelen ze de lead). Melodie
  als 16e-arpeggio's: melodienoot op zijn eigen tick + op elke tel, daartussen akkoordtonen; controle = elke
  (tick, toets) van het origineel zit er nog in.
- **Ronde 7 (Jordi):** Heatran v6 "te saai, statisch" → v7: meerdere actieve riffs met palm-mutes/slides/bends, ±130 bpm snel deel, stops en tomfills (de 'saai-afdwingende' controles weg, anti-ska-controles blijven). Mitch v4 "95%": lead zachter, bas/growl + snare luider. Neo Plasma v8: intro-run vetter, valse noten in de B-sectie, bridge niet stilvallen. Victini v2: intro rommelig. Darkrai v2: mist een climax. Genesect: v2 (Prodigy) afgekeurd, terug naar v1 ("cyber-funk") maar strakker.
- **Previews altijd vanaf 0 s** laten beginnen (of de offset noemen): Jordi geeft tijdstempels; de Neo Plasma-preview begon op 13 s, waardoor zijn "intro" eigenlijk het loopbegin was.
- **Gymleiders ronde 3 (Jordi):** Norman goedgekeurd (+ Wattson, Wallace). Roxanne, Brawly, Flannery, Winona en Tate & Liza klonken alle vijf als "kermis/ska/circus": waarschijnlijk doordat begeleidingssporen van het origineel (PSG-tegenlijnen, koperstoten, pizzicato) bleven meespelen of een vrolijk instrument kregen. Bij een genre-remix: alleen de melodie (+ harmonie als skelet) van het origineel houden en alle begeleiding opnieuw bouwen; anti-kermis-controle in de scripts. Referenties: Stemm "Face the Pain" (Brawly), Hallucinogen "LSD" (Tate & Liza) in `scratchpad/gymref/` (niet in de repo).
- Victini/Darkrai/Genesect v3 (ronde 7): **'intro rommelig' = te veel snelle lagen tegelijk** (roffel + strijkers-rip
  + 32sten-riser + 16en-spiccato): Victini maat 0-3 nu koperstoten op de tellen, begeleiding op de kwarten; de loop is
  noot voor noot v2 (diff per MIDI-kanaal vanaf maat 4: 0 verschillen). **'Kabbelt' eerst meten**: recaudio-RMS per
  sectie Darkrai v2 A/B/D = 3085/3202/3517 (1 dB verschil); v3 climax halverwege (A-B-R-D-C), MIDI-niveau
  (vel x CC7)^2 per sectie: A +1,1 / B +2,0 / R -4,5 -> +5,8 / D +5,8 dB. Genesect: v1 byte-identiek teruggezet uit
  git, dan alleen ghosts/fills/stops/crashes; `groove_checks()` bewaakt dat de swing blijft.
- Heatran v7 (Jordi over v6: 'veel te saai, statisch, eentonig'; recept Odyssey: dreigende slide-intro -> felle
  drumfill -> 130 bpm, afwisseling slopend/beukend, meerdere riffs, palm-mutes, slides/bends, crashes, stops,
  tomfills). **Controles die een fout moesten voorkomen kunnen de volgende afdwingen**: v6 haalde 'niet ska' door
  minimale nootlengte, max. hihats/s, pedaaltoon en een stilstaande bas te eisen = saai. Nu blijven alleen de
  anti-ska-regels (toonladder, geen grote terts, geen skank, geen open hihat op de 'en', geen chromatische loopjes van
  4+, recht raster, accent óp de tel) en komen er 'niet saai'-regels bij (`stoner_checks` + `music_lint.py --genre
  stoner`): >= 3 riffs, >= 2 tempowissels per loop, stop/fill vóór elke riffwissel, palm-mute >= 40% van de 8e/16e-
  aanslagen, slides/bends/min, max. 10-15% lange akkoorden, crash op elke sectiestart, >= 3 tomfills; v6 faalt nu op
  10 punten, v5 op 16. Referenties (Spleeter, `riffs.py`): drums 65-68% óp de tel, 22% 'en', 9-12% 'a', 0% 'e';
  bas 2-2,5 sterke aanslagen/tel over alle 16en, 19-41 slides/min. **Palm-mute + open op één spoor** = programmawissel
  per noot (28 palm-mute-keysplit op dezelfde `keysplit_heatran`-tabel, 30 open), slides = BENDR 12 + bend-ramp aan
  het eind van de noot (zelfde events op gitaar, muur en bas). Palm-mute-sample: GM 28 door de stoner-keten + chug-
  envelop (30 ms, dan exp. 70 ms), noot 14 ticks + release 100 = 1 kanaal per 16e. Stemverdeler: 0% weg (11).

- Mitch v5 (Jordi over v4: '95%; bas moet baas zijn, lead 20-30% zachter, kick/snare harder en droger, kortere diepere
  sidechain'): **'bas luider' en 'drums harder' botsen**: de eerste v5-mix (reese CC7 112 op samples die al +6 dB
  luider waren) gaf kick+snare in 30 ms nog maar +6,5 dB boven de rest (v4 +10,5). Niet nog een test-ROM: **solo-opnames
  (recpcm + volX = 0, `solopcm.py`-achtig) zijn additief** (som = de mix, r 0,996; negeer de eerste 0,5 s) en laten zich
  offline met gains mengen. Ducking van 1-2 frames werkt (bas -10 dB op de slag, terug in ±30 ms). Merges kunnen een
  -V terugzetten (Heatran v6 zette Mitch -V088 terug op -V070): midi.cfg na elke merge per nummer controleren.
- Neo Plasma v9 ('valse noten in de B-sectie'): **eerst de eigen lagen controleren** (`pccheck`: per uitvoernoot de
  toonklasse t.o.v. de brontonen die dan klinken): de v7-off-beat-stoten met 'het laatste akkoord tot 2 tellen terug'
  schuurden in 49 van 79 gevallen (C4 tegen C#/D). Daarna de bron tegen de opname: harmonische salience op de
  Spleeter-stem 'other'+'vocals' (veel schoner dan de mix) vond twee transcriptiefouten in binnenstemmen (G4 i.p.v. A4
  in maat 32-33, G3 in kwintakkoorden). Een mono lead + uitgedund arpeggio kapt aangehouden akkoordtonen af (107 tonen;
  het Bb-akkoord in maat 35 klonk zo als F): meet de dekking per bronnoot. Previews: Jordi's tijden + preview-start!
- Winona/Tate & Liza v3 (Jordi: 'kermis/circus'): **oorzaak gemeten** (`kermis_check()` in `gym_remixes2.py` op v2): de
  originele PSG-sporen 4/5 bleven op blokgolf en speelden de melodie een octaaf hóger (tot C7: 26-36 noten > C6, 21-36%
  van hun noten boven de melodie), plus celesta/piano/buisklok/tamboerijn/pop-pluk/zaps, en 6-8% van de nootduur op E/A
  (C-mixolydisch = vrolijk). v3: alleen melodie (+ B-motief spoor 4) en grondtonen blijven, modaal verduisterd (Winona
  C-eolisch, Tate C-frygisch = het B-deel van het origineel), alle begeleiding nieuw; het script faalt op die vijf punten.
  Referentie 'LSD' (Spleeter): 137 bpm, bas alleen op 16en 2-4, hats op alle 16en, leads 2,5 aanslagen/tel in D3-C#5.
- Gymleiders ronde 3 (Roxanne, Brawly, Flannery 'kermis/ska'; `gym_remixes.py`): **oorzaak gemeten met `kermis_meter()`**
  (op de v2-MIDI's): (1) de drie PSG-sporen van het origineel speelden 1-op-1 mee (vierkant-arpeggio's in achtsten,
  20-35% van de melodietijd bóven de melodie); (2) spoor 1 = de hoorn/trompet-tweede stem in tertsen/sexten (een
  blazerssectie) bleef als tweede gitaar/strijkers/viool, plus piano; (3) de bas van het origineel is een **hoempa-bas**
  (grondtoon op de tel, kwint een octaaf hoger op 94% van de 'en'-noten) met de snare op 2 en 4 van 188-196 bpm =
  polka/ska; (4) Brawly's chugs 163x op de 'en' tegen 100x op de tel (skank); Flannery's nylonmelodie in trémolo (mandoline),
  percussie op het gestippelde paukenritme, PSG-castagnetten van 2 ticks en een snare met sustain 0 = stotterend;
  Roxanne's sd90_solo_snare ringt op 553 Hz (piek/mediaan 54 = 'tonk') en werd na 120 ms gegate + PSG-ruistik.
  **Fix: alleen de melodie (`melody_src`: per sectie het spoor dat hem draagt; noot voor noot gecontroleerd) + grondtonen/
  akkoordkwaliteit per halve maat houden, alle begeleiding nieuw en in half-time** (gevoelde tel = halve maat: 100/108/104
  bpm). `kermis_meter()` weigert te schrijven bij blazers/fluit/klokjes/orgel/piano/strijkers/PSG-tonen, > 1 aanslag op de
  'en' per aanslag op de tel of > 25% maten zonder tel 1 (begeleiding), hoempa (> 25% 'en'-sprongen omhoog in de bas),
  < 85% maten met kick op 1, of tegenlijnen boven/in het register van de melodie. Een rasgueado-roffel die 9 ticks vóór de
  tel begint telt als 'op de tel'. Strums als één sample per slag uit de Emerald-nylon (getransponeerd per snaar,
  `nylon_strum`): 438 slagen, 0% weg. Rock-snare `gym_rox_rsnare`: Power-snare + vel 185 Hz + kamernaklink, -20 dB na 0,54 s,
  piek/mediaan 16. Brawly-referentie (Face the Pain, librosa): ±112 bpm, kick 2-2,7 en gitaar 1-2 aanslagen per tel
  (gesyncopeerde zestienden), 49% < 250 Hz; Spleeter werkt hier niet (typer-fout).

- Brawly v4 (Jordi over v3: 'speelgoedaccordeon/fluitje + akoestische tokkels, onhoorbare bas, blikken kick, scratches
  weg'): **oorzaak gemeten met solo-opnames in één test-ROM** + klankvergelijking (`gba_sim.timbre_rank(..., audio=solo)`:
  dezelfde noten met elk GM-instrument via FluidR3 gerenderd, MFCC-afstand): de chugs (gym_bra_epower, 2 ticks + rel 70
  = ±40 ms) lagen het dichtst bij mondharmonica/tango-accordeon, de bas (5 ticks) bij pick bass/pizzicato, de lead bij
  piano/koper (= Jordi's 'koper/synth-lead'); de scratch was een koor-'aah' met sinusvormige snelheid = zuivere
  glijtoon (flatness 0,005, ±900 Hz) = glijfluitje. Kortom: korte stoten van een aangehouden GBA-distortionakkoord
  zonder plectrumaanslag klinken als riet. `kermis_meter` keurt nu af: tonale kit-effecten (flatness < 0,03 en > 400 Hz),
  en met `metal=True` begeleidingsnoten < 110 ms (incl. uitklinktijd) en een lage laag die < 80% van de loop klinkt.
  De GM-klankvergelijking is alleen info: hij noemt elk vervormd GBA-akkoord 'koper/zaagtand' (ook FluidR3-distortion).
  Fix: palm-mute-sample met plectrum + dichtklappende lowpass, muur-powerchords (tweede Emerald-distortion) op tel 1 en
  elke akkoordwissel, overdrive-bas uit de Emerald-fingered bass in achtsten, PSG-ruis open hats (. x . x), breedbandige
  scratches alleen op de overgangen. Bas t.o.v. lead +40%, t.o.v. drums +34%, t.o.v. de rest +25% (de muur is erbij).
  -V068: 0 overlopen, piek 81/127, RMS 2960. Restverschil met Face the Pain: < 60 Hz 2,5% tegen 11-19% (subkick).
- Neo Plasma v10 (Gemini-feedback over v9): **eerst de preview-start vaststellen** (hier 0 s: Gemini's 'arpeggio's
  0:10-0:30 goed' = de farp van maat 7-22, '1:08' = het orgeldeel maat 50). **Octaaffouten in een transcriptie** vind
  je met `octcheck` (per maat: CQT van de Spleeter-stem 'other' op de noot vs. een octaaf lager/hoger; lage noten
  kloppen niet, die zitten in de basstem): orgel/saw/sinus in maat 50-62 een octaaf te hoog (10-16 dB). 'Hol piepje' =
  te weinig grondtoon in de sample (sc88pro_synth_bass: 17% op f0, 46% op 2f0 = klinkt een octaaf hoger): grondtoon als
  sinus erbij, fase uit de FFT van de loop, exact 16 perioden per loop. Glissando = één noot per stuk ladder met
  pitchwheel elke 16 ticks (BENDR 12, ±12 halve tonen; mid2agb schrijft BEND + running status). **Mix-varianten
  meten zonder extra ROM**: volX (MusicPlayerTrack +19, standaard 64, x = vol*volX>>5) per spoor elke frame zetten +
  vlag 0x03 (anders pakt m4a het niet op) bootst CC7- en -V-wijzigingen exact na in recpcm/recaudio. -V064: 0
  overlopen, piek 86/127, RMS 3157; < 150 Hz in de brug 42% (met de dunne bas 34%, origineel 52%).
- Burglar v1 (`burglar_theme.py`, samples `burglar_samples.py`, kit `drumsets/burglar.inc`; noir-jazz-heist, D-klein):
  swing 150 bpm (de 'en' op 2/3 van de tel: `tick()`), accelerando per tel 152-174 in de twee alarmmaten -> 176 recht,
  ritardando terug; tempo van het loopbegin op de looptick. Anti-kermis als harde controle in het script
  (`anti_kermis()`: geen begeleidingsnoot boven de klinkende melodienoot, voor de alarmstoot de bovenste toon van de
  voicing; geen bas-sprong >= 5 halve tonen omhoog op een 'en'; PSG-sirene alleen waar de melodie rust). Alarmstoot =
  één sample per voicing (bari D3 + koper D4/Ab4/C#5, tanh + stootenvelop: FluidR3-koper zwelt anders aan, piek pas op
  0,43 s). Vingerknip gesynthetiseerd (ruis door bandpass 2,3 kHz, 35 ms). FluidR3 Brush-kit = bank 128 prog 40.

- Brawly v5 (Gemini noemde muur, bas en open hats 'ontbrekend' terwijl v4 ze had): **meet hoorbaarheid A-gewogen per
  solo-spoor** (emulator-audio met volX = 0 op de andere sporen, incl. PSG): lead 74% van de waargenomen luidheid,
  muur 15%, bas 7%, hats 0,4%. Oorzaken: (1) **`gba_tone(..., base)` = de echte toonhoogte van de bronsample op zijn
  eigen samplerate** (FFT meten, niet afleiden uit de samplerate): sc88pro_fingered_bass klinkt C4, sd90_..._low C3
  (toets 60!); v4 gaf base 36/60 en de bas klonk twee octaven te hoog (C4 met label C2), de chug een octaaf te laag;
  (2) muur op volume 62; (3) PSG-hats: -V schaalt ook PSG, decay 2 tot 0 + release 0 + 8 ticks = tik van 90 ms op
  ±5/15; (4) kick van 6 ticks kapt zijn subtoon af. v5: bas op echt C2 (grondtoon + grom 250-1300 Hz, nog eens zacht
  geklemd), muur dikker (lage distortion erbij, HPF 105 Hz), hats decay 1/sustain 5/release 1 op 18 ticks vol 127,
  kick 16 ticks, lead 106 -> 68, chugs 84 -> 60, -V076. In-game: hats 15% (>6 kHz 2,8% = Face the Pain), bas/lead
  A-gewogen 0,10 -> 0,23, < 60 Hz 2,4 -> 7%, 0 overlopen, piek 88/127, RMS 3231 (iets boven 3000).
- Neo Plasma v11 (Gemini: 'theremin met vibrato op de lead, houtachtige tik-bas'): **de 'vibrato' zat in de sample, niet
  in bends** (die gingen terug naar c_v+0): `sc88pro_square_wave` is zelf een gechorusde blokgolf (7-10 dB tremolo op
  1,7-5 Hz, zwaartepunt schommelt 28%, 93% energie op de grondtoon = fluittoon); meet een lead-sample met
  `sample_tremolo()` (neo_plasma_theme.py, nu een harde regel). 'Tikkende bas' = 16en van 27 ticks door detach met een
  lange release: korte release (50) + langere noot geeft dezelfde kanaalbezetting. **Spleeter-model leeg** (download
  faalde: h2/302) geeft 4 identieke stems zonder fout: md5 controleren; model met curl -L van de GitHub-release halen.
- Brawly v6 (Jordi schrapte v1-v5; 'hi-hats als vervelende snare'): opnieuw als Rocky/Eye of the Tiger, alleen stock
  samples, geen PSG/hats, max. 5 lagen (`brawly_check()` i.p.v. kermis_meter, dat koper/bellen verbiedt). **CC7 werkt
  niet lineair op de waargenomen balans**: lead 100 -> 67 (-3,5 dB) haalde zijn A-gewogen aandeel maar van 63 naar 50%.
  Stock-toonhoogtes (FFT) op toets 60: distortion_low, trinity_big_boned/30303 = C3; tubular_bell, trompet_60 = C4;
  fingered bass C4 (C2 = toets 36, in de game gemeten Bb1 = 59 Hz). Emerald heeft geen synth-brass: trompet+hoorn (56/60).
- Neo Plasma v12 (Jordi: 'kapotte speaker'; alleen stock-instrumenten): **instrumenten wisselen zonder de noten te
  raken** = de stemverdeler laten rekenen met een bevroren release-tabel (V11_REL) en dan pas de voicegroup vervangen.
  **Klinkende hoogte van stock-samples meten** (harmonic product spectrum): fingered/synth bass, trompet, square_wave
  klinken op de geschreven noot, sc88pro_organ2 een octaaf lager. Een keysplit in een eigen bestand
  (`keysplits/<naam>.inc`): musiclib/lint lezen de release alleen uit `<naam>.inc` (anders 200 = valse DS-overload).
  rs_drumset-releases (kick 242) bezetten kanalen: release per kitnoot overnemen van de oude kit.
- Tapu fase 1 (`tapu_theme.py`, alleen noten/ritme; geen MIDI van de bron): **eerst het raster vastleggen** (tempo via
  onset-autocorrelatie over 128 tellen = 174, loop via zelfgelijkenis van mel-spectra = lag 82,80 s = 60 maten, maat 1 =
  eerste slag) en daarna alles per 16e meten: drums per band (laag/mid/hoog, envelop-sprong), bas via basic-pitch op de
  stem, chant via CQT van de vocal-stem per 16e (pyin faalt op koren: 'onstemhebbend'). Transcriptie controleren met
  chroma-correlatie per maat (eigen solo-render vs. stem) en onset-correlatie per 4 maten (drums).
- Tapu v2 (Jordi: 'game_e_alles lijkt totaal niet, terwijl de fluid-drums kloppen'): **solo-opname in de game** (volX = 0
  op de andere sporen, mixbuffer) liet zien dat de drums er wel waren maar als tikjes: drumnoten van 2-3 zestienden
  + release 140 op stock-trommen van 0,3-0,4 s (drumsolo maat 1-8: 3-25 dB vs. drumstem 26-32 dB, onset-correlatie
  0,04-0,76). FluidR3 negeert note-offs op drums, de GBA niet. Fix: eigen samples (FluidR3 Taiko + gesynthetiseerd vel
  met dalende toonhoogte + velslag + ruimtegalm, ±1 s, `tapu_samples.py`) en `ring_gates()`: een slag klinkt door tot
  RING of de volgende slag in dezelfde partij -> per maat 25-34 dB, correlatie 0,6-0,9. **Kanaalbezetting nalopen met
  een kanaallog** (gSoundInfo.chans per frame: spoor, noot, envelop) i.p.v. gokken op kanaalroof.
  **Eerst de vorm uit Jordi's beschrijving op de opname leggen**: v1 dacht dat de mp3 met de HIT begon; de chant loopt
  0,9-5,8 s (maat 1-4), de 'HOO' + slag valt op maat 5 (6,26 s) en het 'TUDUDU'-'deuntje' is het taikomotief van
  maat 9 (16e 0,2,3,4 | 8,9,12,14), geen melodie (de tonale stems hebben daar alleen een tremolo). Stemmen zonder
  opname-audio: additieve formantsynthese (harmonischen x formanten van een klinker, groep van 4-6 ontstemde stemmen,
  ademruis), 16en-chant legato (geen detach: dat maakte stipjes). Het 'fluitje' (maat 41-48) waren korte E6-tikjes,
  geen kwarten: 1 zestiende op een staccato-fluit. -V082: 0 overlopen, piek 96/127, RMS 3134 (drums bewust luid).
- Ho-Oh v1 (song 658, eigen compositie, 180 bpm): **grondtoon van stock-samples meten** (harmonischenreeks, niet
  alleen autocorrelatie: die vindt een suboctaaf): shakuhachi en koto_high klinken C5 op toets 60, whistle C6,
  koto_low C4, distortion_low C3 -> per instrument een OCT-verschuiving in het script, noten op klinkende hoogte.
  **Drums in de stemverdeler per sample**: bezet = min(lengte sample, noot + release) (rnd_kick 12 ticks, taiko 60,
  laag gestemde taiko 90; geloopte toms/bekkens = noot + release); met één staart voor de hele kit viel 65% van de
  strijkers weg. Koto/shamisen in 16en: release 90 + noot tot 'volgende aanslag - staart' = 1 kanaal. -V090: 0
  overlopen, piek 99/127, RMS ±3000; audiocheck '54-85 Hz' = bas (E/A/F in achtsten) + taiko + framerate, geen brom.
- Forces v1 (`forces_theme.py`, songs 659-661, alleen stock-samples, één voicegroup `grounded_forces` + keysplit
  `forces_spicc`): **drie arrangementen van één motief = één materiaalblok (MEL/PROG in D-klein) + per thema een
  bouwfunctie en een SHIFT** (Tornadus +2/176 bpm, Thundurus -2/152, Landorus 0/112). **Elke DS-partij door `detach`**
  (noot + uitklinktijd vóór de volgende aanslag), anders kost een 16e-ostinato 2 kanalen (Landorus: koor 67% en klokken
  100% weg -> 0%). **sc88pro_taiko klinkt 88 Hz op toets 60**: op C3 gaf hij 29% energie < 60 Hz (piek 45 Hz) -> toets 57.
- Lugia v1 (`lugia_theme.py`, 657, 144 bpm, D-groot/D-klein, alleen stock-samples): **dualiteit = één melodie in twee
  gedaanten** (groot, breed in halve noten = beschermer; klein met F#->F/B->Bb, dubbel zo snel en dubbel gepunt = storm).
  Jordi: geen wiegenlied, de beschermer is heldhaftig. **Paukenroffels op een eigen programma met korte release (90)**:
  16en op de gewone pauk (release 200 = 44 ticks) bezetten 3 kanalen en lieten de windvlagen wegvallen (71%). Drumnoten
  op hun echte samplelengte (kick 0,09 s) i.p.v. een tel. Wind = `sc88pro_wind` (gelust) met trage aanzet + pitch bend
  op/neer per vlaag. -V100 gaf RMS 3400-4100 -> -V078: 0 overlopen, piek 85/127, RMS 2600-3200.
- Ho-Oh v2 (Jordi over v1: 'te vrolijk, trompetten/fluiten schel, niet Japans genoeg'): **eigen Japanse samples per
  ±7 halve tonen** (`hooh_samples.py`, keysplits hooh_shami/koto/shaku, 132 KB): FluidR3-shamisen mist in de lage
  ligging de grondtoon (E3 begint bij de 3e harmonische) -> 1e/2e erbij + bachi-tik + sawari; FluidR3-shakuhachi is
  bijna een sinus -> 2e/3e harmonische + ademruis rond de grondtoon, lowpass 3,2 kHz. Expressie via pitch bend (meri
  omhoog, yuri-vibrato, kari-val). **'Vrolijk' meten met Krumhansl**: v1 groot/klein liepen gelijk op (marge 0,02),
  v2 Em/F#m 0,72-0,89 met marge 0,13-0,29. **Drumpartij = één speler** (`ring_gates` laat de slag los vóór de
  volgende slag mínus de release): taiko 1,8 -> 1,1 kanaal; koto/shamisen release 100 = 16en op 1 kanaal. Lange
  pads/koper krijgen voorrang op kleine percussie (anders 65-90% weg). Harmonische-som-toonhoogtemeting faalt op de
  shamisen (inharmonisch): controleer met een piekenlijst. -V080: 0 overlopen, piek 80/127, RMS 2000-2700; leads
  > 4 kHz 0,1-0,9%; A-gewogen shakuhachi 55 > shamisen/koto 50-52 > bas/gitaar 45-48 dB.
- Lugia v2 (Jordi: 'bijna helemaal goed, maar tussen 30 en 40 s mag het tempo omhoog, opbouwen met goed drumgebruik'):
  de stilte na de climax (maat 19) werd een **drumopbouw die versnelt** (achtsten taiko/toms -> 16en toms -> 32ste
  snareroffel, aanzwellende paukenroffel, strijkersloop omhoog) met een **accelerando per tel** 144 -> 164 (maat 18-19),
  C en D op 164. **Tempo terugzetten op het loopbegin**: een TEMPO-event op dezelfde tick als de '['-marker komt in de
  .s ná het loop-label (controleer `grep TEMPO` + `_B1:`), anders blijft de loop op 164. -V078: 0 overlopen, piek 86.
- Forces v2 (Jordi: 'klinkt heel erg als Megaman, alsof dit voor een SNES is'; Tornadus 'gedragen door dat hoge fluitje,
  wimpy'; Thundurus 'voller GBA-sound'; Landorus 'saai, een aankondiging i.p.v. een battle theme'): **chiptune-gevoel =
  PSG-blokgolfleads/-arpeggio's/-echo + PSG-ruis als snare** -> weg (PSG alleen nog als sub en voor wind/bliksem); lead
  = trompet + strijkers unisono, hoorns als tweede stem, echte snare (rnd + orkest). **Solo A-gewogen meten per laag**
  (scratch `solo_aw.py`, volX = 0 op de rest): de spiccato-ostinato's waren -18 dB (0-1%) = onhoorbaar, door de
  keysplit-envelope (sustain 0) en een te lage ligging (D3, A-weging); nu sustain 255/release 110, een octaaf hoger,
  spoor 127. **Kanaalroof door lagen stapelen**: kick op de taikoslagen, extra crashes en een koor naast een
  tegenmelodie kostten 60% van het koor; per sectie kiezen (a2 tegenmelodie, C koor) i.p.v. alles tegelijk.
  **Stereo**: nieuwe saves staan op Mono (`new_game.c`), dus pan-spreiding hoort alleen wie Stereo kiest.
- Tapu v3 (Jordi over v2: 'HOO wimpy', 'TUDUDU onhoorbaar, is een synth', 'baslijn klopt niet', 'drums niet hard
  genoeg'): **een neurie op het raster leggen** (pyin/basic-pitch, onsets / 0,0862 s): Jordi's 5,9 s = precies maat
  9-12; vier tonen per halve maat + 16en-trillers. In de stem 'other' stijgt daar een brede synth (E3, B3, E4, F4;
  basic-pitch + harmonische som per 16e); de eerste sprong (kwint) klopt met de neurie, de rest van de neurie +11.
  **Spleeter zet een boventoonrijke synthbas half in 'other'**: wat daar in maat 13-60 als 'riff' leek (F4/E4/D4)
  waren 3e harmonischen van de bas (A#2/A2/G2) -> de bas zelf op een zaagtand-sample (`tapu_synth`, twee ontstemde
  zaagtanden, loop = kgv(80, 81) samples = exact). Bas per 16e vergelijken (toonklasse MIDI vs. stem): 75% -> 83%.
  PSG-blokgolf (16en-puls) en PSG-ruis (hats) voor energie zonder DS-kanalen. Opname-offset zelf meten (maat 1 =
  0,07 s in recsolo/recaudio, niet 0,55). -V076: 0 overlopen, piek 102/127, RMS 3180 (groove 3300-3500, bewust).
- Tapu v4 (Jordi over v3: 'baslijn die niet bestaat', 'drums te zacht', 'klap op 6 harder', 'synth valt weg vanaf 13 s'):
  **eerst per stem meten of een partij er echt is**: de 'bas' van maat 1-11 was de lage romp van de taiko's in de
  basstem (pyin-stemhebbendheid 1-40%, C#2/D2 per slag); de eerste echte bastoon (F2, 40-67%) komt in maat 12.
  **detach() op een 16en-lead met een uitklinktijd > een 16e maakt halve stipjes**: de synth nu legato (noot tot de
  volgende aanslag) en gaten gedicht. **Een lange release (impact 230) in een drumpartij verhoogt de staart van de hele
  partij in allocate()**: zulke slagen als eigen partij verdelen en daarna op het spoor zetten. Balans per sectie
  A-gewogen t.o.v. de mix (solo-opnames, `bal4.py`): maat 1-4 drums -1,8 / chant -4,5 dB (origineel -4,1 / -7,0).
  De klap zat al op de top van de 8-bit-mixer (piek 106/127): meer impact via stapelen + 4 zestienden stilte ervoor.
  -V076: 0 overlopen, piek 106/127, RMS 2800-3500.
- Tapu v5 (Jordi over v4: 'alles behalve de synth klopt; klinkt gehaast; kloppen de noten; is synth het juiste
  instrument?'): **eerst vaststellen of een 'lead' een lijn of een akkoord is** (piek-tracking + pyin per band + basic-pitch,
  per 16e): het was een opbouwend, liggend akkoord (E3+E4, +B3, E4->F4, dan 2,5 maat B3+F4). Het gewiebel en de 'woepsen'
  in een neurie zijn de zweving van een ontstemd ensemble en een nieuwe aanzet + filter dat opengaat, geen trillers/noten:
  v4 maakte er 16 losse 16en van in een eenstemmige lijn (= 'gehaast'). Klank op het harmonischenprofiel gekozen (zwakke
  grondtoon, top op 2e-3e harmonische = synth-brass; eigen sample: 5 ontstemde stemmen, exacte loop, heldere variant
  via programmawissel). Chroma per 16e (FluidR3 vs stem) 0,60 -> 0,88; A-gewogen spectrum game vs stem r = 0,98.
- Tapu v6 (Jordi over v5: 'vanaf 5 s mis ik het stuk dat de climax verzorgt' + neurie): **een figuur boven een liggend
  akkoord zoek je met grondtonen t.o.v. het akkoord, niet met piek/pyin per band**: de noten E5/F5/E6/F6 zijn ook
  boventonen van E3/B3/F4. Werkwijze: FFT per kandidaat-noot (h1 en h2) in het venster tegen een akkoord-only-venster
  (10:12-10:15): de grondtoon van de figuur stijgt +7..+15 dB, een boventoon van het akkoord niet. Zo ook het octaaf
  bepalen (E5 op x:0, E6 op x:4; A#4 stijgt niet, A#5 wel). Spleeter zette de hoge helft van de figuur in 'vocals'
  (stem 'vocals' +12 dB in maat 11). Een tritonus in een neurie is octaaf-dubbelzinnig (A2 onder E3 = A#5 boven E5).
- Mitch v6 (Mitch zelf over v5: 'horn klinkt heel low quality; probeer hem screechy/high pitched zoals de E4-theme;
  de wobbles zijn een mooie touch'): alleen het koper (MIDI-noten/CC's identiek, alleen programmanummers). **'Low
  quality' = de sample, niet de partij**: één Eb4-sample op 22.050 Hz tot C5 omhoog (x1,7, boven ±6 kHz vouwt het
  terug), tanh zonder oversampling, en een ingebakken staart die in 8 bit naar 0 korrelt. Nu één sample per lead-noot
  op de mixfrequentie 21.024 Hz (stap 1 = geen transpositie, 12 x ±2 KB), vervorming op 8x, aanzet uit FluidR3 + een
  **loop opnieuw opgebouwd uit de harmonischen** van het aangehouden deel (een loop van een paar echte perioden zoemt:
  ensemble/aanzet = energie tussen de harmonischen, -10..-17 dB), envelope in de voicegroup (255/248/200/160).
  Ruis/aliasing in de toon (GBA-simulatie: 8 bit + lineaire interpolatie, let op de loopsprong: i+1 = loopbegin):
  v5 -10..-15 dB, v6 -27..-31 dB. **E4-hoorns** (vs_elite_four) = sc88pro-trompet = hetzelfde spectrum als FluidR3
  56 (vlak tot h8, zwaartepunt ±1,4 kHz op C4), gespeeld rond D5-Bb5: B = trompet een octaaf boven de geschreven noot
  + body op de noot. Kanalen/stemverdeler ongewijzigd. B: -V066, 0 overlopen, piek 72/127, RMS 2616.
- Ruinous v1 (`ruinous_theme.py`, 683, SV Treasures of Ruin, 152 bpm, B met frygische C): **eerst het 16e-raster fijn
  vastleggen** (fase met STFT-flux per band: 0,070 s; het 16e-patroon van de eerste analyse hing aan de beat_track-fase
  en lag een 16e verschoven: 'kick op de laatste 16e' was in werkelijkheid één grote slag op elke tel, alle banden).
  **Een tijdstip uit Jordi's feedback hoort bij het fragment dat hij hoorde**: de ostinato-clip begon op 25,0 s
  (kruiscorrelatie met de stem), dus zijn '7 s' = maat 21, waar een tokkellijn in B4-C6 begint (16e-heraanslagen).
- Legends3 v1 (`legends3_theme.py`, 684-686, alleen stock-samples, één voicegroup `grounded_legends3` + kit `drumsets/legends3`):
  **twee/drie motieven op hetzelfde akkoordschema schrijven** (meren: F#m-D-E-C#m-Bm-D-G-C#) zodat ze in de slotsectie
  zonder aanpassing samen kunnen klinken; Xerneas/Yveltal = één melodie met `to_death()` (G#/C#/D# een halve toon
  omlaag, behalve D# op de dominant), gecontroleerd met de duur per toonklasse per sectie (groot: 0 G/C/D, klein: 0 G#/C#).
  **8-bit-fuzz vermijden**: DS-velocities >= 76 (assert in het script), geen fluit, sub op de PSG-golf, DS-bas >= C2,
  zuivere lichte figuren (Uxie, waterrimpelingen) op PSG. **Kit met `voice_directsound <toets>`** i.p.v. _no_resample
  (speelt op de sample-rate, niet op 21 kHz). Harp/spiccato in 16en: release <= 100-110, anders bezet elke 16e 2 kanalen
  (detach houdt min. 6 ticks); koper eigen keysplits met release 112/120 voor 16en-opmaten. Tomfills laten eindigen
  vóór de tel waarop de crash valt, en geen hihat op een crash: scheelt 2 kanalen op de zwaarste tel.
- Area Zero v1 (`areazero_theme.py`, 681 + remix 682): **transcriberen uit een dichte mix = per laag een ander gereedschap**:
  kristal-arpeggio's met onset-per-halve-toon (`onsets.py`), de 'stem' met harmonische som + zwaartepunt per 16e
  (`seg.py`: noten met hun afwijking), akkoorden met chroma per halve maat, drums per band; daarna **chroma-correlatie per
  maat render vs. origineel** (0,70 -> 0,83): lage maten wezen precies de foute grondtoon aan (Ab-bas was Eb-orgelpunt,
  bas-stem toonde boventonen). De lead zingt systematisch ±0,4 halve toon te hoog met brede vibrato (= het 'uncanny');
  nagebootst met pitch bend per noot + MOD. 8-bit-covers zijn niet noot-voor-noot (andere timing): alleen ter controle.
  Stock-glockenspiel/unknown_bell klinken een kwarttoon vals op toets 60 (1361/1227 Hz): kristalbel zelf gesynthetiseerd.
- Ruinous v2 (Jordi: 'drumritme goed, voor de rest alles niet'): **Spleeter zet een getokkeld instrument in de stem
  'piano'** (de intro E2/F#2/B2 met heraanslagen in 16en zat daar, niet in 'other'); v1 hield de hoge boventonen in de
  mix voor 'twinkelingen'. Kijk bij elke laag in álle stems (dominante toon per 16e, `dom.py`-achtig). Een zachte laag
  in het origineel (de F#5-'roep', bijna zuiver) niet op een luid instrument zetten: weglaten. 'Lange tonen' in
  'other' kunnen het ostinato zelf zijn (B3+F#4 pulseren in het ostinato-ritme): eerst het ritme per noot meten.
- Area Zero v4 / 682 v2: **kanaalroof eerst meten, niet aannemen**: kanaallog per frame (gSoundInfo.chans = mixbuffer
  - 12x64 bytes; status, spoor via track-pointer, toets, envelop) gaf in 681 max. 9 kanalen en 0 geroofde noten. De
  'haperende aria' en 'roepen die loopen' waren detach-gaten (0,2 s stilte vóór elke noot) en te korte loops (0,3 s);
  fix: noten laten aansluiten, loops >= 1 s met gelijk-vermogen-crossfade (cos/sin). In 682 gaf hetzelfde log 12
  kanalen bij een bekken + herhaalde leadnoot + strijkers per maat opnieuw: stemverdeler op 10 rekenen, strijkers als
  één lange noot. Geraden lagen (arpeggio's, ostinato) klinken voor Jordi als 'een ander nummer': weglaten.
- Area Zero v5: **solo-opnames: mid2agb laat lege MIDI-sporen weg**, dus het m4a-spoornummer is de index onder de
  níet-lege sporen (`NumTrks` in de .s); anders neem je het verkeerde spoor solo op (chroma A/B werd negatief).
  'Piepjes missen de helft' = de belletjes van het origineel klinken elk ±1 maat door (wolk); de aria in hele frasen
  uit de stem (zoals het koor) klinkt vloeiend; wat Spleeter in 'other' zette (m36, m39) bleef als noten.

- Ruinous v3 (Jordi over v2: 'lijkt nergens op, een glitchend systeem; isoleer de instrumenten'): **een laag die je
  niet kunt benoemen, knip je uit de stem zelf**. De stem 'other' (25% van de energie: pad + 16e-figuur + hogere
  lijn) als één halve maat per akkoord, geknipt waar dat akkoord in het origineel klinkt (9 knipsels à 9 KB), gaf in
  de A/B chroma 0,7-0,95 per maat; een eigen ostinato-noot getransponeerd per akkoord (v2) klonk als 'systeem'.
  Half-maat-knipsels 30 ms langer dan de halve maat + release 140 = naadloos. Laag met weinig energie en een A/B
  die niet klopt (de hogere 'piano'-lijn, chroma 0-0,4): weglaten. Solo uit de mixbuffer: `volX = 0` per spoor
  elke frame; de opname begint 0,74 s ná maat 1 (meten aan de inslag, niet met een kruiscorrelatie over 0,8 s).

- Mitch v7 (Mitch: 'nog steeds te goedkoop, misschien een ander instrument dan de horn'; SickBlik klinkt beter):
  **'goedkoop' gemeten** (gba_sim per spoor, `smpmetrics`-achtig: zwaartepunt, % boven 2/4 kHz, % 'dichte' FFT-bins):
  alle synths < 2% boven 2 kHz, de horn één oscillator met een loop van 20 ms (alleen harmonische lijnen, dicht 4-6%),
  en **`resample_wav.py --all` had de v6-horn van 21 naar 11 kHz gezet** (de v6-fix weer ongedaan); SickBlik =
  echte instrumenten/ensembles/akkoorden in één sample, 54% van de mix in 150-2000 Hz (Mitch 23%). v7: synth-leads
  als stapel stemmen in één sample op 16 kHz (KEEP_16K in resample_wav.py), 3 samples per kandidaat (transpositie
  -2..+5: onder de 10,5 kHz van de mixer). **De -V-grens van Mitch was de build-up**: kick + roffelsnare tegelijk =
  +35% boven de drops (offline), daarom liep -V > 066 over; roffelslag op/na een kick x0,5 -> -V092, piek 98, RMS 3950.
- Area Zero v7 (Jordi: 'vanaf 8 s doen de piepjes hun eigen ding; vanaf 1:18 een deuntje dat er niet in hoort'):
  **nooit een laag toevoegen die alleen gemeten en niet met een geïsoleerde A/B tegen de stem gecontroleerd is.** Een
  dichte belletjeswolk (16en + echo + wisselnoten) is niet na te spelen; waar een stem alleen die laag bevat (intro,
  pauzes) knip je hem als geheel (chroma A/B 0,97); de geraden cel/groove-arpeggio's zijn weg.
- Area Zero v8 (Jordi: 'vanaf 8 s naar de achtergrond; distorted melodie op 13 s kapt af; 22 s en 47 s te muffled'):
  **eerst per 0,5 s niveau + % boven 2 kHz van GBA-opname naast mix én stems zetten** (gelijke luidheid over het
  venster): de intro stond 11 dB bóven de wolk (origineel 8 dB eronder), de knip stopte midden in de vervormde
  Eb-akkoordklank (die zat deels in de bas-stem: PSG-bas zit niet in een mixbuffer-opname!), en de glans op 22/47 s
  zat in 'other'. Opgelost met de begeleiding als aansluitende knippen uit other+bass(+drums) (lineaire crossfade van
  15 ms op de naad, herhalen waar de golfvorm-correlatie per maat ≥0,5 is) en **alle knippen op één schaal**
  (velocity = 127 x piek / grootste piek, lineair): dan is de verhouding stem/begeleiding vanzelf die van het
  origineel (gemeten ±1 dB). Spleeter zet bromtonen soms in 'drums' (Eb-orgelpunt m24+): chroma per laag tegen de
  stem controleren. **Weergaveketen meten** (solo vs stem, opname vs mixbuffer): 16 kHz-sample + mixer + GBA-uitgang
  = -2 dB bij 2 kHz tot -6,6 bij 7 kHz; het omgekeerde als voorversterking in de knip (`EQ` in
  `areazero_samples.py`) maakt de opname ±1 dB vlak t.o.v. het origineel.
- Area Zero v9 (Jordi: 'tot 1:18 geweldig, dan een hele luie variant'): waar knippen ophouden en eigen partijen
  overnemen, **een 16e-raster van de energie per band** (laag <150 Hz / hoog >3 kHz, `#o.`) naast het origineel zetten:
  het origineel had een doorlopende 16e-was (pulserende ruis + hi-hats), wij achtsten. Goedkoopste fix: 2 maten
  'other'+'drums' alleen boven 2 kHz knippen (14 kHz, 56 KB) en elke 2 maten herhalen; akkoorden/bas/kick blijven van
  ons, dus geen akkoordbotsing. **Dezelfde kitnoot direct na zichzelf**: eind = volgende start (of erna) geeft in
  mid2agb N01-noten (de note-off van de oude doodt de nieuwe); laat de noot 1 tick eerder eindigen.
- Area Zero v10 (DPCM halveert de knippen; Jordi: 'quality first'): hele begeleiding m1-64 uit het origineel.
  **Herhalen per maat i.p.v. per blok**: knip losse maten als eigen samples (zelfde bytes) en kies per doelmaat de
  bron met de hoogste chroma-correlatie per 8e in het origineel (blokherhaling m48-63 gaf 0.73-0.92, per maat >= 0.94).
  **DPCM-nultest** (opname gecomprimeerd - ongecomprimeerd): ruis ±-50 dB, bij luide knippen 22-24 dB eronder (prima),
  bij zachte knippen (wolk, intro) maar 8-14 dB: die blijven ongecomprimeerd. **De 8-bit-uitgang heeft een ruisvloer**
  ±-48 dB: een intro die in het origineel 27 dB onder het hoofddeel zit, wordt op de GBA ruis (34% >2 kHz waar het
  origineel 0% heeft); daar dus bewust luider dan het origineel.
- Battle! Area Zero v1 (682, `vs_areazero_samples.py` + `vs_areazero_theme.py`): **eerst meten of een nabouw met
  knippen-bibliotheek kan**: per maat de unieke maten tellen (golfvorm per stem, chroma per 8e op de mix). De battle is
  doorgecomponeerd (54/69 uniek), dus het hele origineel in aansluitende knippen (11025 Hz, DPCM, ±700 KB). **Frame-exact
  knippen**: m4a op 150 bpm met 24 ticks/tel = 1 tick per frame (59,7275 Hz); de bron met factor K = P*fps/L
  herbemonsteren zodat lus en grenzen op hele frames vallen. **Stukgrenzen op frame-afstanden met een (bijna) heel aantal
  samples** (frames * rate/fps): een nieuwe noot begint op sample 0 terwijl de lopende op een gebroken positie staat
  (mixer interpoleert); met willekeurige afstanden gaf de crossfade -10 dB fout, zo -33..-41 dB (= kwantisatie).
  Doorgang 1 wijkt af (intro-staarten): stuk 0 = intro + doorgang 1 tot maat 9, de lus komt uit doorgang 2->3.
  Niveau: één spoor op 127/127 gaf -26 LUFS, een tweede spoor met dezelfde noten (coherent) +4..6 dB -> -22,5 LUFS
  (Giratina -22,7). Kreet: de engine dempt de BGM tot ±0,35-0,4 tijdens de kreet (gemeten), geen botsing.

- Tower v1 (`tower_theme.py`, 687, gevechtsremix van `mus_rg_lavender.mid`): **origineel tpb 24 x 4 = 96 en de intro is
  ook 4 maten**, dus elke noot staat op tick x 4 en de loop (40 maten) blijft 1-op-1 (melodie spoor 1, jammerlijn spoor 5,
  fluitlijn spoor 4, arpeggio spoor 7, atarigane spoor 6). Melodie per sectie op een ander instrument in eigen sporen
  (orgel / strijkers / koor / trompet+strijkers) = geen programmawissels rond de looptick. PSG draagt arpeggio,
  jammerlijn, fluitlijn en hats (0 DS-kanalen); 1 basnoot van 490 valt weg. **`drum_and_percussion_kick` als
  `voice_directsound 60` speelt op 13.379 Hz = subdreun** (< 60 Hz 26-33% van de mix); op toets 67 (zoals de FRLG-kit
  via _no_resample) 10-15%. -V100: 0 overlopen, piek 105/127, RMS 3120; audiocheck 49-67 Hz = kick + grondtonen C2/B1.


- Legendary v1 (`legendary_theme.py`, 670, generiek legendary-thema, E-klein 176 bpm, alleen stock-samples): **de
  Weather Trio-'percussie' is vooral de pauk** (mus_vs_kyogre_groudon: 235 paukennoten, achtsten laag-hoog-laag-laag-
  hoog-laag-laag-hoog op kwint/grondtoon; drums alleen bekkens). Pauk-ostinato op release 170 + roffels op een aparte
  pauk met release 90 houdt het op max. 11 kanalen zonder weggevallen noten. E4-koper = stock trumpet/horn-keysplits,
  hoorns harmoniseren automatisch (hoogste akkoordtoon >= 3 halve tonen onder de trompet). -V090: 0 overlopen, piek
  100/127, RMS 3140; audiocheck 71-90 Hz = grondtonen D2-F#2 van bas/pauk. ±6 KB (song 4,7 KB + voicegroup).
- Arceus v1 (`arceus_theme.py`, MUS_GROUNDED_VS_ARCEUS 676; bron `Battle_Arceus.mid` op origin/master, Domino-bewerking
  van de SSEQ-rip SEQ_BA_SECRET1, 150 bpm, tpb 48): **uitgeschreven echo** in de bron (zelfde noot elke tel, velocity
  110 -> 38 -> 27 ... 7) = elke herhaling een kanaal; stoot + echo per spoor samen `detach`en en de echo's als aparte
  partij achteraan in de stemverdeler (onder v20 weg). Een **rip-kopie op 2 ticks met detune** (spoor 5, pitchwheel
  -384 bij bend-range 12 = stereo-chorus) kost alleen kanalen: weg. Spoor 'Track 10' op kanaal 8 met programma 117 is
  een GM-drumspoor (41/45 toms, 52/57 bekkens op tel 3 en 3-en), geen melodische taiko: eigen kit. Bekkens die een
  achtste later terugkomen eerder los (anders 2 kanalen). Loop = maat 10-50 (maat 41.3-49 herhaalt de intro-gebaren).
  Batchrec: 0 overlopen, piek 111/127, RMS 556-3590 (strijkerssecties het luidst), max -4,9 dB; ±3,6 KB ROM.
- Mew v1 (`mew_theme.py`, 679, remix van Battle! Mewtwo; Jordi: "minder evil, curious, geen kloon, originator"):
  zelfde vorm/contouren, 132 bpm, A-lydisch (Mewtwo's frygische Bb -> B-groot = lydische II), motief als vraag
  (fluit) en antwoord (glock 8va), hikje elke 4e maat; Mewtwo's halve-toon-echo wordt de frase gespiegeld in de
  toonladder op de glock. Hergebruikt `voicegroup_grounded_mewtwo` (geen nieuwe samples/voicegroup). Glock/harp hebben
  release 242 (±174 ticks staart): 8en op de glock of harp vreten kanalen, gebruik kwarten of zet ze op de 'en'.
- Dialga/Palkia v1 (Jordi's `DialgaPalkiaMIDIBeta.mid`, origin/master): **vorm zoeken met een spoor-voor-spoor-
  vergelijking per halve maat** (gelijk / zelfde ritme / anders) i.p.v. op het gehoor: de MIDI heeft na maat 48 een
  halve maat verschuiving (lange noten op tel 3 i.p.v. 1), en het einde (115,5) sluit naadloos aan op maat 6 (bas,
  arpeggio, drums en pauken lopen door) = de loop. 'Humanize'-vertragingen (spoor 7 overal 12 ticks te laat, spoor 4 =
  octaaf-echo van spoor 6) eerst op de tel zetten; de echo/arpeggio op PSG-vierkanten kost geen kanalen. fp-houdnoten
  (accent + dezelfde noot op v40) samenvoegen. balance.py tegen FluidR3: GM-synthbas is 11 dB luider dan de GBA-
  synth bass (spoor op 127 is het maximum). -V088: 0 overlopen, piek 94/127, RMS 2985; ROM ±9 KB (alleen stock).
- Ultra Beast v1 (`ub_theme.py`, 677, 168 bpm, octatonisch C, B heeltoons in 7/8): **'andere dimensie' zonder horror of
  euforie** = een ladder zonder grondtoonfunctie (octatonisch: het thema een kleine terts omlaag/omhoog geeft dezelfde
  tonen) + microtonale details (kwarttoon-scoops/-wiebels op de lead via BENDR 2, PSG-echo 0,3 halve toon te hoog,
  twee koorstemmen die tegengesteld een kwarttoon wegbuigen). Glazen lead = FM met een niet-harmonische modulator
  (x1,41) en exacte loop (gehele perioden van alle oscillatoren in 2760 samples, 11 kHz). Omgekeerde zwelling =
  FM-klok achterstevoren, 1,15 s eindigend op de downbeat (2 kanalen). Batchrec -V090: 0 overlopen, piek 95/127,
  RMS 3000-3450, max -5,6 dB; audiocheck 45-62 Hz = rnd-kick + C2-pedaal (stijgt pas als de drums invallen). ±25 KB.
- Mew v2: v1 "tonen klinken raar, te hoog, niet in een goed tempo, maak het meer fluïde". -> gewoon A-groot (geen
  lydische D#), geen glockenspiel, hook een octaaf lager (max. E5), Mewtwo's staccato-16en als legato-8en (frases van
  2 maten), doorrollende harp-arpeggio's door het hele nummer, golvende bas, geen hikjes/stops. Twee gevoelens in één
  script (`FEEL` 44 = 156 bpm rollend, 128 = 12/8 op 120 via `warp()`). Eigen `voicegroup_grounded_mew`: harp-release
  242 -> 200, anders bezetten arpeggio's in 8en 5-6 kanalen. Pads per akkoord (2 maten) en een 8e vóór de wissel los
  laten: aangehouden pads per maat stapelen hun release op de maatgrens (koor viel 14/16 weg).
- Mew v3: v2 "nog veel te lieflijk ... wolkentheme", "Mew heeft alsnog hoge stats", "Mewtwo's theme is super vet,
  dat mag iets minder dreigend, wat neutraler". -> Mewtwo's arrangement bijna 1-op-1 (128 bpm, four-on-the-floor,
  16e-bas, gate, koor, pauken, blokgolf, PSG-lagen); alleen de dreiging eruit: geen frygische Bb/verminderde maat
  (Am-G-Am-Em, B: D-Am-F-G, C eindigt op bVII G -> loop naar Am), zuivere octaaf-echo i.p.v. halve toon ernaast,
  kerkorgel -> blokgolf + trompet unisono, hook een octaaf lager (max. D5). Les: bij een remix van een goedgekeurd
  nummer eerst vragen/aannemen dat de productie blijft en alleen het karakter (harmonie, 1-2 klanken) verschuift;
  v1/v2 veranderden tempo, groove en instrumenten tegelijk en verloren zo wat Jordi 'vet' vond. -V090: piek 81, RMS ±2900.
- Ruinous v4 (Jordi over v3: 'lo klopt alleen de eerste toon, OST mist de diepe strijker, oth loopt een noot en
  verdwijnt, oth2 als een vastslaande cd-speler, bas een rare remix'): **(1) de A/B-uitlijning zelf eerst controleren**:
  v3 nam aan dat maat 1 op -0,74 s lag (een andere aanzet gekozen), echt is +0,034 s (kruiscorrelatie van een sample
  dat uit het origineel komt): de B-fragmenten lagen een halve maat verschoven. **(2) A en B op gelijke RMS**, niet op
  de piek ('het origineel heb je erg zacht opgenomen'). **(3) frasen waar het origineel doorloopt**: intro (maat 1-4,
  alle stems = de mix, 70 KB) en de lo-frase (maat 5-8, 8 kHz) als één sample; maatknipsels van het pad alleen < 450 Hz
  (dan is herhaling een aangehouden akkoord, geen haperende melodie), 4 kHz, en een eigen knipsel per maat waar het
  getransponeerde pad in de offline-A/B < 0,75 chroma gaf. **(4) bas noot voor noot met pyin per 16e** (aanzetdrempel
  2,5x mediaan), één B1-sample: chroma 0,9-0,97 per maat. Offline-A/B (`sim.py`: noten x sample vs stem) vóór de ROM.
  De bovenlijn/16e-figuur van 'other' (±45% van die stem boven 500 Hz) bleef onbetrouwbaar (pyin en salience mengen
  figuur en melodie): niet nagemaakt; streamen kost ±650 KB (beslissing Jordi).
- Ruinous v5 (Jordi over v4: 'intro is nu goed, maar kost veel samples; vanaf 32 s mis ik de strijker'): **goedkoper
  maken offline meten vóór je kiest** (GBA-simulatie: samplerate, 8 bit, lineaire interpolatie; log-mel-correlatie per
  maat t.o.v. het origineel): 4 maten 11 kHz (70 KB) mel 0,84; 8 kHz 0,74; 6 kHz 0,74; maat 3-4 = maat 1-2 +2 halve
  tonen (zelfgelijkenis 0,90), dus 2 maten x2 (34 KB) 0,78 maar maat 4 zakt (0,60): sneller afspelen van een
  getransponeerd frase-sample verkort hem ook. **Een aangehouden lijn boven een 16e-figuur** vind je met salience
  alleen boven de figuur (> C#5, 560-4000 Hz): terugkerende motieven = betrouwbaar. Stock-strijkers (0 KB) en een
  knipsel uit het origineel (18 KB) scoorden gelijk (spectrum-r 0,77, chroma 0,75): stock gekozen.
- Ruinous v6 (Jordi over v5: 'vanaf 6 s en 19-20 s is de hoofdmelodie weggedrukt, te muffled; het instrument vanaf
  31 s is te veel blazer, te weinig strijker, qua maten de hele tijd off'): **meet de hele mix per maat per band tegen
  het origineel** (gelijke totale RMS; `mixcmp.py`): maat 5-12 500-1000 Hz -6 dB en maat 13-16 alles boven 500 Hz
  -10..-20 dB. Oorzaak: lagen die in de stems zaten maar nooit nagemaakt waren (de aangehouden roep F6-F5-F#5 in de
  stem 'vocals' maat 5-12; de hoge B5-ostinatolijn in 'other' 13-20). Een lijn die niet in de stem staat waar je
  zocht, staat in een andere stem: **per stem per band per maat** (`stembar.py`) vóór je de oorzaak in de balans
  zoekt. Roep = één harmonisch gemaskerde F#5 (deeltonen +-35 ct, rest -12 dB: lekkage weg) met ping-pong-loop
  (15 KB) + CC7 per 8e uit het gemeten niveau. **Koperachtig = aanzet 255 + te helder** (stock-strijkers 1-4 kHz
  +4..+7 dB); eigen strijkerknipsel (zelfde masker, +5 dB plank > 1,2 kHz voor het zwaartepunt) met aanzet 80
  (~50 ms). **'Off' = gestotterde noten, geen rasterfout**: de toonhoogte per 16e lag op verschuiving 0 (79% gelijk),
  maar salience-aanzetten pakten de 16e-lekkage van het ostinato als herhaalde aanslagen; legato samenvoegen (zelfde
  toon, gat <= 2) + doortrekken tot de volgende noot zolang het niveau < 6 dB zakt. Velocity per noot uit het
  gemeten niveau van die toon (stem vs. GBA-solo, h1+h2), maatniveau als CC7. Onset-xcorr per maat is onbruikbaar
  bij een legato lijn boven een periodieke figuur (springt +-2 16en); vergelijk de toon per 16e (`pitchlag.py`).
