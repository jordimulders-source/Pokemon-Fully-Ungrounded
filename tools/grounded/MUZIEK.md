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
