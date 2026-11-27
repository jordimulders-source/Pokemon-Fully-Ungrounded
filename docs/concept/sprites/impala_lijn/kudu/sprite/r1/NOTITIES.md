# Kudu sprite ronde 1 (maker)
Model: `referenties/model_r3b.png` (Gemini r3b). r3, r3b en r3c zijn buiten de manen pixel-gelijk (lijf-diff ±1%), dus de lokken zijn als asset uit te knippen.
Keelfranje: blijft in alle varianten zoals in r3b (Jordi: "nee hoor ik zie daar echt ruimte tussen"); geen variant zonder.

## Werkwijze (scripts in `sprite/`)
- `haarmasker.py`: manenmasker = pixels van r3b (en r3c) die afwijken van r3, binnen het manengebied. Dat is precies het nekhaar (halslokken + kamlokken over de schoft); de keelfranje is in r3 en r3b gelijk en valt er dus buiten. Viz: `haar_r3b_viz.png`, `haar_r3c_viz.png`.
- `reduce.py`: kale reductie per spritecel (16 modelpx, model is pseudo-pixelart met ±5,15 px per natieve pixel): voorgrond = alles behalve rand-wit, alpha >= 0,45, cel met >= 25% zwarte modellijn = lijn (de modellijn is 1 natieve px = ±31% van een cel; met 50% zoals bij de impala verdween bijna alle lijn), anders vlakgemiddelde zonder lijn -> dichtstbijzijnde van 15 modelkleuren (k-means op r3b). Technisch daarna alleen: buitenlijn dicht.
- `r1.py`: varianten op modelniveau (lokken verschuiven/verlengen, alleen binnen het silhouet van het model), daarna dezelfde reductie. `vel.py`: vel.

## Grootte
Figuur = volle hoogte 64 px (rij 0-63), 51 px breed (x 6-56). Hoorns alleen (boven de oren): rij 0-16 = 26% van de hoogte; hoorns tot hun voet ±rij 19 (30%).

## Varianten (pixels t.o.v. de kale reductie; buiten de manenzone overal 0)
- **kaal**: kale reductie r3b + buitenlijn dicht (174 px buitenlijn).
- **A**: hele r3b-manenasset +70 px rechts, +30 omlaag over het origineel gelegd: de manen worden breder en vallen over de nabije schouder. 120 px anders (rij 27-44, kolom 19-38).
- **B**: r3b-manen 1,3x verlengd (modelrijen herhaald vanaf de bovenkant achter de oren) en +40 rechts: lokken hangen lager over de schouder. 146 px anders (rij 24-47, kolom 17-36).
- **C**: de grotere lokken van r3c (alleen het halsdeel, x >= 380, dus zonder de r3c-keelfranje) +90 rechts, +20 omlaag op r3b: losse lokken liggen zichtbaar op de schouder. 90 px anders (rij 26-48, kolom 23-39).
- **groot_kaal / groot_A**: reductie op 72 rijen, daarna 8 rijen uit het hoornstuk geschrapt (rij 2,4,7,8,9,11,13,15 van 72): kop en lijf ±12% groter (58 px breed). NIET goed: de hoornspiraal wordt een zigzag; de hoornvorm is "het belangrijkste". Alleen ter vergelijking van de maat.

## Eigen zwakke punten
- Witte flankstrepen en de witte V vallen grotendeels weg (1 natieve px dun): moeten in een volgende ronde terug uit het model.
- Hoorns trappig, plekken 1 px dun; nog niet gerepareerd (impala `hoornskelet.py` kan helpen).
- Manen lezen in alle varianten nog als een vlek van strengen met losse zwarte lijnpixels (ruis); nog niet opgeschoond (<=3 tinten per groep, binnenlijnen in eigen tint).
- Variant A heeft een dubbele kamrand (origineel + verschoven kopie) op de schoft.
- Palet = modelkleuren (15 + transparant), nog niet naar Gen 3 / goud-staal-lijnbesluit gemapt; geen selout.
