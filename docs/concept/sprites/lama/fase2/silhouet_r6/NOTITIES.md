# Silhouet lama fase 2, ronde 6 – notities

**Opdracht:** het hele silhouet overtrekken van het goedgekeurde poppetje (`fase2_r4('F_pas', head_yaw=55)`, camera `bron.py`) op de
50%-dekkingsgrens, max. 1 px afwijking, alleen korrels weghalen. Niets ontworpen of verbeterd.

## Meting
- Model bij 50%: 1163 px (de opdracht noemde ±1160). Ronde 6: 1163 px.
- **Alleen ronde 6: 7 px, alleen model: 7 px; 0 afwijkingen > 1 px** van de 50%-grens (`diff_model.txt`, script `diff_model.py`).
- `korrel.py`: 0 uitsteeksel-px, 0 inkeping-px, 0 tanden. Eén component, 0 losse px.
- **Gaten: 24 px**, en dat is het model: de ruimte tussen de twee voorpoten (x21–23, y49–58) is boven dicht door de buik en onder
  dicht doordat de rode handschoenen elkaar in het model raken (y59–60, dekking 60–100%). Openen kan alleen door de hoeven uit elkaar
  te halen (o.a. x21–22 y60 met 100% dekking weg); dat is precies wat niet mag. **Niet opgelost, alleen gemeld.**

## Afwijkingen per onderdeel (alle 14, elk max. 1 px)
- **Kop (y0–21):** letterlijk ronde 5f. Afwijkingen t.o.v. 50%: −x18 y1 (85%), +x21 y2 (14%), +x22 y6 (47%), −x21 y9 (50%). Alle vier binnen 1 px.
- **Hals (y22–26):** 0 afwijkingen.
- **Lijf + aguayo (y25–43):** +x46 y25 (49%) en +x39 y26 (44%) vullen 1-px inkepingen in de bovenrand; −x38–39 y43 (56/53%):
  los stukje onder de buik met een 1-px inkeping ernaast.
- **Staart:** de pluim (x47–50, y24–26) precies zoals het model; 0 afwijkingen.
- **Halsband, aguayo, handschoenen:** zoals het model (geen eigen afwijkingen buiten de hoeven hieronder).
- **Poten:** voorpoten x17–22 en x23–29, opening y49–58 zoals het model; +x23 y48 (39%): 1-px inkeping, de opening begint
  nu op y49; −x22 y58 (72%): 1-px inkeping onderaan de opening; −x13 y61 (76%): uitsteeksel aan de nabije hoef.
  Achterpoten: in het model valt de verre achterpoot vrijwel helemaal achter de nabije (één kolom x42–49); zo gelaten.
  −x43 y60 (57%) uitsteeksel; +x44 en +x46 y61 (40/46%) zodat de hoef geen 1-px punt is.

## Wat op 1× niet leest (eerlijk; niet opgelost)
- **Achteraan lezen maar drie poten:** de verre achterpoot is in het model verborgen achter de nabije; op 1× is er één achterpoot.
- **De voorpoten lopen onderaan samen** (handschoenen raken elkaar); op 1× is het een omgekeerde V/ingesloten gat, geen twee losse poten.
- **De staartpluim** is maar een bultje van 4×3 px boven de rug; op 1× leest hij als een hoekje van de rug, niet als staart.
- Het aguayo-dekje en de halsband zijn in het silhouet niet te onderscheiden (liggen binnen de lijfomtrek); dat komt pas met kleur.
- Dit zijn eigenschappen van het model in deze pose/camera. Wil Jordi ze anders, dan moet het poppetje veranderen, niet het silhouet.

## Lessen
- Zonder scipy: componenten/gaten met een eigen floodfill (`diff_model.py`).
- De dekkingskaart van het hele model op 50% had maar 8 korrels (3 uitsteeksels, 5 inkepingen); overtrekken is vrijwel 1-op-1, eigen vormeisen zijn niet nodig.
