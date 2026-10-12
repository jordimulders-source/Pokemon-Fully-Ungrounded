#ifndef GUARD_CONSTANTS_STADIUM_H
#define GUARD_CONSTANTS_STADIUM_H
// Project Grounded: Battle Stadium (ook voor scripts)
#define STADIUM_SINGLES 0
#define STADIUM_DOUBLES 1

// Project Grounded: Battle Casino (src/battle_casino.c), ook voor scripts
#define CASINO_STATE_ARENA      10  // VAR_STADIUM_STATE: casinogevecht in de Stadium-arena (OnFrame van de arena)
#define CASINO_STATE_RESULT     11  // VAR_STADIUM_STATE: terug in het casino, uitslag nog tonen
#define CASINO_EXIT_NONE        0   // Casino_OpenCard: geen inzet
#define CASINO_EXIT_RESULT      1   // uitslag bekend (meegekeken of alleen de uitslag)
#define CASINO_EXIT_ARENA       2   // Stadium-modus: eerst naar de arena
#endif // GUARD_CONSTANTS_STADIUM_H
