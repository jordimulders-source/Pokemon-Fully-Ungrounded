#ifndef GUARD_BURGLAR_H
#define GUARD_BURGLAR_H

// Project Grounded: de Burglar die af en toe uit een huis in de steden komt (src/burglar.c).
void Burglar_OnMapEnter(void);
bool8 Burglar_TryTriggerOnStep(s16 x, s16 y);

#endif // GUARD_BURGLAR_H
