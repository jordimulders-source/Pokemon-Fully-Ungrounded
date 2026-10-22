# Muziek

## Besloten
- De soundtrack wordt gebaseerd op diverse **Zuid-Amerikaanse en Latijns-Amerikaanse muziekstijlen** (Jordi, 22 okt). Welke stijlen: zie hieronder (wordt aangevuld).

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
| Samba / batucada | surdo, tamborim, caixa, cuíca, agogô | **lastig** | veel gelijktijdige percussie kost kanalen; cuíca is moeilijk na te maken; een uitgedunde versie kan |
| Bossa nova | nylongitaar-akkoorden, zachte zang | **lastig** | ingetogen akkoorden en stem zijn waar de GBA het zwakst is; als melodie op fluit kan het wel |
| Vallenato / kaseko | accordeon, caja/snaredrum, guacharaca | **goed** | vergelijkbaar met cumbia |
| Bachata | twee gitaren (requinto-arpeggio's), bongo, güira | **goed** | heldere tokkelende gitaarlijn + ritme; eigen gitaarsample |
| Latin rock (Soda Stereo-achtig) | elektrische gitaar met chorus/delay, bas, synths, drums | **redelijk** | GBA-rock werkt (vgl. bestaande gevechtsmuziek); de chorusgitaar vraagt een eigen sample |
| Nueva canción / folk | akoestische gitaar, stem, charango | **redelijk** | zonder stem moet een melodie-instrument de zang overnemen (quena, fluit) |
