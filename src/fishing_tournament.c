// Project Grounded: het wekelijkse visserstoernooi op de steiger van Dewford (ZEE_PLAN.md).
// Geen minigame: de jury weegt automatisch de zwaarste vis uit je team. Alleen echte vissen tellen (sFish; geen
// Wailord, Kyogre, Tentacool of schelpen). Gewicht = gewicht van de soort (gSpeciesInfo, hg) x groottefactor^3;
// de groottefactor komt uit dezelfde hash/tabel als de Lotad/Seedot-meter (GetMonSizePermille, max. 1800).
// Elke week (RTC-dag / 7) een nieuwe recordhouder: altijd iemands absurd grote Magikarp, en die is altijd
// zwaarder dan het theoretische maximum van elke vis in sFish (onverslaanbaar, Jordi).
// Prijzen (1x per week): verliezen = troostprijs: de eerste keer een Lucky Egg, daarna per week een klein nuttig
// item. (De winnaarstak met één Poké Ball + trofee bestaat nog in het script, maar is onbereikbaar.)
// Flags: FLAG_FISH_TOURNEY_WEEK_BIT0-4 (week % 31 + 1), FLAG_FISH_TOURNEY_TROPHY, FLAG_FISH_TOURNEY_LUCKY_EGG.
#include "global.h"
#include "event_data.h"
#include "pokemon.h"
#include "pokemon_size_record.h"
#include "rtc.h"
#include "string_util.h"
#include "constants/characters.h"
#include "constants/items.h"
#include "constants/species.h"

static const u8 sRecordOwner_0[] = _("OLD GUS");
static const u8 sRecordOwner_1[] = _("a TUBER named KEVIN");
static const u8 sRecordOwner_2[] = _("GRANDMA DOROTHY");
static const u8 sRecordOwner_3[] = _("MR. BRINEY's ex");
static const u8 sRecordOwner_4[] = _("a man who won't say his name");
static const u8 sRecordOwner_5[] = _("SLATEPORT's harbor master");
static const u8 sRecordOwner_6[] = _("a suspiciously wet child");
static const u8 sRecordOwner_7[] = _("DEWFORD's mayor (again)");

static const u8 *const sRecordOwners[] =
{
    sRecordOwner_0, sRecordOwner_1, sRecordOwner_2, sRecordOwner_3,
    sRecordOwner_4, sRecordOwner_5, sRecordOwner_6, sRecordOwner_7,
};

// vis van de opschepper (vaste NPC op de steiger), elke week een andere
static const u16 sBoasterFish[] =
{
    SPECIES_SHARPEDO, SPECIES_SEAKING, SPECIES_WHISCASH, SPECIES_LANTURN, SPECIES_RELICANTH,
    SPECIES_HUNTAIL, SPECIES_BASCULIN, SPECIES_BARRASKEWDA, SPECIES_QWILFISH, SPECIES_LUMINEON,
};

// troostprijzen na de Lucky Egg: klein, maar nuttiger dan één Poké Ball
static const u16 sConsolationPrizes[] =
{
    ITEM_RARE_CANDY, ITEM_PP_UP, ITEM_EXP_CANDY_M, ITEM_BIG_PEARL, ITEM_DIVE_BALL, ITEM_HEART_SCALE,
};

// wat de jury als vis erkent (zie ook het reglement in DewfordTown_Text_FishJudgeRules)
static const u16 sFish[] =
{
    SPECIES_MAGIKARP, SPECIES_GYARADOS, SPECIES_GOLDEEN, SPECIES_SEAKING, SPECIES_HORSEA, SPECIES_SEADRA,
    SPECIES_KINGDRA, SPECIES_CHINCHOU, SPECIES_LANTURN, SPECIES_QWILFISH, SPECIES_QWILFISH_HISUI, SPECIES_OVERQWIL,
    SPECIES_REMORAID, SPECIES_MANTYKE, SPECIES_MANTINE, SPECIES_CARVANHA, SPECIES_SHARPEDO, SPECIES_BARBOACH,
    SPECIES_WHISCASH, SPECIES_FEEBAS, SPECIES_MILOTIC, SPECIES_HUNTAIL, SPECIES_GOREBYSS, SPECIES_RELICANTH,
    SPECIES_LUVDISC, SPECIES_FINNEON, SPECIES_LUMINEON, SPECIES_BASCULIN_RED_STRIPED, SPECIES_BASCULIN_BLUE_STRIPED,
    SPECIES_BASCULIN_WHITE_STRIPED, SPECIES_BASCULEGION_M, SPECIES_BASCULEGION_F, SPECIES_ALOMOMOLA,
    SPECIES_STUNFISK, SPECIES_STUNFISK_GALAR, SPECIES_WISHIWASHI_SOLO, SPECIES_WISHIWASHI_SCHOOL, SPECIES_BRUXISH,
    SPECIES_ARROKUDA, SPECIES_BARRASKEWDA, SPECIES_ARCTOVISH, SPECIES_DRACOVISH, SPECIES_VELUZA, SPECIES_DONDOZO,
};

#define MAX_SIZE_PERMILLE 1800

static const u16 sWeekFlags[] =
{
    FLAG_FISH_TOURNEY_WEEK_BIT0, FLAG_FISH_TOURNEY_WEEK_BIT1, FLAG_FISH_TOURNEY_WEEK_BIT2,
    FLAG_FISH_TOURNEY_WEEK_BIT3, FLAG_FISH_TOURNEY_WEEK_BIT4,
};

static u32 Mix(u32 h)
{
    h ^= h >> 15;
    h *= 2246822519u;
    h ^= h >> 13;
    h *= 3266489917u;
    h ^= h >> 16;
    return h;
}

static u32 GetWeek(void)
{
    RtcCalcLocalTime();
    if (gLocalTime.days < 0)
        return 0;
    return gLocalTime.days / 7;
}

static u32 WeekHash(u32 week)
{
    u16 tid = gSaveBlock2Ptr->playerTrainerId[0] | (gSaveBlock2Ptr->playerTrainerId[1] << 8);
    return Mix(week * 2654435761u ^ (tid * 40503u) ^ 0xF15Bu);
}

static u32 ScaledWeight(u16 species, u32 permille);
static bool32 IsFish(u16 species);

// zwaarste vis die theoretisch kan bestaan (grootste soort x maximale groottefactor)
static u32 MaxFishWeight(void)
{
    u32 i, w, max = 0;
    for (i = 0; i < ARRAY_COUNT(sFish); i++)
    {
        w = ScaledWeight(sFish[i], MAX_SIZE_PERMILLE);
        if (w > max)
            max = w;
    }
    return max;
}

// de record-Magikarp: altijd minstens 800 kg en altijd zwaarder dan elke mogelijke vis (hg)
static u32 RecordWeight(u32 week)
{
    u32 floor = MaxFishWeight() + 1;
    if (floor < 8000)
        floor = 8000;
    return floor + WeekHash(week) % 8001;
}

static u16 BoasterSpecies(u32 week)
{
    return sBoasterFish[Mix(WeekHash(week)) % ARRAY_COUNT(sBoasterFish)];
}

static u32 ScaledWeight(u16 species, u32 permille)
{
    u64 w = GetSpeciesWeight(species);
    return (u32)(w * permille * permille * permille / 1000000000u);
}

static u32 BoasterWeight(u32 week)
{
    u32 permille = 1000 + Mix(Mix(WeekHash(week))) % 301;
    return ScaledWeight(BoasterSpecies(week), permille);
}

static void FormatWeight(u8 *dst, u32 hg)
{
    dst = ConvertIntToDecimalStringN(dst, hg / 10, STR_CONV_MODE_LEFT_ALIGN, 6);
    *dst++ = CHAR_PERIOD;
    dst = ConvertIntToDecimalStringN(dst, hg % 10, STR_CONV_MODE_LEFT_ALIGN, 1);
    *dst++ = CHAR_SPACE;
    *dst++ = CHAR_k;
    *dst++ = CHAR_g;
    *dst = EOS;
}

static u32 StoredWeek(void)
{
    u32 i, v = 0;
    for (i = 0; i < ARRAY_COUNT(sWeekFlags); i++)
    {
        if (FlagGet(sWeekFlags[i]))
            v |= 1 << i;
    }
    return v;
}

static void StoreWeek(u32 v)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sWeekFlags); i++)
    {
        if (v & (1 << i))
            FlagSet(sWeekFlags[i]);
        else
            FlagClear(sWeekFlags[i]);
    }
}

static bool32 IsFish(u16 species)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sFish); i++)
    {
        if (sFish[i] == species)
            return TRUE;
    }
    return FALSE;
}

static bool32 IsWaterType(u16 species)
{
    return gSpeciesInfo[species].types[0] == TYPE_WATER || gSpeciesInfo[species].types[1] == TYPE_WATER;
}

// Bord / jury: STR_VAR_1 = eigenaar van de record-Magikarp, STR_VAR_2 = gewicht, STR_VAR_3 = vis van de opschepper.
void FishTourney_GetBoardInfo(void)
{
    u32 week = GetWeek();
    u8 *s;

    StringCopy(gStringVar1, sRecordOwners[Mix(WeekHash(week) ^ 0x1234) % ARRAY_COUNT(sRecordOwners)]);
    FormatWeight(gStringVar2, RecordWeight(week));
    s = StringCopy(gStringVar3, GetSpeciesName(BoasterSpecies(week)));
    *s++ = CHAR_COMMA;
    *s++ = CHAR_SPACE;
    FormatWeight(s, BoasterWeight(week));
}

// Weegt de zwaarste vis (sFish) uit het team.
// VAR_RESULT: 0 = geen vis, anders de plaats (1-3). STR_VAR_1 = bijnaam, STR_VAR_2 = gewicht.
// VAR_0x8004 = 1 als de prijs van deze week al is opgehaald; VAR_0x8005 = prijs (blijft heel na giveitem, dat
// 0x8006/0x8007 overschrijft); VAR_0x8007 = 1 als er geen vis is maar wel een Water-Pokémon (STR_VAR_3 = de
// zwaarste daarvan, voor "dat is geen vis").
void FishTourney_Weigh(void)
{
    u32 i, week, best = 0, bestIdx = PARTY_SIZE, place, wetBest = 0, wetIdx = PARTY_SIZE;

    for (i = 0; i < gPlayerPartyCount; i++)
    {
        struct Pokemon *mon = &gPlayerParty[i];
        u16 species = GetMonData(mon, MON_DATA_SPECIES);
        u32 w;

        if (species == SPECIES_NONE || GetMonData(mon, MON_DATA_IS_EGG))
            continue;
        w = ScaledWeight(species, GetMonSizePermille(mon));
        if (w == 0)
            w = 1;
        if (!IsFish(species))
        {
            if (IsWaterType(species) && w > wetBest)
            {
                wetBest = w;
                wetIdx = i;
            }
            continue;
        }
        if (w > best)
        {
            best = w;
            bestIdx = i;
        }
    }

    gSpecialVar_0x8007 = FALSE;
    if (bestIdx == PARTY_SIZE)
    {
        gSpecialVar_Result = 0;
        if (wetIdx != PARTY_SIZE)
        {
            gSpecialVar_0x8007 = TRUE;
            GetMonData(&gPlayerParty[wetIdx], MON_DATA_NICKNAME, gStringVar3);
            StringGet_Nickname(gStringVar3);
        }
        return;
    }

    week = GetWeek();
    GetMonData(&gPlayerParty[bestIdx], MON_DATA_NICKNAME, gStringVar1);
    StringGet_Nickname(gStringVar1);
    FormatWeight(gStringVar2, best);

    place = 1;
    if (RecordWeight(week) >= best) // gelijkspel gaat naar de Magikarp
        place++;
    if (BoasterWeight(week) >= best)
        place++;
    gSpecialVar_Result = place;

    gSpecialVar_0x8004 = (StoredWeek() == (week % 31) + 1);
    if (place == 1)
    {
        gSpecialVar_0x8005 = ITEM_POKE_BALL; // de trofee (FLAG_FISH_TOURNEY_TROPHY) regelt het script
    }
    else if (!FlagGet(FLAG_FISH_TOURNEY_LUCKY_EGG))
    {
        gSpecialVar_0x8005 = ITEM_LUCKY_EGG;
    }
    else
    {
        gSpecialVar_0x8005 = sConsolationPrizes[week % ARRAY_COUNT(sConsolationPrizes)];
    }
}

// Na het geven van de prijs (VAR_0x8005 nog van FishTourney_Weigh).
void FishTourney_ClaimPrize(void)
{
    StoreWeek((GetWeek() % 31) + 1);
    if (gSpecialVar_0x8005 == ITEM_LUCKY_EGG)
        FlagSet(FLAG_FISH_TOURNEY_LUCKY_EGG);
}
