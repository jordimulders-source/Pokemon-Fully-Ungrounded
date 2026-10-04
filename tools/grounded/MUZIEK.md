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
5. `python3 tools/grounded/maptools/audiocheck.py <uit.wav>`: geen pieken/clipping na de eerste 0,1 s, geen
   onverwachte constante tonen, RMS rond 700–2700 (Zarude ≈ 2700 = bovengrens).
6. mp3 maken (`ffmpeg -ss 0.1 ... -af afade=...`), `volumedetect`: max_volume onder −1 dB.
7. Pas dan naar Jordi (regel van Jordi: geen zoemtonen of andere dingen die gehoorschade kunnen geven).

## De engine (m4a)
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
