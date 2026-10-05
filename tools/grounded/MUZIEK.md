# Muziek componeren en arrangeren voor Project Grounded

Dit is het geheugen voor muziekwerk. **Lees dit vóór elk nieuw nummer, en vul het aan na elke feedbackronde van Jordi**
(wat fout ging, wat hij mooi vond, welke controle het had kunnen vangen). Een nieuwe fout die automatisch te
herkennen is, komt ook als controle in `music_lint.py`.

## Werkwijze (verplicht, in deze volgorde)
1. Componeren/arrangeren met een script (`zarude_theme.py`, `wally_theme.py`), nooit met de hand in de MIDI.
2. `python3 tools/grounded/music_lint.py sound/songs/midi/<nummer>.mid`: moet **OK** zijn.
3. Test-ROM: `python3 tools/grounded/maptools/testrom.py <map> "playbgm MUS_X, FALSE"`.
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

## Log van feedbackrondes
- Zarude v1–v10: losse piepjes = PSG-drumnoot 44 in een tomroffel; brass pas na de transitie; groove niet te kaal.
- Wally v0.9.20: opname kapot (bufferoverloop). v0.9.24: snips door kanaalroof (tot 17 noten tegelijk bij 5
  kanalen) + dubbele noten in de bron; engine naar 8 kanalen, stemverdeler, `music_lint.py`.
- Wally ronde 2: snips op 3/12 s = mGBA-resampler (niet de game); 1 te hoog/melancholisch → dorps; 5 chaotisch
  (dubbele bassdrum verdrong instrumenten) → strak; gehaaste inzetten op x.875; engine 12 kanalen, release-bewust.
- Wally ronde 3: resterende snips bleken opname (recpcm is schoon); drums afgekapt door DRUM_LEN; 5 te weinig
  gitaar → leadgitaar (overdrive) op de melodie; -V125 tegen de ruis.
- Wally ronde 4: 'tweede beat gehaast' = een voorslagnoot op tel 11,875 die alleen in de 2e frase zit (bron-
  transcriptie). Vergelijk bij zo'n klacht frase 1 en 2 noot voor noot; ritmes die herhaald horen te worden, moeten
  gelijk zijn. Bas-anticipaties die in élke frase terugkomen zijn groove: laten staan.
- Ruis/'vinyl': de 8-bit-mixer op 13.379 Hz. Zarude valt minder op door schone PSG-sporen. Op 21.024 Hz is de hoge
  ruis ±40% lager; Jordi koos die (v0.9.32). Lag meten: tijdelijke teller in de hoofdlus van `src/main.c`
  vergelijken met `gMain.vblankCounter1` (verschil = vertraagde frames).
- Wally ronde 5: een tab van Jordi (`sound/songs/grounded_src/` + chat) toonde dat de 2e frase G-A-F#-**B**-A-G is;
  de bron had daar E + voorslag-B. Bij twijfel: een tweede bron (MIDI `wally_battle_ss17.mid`, tab, bladmuziek)
  naast de eerste leggen; waar twee bronnen het eens zijn, klopt het. Let op: bladmuziek "Wally's Theme" is het
  overworld-thema, niet "Battle! Wally".
- Regigigas v1: legato-partijen (koper, koor, tuba) bezetten op elke nieuwe noot 2 kanalen (de release van de vorige
  klinkt nog). `musiclib.detach()` laat de vorige noot de uitklinktijd eerder los; `allocate()` neemt de tail per partij.
  Daarmee viel er niets meer weg. RMS via recaudio ±3000 is de bovengrens (Zarude ±2700): -V95.
- Regigigas v2 (Jordi: 'veel kaler dan het origineel'): een remix van een bestaand nummer = het origineel 1-op-1
  laten staan (sporen kopiëren, zelfde voicegroup + extra instrumenten erachter) en alleen lagen tóévoegen die het
  origineel nog niet heeft (koor, tuba, taiko). Geen verdubbeling van wat er al is (koper). Intro gelijk aan het
  origineel; de Slow Start pas als het gevecht begint (±6 s). Een inzinking op een frasegrens beginnen en tel voor
  tel vertragen, niet per maat (Jordi: 'te laat, niet lekker').
- Vanilla-nummers zijn voor 5 kanalen gemaakt maar gebruiken er tot ±9 (de engine kapte toen af). Tel ze mee als
  preset in `allocate()`. Legendary-gevechten mogen 11 kanalen (MAX_PER_SONG in de lint).
- **recaudio neemt twee keer op** (32768 en 44100 Hz) en vervangt elk glitchvenster door het echte geluid uit de
  andere opname (de glitchtijden hangen af van de samplerate). Lineair overbruggen liet een hoorbaar gaatje ('snip').
- Regigigas v3: de inzinking volgt de muziek: afremmen vóór de rust van de melodie (maat 27), traagst in de rust,
  opbouwen in de lange noten; daarna een climax die het origineel niet heeft (tempo 1,06×, trompetfanfare op de
  grondtonen, pauken, crashes om de 2 maten). Zoek bij een tempo-effect eerst de frasen/rusten in de melodie.
- Regigigas v4 ('ik mis de epische climax', 'weinig verschil v2/v3'): lagen bóvenop een vol origineel hoor je
  nauwelijks. Een climax moet iets structureels zijn: een extra sectie (hoofdthema +2 halve tonen), waarin het
  originele koper zwijgt en een eigen koperkoor de melodie luid overneemt; plus taiko/crash/pauken en tempo 1,08×.
  Slow Start op ±5 s (Jordi), niet op een maatgrens maar waar de transitie eindigt.
- Opname: al vóór de laatste A opnemen (anders mis je de eerste ±0,2 s); geen -ss meer bij ffmpeg, alleen een fade-in.
- recaudio: tweede glitchpatroon (exacte nullen om en om in niet-stille muziek) wordt ook overbrugd (Dave-snip op 3 s).
- Dave ronde 4 ('abrupt, niet zoals het origineel'): een origineel nooit inkorten door secties over te slaan (4 -> 53
  sloeg de hele opbouw over). Lees eerst per spoor per maat uit wanneer elk instrument invalt (een tabel als in
  freed_theme.py) en neem het nummer doorlopend over; loop pas op een plek waar het nummer zelf zo'n overgang heeft.
  Drumnoten die buiten de kit/PSG vallen (ride 51, pedaal-hihat 44) omzetten i.p.v. weglaten: ze dragen de opbouw.
- Regigigas v5: de climax-trompet en -hoorn werden berekend maar nooit weggeschreven (oude lege 'fanfare' in de
  uitvoerlijst), dus Jordi hoorde 'geen climax'. Laat een script altijd controleren dat elke niet-lege partij in de
  MIDI staat (assert in regigigas_theme.py), en luister/meet de climax apart (RMS per sectie).
- Regigigas: een extra stem op exact dezelfde noten/ligging als het origineel versmelt (trompet niet hoorbaar) ->
  een octaaf hoger. Klokken (tubular bell, 6689 Hz) een octaaf omhoog klinken kort en dun -> in de ligging van de
  melodie, op volle sterkte en per maat opnieuw luiden. Prioriteit: wat Jordi wil horen (trompet) eerst.
- Mewtwo v1 (eigen compositie, `mewtwo_theme.py`): intro getimed op de transitie (frames uit `battle_transition.c`:
  ogen 88, barsten 96-108, burst 114 = ±1,9 s -> 128 bpm zodat de burst op maat 1 tel 0 valt). DirectSound-blokgolf
  (`sc88pro_square_wave`) als synthlead, PSG-vierkant alleen zacht voor arpeggio's. Opname via het echte gevecht
  (`setwildbattle` + `BattleSetup_StartLegendaryBattle`), zodat je de sync met de transitie hoort.
- Mewtwo v2: de cry van een wilde Pokémon klinkt ±2,3-3 s na de start van het gevecht (na de transitie) en botst
  met een drop op dat moment -> een 'ademmaat' na de transitie (alleen drone/zachte kick) en de loop daarna laten
  beginnen. 'Kaal' -> pompende trance-strijkers in achtsten (gate), koor, orgel. 'Lead te schel/niet evil' ->
  blokgolf een octaaf lager + kerkorgel (`sc88pro_church_organ3_low`, uit rayquaza_appears) op de melodie.
- Mewtwo v3: twee cries (transitie + gevechtsstart) botsten met de beat -> de cry in de transitie weg, de transitie
  filmisch vertraagd en op de maten van de muziek gelegd (1 maat = 112 frames bij 128 bpm), daarna 1 ademmaat voor
  de cry + 1 opbouwmaat. 'Maximalistischer zonder het bestaande te veranderen' -> lagen op de vrije PSG-kanalen
  (delay-arp op vierkant 2, sub op de golf, shaker en riser op ruis): kosten geen DirectSound-kanalen.
- Beasts (`beasts_theme.py`): origineel (voicegroup_dummy, 3 sporen die van instrument wisselen) + één laag per beest.
  Sporen die midden in het nummer van programma wisselen: bezetting per noot rekenen (`musiclib.ds_occupancy`),
  anders klopt de stemverdeling niet met de lint. Glockenspiel met korte release (170) i.p.v. 242.
- Open: `mus_grounded_vs_zarude.mid` geeft nog meldingen in de lint (dubbele noten in de tomroffel, soms 9–10
  noten tegelijk). Jordi keurde hem goed; repareren bij de volgende Zarude-ronde.
- Dave / Freed From Desire (v1, `freed_theme.py`): bladmuziek voor **Bb-trompet** staat een grote secunde hoger
  genoteerd (E-klein op papier = klinkend D-klein, zoals de MIDI). Melodie uit het blad (herhalingen gelijk), begeleiding
  uit de MIDI. De bron-drums duren allemaal 2 ticks: geef elke drumnoot een eigen lengte (kick/snare/hihat 1/2 tel,
  tamboerijn 1/4, crash 2 tellen).
- Stemverdeler-trucs: lange padnoten (8 tellen) vielen voor 97% weg; in stukken van 2 tellen knippen die een
  uitklinktijd eerder stoppen (pulserende pad) -> 10%. Pianostoten: lengte + release korter dan de afstand tot de
  volgende stoot (eigen piano met release 200 i.p.v. de keysplit met 239), anders 4 pianonoten tegelijk.
  `musiclib.allocate` accepteert nu een uitklinktijd per spoor (`tail={naam: ticks}`).
- `recpcm.py` meldt veel "sprongen>40" bij hihat/tamboerijn (ruis-samples, 21 kHz): geen glitch zolang ze niet op
  framegrenzen (elke 352 samples) liggen.
- Dave ronde 2 (Jordi: "lijkt een remix, melodieën in de verkeerde volgorde en door elkaar"): een bekend nummer
  **niet** herschikken of uit losse secties samenstellen. Neem één aaneengesloten stuk van de bron in de originele
  volgorde (Dave: bronmaat 49-52 intro, 53-85 loop) en kopieer de sporen 1-op-1; alleen instrumenten mappen, drums
  omzetten, uitdunnen. Loop op een maatgrens met dezelfde overgang als in het nummer (85 C -> 53 Dm = 37 -> 38).
  Melodie = het zangspoor van de MIDI; bladmuziek alleen als controle, nooit als extra stem erbovenop. Eén melodie
  tegelijk (unisono-dubbeling mag); haal ook legato-overlap van 1-2 ticks in het melodiespoor weg.
- Opname-glitch (mGBA): een venster met >= 4 exacte nullen binnen 12 samples terwijl de omgeving niet stil is;
  overbruggen (±32 samples, lineair). Dave: één bij 11,5 s.
- Dave ronde 3 (Jordi: "begin met de tududu-tututu zonder beat, één drumslag, dan de zang; het origineel is perfect"):
  begin zoals het nummer begint (bronmaat 2-4: riff twee keer solo), dan het couplet met volle begeleiding. Couplet 2
  (53-60) = couplet 1 (5-12) met alle instrumenten en een kick + crash op de eerste tel: zo blijft alles uit de bron.
  Let bij zo'n sprong op het ritme van de riff (riffmaat / lege maat om en om): 4 -> 53 klopt omdat 52 -> 53 zo is.
- audiocheck meldt een "constante toon" in een nummer met een solo-intro: de stilte tussen de riffs maakt de mediaan
  klein. Controleer eerst of de stille stukken echt 0 zijn (Dave: ja, 77 Hz = de bas, geen bromtoon).
- Zinnia (v0.9.60, Jordi: 'knappert soms'): de mixer sloeg om op stapels strijkers (tot 12 noten, vel 127) + synthbas
  + kick. Alleen -V omlaag (90 -> 72) hielp niet genoeg; per categorie zachter (`volume=` in prepare_auto: strijkers 80,
  synthbas 85, orgel 105, drums 112) + -V072 gaf 0 overlopen, piek 118/127.
- Ghetsis (v0.9.60, Jordi: 'lange puuup bij de vocalen'): de koperpartij speelde de 'Ghetsis!'-koorakkoorden twee
  octaven lager mee (noot 18-27) en de e-piano had noten 7/13. Een sample zo ver omlaag gestemd = trage, lange 'puuup'.
  `prepare_auto(..., min_note={kanaal: 36})`. De lint waarschuwt al voor noten < E1: neem die waarschuwing serieus.
- Raikou (v0.9.60, Jordi: 'valt een beetje weg'): een PSG-lead naast het volle origineel op spoorvolume 72 is te zacht;
  127 + duty 25% (voller dan 12,5%). Suicune (klokken) en Entei (gitaar) goedgekeurd.
- Neo Plasma v2 (Jordi: 'puur synth-deuntje, lijkt qua instrumenten niet op het origineel'): `prepare_auto` groepeert
  per GM-categorie en zette gitaar (27) + sawtooth (81) samen op één PSG-vierkant, sine op een tweede vierkant en de
  **steel drums (114) op een crashbekken** (categorie 'cymbal' = 112-119). Gebruik `prepare_auto` niet meer voor een
  nummer dat herkenbaar moet blijven: lees per bronspoor programma, register en rol uit en kies per spoor een echt sample
  in een eigen voicegroup (`neo_plasma_theme.py`). PSG alleen voor wat in de bron echt '8-bit' is, zacht.
- audiocheck meldt bij snelle nummers (176 bpm) 'constante tonen' op 59,7/119,5 Hz: dat is de framesnelheid. De m4a-
  sequencer start noten alleen op framegrenzen; bij een 16e van 5,1 frames geeft een rij drum-/gitaaraanslagen spectrale
  lijnen op veelvouden van 59,73 Hz. Geen bromtoon (zit ook in de oude versie); controleer met een opname per spoor.
- Ghetsis ronde 2: min_note 36 was niet genoeg; koper (trompet-keysplit) onder C3 klinkt nog als 'puuup'. Voor koper
  min. C3 (48), voor piano/strijkers is C2 (36) prima. Raikou: buzz 110 = goed (127 net te hard, 72 viel weg).
- Neo Plasma v3: **balans meten i.p.v. raden.** `balance.py` (FluidR3-render van de bron per groep vs. GBA-solo via volX
  = 0 op de andere sporen) liet zien dat gitaar/orgel 7-9 dB te zacht zaten. Bij een bron met overal dezelfde velocity
  (onlinesequencer) is de GM-render de beste referentie. Velocity op 127 en balans met CC7 geeft meer ruimte.
- **Ontbrekend instrument? Maak een sample** met `gm_samples.py` (FluidR3, `apt-get install fluidsynth
  fluid-soundfont-gm`): uitklinkende instrumenten zonder loop, aanhoudende golven als exacte loop van een paar perioden.
  Liever het juiste instrument dan een 'verwante' sample (schone gitaar ≠ distortion).
- -V127 liep over (26x) terwijl -V108 maar piek 86 gaf: niet lineair, dus altijd opnieuw meten.

- Keccles v1 (`keccles_theme.py`, salsa dura, 190 bpm, Am, clave 2-3): er is geen trombone-sample; trombone =
  trompet-keysplit een octaaf lager (A3-D5, nooit onder C3). Eigen drumkit in `drumsets/keccles.inc` (naam
  `<x>_drumset`, dan vindt de lint hem): clave/cascara = hyoushigi (66/79), timbales = sc55-tom hoog (70/77),
  campana = sd90_cowbell, conga's = mute_high/open_low, rimshot = orchestra_snare op 72; alles DirectSound. Güiro
  op het PSG-ruiskanaal (lang-kort-kort per tel) kost geen kanaal. Eigen keysplit `keysplits/<x>.inc` met
  `voice_group <x>_keysplit`: dan rekenen `releases()` en de lint met de echte release. Montuno-piano in octaven op
  elke achtste: release 150 + nootlengte 11 ticks (= precies een achtste bezet), anders 4 pianonoten tegelijk.
  Timbale-fills vielen eerst weg (11%) achter piano/conga: fills en rimshots op de sectiegrens boven piano in de
  prioriteit. -V100 gaf piek 127/127 (geen overloop, maar op de grens) -> -V088: piek 111, RMS 2560.
  Loop naadloos: de maat vóór het loopbegin in de intro (3) is gelijk aan de laatste maat van de loop (51), en
  geen noot loopt over de loopgrens (tumbao-anticipatie daar inkorten).
- Ghetsis ronde 3 (v0.9.65): ik zocht de 'puuup' twee keer in het verkeerde spoor (koper). **Vind een geluid eerst met
  solo-opnames per spoor** (volX = 0 op de rest, zie `balance.gba`; vensters van 0,25 s) i.p.v. te gokken uit de MIDI.
  Het was drumnoot 49 = PSG in rs_drumset. **Lint-meldingen 'drumnoot is PSG' altijd oplossen** (`drum_map`), nooit
  laten staan. Niet aankomen wat Jordi goed vond (de vocalen).

- Shaymin v1 (`shaymin_theme.py`, 6/8, gestippelde kwart 88, D-groot): eigen samples uit FluidR3 voor harp, celesta,
  nylon, fluit en klarinet. `gm_samples.py` kan nu ook **aanhoudende instrumenten met een loop** renderen
  (`loop=(begin_s, perioden)`): samplerate = grondtoon x 32/64, loop van exacte perioden, het loopeinde vloeit over in
  het loopbegin (geen klik). Stemverdeler-trucs: gitaar wijkt vooraf voor de celesta-blaadjes (anders willekeurige gaten,
  22% -> 7%), pad per halve maat; bongo's (0,1 s-sample) niet als `drum_parts` tellen (drum_len 1 tel overschat ze),
  alleen de triangel. -V100: piek 87/127, RMS 2770.
- Magikarp v1 (`magikarp_theme.py`, komisch, 150 bpm, Bes): **glijtonen via pitch bend werken** in mid2agb/m4a:
  CC20 = BENDR (bereik in halve tonen), pitchwheel → BEND (alleen de MSB telt: ±64 = ±BENDR), CC1 = MOD (vibrato),
  CC21 = LFOS. `Song.add(..., extra=[(tick, mido.Message)])` schrijft ze weg (na note-offs, vóór note-ons op dezelfde
  tick). Zet de bend pas terug bij de volgende noot (niet bij de note-off: dan springt de uitklinkende staart omhoog).
  In de .s staan na de eerste `BEND` alleen nog waarden (running status), dus `grep -c BEND` telt niet alles.
  Eigen samples: fagot/woodblock/vibraslap uit FluidR3 (drumnoten via `('drum', n)` in gm_samples), kazoo als
  gesynthetiseerde zoempuls met formanten, boing als synth-oneshot (`ONESHOTS`). Fluitje (sd90 whistle) + BENDR 12
  = slide whistle. -V108: piek 89/127, RMS 2377.
- Jirachi v1 (`jirachi_theme.py`, eigen compositie, 152 bpm, D-groot, climax in E): **sync met een transitie meten,
  niet uit de code afleiden.** Lees per frame `gMPlayInfo_BGM.clock` (offset 12; 24 per tel) naast de gemiddelde
  helderheid van het beeld: de route-transitie begint ±25 frames ná de muziek (eerst dimt het beeld), dus de flits
  (t = 68) viel op tel 4, niet op tel 3. Tempo zo kiezen dat de transitiemomenten op tellen vallen (23,7 frames/tel).
  Ontbrekende instrumenten via `gm_samples.py`: celesta (GM 8), speeldoos (GM 10) en een windgong als `RUNS`-sample
  (een loopje glockenspielnoten in één sample = één kanaal). Lange koornoten in stukken van 2 tellen: 36% -> 10%
  weggevallen. Harp-release 170 (i.p.v. 242) voor 16e-arpeggio's. audiocheck '120 Hz' = 2x framesnelheid (119,45 Hz
  precies), geen bromtoon.
- Heatran v1 (`heatran_theme.py`, stoner metal à la Kyuss, 116 bpm, D/drop D): **een powerchord als één sample**
  (G2+D3+G3 samen door de FluidR3-fuzz gerenderd) = 1 kanaal per akkoord en klinkt echter dan losse noten (de
  intermodulatie van een echte versterker zit erin). Dubbele opname = tweede spoor rechts met een vaste pitchbend van
  +3 (±9 cent). `gm_samples.py` kan nu akkoorden (noot als tuple), GM-drums (programma 128), een automatische
  gecrossfade loop (`'auto'`, voor aanhoudende fuzz) en extra overdrive (`DRIVE`, fuzzbas = picked bass + tanh);
  nieuwe samples krijgen een anti-aliasfilter bij het omlaag resamplen (fuzz zit vol hoge tonen). Bends en vibrato
  op de lead: pitchwheel/CC1 pas terugzetten op de volgende noot (bij de note-off zakt de uitklinktijd mee).
  Fuzzbas (tanh) is veel dichter dan de gitaar: spoorvolume 54 i.p.v. 84 (solo-RMS gemeten). -V112: piek 99/127.
- Rayquaza v1 (`rayquaza_theme.py`, gamelan/gong kebyar): het weather trio-thema maat voor maat behouden, alleen
  instrumenten vervangen + gamelanlagen. **Pelog selisir op de grondtoon (R, R+1, R+3, R+7, R+8)** valt op C samen
  met de kerntonen van het thema (C-C#-G-G#-D#): melodie intact, kotekan/kempli in pelog. Gamelan-samples zelf gemaakt
  (`gm_samples.py` ADDITIVE: inharmonische partialen met t60 per partiaal, geen loop); **ombak in de sample bakken**
  (tweede, licht ontstemde kopie) kost één kanaal per paar. Kotekan: polos/sangsih om en om op de zestienden
  (nooit tegelijk) met release 175 = ±2 kanalen. Gong/kempur: noot kort (2 maten / 1 maat) houden, anders zit de
  gong de stemverdeler 4 maten dwars. Eenstemmige metallofoonlijnen `detach()`en. Kendang (indian drum/conga's op
  elke achtste) geeft in audiocheck een 'constante toon' rond 175-180 Hz: de toonhoogte van de trommels, geen brom
  (solo-opname: kendang 12% van het spectrum in die band). -V076: 0 overlopen, piek 94/127, RMS 2800.
- Keccles v2 (Jordi: 'te eentonig, reguliere salsa i.p.v. Colóns salsa dura'): structuur met contrast i.p.v. meer
  noten: hook eerst alleen 2 trombones in tertsen, corte (tutti-stoot + stilte), zachte coro (koor + cuatro-antwoord,
  geen clave/bongó), pianosolo, descarga (bas + percussie), gestapelde mambo, en **CC7 per spoor per sectie**
  (`Song.add(..., ccs=[(tick, 7, v)])`; mid2agb kent alleen CC7/CC10/CC1, CC11 doet niets). Zet de CC7 op elk
  sectiebegin opnieuw (ook het loopbegin; mid2agb zet een VOL op de looptick ná het label, dus dat werkt). Meet de
  RMS per sectie (niet per 5 s): coro 1600 vs. mambo 2700-3170.
- Eigen samples uit de GM-drumkit: `gm_samples.py` met programma 'drum' (kanaal 10, grondtoon 60) en `loop='auto'`
  voor koper (loop van hele perioden + crossfade). Trombone = FluidR3 GM 57 op vel 127 (brallend), 2 samples op de
  keysplit-tabel french_horn.
- Montuno-octaven: nootlengte + uitklinktijd moet ≤ een achtste zijn (10 + 14 ticks), 1 tick overlap = 2 extra stemmen
  op elke tel: daardoor vielen 9% van de bongóslagen weg. Analyse 'wat klinkt er als een noot wegvalt' per maat.
- Een melodie-constante met dezelfde naam als een programmaconstante (CORO) overschreef het programma: geef
  melodieën een achtervoegsel (`CORO_MEL`).
- Keccles v3 (Jordi: 'ruimte voor een riffende elektrische gitaar à la Vigilante? Niks weghalen'): een laag
  tóévoegen zonder iets te veranderen = nieuw spoor áchteraan (`TRACKS`, eigen kanaal) en **als laatste in de
  `allocate`-volgorde** (de verdeler is gretig per spoor: de bestaande partijen houden exact dezelfde noten en
  weggevallen percentages). Controleer met een diff per MIDI-spoor (noten/CC's identiek). Waar de mix al vol zit
  (maat 47: trombone-swell + timbalefill) viel de hele gitaarfill weg: daar niets zetten. FluidR3 GM 29
  (Overdriven) is in de 2-4 kHz al zo fuzzy als een distortion; lichte crunch = GM 27 (clean) door `tanh` x4 +
  lowpass 3,5 kHz (`CRUNCH` in keccles_samples.py). Solo-meting gitaar: descarga -3 dB onder de rest (solo), mambo
  -9 dB (kruiding).
- Magikarp v2 (Jordi: 'het eerste dominante deuntje te hoog, tot het irritante aan toe'): kazoo een octaaf lager (F3-D5),
  xylofoon-verdubbeling een octaaf boven de kazoo (i.p.v. twee) en zachter, fluitje niet boven D6. **Meet 'schel'**:
  aandeel van het spectrum boven 2 kHz per sectie (A: 31% -> 14%, boven 4 kHz 9,8% -> 2,8%, zwaartepunt 1660 -> 1070 Hz).
  **Een echte cry als sample**: de Gen 3-cry (`cries/<soort>.wav`, 8 bit 10.512 Hz) kan zo als gewone DirectSound-sample
  (grondtoon 60, eigen generator `magikarp_samples.py`); DJ-scratch = varispeed (aantrekken 0,35x -> 1,15x, afkappen,
  kort achteruit). In de drumkit + een eigen spoor met hetzelfde programma 127 = eigen volume. Niet in de intro: de
  echte cry van een wilde Pokémon klinkt daar al (±2,3-3 s). Solo-RMS cry 1300 vs. kazoo 1850 = net onder de lead.
- Shaymin v2 (Jordi: 'thema uitstekend, maar meer route- dan battle-theme'): zelfde melodieën/instrumenten, maar
  gestippelde kwart 88 -> 112, intro-stoot (D - C/D - Bb/D tutti + toms), bas-ostinato in achtsten (contrabas uit
  FluidR3, `shaymin_samples.py`), spiccato-strijkers (string_ensemble met harde aanzet, release 130) en een lichte kit
  (FluidR3-bassdrum/toms, orchestra snare, tamboerijn, kc-bongo's). Het B-deel half-time met tom-hartslag en dan een
  opbouw (snare 8sten -> 16den, spiccato-tremolo). **Een routenummer battle-waardig maken = ritme, niet meer lagen:**
  harp-/bas-/spiccatonoten zo kort dat nootlengte + uitklinktijd ≤ een achtste is (eerst 67% celesta weg, daarna 0%);
  gitaar/pizzicato uit de drukke delen (C: pizzicato speelt de spiccato-figuur = lichter). audiocheck '37-43 Hz' = de
  grondtoon van de bassdrum op elke tel, geen brom. -V088: piek 102/127, RMS 2790.
- Rayquaza v2 (Jordi: 'pas op 28 s herken ik het, tonen weggevallen 50-60 s en vanaf 1:10; mag intenser, lage
  koren'): de stemverdeler liet niets vallen; de herkenning zat in sporen die ik had vervangen. **Meet bij een remix
  eerst per bronspoor solo wat het origineel draagt** (`tools/grounded/solo_rms.py`: RMS per sectie per spoorgroep): in maat 8-19 waren de pauken
  (G-C-ostinato) het luidste spoor, daarna bas en de PSG-lijnen; de trompetmelodie zelf was zacht. v1 maakte van de
  pauken ongestemde conga's, liet de PSG-sporen weg (kotekan ervoor in de plaats) en de bas alleen op de tellen.
  Herkenbaar bleef alleen maat 20-23, waar de fluit (suling) de melodie draagt. Fix: pauken op gestemde
  kendangslagen (conga 222 Hz -> key 58/63 = G3/C4; toonhoogte van een drumsample meten met een FFT), PSG-sporen
  1-op-1 terug (incl. programma-/CC-wissels en XCMD-echo: `src_events`), hele baslijn. Pelog-kotekan: een toon van het
  origineel die niet in de toonladder zit vervangt de buren (anders Db/Eb tegen D). Laag koor als kwint-tweeklank in
  één sample (FluidR3 52+53 op C3+G3, `rayquaza_samples.py` CHOIRS). Spookslagen als aparte partij met de laagste
  prioriteit (anders verdringen ze de sangsih: 25% -> 3%). -V070: piek 91/127, RMS 2840. audiocheck '196 Hz' = de
  op G3 gestemde kendang (45% van zijn solo-spectrum in die band), geen brom.

- Heatran v2 (Jordi: 'geen stoner metal maar Bowser's Castle-metal; meer heavy, meer fuzz', met een genrebeschrijving):
  **een genre = een vorm, niet alleen een klank.** v1 had de juiste instrumenten maar een metalstructuur (riff na riff,
  alles vol). v2 (100 bpm, drop C) volgt de vorm: strofen alleen fuzzbas + drums (melodische baslijn, hihat/ride, ghost
  notes), later zacht de **refreinriff palm-muted**; refreinen halftempo (snare op 3) met de riff voluit, bas + gitaren
  unisono, syncopen en een stopmaat; rustig middenstuk met cleane arpeggio's (dorisch) en opbouw. Dynamiek meten per
  sectie (RMS via recaudio: strofe 1500-2500, refrein 3500-3800). 'Big Muff' = eigen fuzz in `heatran_samples.py`
  (`muff()`: 150-700 Hz +6 dB, twee tanh-stadia, lowpass 3,4 kHz); een octaaffuzzbas verliest zijn grondtoon in de
  fuzz -> schoon laag (< 160 Hz) erbij mengen (bas-blend). Laat de stopmaat aan het eind van de loop gelijk zijn aan
  de laatste intromaat (naadloze loop). -V100: piek 110/127, 0 overlopen, RMS 2911.
- PSG-drums opgeruimd (v0.9.67) in Zinnia, Colress, Giratina, Birch, Sunset Wilds, Yoshi's Castle en Broken Pier via
  `drum_map` (ook in `prepare()`; waarde `(noot, factor)` schaalt de velocity, bv. side stick -> snare x0,6).
  **Drumnoten buiten rs_drumset (36-64) lezen de buren in het geheugen**: boven 64 = `frlg_drumset` (noot n -> frlg
  n-29; Birch' open triangel 81 = frlg 52 = PSG-blokgolf), onder 36 = het einde van `dummy.inc` (35 = hyoushigi,
  33 = unknown_snare). Reken het na met `arm-none-eabi-nm pokeemerald.elf | grep drumset` (label = begin - 36x12).
- Jirachi v2 (Jordi: 'vet om tussen 40-50 s op te bouwen naar een climax met een stuk hogere BPM, euforische
  Ibiza-trance, en dan terug naar de hoofdmelodie een octaaf hoger'): begin 1-op-1 behouden (MIDI tot de opbouw
  noot voor noot vergeleken met v1), dan opbouw -> drop -> breakdown -> drop -> ritardando naar het thema in E.
  **Tempowissel per tel** via `Song.tempo` (152 -> 168, ease-in; ritardando per achtste terug); 138-140 'trance-bpm'
  zou trager zijn dan de 152 van het thema, dus 'hoger' = 168 + four-on-the-floor. **Supersaw als één sample**
  (`jirachi_samples.py`): 7 zaagtanden met M+k trillingen per loop van M perioden = exacte loop mét zweving (M = 128 ->
  13,5 cent per stap); 1 kanaal per akkoordnoot. 'Filter dat opengaat' = drie samples (dark/mid/bright) waartussen het
  spoor per maat wisselt + CC7-ramp per tel. Weinig harmonischen in de sample (de GBA transponeert zonder filter:
  aliasing); de lead krijgt een eigen sample op C5. Hihats, riser en sub op PSG (ruis met programmawissel per sectie,
  golf) kosten geen kanalen. Trance-partijen op sporen van instrumenten die dan zwijgen (programmawissel + CC7 via
  `ccs`, terugzetten op de sectie erna; max. 16 sporen). Een opbouw is snel luider dan de drop (aangehouden supersaw
  + roffel + riser): RMS per seconde meten en de opbouw zachter beginnen, anders 'valt' de drop weg. -V100: piek
  102/127, RMS drops 3470-3550, opbouw 3340, breakdown 2500.
- Ronde 2 (5 okt): **goedgekeurd**: Keccles v3 ("niet helemaal wat ik bedoelde, maar leuk, perfect zo"), Shaymin v2,
  M2 (PSG-drums: Giratina, Sunset Wilds, Broken Pier, Yoshi's Castle "overduidelijke verbetering"). Zinnia klinkt Jordi
  'niet als GBA', maar is gewoon grounded_gm (game-samples): een strak gearrangeerde bron met weinig gelijktijdige
  partijen in het goede register is wat het doet klinken.
- Jordi's Jirachi-idee was **geen tempo-opbouw van de bestaande delen**, maar een **tussenstuk met lang uitgerekte
  'wahhh'-vocalen boven een snelle beat**, daarna terug. Vraag bij een vaag idee door of geef twee varianten.
- Magikarp v3 (Jordi: 'hoofdtoon iets te luid; de scratch mag vaker'): **lead zachter = solo-RMS per sectie meten**
  (kazoo vs. alle andere sporen samen): A 1833 vs. 1527 -> kazoo-volume 100 -> 67 (-3,7 dB gemeten), cry mee omlaag
  (90 -> 60, elke scratch 4-6 dB onder de kazoo), en het verlies in de totale mix terug met -V108 -> 120 (piek 94/127,
  RMS 2403). Scratch-varianten als losse drumkit-noten: stotter ('Ma', 0,08 s, in zestienden), dezelfde scratch een
  kwart hoger (key 65 in de kit = toonhoogte, de gespeelde noot telt niet) en de cry achterstevoren die 2 ticks vóór de
  loopsprong eindigt (riser naar de crash van A1). Eigen solo-RMS-script met de echte maatgrenzen (5/8, 7/8): kopie van
  `solo_rms.py` met secties uit `START` van het thema; de eerste 0,2 s van een opname is ruis van de vorige muziek.

- Neo Plasma v4 (Jordi over v2/v3: 'rotzooi, klinkt totaal niet zoals de bron, eentoniger'): **meet tegen een opname van
  het origineel, niet tegen een GM-render van de MIDI.** Werkwijze: (1) bronscheiding met Spleeter 4 stems (`pip install
  --no-deps spleeter` + typer/pandas/future/norbert/ffmpeg-python; model `4stems.tar.gz` van de GitHub-release van
  deezer/spleeter; demucs-/torch-downloads zijn geblokkeerd); (2) uitlijnen: onset-kruiscorrelatie per 8 maten (de
  MIDI liep exact gelijk met de mp3, maat k = 0,75 s + k x 1,364 s) en structuur: de MIDI bevatte de loop twee keer
  (74-137 = 10-73) -> v4 = intro 0-9 + loop 10-73; (3) **instrument per spoor kiezen met NNLS**: render elk bronspoor
  solo met kandidaat-GM-programma's en kijk welke combinatie het mel-spectrogram van het origineel het best verklaart
  (per sectie): 'Electric Guitar' bleek een aanhoudende synth brass, de bas Slap Bass 2 een octaaf lager, het orgel
  percussief, de kit een grote elektronische kick (de MIDI-snares op de off-beats zijn hihats); (4) balans met
  `tools/grounded/balance_orig.py` (GBA-solo per groep, NNLS tegen het origineel + octaafbanden per sectie).
  v3 had 31-125 Hz 4-9 dB te weinig en 0,5-8 kHz 4-5 dB te veel (dun, schel); v4 zit overal binnen ±1,5 dB (8 kHz +4).
- Uitlijnen op aanslagen (kick op elke tel) kan precies één tel verkeerd vallen; `balance_orig.align` lijnt uit op chroma.
- Spectrogrammen (CQT, log-frequentie) van origineel en GBA naast elkaar als PNG bekijken werkt goed om rollen te zien:
  lange lijnen = doorklinkende noten (het origineel liet arpeggio's/akkoorden doorklinken; de MIDI had korte noten),
  een constante lage lijn = een te lang uitklinkende, gestemde kick op achtsten (bromde op 52 Hz -> kick korter, op C2).
- Spleeter-stems zijn bruikbaar voor drumpatronen (aanslag per band per 16e) en octaafcontrole per spoor (energie op f0/2,
  f0, 2f0), maar harmonische vingerafdrukken uit een volle mix zijn onbetrouwbaar (te veel overlap).
- Rayquaza v3 (Jordi: 'te rustig, melodie valt weg tegen het getokkel, kebyar feller, gongs keihard op de
  maatovergangen'): **een remix speelt in het tempo van het origineel** (196 bpm vast; v2 had een statig intro op 0,82x
  en was daardoor 1,1 s langer). Melodie weer op de **originele instrumenten van het melodiespoor** (trompet/strijkers/
  hoorn met dezelfde programmawissels, en spoor 2 in maat 8-19 erbij zoals in het origineel), de gamelan alleen nog als
  korte kleur (reyong één aanslag, release 205; opnieuw aanslaan van lange noten vertroebelde het ritme). Meten met
  `solo_rms.py`: melodie t.o.v. kotekan v2 +2..+4 dB -> v3 +6..+11 dB. Angsel = alles afkappen op tel 4 behalve
  noten die precies op 4 en 4+ beginnen (daar heeft het origineel zelf zijn stoten) + klappen; **de gong moet vóór de
  angsel uitgeklonken zijn** (anders hoor je geen stop) en de klappen op korte releases (gedempte gangsa 140, pauken via
  een programmawissel naar een kopie met release 165). Zware maatovergang om de 2 maten = gong + lage gongbas + echte
  pauken; de gongnoot een uitklinktijd vóór de volgende gong laten stoppen, anders vallen bas/reyong weg op precies die
  tellen. Partijen met hetzelfde programma delen na de stemverdeler een spoor (byar->gangsa, kempur->gong) om onder de
  16 sporen te blijven; let dan op de release van het programma van dat spoor (lint rekent daarmee). -V074: piek
  94/127, RMS 2970. audiocheck '133 Hz' = gong/gongbas/pauken op C (16% van hun solospectrum), geen brom.
- Jirachi v3 (tussenstuk i.p.v. versnelling): reguliere delen weer noot voor noot v1 (gecontroleerd met een diff per
  MIDI-kanaal), deel C vervangen door een tussenstuk van 16 maten op 164 bpm (abrupte tempowissel erin en eruit, geen
  ease). **Lang uitgerekte vocals = één noot-aan met pitch bend:** BENDR 4 geeft exact 16 BEND-stappen per halve toon
  (BENDR 12 = 5,33: vals), zodat G5 -> F#5 -> E5 of D6 -> C#6 -> D6 -> B5 als één 'aaah' van 4-6 maten glijdt; scoop
  van een halve toon onder de noot bij de inzet, MOD (vibrato) pas na een tel laten opkomen, aanzwellen via CC7.
  **FluidR3 Choir Aahs (52) pulseert** (luidheid x0,6-x2 per 50 ms; Voice Oohs 53 is stabiel): na de aanzet egaliseren
  met een omhullende van 60 ms, en ná de loop-crossfade nog eens cyclisch over de loop (de crossfade doofde 40% uit).
  Balans gemeten met `solo_rms.py` (vocals vs. rest): totaal -4 dB door de kick, maar boven 200 Hz +3,5 dB = de vocals
  leiden. Een programmawissel op een spoor dat in de maat ervoor nog speelt (hoorn in B) pas op de eerste tick van het
  tussenstuk zetten, anders zingt de vocal-sample de hoornnoten.
- Heatran v3 (Jordi: 'nog steeds surf rock/ska-punk/60s rock', strikte briefing Kyuss/Sleep): **een genregevoel eerst
  meten, dan pas klank.** De v2-mix was al vrij donker (zwaartepunt 400-1000 Hz); het 'surf/ska' zat vooral in het
  ritme en de wendingen: 100 bpm, korte riffstoten (gem. 0,78 tel; losse noten 0,07 tel na detach), 16e-baslijn (2,9
  aanslagen/s), kick 60% naast de tel, ghost notes, hihat-8en met open hihat op de laatste 'en', chromatische
  opstapjes (G-Bb-B -> C). En in de klank: Muff mét middenboost (= 60s-fuzz-honk), fuzzlead 46% > 2 kHz, schone GM 27
  (twang) in het middenstuk. v3: 84 bpm, aangehouden powerchords (gem. 1,2 tel), slides i.p.v. opstapjes, bas 1,2
  aanslagen/s, bekkens 0% naast de tel (kwarten), snare op 3 in de refreinen; fuzzketen = schone gitaar -> Muff
  (middenscoop) -> SVT/kast (lage shelf, steile lowpass 3,2 kHz) in `heatran_samples.py`; FluidR3 'Power'-kit
  (programma 16 op kanaal 10). Meetscripts: zwaartepunt / % < 500 Hz / % > 2 kHz per sectie, nootlengtes en
  off-beat-aandeel per spoor. **Dezelfde toonhoogte mag in één spoor niet overlappen** (arpeggio's die doorklinken):
  de note-off van de eerste kapt de tweede af; inkorten tot de volgende aanslag. -V090: piek 107/127, RMS 2938.

- Neo Plasma v5 (Jordi over v4: melodie strak, tempo exact, scherpe pulse-lead, punchy brass, diepe staccato-bas,
  standaard drumkit, melodie voorop). **De GBA speelt elk tempo 0,45% te traag** (59,73 i.p.v. 60 frames/s) en kent
  alleen even bpm's (`TEMPO` = bpm/2): 176 klinkt als 175,2 (gemeten). Moet het exact gelijk lopen met een opname
  (hier 175,96 bpm, gemeten met een kickraster over het hele nummer), wissel dan per tel 176/178 (Bresenham,
  `tempo_map` in neo_plasma_theme.py): gemeten 175,965. **Timing van een transcriptie per spoor controleren**: schuif
  de noten van één spoor ±48 ticks en zoek waar de toonhoogte-specifieke aanslagen (spectrale flux op de harmonischen
  van elke noot) in de opname het sterkst zijn, t.o.v. de andere sporen. Het sawtooth-spoor stond 17 ticks te vroeg,
  het orgel 'strumde' 24 ticks vóór de tel (`tools/grounded/transcript_check.py`). Noot-voor-noot-controle met
  harmonische salience (eigen toonhoogte vs. ±1/±2 halve toon, buren die een ander spoor verklaart niet meetellen) vond
  in de melodie geen consistente fouten; meldingen in snelle 16e-arpeggio's onder C4 zijn ruis van de volle mix.
- Bas een octaaf lager zonder noten < E1 in de MIDI: **label de sample een octaaf te hoog** (`write_wav(..., key)`:
  gesynthetiseerd op C2, gelabeld C3) en laat de MIDI-noten staan. Een gestemde kick op B1 (62 Hz) gaf in de
  chroma-vergelijking op elke tel een 'extra B' t.o.v. het origineel: drums ook tonaal controleren.
- Staccato-partijen (16e-stoten brass/orgel) bezetten met de release 2 kanalen per noot: `detach()` op elke
  DirectSound-partij (orgel 11% -> 0,2% weggevallen, steel drums 38% -> 1%).
- SickBlik v1 (`sickblik_theme.py`, slap-funk à la 'Dean Town', 108 bpm, E-dorisch): **articulaties = aparte programma's
  met eigen samples** (thumb, pop, dode thumb, dode pop; `sickblik_samples.py`), elk op een eigen spoor, maar als één
  snaar behandeld (`one_string()`: elke noot stopt bij de volgende, minstens de halve afstand). **Hammer-on = pitch bend
  op de klinkende noot** (geen nieuwe aanslag), slide = bend van -2 halve tonen omhoog in 4 stappen van 3 ticks.
  FluidR3 Slap Bass 1/2 hebben geen velocitylagen en zijn dof (2-5 kHz 2-4% in de aanslag): eigen aanslag (hoog deel
  > 1,5 kHz x6 met 20 ms-envelope + ruisstoot) -> 15%, geen 'zaag' (> 5 kHz < 1%). Dode noten = dezelfde aanslag die in
  12-20 ms uitsterft. FluidR3-pops beginnen +3 halve tonen hoog en zakken in 30 ms (zoals een echte snaar): een
  toonhoogtemeting van korte pops in de game (80 ms-venster) geeft +0,5-1 halve toon; geen stemfout (na 40 ms +10 c).
- Unisono-blazers als één sample (trompet + tenorsax een octaaf lager samen gerenderd) = 1 kanaal per noot; een tweede
  sample vanaf C5 (minder transponeren). In de drukste hook de hihat in 8en i.p.v. 16en: de clavinetverdubbeling viel
  dan nog maar 5% weg i.p.v. 17%.
- `solo_rms.py` rekent met 24 ticks per tel in de MIDI (`sec_at`); bij TPB 96 een kopie met eigen secties maken.
  -V125: 0 overlopen, piek 99/127, RMS 2223 (A 1800-2000, hook 2400-2600).

- Mitch v1 (`mitch_theme.py`, Drum & Bass, 174 bpm, F-klein; samples `mitch_samples.py`): **het PSG-golfkanaal speelt
  een golf van één periode (ProgrammableWaveData_8) een octaaf lager dan genoteerd, en kan niet onder ±32,7 Hz** (CGB-
  frequentieregister); een golf met twee perioden (Data_1, Jirachi) klinkt op de genoteerde hoogte maar dus niet onder
  ±65 Hz. Een sub op F1 (43,7 Hz) = Data_8 en F2 noteren. Gevonden met een solo-opname (eerst gegokt: 32,7 Hz in elke drop).
  Reese = twee zaagtanden met M±1 trillingen per loop (zweving in de sample); 'pratende' bas = programmawissel per noot
  (dicht/half/open/grom). **Wobble op tempo = filter-LFO in de sample**, twee maten per loop, één sample per grondtoon
  (M = 2 maten x f0 afgerond: < 0,4% tempofout); getransponeerd zou hij versnellen. Eerste mix had 75-85% van het
  spectrum onder 150 Hz en < 2% boven 2 kHz (snare/hihats verdwenen): grondtoon in de reese-samples x0,45 (de PSG-sub
  draagt het laag), snare met meer ruis en highpass 230 Hz, hihats (ruis) 40 -> 90, ride 70 -> 112, kick x0,8 met een
  klik. Meet de banden per sectie (`spec.py`-achtig: <150 / 150-600 / 0,6-2k / >2k). DJ-rewind = een maat drop
  achterstevoren met een snelheidscurve die ±1 maat materiaal verbruikt (anders is het na 0,4 s op en hoor je stilte).
  -V100: 0 overlopen, piek 85/127, RMS 2614.
- Ashfrost v1 (`ashfrost_theme.py`, wintervariant van Fallarbor, 148 -> 138 bpm): het origineel spoor voor spoor gekopieerd
  (noten, CC7-swells), alleen programma's gewisseld + sleebellen/wind erbij. **Het vanilla-origineel zelf haalt de lint
  niet** (tot 19 noten door harp-/glockenspiel-releases 242/249): in een eigen kopie van de voicegroup de releases korter
  (harp 175, glock 200, fluit 135), legato-partijen op een andere klank (pad, contrabas, hoorn) een uitklinktijd eerder
  loslaten, korte doorgangsnoten in een pad met trage aanzet weglaten, en een parallelle draaier in de tegenstem tot één
  noot. **FluidR3-klarinet (GM 71) is onbruikbaar als lead:** 87% van zijn energie zit in de 3e boventoon (2-4 kHz) =
  schel in de GBA-mix (solo 300-550 'boven 3 kHz' vs. 50 voor de fluit). Meet de helderheid van een GM-programma vóór je
  het kiest (`render()` + FFT; fluit/blokfluit/ocarina/hobo < 3,5% boven 2 kHz). Blokfluit (GM 74) op D5 gerenderd = zacht.
  Een aanhoudende lead op de plek van een uitklinkende nylon klinkt ±3 dB luider (CC7 x 0,75). PSG-ruis als wind: toets
  ±50 (LFSR ±1 kHz = laag 'whoosh'), stem `voice_noise 60,0,0,7,0,15,7` + CC7-zwelling met top 14-20 (100 = luider dan
  de hele mix). Een windnoot op tick 0 bleef stil: begin de eerste vlaag een maat later. -V116: piek 65/127, RMS 1924
  (origineel Fallarbor 1939).
- Ronde 3 (5 okt): **goedgekeurd**: Ashfrost (wintervariant). Rayquaza v3: balans trompet/melodie "precies zo houden".
  Jordi geeft nu gedetailleerde briefings (vaak met Gemini geschreven); volg ze punt voor punt en houd wat hij goed
  vond expliciet ongewijzigd (diff per spoor).

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

### Feedback ronde 5 (Jordi, 5 okt middag)
- **Goedgekeurd:** Jirachi v4 ("geweldig, done"), SickBlik v2, Rayquaza v4 ("perfect"). Niet meer aanraken.
- **Heatran → v5:** gebaseerd op Kyuss' "Odyssey": traag sludge-stuk (~75 bpm) wisselt met snelle desert-pump (~135 bpm). Moet klinken alsof Kyuss de originele R/S-Heatran-baasmuziek op de GBA inspeelde: crunchy low-bitrate gitaarsamples (C-standard), doffe fuzz-synthbas die de gitaar volgt, doffe Gen 3-drums (doffe snare, blikkerige crashes). Geen moderne studioklank.
- **Mitch → v3:** v2 klonk als drukke chiptune/happy hardcore; alleen het stuk rond 1:00 had de juiste sfeer. Duister, minder pieperig (leads 1–2 octaven lager), less is more, two-step 172 bpm met keiharde droge snare + ducking, lage reese met portamento, intro → build-up → 1 tel stilte → drop.
- **Neo Plasma → v7:** te kaal/dun. Octaafverdubbeling van de lead, sub onder de bas, gesplitste arpeggio's L/R, staccato off-beat-akkoordstoten, four-on-the-floor met ghost-snares en 16e-hats met accenten.
- Neo Plasma v7 (Jordi over v6: 'kaal, dun, los zand'; GBA-lagen): lead op bronhoogte (DS) + octaaf lager op PSG-
  vierkant 1 (vel 96), sub op de PSG-golf, arpeggio B op PSG-vierkant 2 (16 ticks later, pan 85), off-beat-tweeklanken
  (np_stab) alleen uit brontonen (gitaar is meestal 16e-octaven = alleen grondtoon -> arpeggiotonen van die tel; geen
  secundes, niet in unisono-riffs), four-on-the-floor, snare 2/4 + ghosts, 16e-hats met accent op de kwart.
  **PSG-noten onder C2 (36) klinken allemaal als C2** (`MidiKeyToCgbFreq` klemt key <= 35): een sub-bas op de golf kan
  niet onder 65 Hz. **De game staat standaard op mono** (`optionsSound`): panning hoor je alleen in stereo; maak een
  L/R-splitsing ook in mono zinvol (ander timbre/kleine vertraging). Lagen op PSG kosten geen DS-kanalen: daarmee bleef
  de stemverdeler binnen 10 (melodie/bas/drums 0% weg). Tempo-check op de mp3 (fold-scherpte): 175,96 scherp, 150-155 vlak.
