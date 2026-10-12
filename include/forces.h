#ifndef GUARD_FORCES_H
#define GUARD_FORCES_H

// Project Grounded: Tornadus, Thundurus en Landorus die af en toe op een route staan (src/forces.c).
void Forces_OnMapEnter(void);
bool32 Forces_ActiveHere(void);
extern u8 gForcesStartingStatus;

#endif // GUARD_FORCES_H
