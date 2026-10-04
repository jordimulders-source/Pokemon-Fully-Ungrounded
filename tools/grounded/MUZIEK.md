# Muziek componeren en arrangeren voor Project Grounded

Dit is het geheugen voor muziekwerk. **Lees dit vóór elk nieuw nummer, en vul het aan na elke feedbackronde van Jordi**
(wat fout ging, wat hij mooi vond, welke controle het had kunnen vangen). Een nieuwe fout die automatisch te
herkennen is, komt ook als controle in `music_lint.py`.

## Werkwijze (verplicht, in deze volgorde)
1. Componeren/arrangeren met een script (`zarude_theme.py`, `wally_theme.py`), nooit met de hand in de MIDI.
2. `python3 tools/grounded/music_lint.py sound/songs/midi/<nummer>.mid`: moet **OK** zijn.
3. Test-ROM: `python3 tools/grounded/maptools/testrom.py <map> "playbgm MUS_X, FALSE"`.
4. Opnemen: `PYTHONPATH=tools/grounded/maptools python3 tools/grounded/maptools/recaudio.py <rom> <intro.bin> <k> <sec> <uit.wav>`.
5. `python3 tools/grounded/maptools/audiocheck.py <uit.wav>`: geen pieken/clipping na de eerste 0,1 s, geen
   onverwachte constante tonen, RMS rond 700–2700 (Zarude ≈ 2700 = bovengrens).
6. mp3 maken (`ffmpeg -ss 0.1 ... -af afade=...`), `volumedetect`: max_volume onder −1 dB.
7. Pas dan naar Jordi (regel van Jordi: geen zoemtonen of andere dingen die gehoorschade kunnen geven).

## De engine (m4a)
- **8 DirectSound-kanalen** (`src/m4a.c`, was 5 in vanilla). Meer noten tegelijk = kanaalroof: een nieuwe noot
  kapt een andere af. Dat hoort Jordi als **snips** / "overhaast eindigende maat". Ook uitklinkende noten (release)
  en lange drumnoten houden een kanaal bezet. PSG-sporen (vierkant/ruis/golf) tellen niet mee.
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
- mGBA (python-binding) geeft af en toe een burst van ~10 samples (0 / 15136 / 32520 om en om). In de game zit
  dat niet. `recaudio.py` werkt ze weg en meldt het aantal. Jordi hoorde ze als snips op 3 s en 11 s.
- De eerste 0,03 s bevat een klik van het starten: knip 0,1 s weg.

## Smaak van Jordi
- **Catchy > veilig.** Een piepje oplossen door hele sporen weg te halen verloor in Zarude v2 de catchiness;
  zoek de ene foute noot (v10 = intro van v9 + loop van v1).
- Legendary-intro's: opbouw in sync met de gevechtstransitie (10–20 s), percussie die episch opbouwt, blazers pas
  na de transitie.
- Wally groeit mee: dezelfde iconische melodie, steeds zwaardere instrumenten. 1 = fluitje + akoestisch, traag,
  "wimpy"; 5 = heavy metal ("balls to the wall"). De "piano" in de ORAS-MIDI is eigenlijk een elektrische gitaar.
- Regigigas: het bestaande Regi-thema bombastisch remixen, met **Slow Start**: traag beginnen en versnellen naar
  het normale tempo, halverwege nog één keer afzwakken en vertragen ("bijkomen") en dan vol gas.
- Jordi geeft feedback met tijdstempels; gebruik die om noten op te zoeken (tick = s × 1e6 / tempo × tpb).

## Log van feedbackrondes
- Zarude v1–v10: losse piepjes = PSG-drumnoot 44 in een tomroffel; brass pas na de transitie; groove niet te kaal.
- Wally v0.9.20: opname kapot (bufferoverloop). v0.9.24: snips door kanaalroof (tot 17 noten tegelijk bij 5
  kanalen) + dubbele noten in de bron; engine naar 8 kanalen, stemverdeler, `music_lint.py`.
- Open: `mus_grounded_vs_zarude.mid` geeft nog meldingen in de lint (dubbele noten in de tomroffel, soms 9–10
  noten tegelijk). Jordi keurde hem goed; repareren bij de volgende Zarude-ronde.
