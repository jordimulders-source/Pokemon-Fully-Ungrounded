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
