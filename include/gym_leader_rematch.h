#ifndef GUARD_TRAINER_REMATCH_H
#define GUARD_TRAINER_REMATCH_H

#include "constants/rematches.h"

void UpdateGymLeaderRematch(void);
void GymLeaderRematch_OnRematchWon(u16 trainerId);
const u8 *GymLeaderRematch_TryRequestByCall(u32 rematchIdx);
s32 GetCurrentGymLeaderRematchLevel(void);

#endif //GUARD_TRAINER_REMATCH_H
