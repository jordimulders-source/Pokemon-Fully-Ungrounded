# Sauna-yeti – sprite ronde 2 (maker)

`sauna_yeti_r2.png` = r1 met 37 benoemde pixels (`bouw.py` print ze allemaal); verder diff 0. `vel.png` = r2 | r1 | model.

| code | px | wat |
|---|---|---|
| G1 | 4 | wenkbrauwlijn rij 22 (model y190–202) direct boven de oogleden: lijntint → s op (25,22)(26,22)(29,22)(31,22). Zelfde plek, lichtere tint; zo lezen oogleden + pupillen los van de wenkbrauw (het model tekent de vachtlijnen ook lichter dan de leden). |
| G2 | 4 | wangvacht naast het gezicht op de oogrij: (24,23)(25,23)(37,23)(38,23) lijntint → s (liep anders door als één lange ooglijn). |
| Z1 | 7 | losse zwarte binnenlijnpixels zonder zwarte buur (lijnoverdracht) → lijntint: (22,33)(49,39)(10,44)(48,46)(36,52)(38,53)(33,54). |
| S1 | 22 | steenrand gloeit waar het model ≥ 40 % gloed heeft (r1 50 %; nu dezelfde drempel als de scheuren). De buiksteentjes lazen op 1× als zwarte vlekjes met alleen een oranje onderrand; het model heeft rondom een gloeirand behalve linksboven. Gloed nu 78/256 steenpixels = 30 % (model 28 %). |

Gezicht (beschermd, ronde 1): ogen, neus en mond ongewijzigd.

## Controle
bbox x1–62, y12–60 (62×49), 16 kleuren incl. transparant, geen lichte kleur op de buitenrand, geen losse zwarte pixels buiten gezicht en stenen.

## Zelf nog zwak
- Vacht rond kop/schouders blijft wat druk (de vele modelstrengen op hun plek); niet gladgestreken (regel "rustiger = pixelblur").
- Linkerschoudersteen: 3 gloeiende naden binnenin (gemeten), het model toont een fijner brokkenpatroon dat op 10×9 px niet meer past.
