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
| Mitch (DnB) | `mitch_theme.py` | v3 in de maak (duistere DnB) | "Mitch" |
| Neo Plasma (BW2-remake) | `neo_plasma_theme.py` | v7 in de maak (vol, gelaagd) | "Neo Plasma" |
| Victini, Darkrai, Genesect | nieuw | v1 in de maak | – |

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
