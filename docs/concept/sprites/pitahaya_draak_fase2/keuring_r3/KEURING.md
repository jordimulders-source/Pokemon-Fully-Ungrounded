# Keuring r3 – pitahaya-draak fase 2, `sprite_r3/pitahaya2_r3.png` (+ variant `_lipB`)

Keurder: dezelfde als r2. Hulpmiddelen hier: `zij.py`/`zijB.py` (bek naast het model met raster: `bek_r3.png`, `bek_r3_detail.png`, `bek_lipB.png`), `meet_r3.py`/`meet_lipB.py` (tinten, clusters, dambord), `r2_r3_lipB_2x.png` (r2 | r3 | lipB op 2×, witte achtergrond).
Diff r2 → r3: 29 px, allemaal in de opdrachtzones. Palet, maat en silhouet zijn gelijk. Zwart binnen de figuur 5,4 %.

## Oordeel: PASS (hoofdversie)

### 1. Reparaties uit r2
- **1 Mondhoek:** goed. De lichtroze modelstreep loopt nu als één strook van (19,44) naar (15,50), rechts p en r waar het model donker is. Er is geen p/P om en om meer. Trouw aan het model (bek_r3_detail).
  - (15,49) staat nog op **W**. De NOTITIES zeggen W → P, maar die wissel staat niet in de diff. Hertelling: het modelblok (15,49) is 6/9 licht en 0/9 roze, dus **W is juist** (mijn r2-schatting "roze" was fout). Laten staan; alleen de NOTITIES kloppen niet.
- **2 Linker lipband (7,50)–(7,53) → r:** goed. Het wit raakt de buitenlijn niet meer en het volgt het model.
- **4 Dambord:** goed. De voorvoet (11,58) en (13,57) heeft geen g/G om en om meer, en ook (9,36) en (39,46) zijn opgelost.
- **5 Onderste lipband (9,53) en (10,53) → p:** goed. (12,54) is terecht K gebleven, want anders gaat de buitenlijn open.

### 2. Nieuwe fouten
Geen. De nieuwe kleine clusters zijn r (20,47)–(20,48), r (15,52)–(16,52) en de losse r (11,37), die overbleef van (10,37). Het zijn donkere randtonen langs de modelvorm, geen lichte vlekjes. Er zijn geen nieuwe lichte losse pixels.

### 3. Per onderdeel tegen r2
- **Bek:** beter. Lipband rondom gesloten, mondhoek rustig, pitjes en tanden ongewijzigd. Leest op 1× en 2× als een open doorgesneden dragonfruit.
- **Kop en oog:** gelijk, op (10,37) na (r → p op de snuitbult, uit het model).
- **Lijf:** gelijk, op (39,46) na.
- **Voorvoet:** rustiger.
- **Rug, staart en achterpoten:** 0 diff.

### Resterende dambordjes (genoemd door de maker): normaal, geen fout
- **K/g (26,51), (27,53), (50,53), (51,55):** de zwarte buitenlijn of poot-over-lijf-lijn loopt diagonaal langs een donkergroene vulling. Een diagonale lijn van 1 px geeft altijd dit 2×2-patroon; in Gen 3 is dat normaal.
- **(30,36) p/h en (37,42) G/r:** groene schubnerf uit het model, diagonaal door het roze. Dit is ook een 1-px-lijn en geen ruis tussen twee vultinten van één groep.

## lipB tegen de hoofdversie
- **Trouw aan het model:** lipB is iets trouwer, want de verre lip loopt in het model tot ongeveer (12,45).
- **Leesbaarheid:** op 12× vormen (11,46) en (12,45) een korte schuine streep. Op 1× en 2× wordt (12,45) een los roze stipje in het grijs, en het nieuwe w/r-patroon op (11,45) is een tint-op-tint diagonaal binnen het vruchtvlees.
- **Techniek:** beide versies voldoen aan de Gen 3-eisen. Ik kies hier niet tussen de twee.

## Mondvorm van binnen zichtbaar (Jordi: "zorg er wel voor dat de mondvorm van binnen zichtbaar blijft")
**Model:** de binnenkant heeft drie delen.
1. Bovenin het grijze gehemelte achter de tanden.
2. Daaronder de verre lip: een dunne roze strook die diagonaal loopt van linksonder (8,48) naar het midden (12,45).
3. Daaronder het vlees van de onderkaak. Dat is bovenaan grijs en loopt onderaan over in wit, en wordt links, onder en rechts omsloten door een roze lipband (2 px). Pitjes zitten op het gehemelte en op het vlees.

**Hoofdversie:**
- Het gehemelte is als grijs vlak zichtbaar.
- De onderkaak is als wit ovaal binnen een gesloten roze lipband zichtbaar: links (7,50)–(7,53), onder rij 53–54, rechts de mondhoekstreep.
- De verre lip zie je alleen links, als een korte verticale roze strook op x9–10, y44–47. Hij loopt niet diagonaal door naar het midden.
- Daardoor wordt de grens tussen gehemelte en onderkaak alleen bepaald door de tintstap grijs → wit rond rij 47/48. Het gehemelte en het bovenste grijze deel van de onderkaak lopen in één grijs vlak in elkaar over.
- Op 1× en 2× zie je een grijs vlak boven en een wit vlak onder, met pitjes, binnen een roze rand.

**lipB:**
- Gehemelte en onderkaak zijn hetzelfde als in de hoofdversie.
- De verre lip loopt hier wel diagonaal door van (10,46) via (11,46) naar (12,45), zoals in het model. Het grijs boven en links van die strook leest als gehemelte, het deel eronder als onderkaak.
- Rechts van x12 (x13–16, y45–47) is er geen strook meer en loopt het grijs nog door. Dat staat ook zo in het model: daar is de strook dun en vervaagt hij.
- Op 12× is de diagonaal te zien. Op 1× en 2× is het een klein roze puntje in het grijs; de scheiding is daar zwak maar wel aanwezig.

## Reparaties
Geen verplichte. Kleine administratieve punten in `sprite_r3/NOTITIES.md`:
- (15,49) is niet gewijzigd en dat is juist.
- (39,46) ging van d naar r, zoals vermeld.
