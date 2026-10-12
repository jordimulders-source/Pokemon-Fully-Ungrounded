// Project Grounded: de rivaal na de Hall of Fame (gevecht 7 in Pacifidlog, gevecht 8 bij de Battle Tower,
// daarna dagelijks in het Paradiso Resort). De trainer-id's waren op, dus er zijn er maar drie: een per starter
// van de speler (TRAINER_RIVAL_POSTGAME_*). Naam, foto, muziek en team komen uit src/data/rival_postgame.party:
// BRENDAN of MAY (geslacht van de speler) en fase 1 (Pacifidlog) of fase 2 (Frontier/Paradiso, na
// FLAG_RIVAL_PG_PACIFIDLOG_DONE). GetTrainerStructFromId (data.h) stuurt deze drie id's hierheen.
#include "global.h"
#include "data.h"
#include "event_data.h"
#include "battle.h"
#include "battle_transition.h"
#include "trainer_pools.h"
#include "constants/abilities.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/trainers.h"
#include "constants/battle_ai.h"

enum
{
    RIVAL_PG_BRENDAN_PACIFIDLOG_TREECKO,
    RIVAL_PG_BRENDAN_PACIFIDLOG_TORCHIC,
    RIVAL_PG_BRENDAN_PACIFIDLOG_MUDKIP,
    RIVAL_PG_BRENDAN_FRONTIER_TREECKO,
    RIVAL_PG_BRENDAN_FRONTIER_TORCHIC,
    RIVAL_PG_BRENDAN_FRONTIER_MUDKIP,
    RIVAL_PG_MAY_PACIFIDLOG_TREECKO,
    RIVAL_PG_MAY_PACIFIDLOG_TORCHIC,
    RIVAL_PG_MAY_PACIFIDLOG_MUDKIP,
    RIVAL_PG_MAY_FRONTIER_TREECKO,
    RIVAL_PG_MAY_FRONTIER_TORCHIC,
    RIVAL_PG_MAY_FRONTIER_MUDKIP,
    RIVAL_PG_COUNT
};

static const struct Trainer sRivalPostgameTrainers[DIFFICULTY_COUNT][RIVAL_PG_COUNT] =
{
#include "data/rival_postgame.h"
};

const struct Trainer *GetRivalPostgameTrainer(u32 trainerId)
{
    u32 idx;

    if (trainerId == TRAINER_RIVAL_POSTGAME_TREECKO)
        idx = 0;
    else if (trainerId == TRAINER_RIVAL_POSTGAME_TORCHIC)
        idx = 1;
    else
        idx = 2;
    if (FlagGet(FLAG_RIVAL_PG_PACIFIDLOG_DONE))
        idx += 3;
    if (gSaveBlock2Ptr->playerGender == MALE) // speler is een jongen: de rivaal is MAY
        idx += 6;
    return &sRivalPostgameTrainers[DIFFICULTY_NORMAL][idx];
}
