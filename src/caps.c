#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "caps.h"
#include "pokemon.h"
#include "data.h"
#include "constants/opponents.h"


u32 GetCurrentLevelCap(void)
{
    static const u32 sLevelCapFlagMap[][2] =
    {
        {FLAG_BADGE01_GET, 15},
        {FLAG_BADGE02_GET, 19},
        {FLAG_BADGE03_GET, 24},
        {FLAG_BADGE04_GET, 29},
        {FLAG_BADGE05_GET, 31},
        {FLAG_BADGE06_GET, 33},
        {FLAG_BADGE07_GET, 42},
        {FLAG_BADGE08_GET, 46},
        {FLAG_IS_CHAMPION, 58},
    };

    u32 i;

    if (B_LEVEL_CAP_TYPE == LEVEL_CAP_FLAG_LIST)
    {
        for (i = 0; i < ARRAY_COUNT(sLevelCapFlagMap); i++)
        {
            if (!FlagGet(sLevelCapFlagMap[i][0]))
                return sLevelCapFlagMap[i][1];
        }
    }
    else if (B_LEVEL_CAP_TYPE == LEVEL_CAP_VARIABLE)
    {
        return VarGet(B_LEVEL_CAP_VARIABLE);
    }

    return MAX_LEVEL;
}

// Project Grounded: ace-level van de volgende mijlpaal (gym, na badge 8 de kampioen, daarna 100); zie LEVELCURVE.md
u32 GetGroundedCatchUpTarget(void)
{
    static const u16 sMilestones[][2] =
    {
        {FLAG_BADGE01_GET, TRAINER_ROXANNE_1},
        {FLAG_BADGE02_GET, TRAINER_BRAWLY_1},
        {FLAG_BADGE03_GET, TRAINER_WATTSON_1},
        {FLAG_BADGE04_GET, TRAINER_FLANNERY_1},
        {FLAG_BADGE05_GET, TRAINER_NORMAN_1},
        {FLAG_BADGE06_GET, TRAINER_WINONA_1},
        {FLAG_BADGE07_GET, TRAINER_TATE_AND_LIZA_1},
        {FLAG_BADGE08_GET, TRAINER_WALLACE_1},
        {FLAG_IS_CHAMPION, TRAINER_CHAMPION_STEVEN},
    };
    u32 i, j, ace = 0;

    for (i = 0; i < ARRAY_COUNT(sMilestones); i++)
    {
        if (!FlagGet(sMilestones[i][0]))
        {
            const struct Trainer *trainer = &gTrainers[DIFFICULTY_NORMAL][sMilestones[i][1]];
            for (j = 0; j < trainer->partySize; j++)
            {
                if (trainer->party[j].lvl > ace)
                    ace = trainer->party[j].lvl;
            }
            return ace;
        }
    }
    return MAX_LEVEL;
}

// Project Grounded: inhaal-EXP. Onder het ace-level van de volgende mijlpaal krijgt een Pokémon
// B_CATCHUP_EXP_STEP procent extra EXP per level achterstand (max. B_CATCHUP_EXP_MAX procent).
// Erboven verandert er niets (geen levelcap).
static u32 GetGroundedCatchUpExp(u32 level, u32 expValue)
{
    u32 target, bonus;

    if (!B_GROUNDED_CATCHUP_EXP)
        return expValue;
    target = GetGroundedCatchUpTarget();
    if (level >= target)
        return expValue;
    bonus = (target - level) * B_CATCHUP_EXP_STEP;
    if (bonus > B_CATCHUP_EXP_MAX)
        bonus = B_CATCHUP_EXP_MAX;
    return expValue * (100 + bonus) / 100;
}

u32 GetSoftLevelCapExpValue(u32 level, u32 expValue)
{
    expValue = GetGroundedCatchUpExp(level, expValue);

    static const u32 sExpScalingDown[5] = { 4, 8, 16, 32, 64 };
    static const u32 sExpScalingUp[5]   = { 16, 8, 4, 2, 1 };

    u32 levelDifference;
    u32 currentLevelCap = GetCurrentLevelCap();

    if (B_EXP_CAP_TYPE == EXP_CAP_NONE)
        return expValue;

    if (level < currentLevelCap)
    {
        if (B_LEVEL_CAP_EXP_UP)
        {
            levelDifference = currentLevelCap - level;
            if (levelDifference > ARRAY_COUNT(sExpScalingUp) - 1)
                return expValue + (expValue / sExpScalingUp[ARRAY_COUNT(sExpScalingUp) - 1]);
            else
                return expValue + (expValue / sExpScalingUp[levelDifference]);
        }
        else
        {
            return expValue;
        }
    }
    else if (B_EXP_CAP_TYPE == EXP_CAP_HARD)
    {
        return 0;
    }
    else if (B_EXP_CAP_TYPE == EXP_CAP_SOFT)
    {
        levelDifference = level - currentLevelCap;
        if (levelDifference > ARRAY_COUNT(sExpScalingDown) - 1)
            return expValue / sExpScalingDown[ARRAY_COUNT(sExpScalingDown) - 1];
        else
            return expValue / sExpScalingDown[levelDifference];
    }
    else
    {
       return expValue;
    }
}

u32 GetCurrentEVCap(void)
{
    static const u16 sEvCapFlagMap[][2] = {
        // Define EV caps for each milestone
        {FLAG_BADGE01_GET, MAX_TOTAL_EVS *  1 / 17},
        {FLAG_BADGE02_GET, MAX_TOTAL_EVS *  3 / 17},
        {FLAG_BADGE03_GET, MAX_TOTAL_EVS *  5 / 17},
        {FLAG_BADGE04_GET, MAX_TOTAL_EVS *  7 / 17},
        {FLAG_BADGE05_GET, MAX_TOTAL_EVS *  9 / 17},
        {FLAG_BADGE06_GET, MAX_TOTAL_EVS * 11 / 17},
        {FLAG_BADGE07_GET, MAX_TOTAL_EVS * 13 / 17},
        {FLAG_BADGE08_GET, MAX_TOTAL_EVS * 15 / 17},
        {FLAG_IS_CHAMPION, MAX_TOTAL_EVS},
    };

    if (B_EV_CAP_TYPE == EV_CAP_FLAG_LIST)
    {
        for (u32 evCap = 0; evCap < ARRAY_COUNT(sEvCapFlagMap); evCap++)
        {
            if (!FlagGet(sEvCapFlagMap[evCap][0]))
                return sEvCapFlagMap[evCap][1];
        }
    }
    else if (B_EV_CAP_TYPE == EV_CAP_VARIABLE)
    {
        return VarGet(B_EV_CAP_VARIABLE);
    }
    else if (B_EV_CAP_TYPE == EV_CAP_NO_GAIN)
    {
        return 0;
    }

    return MAX_TOTAL_EVS;
}
