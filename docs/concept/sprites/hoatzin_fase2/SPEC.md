# Hoatzin fase 2 (Poison/Dark): SPEC

## Jordi (19 nov, letterlijk)
- "2 fases, poison/dark. Fase 1 doen we een kuiken en gaan we iets meer overdrijven met die klauwen en die smerige look. fase 2 wordt een volgroeide hoatzin die er eng en geniepig uit ziet"
- "Het blauwe hoofd wil ik behouden, die blik moet niet zo geniepig, de normale hoatzin is juist zo interessant omdat die zo'n typisch alert vogel oog heeft." · "het oog is niet rood met een zwart puntje"
- "Dit dier is zo bijzonder dat die niet eens heel veel hoeft af te wijken he" · "ja ik wil dat die meer op het dier lijkt in het algemeen"
- "met poison kleur bedoel ik dat typische poison paars" · later: "optie 1, alleen de buik paars" · "Vleugels misschien zo behouden, buik een tint lichter en de rest van het lichaam wat meer poison kleuren?" · "Ja wat paars tinten, maar dan wel een paars tint die goed past bij het roestachtige bruin, verder misschien op het rode oog en blauwe gezicht na de kleuren zo doen dat het er dark/poison uit ziet, maar niet vloekt" · "of misschien de vleugels 1 tint meer richting paars, bruinpaars" · "De buik vind ik nog een beetje vloeken, kan die misschien 1 tint meer richting de rest van het lichaam?" · "al zou ik de kuif wat bruiner willen en de buik iets lichter, zodat het opvalt"
- Pose: "ik zou een meer open pose willen" (Cornell-foto, `referenties/cornell_pose.png`) → v5 r1: "pose is nu goed"
- Kuif: naar de echte hoatzin (`referenties/kopportret.png`, `referenties/ref_kuif_illustratie.png`: "moeten meer zo"); te overdreven afgekeurd.
- Snavel: die van vóór het slijm (v6 r1), op v7 r4 geplakt.
- Bij het definitieve model (hertekende versie afgekeurd): "Misschien met de vorige maar gaan bouwen en tijdens het spriten aan de kleur werken" · "nee begin met de sprite maken".
- Zuur uit de bek ("een beetje zuur uit de mond lopen? Zoals bij gloom?"): Gemini kreeg het niet goed; nu niet in de sprite, open.

## Model (bevroren)
`MODEL.png` (= `gemini/v7_r4_snavel.png`). Vorm, pose, onderdelen en tekening uit het model.

## Kleur in de spritefase
- Buik een tint paarser: richting #8E6280 (licht #A57A98, schaduw #7A5270); nu ±#946869. Moet opvallen en niet vloeken.
- Blauw gezicht en rood oog met zwart puntje blijven.

## Sprite r5 (19 nov)
- Jordi: "D is het mooiste, maar de hele sprite is nog erg blurry" → buik D (#4C2860 / #7C4498 / #B47CD6).

## Op r16 (20 nov), Jordi letterlijk (aantekeningen: `sprite/r16/jordi_aantekeningen.webp`)
- "eigenlijk is niks beter geworden"
- "ok er gaat namelijk echt flink wat fout, omdat je niet goed naar het model kijkt, wat heel raar is want die kan je ook gewoon op een raster zetten. De poten zijn opnieuw getekend, altijd een belachelijk slechte keuze, de kuif is helemaal niet mooi, de nek gaat nog steeds niet goed over, de vleugels hebben een andere vorm, bovenste stuk past niet eens in het raster. Ik heb een aantal lijnen gezet ter indicatie, het is een indicatie, maar je moet echt nog even beter naar het model kijken en meten hoe het daar precies is gegaan. Misschien met kleurcodes een pixelblad maken en zo proberen te verbeteren, niks opnieuw tekenen"
- "enige wat echt goed is, is snavel, staart en buik"
- Daarna: "ook ook wel" → bevestigd: "oog is prima"

## Op r17 (20 nov), Jordi letterlijk
- "linkerpoot is helemaal niet gelukt" · "nek is nog steeds niet voldoende los van de vleugel" · "de rest klopt qua vorm" → vorm van r17 (pixelblad) bevroren, behalve linkerpoot.
- Op r18: "nek is nog niet goed doorgetrokken, de lijn, het begin en einde staat er, maar de rest niet, de 2 poten zitten aan elkaar vast en de rechts heeft opeens rare zwarte uiteinden" · "kan dit ook op een manier dat ik niet elke keer hele minimale veranderingen moet keuren" · "ja en ook kleuren, schaduw, belijning. Hij moet echt op het model lijken, de onderdelen van het lichaam moeten ook niet in elkaar overgaan"
- "alleen de kleuren die we besproken hebben mogen afwijken" (= buik D, kuif wat bruiner; rest modelkleuren)

## ONTWERP 2 (from scratch, 20 nov) — vervangt het eerste model
- Jordi: "Ik denk dat B gaat helpen, laten we helemaal from scratch beginnen" (vereenvoudigen; zie RETRO.md en STUDIE_ONTWERP.md).
- Op v9 r1: "Hij is wat blij ... hij mag nog wat lelijker" · "en de pose is wat neutraal". Op v10 r1: "deze is al wat beter, ik twijfel nog over de lichaams kleur ... misschien de haren nog net iets langer, paar cm". Kleur: "ik neig wel naar 3" (bijna zwart blauw-paars lijf, crème nek).
- **Model bevroren: `MODEL.png` = `gemini/v10_r2.png` gespiegeld** (Jordi: "ik denk dat we deze moeten gaan bouwen. Het design lijkt me een stuk simplistischer nu, de haren kunnen we kijken in de sprite hoe ze eruit zien, spiegel de afbeelding en ga van start"). Oud model: `MODEL_v1_oud.png`, oude rondes `sprite/r1–r25`.
- Kenmerken: dreighouding met half opgeheven vleugels, voorovergebogen, snavel open (sissend), rafelige rode-bruine punkkuif, blauw kaal gezicht, rood oog met zwart puntje, grijze haaksnavel, crème nek, paarse hangende krop, bijna zwart blauw-paarse vleugels/rug/staart met crème staartpunt, grijze poten met lichte klauwen.
- Kuif: lengte beoordelen in de sprite.
- Kop groter in de sprite? Jordi: "nee een hoatzin heeft ook een en kleine kop, laten we kijken hoe ver we komen" → kopmaat volgens het model.
- Oog (Jordi): "je kan voor het oog desnoods 1 zwarte pixel doen omringd door óf 4 óf 6 rode pixels, omringd door een cirkel aan blauw" · "maar ga eerst maar niks opnieuw tekenen" → s1 alleen het model overnemen; oogvarianten pas als het nodig is.
- Jordi: "en neem het model over" · "elke keer als de maker gaat tekenen gaat het fout en kost het meerdere rondes".
- Op s1: "je hebt precies genoeg ruimte voor mijn oog idee, zonder dat je iets anders hoeft te veranderen" · over snavel/kuif/pennen: "Hij wil ze toch niet gaan tekenen he?" → nee: alleen de reductie-instellingen verbeteren.
- Op s2: "oog B, 6 rood, ga nu bouwen totdat er een goede versie staat, niet meer blurry".
- "vleugelpennen kan je evt met 1 pixel ipv halve pixel doen en dan minder".
- Snavel: "hoef je de binnenkant van de mond niet te laten zien, hoe die er nu uit ziet is prima, alleen nog mooier afwerken".
- Poten: "vorm ook prima, alleen netter afwerken. Alleen de teen van de linkse poot is iets te bol".
- Op s5: "het zit in de belijning van de kuif, snavel en poten. Daarnaast is er veel teveel effen kleuren, meer kleurtinten, meer schaduw".
- Op s8: "de vorm van de poten is beter, het gaat erop vooruit, maar nog steeds te blurry, snavel heeft nu wel opeens dezelfde kleur als de nek".
- "buik mag ook de zwarte lijn omheen zachter worden".
- Op s9: "ja hij is nog blurry, de buik is nu wel beter. De poten zijn nog niet netjes afgemaakt. De hele sprite mist gewoon schaduw/tinten/contrast. Het is heel veel 2 kleuren per stuk. Alleen de buik heeft er 3 en ziet er daarom al wat beter uit".
- "lichaam/vleugel lijkt ook bijna willekeurig te zijn".
- Op s10: "eindelijk wat vooruitgang, maak maar prompt voor nieuw gesprek. Vooral hoofd en poten moeten nog beter".
