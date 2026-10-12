// Project Grounded: het Gen 1-"GHOST" in Lavender Town en de Pokemon Tower (Spacetime Cave, S2).
// Zonder Silph Scope verschijnt elke wilde Pokemon daar als GHOST (eigen frontsprite, naam GHOST): je Pokemon is
// te bang om iets te doen, de geest zegt "Get out... Get out...", ballen werken niet; wegrennen kan. Met de
// Silph Scope in de tas zie je de echte Pokemon en vecht je gewoon.
#include "global.h"
#include "battle.h"
#include "battle_scripts.h"
#include "gen1_ghost.h"
#include "item.h"
#include "palette.h"
#include "pokemon.h"
#include "constants/battle.h"
#include "constants/items.h"
#include "constants/region_map_sections.h"

static const u32 sGen1GhostPic[] = INCBIN_U32("graphics/grounded/gen1_ghost/front.4bpp");
static const u16 sGen1GhostPal[] = INCBIN_U16("graphics/grounded/gen1_ghost/front.gbapal");
static const u8 sText_Ghost[] = _("GHOST");

bool32 Gen1Ghost_IsActive(void)
{
    if (gBattleTypeFlags & (BATTLE_TYPE_TRAINER | BATTLE_TYPE_LINK | BATTLE_TYPE_SAFARI | BATTLE_TYPE_DOUBLE
                          | BATTLE_TYPE_RECORDED | BATTLE_TYPE_FRONTIER))
        return FALSE;
    if (gMapHeader.regionMapSectionId != MAPSEC_LAVENDER_TOWN && gMapHeader.regionMapSectionId != MAPSEC_POKEMON_TOWER)
        return FALSE;
    return !CheckBagHasItem(ITEM_SILPH_SCOPE, 1);
}

void Gen1Ghost_OnBattleStart(void)
{
    if (Gen1Ghost_IsActive())
        SetMonData(&gEnemyParty[0], MON_DATA_NICKNAME, sText_Ghost);
}

bool32 Gen1Ghost_LoadPic(u32 battler, void *dest, u32 paletteOffset)
{
    u32 i;

    if (IsOnPlayerSide(battler) || !Gen1Ghost_IsActive())
        return FALSE;
    for (i = 0; i < MAX_MON_PIC_FRAMES; i++)
        CpuCopy32(sGen1GhostPic, (u8 *)dest + i * MON_PIC_SIZE, MON_PIC_SIZE);
    LoadPalette(sGen1GhostPal, paletteOffset, PLTT_SIZE_4BPP);
    LoadPalette(sGen1GhostPal, BG_PLTT_ID(8) + BG_PLTT_ID(battler), PLTT_SIZE_4BPP);
    return TRUE;
}

const u8 *Gen1Ghost_MoveScript(u32 battler)
{
    return IsOnPlayerSide(battler) ? BattleScript_Gen1GhostScared : BattleScript_Gen1GhostGetOut;
}
