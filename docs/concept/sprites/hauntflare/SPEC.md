# Hauntflare (SPEC)
Middenfase van de convergente Gastly-lijn: Dustly → Hauntflare → Gengas. Cosmic/Poison (Jordi, 15 nov: "cosmic/poison is goed"). Eindvorm Gengas is af (`../gengas/`).

## Jordi letterlijk
- 13 nov: "Ik wil Gastly een buitenaardse gaswolk maken die dan logisch evolueert van een andere vorm haunter en gengar gebaseerd op verschijnselen die in de ruimte plaatsvinden. Het moet echt convergent zijn he."
- 15 nov: naam "Hauntflare"; namen "zijn definitief".
- 15 nov: "hauntflare tijd, maak een prompt voor gemini"

## Basis
- Verschijnsel: protoster met Herbig-Haro-jets (voorstel Claude 13 nov in `IDEEEN.md`, lijn in `POKEMON.md`: "protoster met jets (de losse knopen = Haunters handen)").

## Prompt
- r1: `gemini/PROMPT_r1.md`, bijlage `referenties/haunter_gen3_8x.png`.
- r2: `gemini/PROMPT_r2.md` (nieuw gesprek, alleen Haunter als bijlage).
- r3: `gemini/PROMPT_r3.md` (basis r2_b, bol en losse ring zoals r1).
- r4 (laatste): `gemini/PROMPT_r4.md`; daarna knip- en plakwerk (Jordi).
- 15 nov, Gemini r1 (`gemini/r1_a.png`): "klopt dit bij je idee?" Beoordeling Claude: kop-jet, staart, losse handen, gezicht en kleur kloppen; afwijkend: stofschijf werd een dunne Saturnusring om alles heen, kijkt naar rechts, beide jets waaieren naar links (komeet/vuurbal i.p.v. twee tegengestelde jets), bal glanst als plastic.
- 15 nov over r1: "het gezicht is juist gengar, schrijf een nieuwe prompt, ik heb alleen de gengas sprite erbij gedaan, nu doe ik haunter ook wel". Prompt r2: `gemini/PROMPT_r2.md`.
- 15 nov, Gemini r2 (`gemini/r2_a.png`), door Jordi gestuurd zonder commentaar. Beoordeling Claude: Haunter-gezicht, kijkt naar links, dikke schijf over de onderhelft, losse handen nabij/ver kloppen; afwijkend: grijze wervellijnen om de schijf (effect), beide jets wijzen weer naar achteren (rechts), bol bleek en leest niet als gloeiend.
- 15 nov over r2: "ja dat effect om de ring lag aan mij." Over r2_b (`gemini/r2_b.png`): "Ik gaf na deze feedback dat ik de bol meer een gas look wilde. Laten we nog 1 keer proberen te prompten, we zitten wel goed in de richting. Ik vond de bol bij de 1e en de ring die niet direct eraan vast zat toffer, maar deze lijkt meer op haunter". Prompt r3: `gemini/PROMPT_r3.md`.
- 15 nov, Gemini r3 (`gemini/r3_a/b/c.png`): "Dit zijn drie ontwerpen. Elk ontwerp heeft wel dingen die tof zijn, al is er nog geen enkele echt perfect. Zet eens alle ontwerpen naast elkaar tot nu toe" → `gemini/overzicht_r1-r3.png`.
- 15 nov: "doe nog 1 laatste prompt en daarna kunnen we met knip en plak werk de topversie maken". Prompt r4: `gemini/PROMPT_r4.md`.
- 15 nov, Gemini r4 (`gemini/r4_a/b/c.png`): "Ok, zet alle 9 naast elkaar" → `gemini/overzicht_r1-r4.png`.
- 15 nov: "Ik heb de volgende suggestie, jij gaat nu met knip en plak werk het model maken, dat jij denkt dat het beste is." → Claude-model: r4_b + staart van r4_a (`model/model_claude_natief.png`, `model/combineer.py`).
- 15 nov: "Ik ga nu typen wat ik zie zitten en die maak je ernaast, jouw initiele model wordt niet beinvloed door mijn idee: ik wil: de mond en ogen van r3_b, de handen van r4_a, de pose en de kleur van de bal van r4_b, de ring van r4_c, de vlammen van r3_b, maar de vlam inkleuring van r4_A" · "dan zetten we de 2 naast elkaar en dat wordt het model" → `model/model_jordi_natief.png` (`model/jordi.py`). Vlammen r3_b = de kuif; de staart van r3_b zat half onder zijn ring en gaf een kapotte vorm, dus staart van r4_b (pose). Naast elkaar: `model/naast_elkaar.png`.

## Opdracht sprite (15 nov)
Jordi letterlijk: "gebruik de jouwe maar als model voor vorm, de vlammen zouden qua kleur nog iets meer vlam mogen zijn, en wat ik tof vond aan de handen is het kleurgebruik er iets meer vlammen van maakt ook. Houd er wel rekening mee dat ik de ogen en mond bij de claude versie teveel gastly vind en te weinig haunter, dat moeten we nog fixen. Gelukkig heeft haunter een hele simpele mond en ogen. Houd er ook rekening mee dat de rechterhand net buiten het frame valt. De ring is te effen, maar dat kunnen we nog fixen. Ga maar bouwen. Kom pas bij me terug als er een net gekeurde eindversie is, en verbied de maker om onderdelen opnieuw te tekenen"
- Vorm: `model/model_claude_natief.png` (99×99). Naar 64×64 door rijen/kolommen te schrappen (Gengas-methode), rechterhand als geheel naar binnen schuiven.
- Ogen en mond: Haunters Gen 3-pixels (`graphics/pokemon/haunter/anim_front.png`, frame 1), niet tekenen.
- Vlammen (kuif en staart; lezing Claude: beide zijn vlammen in dit model) meer vlamkleur; handen in het kleurgebruik van de r4_a-handen (`model/nat_r4_a.png`). Ring minder effen (tonen uit de r4_c-ring, `model/nat_r4_c.png`, op het bruine palet).
- Verboden: onderdelen opnieuw tekenen. Alleen bestaande pixels schrappen, verschuiven, overnemen en herkleuren.
- r1 (`sprite_r1/`): silhouet diff 0, vlammen/handen/ring goed; gezicht mislukt (Haunter-blok geschrapt → mond werd een kruis). r2: Haunter-gezicht 1-op-1 (schaal 1,0) op de bol boven de ring.
- 15 nov over r1: "zelfs het model klopt niet goed, ring is rechts afgekapt, witte lijn onderin, hand is niet goed, de bol is niet rond. Wat gaat hier zo extreem fout?" Oorzaak (Claude): bijna-witte Gemini-ruis bleef in het knipmodel staan (witte lijn); 99→64 schrappen haalt ±22% van de rijen/kolommen weg (Gengas ±13%) en sloopt bol, ringpunt en hand; de maker toetste tegen dat geschrapte model. Nieuwe basis: `basis/basis_64.png` (`basis/basis.py`: ruis weg, oppervlak-middeling, kwantiseren naar modelkleuren).
- 15 nov: "de ogen zijn ook niet haunters ogen terwijl die echt extreem makkelijk na te maken zijn qua lijnen werk en de mond kan je wel zelf tekenen, dat zijn gewoon tanden in dezelfde kleur als het hoofd, gewoon v'tjes" · "en niets opnieuw tekenen"
- v2 (`sprite_v2/`, nieuwe maker op de nieuwe basis): Haunter-ogen 1-op-1, mond met V-tanden; v3 loopt (glans terug, oogcontrast, ring vloeiend, kluwen bij de kuif).
- v3–v6: keuring v3 FAIL (5 uitvoeringspunten) → v4/v5 (maker) → eindkeuring v5 FAIL (10 px) → v6 (Claude, 26 px herkleurd) → herkeuring **PASS**. Kandidaat voor Jordi: `sprite_v6/hauntflare_v6.png` (+ `_8x.png`). Open MAG (niet verplicht): zwarte kluwen kuif/ring (45–48,24–27), (13,53), rechte lichte ringstrook rij 42; de modelglans valt onder Haunters oog (bol vlakker dan het model).
- 15 nov over v6: "Allemaal prima qua vorm, maar wtf is dat linker oog en die mond? De mond moet lager en meer naar links en het linker oog is gewoon waardeloos. Begin met het rechteroog te spiegelen en daarmee verder te werken, kijk dan naar wat voor hoek. De mond kan je niet zomaar copy pasten van de andere haunter sprite, kom op zeg. Laten we dat eerst fixen dan gaan we naar kleur kijken" → `gezicht_v7/` (linkeroog = gespiegeld rechteroog, pupil blijft links kijken; vier hoeken A–D; mond met de hand gezet, 4 px links en 1 px lager).
- 15 nov over `gezicht_v7/`: "ik zei nog niks opnieuw tekenen...." · "dit is schandalig slecht" · "jij kan niet tekenen, doe dat ook niet meer. Jij hebt de mond en de ogen opnieuw getekend en het is zo bespottelijk lelijk" → gezicht_v7 afgekeurd; v6 blijft de laatste sprite.
- 15 nov: "de ogen zijn trouwens niet getkeend, maar je volgt mijn instructie niet" · "je kan die spiegelen, dan naast elkaar zetten en kijken hoe het linkeroog verder aangepast moet worden, die mond heb je getekend en is belachelijk" · "je kan niet zomaar het oog spiegelen, plakken en klaar ermee zijn, je moet kijken naar perspectief" · "ik gaf als tip voor de vorm van het oog dat je dat als eerste stap kan doen, als dat niet werkt prima, maar dan moet je verder kijken" · "de mond gebruik je de haunter mond als vorm, maar die kan je niet 1 op 1 kopieren, omdat die een ander lichaam heeft, dus die moet je dan aanpassen". Opdracht maker: `sprite_v7/`.
- v7 gezicht: linkeroog = gespiegeld rechteroog verkort voor perspectief (12→8 kolommen), mond = Haunters mond ontleed en aangepast (geen 1-op-1), 2 px links en lager, tong; keuring C → C2 → C3 **PASS**. `sprite_v7/hauntflare_v7.png` (= kandidaat_C3).
- 15 nov over v7: "ogen zijn goed, de mond is prima, alleen ik mis tanden, kijk hier naar referentie materiaal" (bijlagen: `referenties/haunter_artwork.png`, `haunter_3d.png`, `haunter_pixel_ref.png`). Ogen en mond = goedgekeurd/bevroren; alleen tanden toevoegen.
