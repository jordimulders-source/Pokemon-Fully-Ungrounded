# Poedelmot silhouet ronde 3 (6 nov): ronde 2 + vijf reparaties

Basis is ronde 2 (`../ronde2/`), met dezelfde bron en dezelfde massa. Alleen de vijf benoemde reparaties zijn gedaan.
Scripts zijn kopieën uit ronde 2; `silhouet.py` → `ronde3.txt`, `delen.txt`, png's; `controle.py` → `controle.txt`;
`keurvel.py` → `vel.png` (+ `vel.png.keuring.md`).

## Reparaties
1. **Oren = vilt** (Jordi: "dit mag als inspiratie voor hoofd, gezicht en oren"): gladde, gesloten bladrand, breedst op ±40 %,
   taps naar een spitse punt, opzij en licht omhoog (±25°). Geen tanden; de strepen komen in de kleur. De voet van het oor
   ligt nu op de kopomtrek, zodat het smalle begin te zien is en het oor los van de kop leest.
2. **Hoorntje weg:** de punt van de verre voorvleugel (en een losse pixel van de verre achtervleugel daarboven) is weggehaald.
   De verre voorvleugel eindigt nu achter het verre oor.
3. **Lijf niet één blok met de vleugels:** er zijn twee inkepingen in de omtrek, buiten de wolbol van het lijf (ovaal, blijft heel):
   - waar lijf en nabije achtervleugel elkaar raken (rechtsonder, ±4 px diep);
   - tussen nabije voor- en achtervleugel aan de buitenrand (±7 px diep, zoals bij Butterfree).
4. **Pompons rond:** één ovaal (1,08 : 1), zonder zijlobben, dus zonder platte onderkant.
5. **Verre voorpoot:** hoger (pompon tot y55 tegen y61 in ronde 2) en meer naar achter, onder de buik. De pompon zit half
   verborgen achter de nabije voorpoot en het lijf. Geen schuine stut meer.
- Extra, als gevolg: `glad()` telt nu ook gaten (lege pixels die niet met de rand verbonden zijn), want het sloot de spleet
  tussen het nabije tweetal tot een gat. Die spleet blijft nu open.

## Meting (`controle.txt`)
1378 px, één component, 0 gaten, 0 korrels buiten de oorpunten. Er zijn 5 afwijkingen van de poppetjemassa buiten de
hand- en reparatiezones. Twee daarvan liggen meer dan 1 px van de grens: x47–48 y33 (100 % dekking), weggehaald door `glad()`
direct naast de vleugelinkeping, als afronding van die inkeping.

## Zwakke punten (eerlijk)
1. **Links is bijna geen vleugel meer.** Het hoorntje weghalen nam de enige zichtbare verre voorvleugel mee; van de verre kant
   blijft alleen een bult (de verre achtervleugel) naast de kop. Op 1× leest het daardoor als een dier met één vleugel
   (rechts), terwijl Butterfree en Venomoth links en rechts vleugels tonen. Mogelijke oplossing (voorstel, niet gedaan):
   de verre voorvleugel als kleine vleugel links naast het oor laten uitsteken in plaats van ertussen.
2. **Kop en nabije voorvleugel raken elkaar bovenaan nog zonder inkeping.** Het gat tussen kop, oor en vleugel is
   ingesloten, dus het lijf leest vooral onderaan los.
3. De **verre poten** zijn nu grotendeels verborgen: van de zes poten zie je in de omtrek vier pompons (nabij voor, nabij tweetal, ver voor half).
4. De oorpunt is 1 px (gewenst, spits), maar dat is de enige korrel die blijft.
