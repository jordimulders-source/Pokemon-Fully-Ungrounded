# Muziek

## Besloten
- De soundtrack wordt gebaseerd op diverse **Zuid-Amerikaanse en Latijns-Amerikaanse muziekstijlen** (Jordi, 22 okt). Welke stijlen: zie hieronder (wordt aangevuld).
- **Grotendeels een nieuwe OST** (Jordi, 22 okt): alle Ungrounded-muziek (remixes, gym-/legendary-/gebiedsthema's, rips) is eruit; alleen de vanilla Emerald-nummers en Keccles' thema's bleven. Vanilla-nummers zijn plaatshouders; een groot deel (of alles) wordt opnieuw gemaakt.
- **Geen nummers namaken** (Jordi, 22 okt): geen covers of rips van bestaande nummers zoals in Ungrounded; alles origineel, in de stijlen hieronder. Dat scheelt ook ruimte: een gedeelde set eigen instrumenten (charango, quena/panfluit, cajón, bombo, cuatro, berimbau, conga's, salsa-blazers, reggaeton-drums) in plaats van samples per nummer.

## Stijlen
- **Kijk goed naar wat de GBA-klank kan namaken** (Jordi): niet elke stijl komt er even mooi uit. Ervaring uit Ungrounded: noten met (eigen) samples werken, gesampelde opnames blijven dof; max. 16 sporen per nummer; eigen samples max. 11 kHz (DPCM); korte stoten van een aangehouden sample klinken als accordeon.

- **Ook iconische artiesten en wat er echt geluisterd wordt** (Jordi): niet alleen 'traditionele' stijlen. Bijv. **Soda Stereo** (Argentijnse rock, hoor je overal in Latijns-Amerika), en stijlen die niet uit Zuid-Amerika komen maar er wel fervent gedraaid worden, zoals **bachata** en **salsa**.

## Artiesten en invloeden (inspiratie, nog aan te vullen)
- **Rock en pop:** Soda Stereo / Gustavo Cerati (Argentinië), Charly García, Los Prisioneros (Chili), Café Tacvba (Mexico, overal populair), Caifanes.
- **Tango:** Carlos Gardel, Astor Piazzolla (nuevo tango), Gotan Project (elektronische tango).
- **Andes:** Los Kjarkas (Bolivia; *Llorando se fue*), Inti-Illimani, Savia Andina.
- **Cumbia en chicha:** Los Mirlos, Juaneco y su Combo (Amazone-chicha), Los Destellos, Bomba Estéreo (moderne Colombiaanse cumbia).
- **Brazilië:** Antônio Carlos Jobim, Gilberto Gil, Jorge Ben Jor, Os Mutantes (tropicália).
- **Salsa en bachata (niet Zuid-Amerikaans, wel overal gedraaid):** Héctor Lavoe, Joe Arroyo (Colombia), Grupo Niche, Juan Luis Guerra, Romeo Santos/Aventura.
- **Reggaeton** (Jordi): Daddy Yankee, J Balvin en Karol G (Colombia), Bad Bunny. Idee: **een van de rivaliserende gangs krijgt reggaeton-thema's** (Jordi).
- **Nueva canción:** Mercedes Sosa, Víctor Jara, Violeta Parra (past bij de serieuze, menselijke toon).

## Haalbaarheid per stijl (inschatting Claude, 22 okt; nog te testen)
| Stijl | Kerninstrumenten | GBA-haalbaarheid | Waarom |
|---|---|---|---|
| Huayno / Andesmuziek | zampoña (panfluit), quena, charango, bombo | **goed** | fluiten zijn ideaal voor GBA-samples; charango als korte tokkels (eigen sample) |
| Diablada / morenada / caporales | fanfare (koper), grote trom, matraca | **goed** | koper en zware trommels klinken sterk op de GBA (vgl. gevechtsmuziek van Emerald) |
| Cumbia | accordeon, güiro, bas, conga | **goed** | accordeon is juist wat korte stoten al opleveren; güiro als kort ruissample |
| Forró / carimbó | accordeon, zabumba, triangel | **goed** | weinig instrumenten, duidelijke ritmes |
| Afro-Peruaans (landó, festejo) | cajón, gitaar, quijada | **goed** | cajón is één goed sample; spaarzame bezetting |
| Tango / milonga | bandoneon, strijkers, piano | **redelijk** | bandoneon ≈ accordeon-sample; staccato strijkers werken, legato-strijkers worden dun |
| Chicha (Amazone-cumbia) | surfgitaar, orgel, timbales | **redelijk** | gitaar met tremolo moet een eigen sample zijn; orgel gaat goed |
| Salsa | koperblazers, piano-montuno, congas, timbales | **goed (bewezen)** | het salsa-thema van Keccles in Ungrounded is erg goed gelukt (Jordi): `tools/grounded/keccles_theme.py`/`keccles_samples.py` als voorbeeld |
| Samba / batucada | surdo, tamborim, caixa, cuíca, agogô | **lastig, maar moet erin** (Jordi: hoort bij het Brazilië-deel) | zie aanpak hieronder |
| Bossa nova | nylongitaar-akkoorden, zachte zang | **lastig** | ingetogen akkoorden en stem zijn waar de GBA het zwakst is; als melodie op fluit kan het wel |
| Vallenato / kaseko | accordeon, caja/snaredrum, guacharaca | **goed** | vergelijkbaar met cumbia |
| Reggaeton | dembow-ritme (kick, snare, hi-hat), synthbas, synth-stabs | **goed** | vooral ritme en een vette bas: de GBA-drums en een eigen 808-achtige bas doen het werk; zang wordt een synthlead |
| Bachata | twee gitaren (requinto-arpeggio's), bongo, güira | **goed** | heldere tokkelende gitaarlijn + ritme; eigen gitaarsample |
| Latin rock (Soda Stereo-achtig) | elektrische gitaar met chorus/delay, bas, synths, drums | **redelijk** | GBA-rock werkt (vgl. bestaande gevechtsmuziek); de chorusgitaar vraagt een eigen sample |
| Nueva canción / folk | akoestische gitaar, stem, charango | **redelijk** | zonder stem moet een melodie-instrument de zang overnemen (quena, fluit) |

## Gedeelde instrumentenset (23 okt, eerste versie)
- **Generator:** `tools/grounded/fu_samples.py` → `sound/direct_sound_samples/fu/` (39 samples), voicegroup `fu`
  (`sound/voicegroups/fu.inc`, `keysplits/fu.inc`, `drumsets/fu.inc`). Elk nieuw nummer gebruikt `-G_fu`; nieuwe
  instrumenten komen in deze ene set, niet per nummer.
- **Programma's:** 21 accordeon (musette), 24 nylongitaar, 25 charango (tokkel, dubbele snaren), 26 charango-rasgueo
  (kwintakkoord, ook cavaquinho), 33 bas, 38 808, 56 trompet / 58 tuba (vanilla), 57 trombone, 73 quena, 75 zampoña,
  78 cuíca, 81 supersaw, 80/82/83 PSG-blokgolven, 121–123 PSG-ruis (güiro/hihat, shaker, wind/riser).
  Drumkit 36–62: dembow-kick/-snare/clap, bombo + aro, cajón, bongó, conga's, güiro, shaker, claves, cowbell, crash,
  caixa, hihats, surdo laag/hoog, tamborim, agogô, apito.
- **Techniek:** melodisch 11 kHz + DPCM, slagwerk 16 kHz onverpakt; grondtonen gemeten (±4 cent); 808 en supersaw
  gesynthetiseerd met exacte loops (geheel aantal perioden). Kosten: ±186 KB samples + ±17 KB voor zes nummers.
- **Schetsen (611–616, previews in `docs/concept/muziek/previews/`):** instrumentendemo, altiplano-route (huayno),
  wild gevecht (Andes + fanfare), La Paz (caporales/saya), reggaeton-bende, samba. Wachten op Jordi's oordeel.
- **Wat (technisch) werkte:** één kwintakkoord-sample voor de rasgueo (1 kanaal per slag, mineur én majeur); hoquetus
  met twee zampoña-sporen links/rechts; PSG voor shaker/ganzá/hihat/wind spaart kanalen.
- **Lastig:** samba is vol (surdo's, caixa, tamborim, agogô, cuíca, cavaquinho, melodie): agogô/cuíca vallen in de
  volste maten soms weg; drumnoten kort houden (¾ 16e), anders bezet elke slag twee kanalen. Een 808 domineert snel
  (85% energie < 150 Hz): bas zachter, master -V084.

## Samba op de GBA (aanpak, nog te testen)
- **Uitdunnen tot de kern:** surdo (één sample, twee toonhoogtes voor de wisselende slagen), caixa (snare in 16e), tamborim (hoog patroon), agogô (twee bellen), cuíca (één kort sample met pitch bend), cavaquinho (korte akkoordslagen) en één melodie.
- **Kanalen sparen:** agogô en tamborim op de PSG-kanalen (square/noise), zodat de DirectSound-kanalen vrij blijven voor surdo, caixa, cavaquinho en melodie.
- **Eerst een korte proef** (±20 s) en die laten horen, vóór er een volledig nummer komt.

## Feedback Jordi op de eerste schetsen (23 okt)
Algemeen: "prima testronde, de muziek gaat wel goedkomen". **Muziek staat even op pauze** (Jordi).
- **Altiplano (612):** de eerste seconden klinken wat vals, maar zodra het deuntje start "echt vet", al 80–90% goed; mag nog net wat meer Pokémon klinken.
- **Wild gevecht (613):** klinkt Pokémon-stijl; het refrein is nog wat kaal. Volgende keer: een agent laten keuren en vergelijken met de Emerald-gevechtsmuziek.
- **La Paz (614):** niet genoeg La Paz-stijl; de fluitjes klinken vrij vals.
- **Bende (615):** wel ok, maar het typische reggaeton-dembow ontbreekt, en een fluitje hoort daar niet de hoofdtoon te hebben.
- **Samba (616):** klinkt tof, maar is geen samba. De cuíca is geinig opgelost.
- **Algemeen:** niet elk nummer moet een fluitje de melodie laten spelen. Let op valse fluiten (quena/zampoña-samples of stemming nakijken).
