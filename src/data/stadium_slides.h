// Project Grounded: Battle Stadium, wat een trainer zegt voor de eerste beurt (trainer slide).
// Placeholders; Jordi herschrijft. Regels breken automatisch af (alleen \p voor een nieuwe pagina).
// Wordt in sTrainerSlides (src/trainer_slide.c) ingevoegd; nederlaag- en winstteksten staan in src/stadium.c.
#define STADIUM_INTRO(trainer, text) [trainer] = { [TRAINER_SLIDE_BEFORE_FIRST_TURN] = COMPOUND_STRING(text) }

STADIUM_INTRO(TRAINER_STADIUM_WARIO, "Wahahaha! I'm only here for the prize money. And the free buffet."),
STADIUM_INTRO(TRAINER_STADIUM_YOSHI, "Yoshi!\p(He looks like he's about to cry. Please be gentle.)"),
STADIUM_INTRO(TRAINER_STADIUM_GOLBAT, "SKREEEEEEEEEE!\p(The GOLBAT from your nightmares. It found you.)"),
STADIUM_INTRO(TRAINER_STADIUM_GRIMER, "Blorp.\p(GRIMER has been in this franchise since 1996. You can tell.)"),
STADIUM_INTRO(TRAINER_STADIUM_BOO, "Heh heh heh... Don't look at me! I'm shy. Also dead."),
STADIUM_INTRO(TRAINER_STADIUM_MEW, "Mew!\p(It crawled out from under the truck. The rumors were true.)"),
STADIUM_INTRO(TRAINER_STADIUM_SHY_GUY_RED, "............\p(He is too shy to talk. He brought six friends instead.)"),
STADIUM_INTRO(TRAINER_STADIUM_SHY_GUY_GREEN, "(He is even shyer than the red one. He refuses to make eye contact with the ball.)"),
STADIUM_INTRO(TRAINER_STADIUM_SHY_GUY_PINK, "Bzzzzzzz!\p(Propeller noises. He refuses to land for the match.)"),
STADIUM_INTRO(TRAINER_STADIUM_SHY_GUY_BLACK, "Psst. Hey kid. Wanna buy a mask? Slightly used."),
STADIUM_INTRO(TRAINER_STADIUM_BURGLAR, "Hands up! This is a robbery!\p...A tournament? Fine. I'll rob you in the bracket."),
STADIUM_INTRO(TRAINER_STADIUM_DITTO, "..."),
STADIUM_INTRO(TRAINER_STADIUM_JOEY, "My POOCHYENA isn't like other POOCHYENA.\pIt's in the top percentage of the top percentage!"),
STADIUM_INTRO(TRAINER_STADIUM_WINSTON, "I had my whole team made shiny. Professionally.\pMo Money, Mo Problems..."),
STADIUM_INTRO(TRAINER_STADIUM_DONALD, "My BUG POKéMON will keep you company!\p...They're still DITTO. All six. Surprise again."),
STADIUM_INTRO(TRAINER_STADIUM_IVAN, "I'm the WATER POKéMON expert! I got some very rare fishies...\pMy MAGIKARP knows HYDRO PUMP. Don't ask."),
STADIUM_INTRO(TRAINER_STADIUM_JOHNSON, "Tik tok, tik tok, tik tok."),
STADIUM_INTRO(TRAINER_STADIUM_LYLE, "My brother evolved them, and this time I actually levelled them!\pI'm indestructible! For real now!"),

#undef STADIUM_INTRO
