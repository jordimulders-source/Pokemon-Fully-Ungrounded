#ifndef GUARD_GEN1_GHOST_H
#define GUARD_GEN1_GHOST_H

// Project Grounded: Gen 1-GHOST zonder Silph Scope (src/gen1_ghost.c)
bool32 Gen1Ghost_IsActive(void);
void Gen1Ghost_OnBattleStart(void);
bool32 Gen1Ghost_LoadPic(u32 battler, void *dest, u32 paletteOffset);
const u8 *Gen1Ghost_MoveScript(u32 battler);

#endif // GUARD_GEN1_GHOST_H
