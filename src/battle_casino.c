// Project Grounded: Battle Casino (Battle Frontier). Je zet BP in op gevechten tussen NPC's en kijkt mee
// (de AI speelt beide kanten via B_FLAG_AI_VS_AI_BATTLE) of vraagt alleen de uitslag.
// - Geen nieuwe trainers: teams, namen en foto's komen uit bestaande trainers (trainers.party), de Stadium-pool,
//   de Frontier-huurpool (gBattleFrontierMons) en de Spire-bazen (spire_encounters.h).
// - Modi worden vrijgespeeld met het aantal afgeronde inzetten (VAR_CASINO_BETS, sUnlockBets).
// - Odds: kracht per team = som over de Pokémon van (BST x level / 100)^2 (x HP-vermenigvuldiger bij bazen),
//   x typevoordeel (gemiddelde beste STAB-effectiviteit tegen het andere team); winkans A = TA^2 / (TA^2 + TB^2);
//   uitbetaling = 0,9 / winkans (1,1x - 5,0x).
// - Wereldmodi: korte tv-overgang (ruis) en direct het gevecht in. Stadium-modi: je kijkt vanaf de rand van de
//   Stadium-arena (BattleFrontier_StadiumArena, VAR_STADIUM_STATE = CASINO_STATE_ARENA).
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "battle_message.h"
#include "battle_setup.h"
#include "battle_tower.h"
#include "battle_transition.h"
#include "battle_util.h"
#include "bg.h"
#include "data.h"
#include "decompress.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "load_save.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "random.h"
#include "scanline_effect.h"
#include "script.h"
#include "sound.h"
#include "spire.h"
#include "sprite.h"
#include "stadium.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/battle_frontier.h"
#include "constants/battle_frontier_mons.h"
#include "constants/characters.h"
#include "constants/event_objects.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/trainers.h"

#define CASINO_MATCHES  4
#define NO_TRAINER      TRAINER_NONE

enum
{
    MODE_WORLD_SINGLES,
    MODE_WORLD_DOUBLES,
    MODE_STADIUM_SINGLES,
    MODE_STADIUM_DOUBLES,
    MODE_FACTORY,
    MODE_SPIRE_BOSS,
    MODE_COUNT,
};

// afgeronde inzetten nodig per modus (ook in de tekst van de croupier)
static const u8 sUnlockBets[MODE_COUNT] = {0, 3, 6, 10, 15, 20};

static const u8 sModeName0[] = _("WORLD SINGLES");
static const u8 sModeName1[] = _("WORLD DOUBLES");
static const u8 sModeName2[] = _("STADIUM SINGLES");
static const u8 sModeName3[] = _("STADIUM DOUBLES");
static const u8 sModeName4[] = _("FACTORY RENTALS");
static const u8 sModeName5[] = _("SPIRE BOSS");
static const u8 *const sModeNames[MODE_COUNT] = {sModeName0, sModeName1, sModeName2, sModeName3, sModeName4, sModeName5};

enum { SRC_TRAINER, SRC_FRONTIER, SRC_SPIRE };

struct CasinoMon
{
    u16 species;
    u16 idx;        // partijplek van de trainer, Frontier-huurmon of Spire-ontmoeting
    u8 lvl;
    u8 src;
    u8 owner;       // trainer 0 of 1 van deze kant
    u8 hpMult;      // in tienden (Spire-baas), anders 10
};

struct CasinoSide
{
    u16 trainer[2];
    u8 trainers;    // 0 = Spire-baas (geen trainer), 1 of 2
    u8 count;
    struct CasinoMon mons[PARTY_SIZE];
};

struct CasinoMatch
{
    struct CasinoSide side[2];  // kant 0 speelt als "speler" (AI), kant 1 als tegenstander
    u16 chanceA;                // echte winkans kant 0 in promille (uitslag, "alleen uitslag", overslaan)
    u16 shownA;                 // winkans volgens de bookies (ruis, soms bewust ernaast): bepaalt de odds
    u16 mult[2];                // uitbetaling in tienden
    bool8 mispriced;            // de bookies zitten er bewust naast (tip van de bookie)
};

struct Casino
{
    struct CasinoMatch card[CASINO_MATCHES];
    bool8 cardValid;
    u8 cardMode;
    u8 mode;
    u8 match;
    u8 side;
    u8 result;      // 0 = kant 0 won, 1 = kant 1, 2 = gelijk
    u8 newUnlock;
    u16 bet;
    u16 savedPartner;
    bool8 skipped;  // gevecht overgeslagen met START
};

static EWRAM_DATA struct Casino sC = {0};
EWRAM_DATA bool8 gCasinoBattle = FALSE;

static const u16 sBets[] = {1, 5, 10, 25, 50, 100};

static bool32 IsStadiumMode(u32 mode);

// --- trainers kiezen -----------------------------------------------------------------------------
static u32 Bst(u16 species)
{
    const struct SpeciesInfo *s = &gSpeciesInfo[species];

    return s->baseHP + s->baseAttack + s->baseDefense + s->baseSpeed + s->baseSpAttack + s->baseSpDefense;
}

static bool32 IsValidWorldTrainer(u16 id)
{
    const struct Trainer *t;
    u32 i;

    if (id == TRAINER_NONE || id >= TRAINERS_COUNT || id == TRAINER_SECRET_BASE)
        return FALSE;
    t = GetTrainerStructFromId(id);
    if (t->party == NULL || t->partySize == 0 || t->partySize > PARTY_SIZE || t->poolSize != 0 || t->overrideTrainer != 0)
        return FALSE;
    if (t->trainerName[0] == EOS)
        return FALSE;
    // jezelf niet (Brendan/May als rivaal van hetzelfde geslacht)
    if (t->trainerPic == (gSaveBlock2Ptr->playerGender == MALE ? TRAINER_PIC_BRENDAN : TRAINER_PIC_MAY))
        return FALSE;
    for (i = 0; i < t->partySize; i++)
        if (t->party[i].species == SPECIES_NONE || t->party[i].species >= NUM_SPECIES || t->party[i].lvl == 0)
            return FALSE;
    return TRUE;
}

static bool32 IsUsed(const u16 *used, u32 n, u16 id)
{
    u32 i;

    for (i = 0; i < n; i++)
        if (used[i] == id)
            return TRUE;
    return FALSE;
}

// minMons: singles altijd 4 tegen 4, doubles 3 per trainer
static u16 RandomWorldTrainer(const u16 *used, u32 nUsed, u32 minMons)
{
    u32 tries;

    for (tries = 0; tries < 300; tries++)
    {
        u16 id = 1 + Random() % (TRAINERS_COUNT - 1);
        if (IsValidWorldTrainer(id) && GetTrainerStructFromId(id)->partySize >= minMons && !IsUsed(used, nUsed, id))
            return id;
    }
    return NO_TRAINER;
}

static s32 RandomPoolEntry(const u16 *used, u32 nUsed)
{
    u32 tries, n = Stadium_PoolCount();

    for (tries = 0; tries < 100; tries++)
    {
        u32 i = Random() % n;
        const struct StadiumEntrant *e = Stadium_GetEntrant(i);

        if (e->rivalFor != 0 && e->rivalFor != gSaveBlock2Ptr->playerGender + 1)
            continue;
        if (IsUsed(used, nUsed, e->trainerId))
            continue;
        return i;
    }
    return -1;
}

static s32 PoolIndexOf(u16 trainerId)
{
    u32 i;

    for (i = 0; i < Stadium_PoolCount(); i++)
        if (Stadium_GetEntrant(i)->trainerId == trainerId)
            return i;
    return -1;
}

// --- teams opbouwen (alleen beschrijving; de echte Pokémon pas bij het gevecht) -------------------
static void AddMon(struct CasinoSide *s, u16 species, u16 idx, u8 lvl, u8 src, u8 owner, u8 hpMult)
{
    struct CasinoMon *m;

    if (s->count >= PARTY_SIZE)
        return;
    m = &s->mons[s->count++];
    m->species = species;
    m->idx = idx;
    m->lvl = lvl;
    m->src = src;
    m->owner = owner;
    m->hpMult = hpMult;
}

// mask = vaste teamplekken (Stadium), anders de sterkste maxMons (in volgorde van het team); lvl 0 = eigen level
static void AddTrainerMons(struct CasinoSide *s, u8 owner, u16 trainerId, u32 maxMons, u8 mask, u8 lvl)
{
    const struct Trainer *t = GetTrainerStructFromId(trainerId);
    u32 i, j, n = min(t->partySize, PARTY_SIZE);
    u8 pick = 0;

    s->trainer[owner] = trainerId;
    if (mask == 0)
    {
        if (n <= maxMons)
        {
            pick = (1 << n) - 1;
        }
        else
        {
            for (j = 0; j < maxMons; j++)
            {
                u32 best = 0, bestI = 0;
                for (i = 0; i < n; i++)
                {
                    u32 q = Bst(t->party[i].species) * t->party[i].lvl;
                    if (!(pick & (1 << i)) && q >= best)
                    {
                        best = q;
                        bestI = i;
                    }
                }
                pick |= 1 << bestI;
            }
        }
    }
    else
    {
        pick = mask;
    }
    for (i = 0; i < n; i++)
        if (pick & (1 << i))
            AddMon(s, t->party[i].species, i, lvl ? lvl : t->party[i].lvl, SRC_TRAINER, owner, 10);
}

static bool32 HasSpecies(const struct CasinoMatch *m, u16 species)
{
    u32 s, i;

    for (s = 0; s < 2; s++)
        for (i = 0; i < m->side[s].count; i++)
            if (m->side[s].mons[i].species == species)
                return TRUE;
    return FALSE;
}

static void AddRentals(struct CasinoMatch *m, struct CasinoSide *s, u32 n)
{
    u32 k = 0, tries = 0;

    while (k < n && tries++ < 100)
    {
        u16 idx = Random() % NUM_FRONTIER_MONS;
        u16 species = gBattleFrontierMons[idx].species;

        if (species == SPECIES_NONE || HasSpecies(m, species))
            continue;
        AddMon(s, species, idx, 50, SRC_FRONTIER, 0, 10);
        k++;
    }
}

static u32 SideMaxLevel(const struct CasinoSide *s)
{
    u32 i, lvl = 1;

    for (i = 0; i < s->count; i++)
        lvl = max(lvl, s->mons[i].lvl);
    return lvl;
}

static bool32 RandomSpireBoss(struct CasinoSide *s, u8 lvl)
{
    u32 tries, n = Spire_BossCount();

    for (tries = 0; tries < 20; tries++)
    {
        u32 i = Random() % n;
        const struct SpireEncounter *e = Spire_GetBoss(i);

        if (e->foes[0].species == SPECIES_NONE)
            continue;
        s->trainers = 0;
        s->trainer[0] = s->trainer[1] = NO_TRAINER;
        AddMon(s, e->foes[0].species, i, lvl, SRC_SPIRE, 0, max(10, min(40, e->foes[0].hp)));
        return TRUE;
    }
    return FALSE;
}

// --- kracht en odds ------------------------------------------------------------------------------
static u64 SidePower(const struct CasinoSide *s)
{
    u64 t = 0;
    u32 i;

    for (i = 0; i < s->count; i++)
    {
        u64 q = Bst(s->mons[i].species) * s->mons[i].lvl / 100 + 1;
        t += q * q * s->mons[i].hpMult / 10;
    }
    return t;
}

// gemiddelde beste STAB-effectiviteit van a tegen b (UQ4.12, 4096 = neutraal)
static u32 TypeEdge(const struct CasinoSide *a, const struct CasinoSide *b)
{
    u32 i, j, k, sum = 0, n = 0;

    for (i = 0; i < a->count; i++)
    {
        const struct SpeciesInfo *as = &gSpeciesInfo[a->mons[i].species];
        for (j = 0; j < b->count; j++)
        {
            const struct SpeciesInfo *ds = &gSpeciesInfo[b->mons[j].species];
            u32 best = 0;
            for (k = 0; k < 2; k++)
            {
                u32 e = GetTypeModifier(as->types[k], ds->types[0]);
                if (ds->types[1] != ds->types[0])
                    e = (e * GetTypeModifier(as->types[k], ds->types[1])) >> 12;
                best = max(best, e);
            }
            sum += best;
            n++;
        }
    }
    return n ? sum / n : 4096;
}

// Echte winkans: TA^2 / (TA^2 + TB^2), T = som (BST x level / 100)^2 x typevoordeel
static void ComputeOdds(struct CasinoMatch *m)
{
    u64 ta = SidePower(&m->side[0]), tb = SidePower(&m->side[1]), a2, b2;
    u32 ea = TypeEdge(&m->side[0], &m->side[1]), eb = TypeEdge(&m->side[1], &m->side[0]);
    u32 c;

    ta = ta * (8192 + ea) / 3;
    tb = tb * (8192 + eb) / 3;
    while (ta > (1u << 26) || tb > (1u << 26))
    {
        ta >>= 1;
        tb >>= 1;
    }
    a2 = ta * ta;
    b2 = tb * tb;
    c = (a2 + b2) ? (u32)(a2 * 1000 / (a2 + b2)) : 500;
    m->chanceA = max(10, min(990, c));
}

// Bookies (Jordi): de getoonde kans = echte kans + ruis (tot ±12 procentpunt bij 50/50, kleiner naar de randen); 1 op 6 wedstrijden zitten ze er
// bewust 25-35 procentpunt naast, richting de underdog (uit te buiten met kennis van types en teams).
// Uitbetaling = 0,92 / getoonde kans, x1,1 tot x30.
static void PriceMatch(struct CasinoMatch *m)
{
    s32 shown = m->chanceA, s, spread = m->chanceA * (1000 - m->chanceA) / 2083;  // 120 bij 50/50, ±23 bij 95/5

    shown += (s32)(Random() % (2 * spread + 1)) - spread;
    m->mispriced = (Random() % 6 == 0);
    if (m->mispriced)
        shown += (m->chanceA > 500 ? -1 : 1) * (250 + (s32)(Random() % 101));
    shown = max(25, min(975, shown));
    m->shownA = shown;
    for (s = 0; s < 2; s++)
    {
        u32 p = s ? 1000 - shown : shown;
        m->mult[s] = max(11, min(300, (9200 + p / 2) / p));
    }
}

// Uitbetaling in hele BP (afgerond, altijd minstens 1 BP winst)
static u32 Payout(u32 bet, u32 mult)
{
    return max(bet + 1, (bet * mult + 5) / 10);
}

// --- de kaart ------------------------------------------------------------------------------------
static bool32 GenerateMatch(u32 mode, struct CasinoMatch *m, const u16 *used, u32 nUsed)
{
    u16 local[16];
    u32 nl = 0, s, k;
    s32 p;

    memset(m, 0, sizeof(*m));
    for (k = 0; k < nUsed && k < 8; k++)
        local[nl++] = used[k];
    switch (mode)
    {
    case MODE_WORLD_SINGLES:
    case MODE_WORLD_DOUBLES:
    case MODE_FACTORY:
    {
        u32 per = (mode == MODE_WORLD_DOUBLES) ? 2 : 1;
        for (s = 0; s < 2; s++)
        {
            m->side[s].trainers = per;
            for (k = 0; k < per; k++)
            {
                u16 id = RandomWorldTrainer(local, nl, mode == MODE_FACTORY ? 1 : (per == 2 ? 3 : 4));
                if (id == NO_TRAINER)
                    return FALSE;
                local[nl++] = id;
                if (mode == MODE_FACTORY)
                    m->side[s].trainer[0] = id;
                else
                    AddTrainerMons(&m->side[s], k, id, per == 2 ? 3 : 4, 0, 0);
            }
            if (mode == MODE_FACTORY)
                AddRentals(m, &m->side[s], 4);
        }
        break;
    }
    case MODE_STADIUM_SINGLES:
    case MODE_STADIUM_DOUBLES:
    {
        u32 per = (mode == MODE_STADIUM_DOUBLES) ? 2 : 1;
        for (s = 0; s < 2; s++)
        {
            m->side[s].trainers = per;
            for (k = 0; k < per; k++)
            {
                const struct StadiumEntrant *e;
                p = RandomPoolEntry(local, nl);
                if (p < 0)
                    return FALSE;
                e = Stadium_GetEntrant(p);
                local[nl++] = e->trainerId;
                AddTrainerMons(&m->side[s], k, e->trainerId, PARTY_SIZE, per == 2 ? e->doublesMask : e->singlesMask, 50);
            }
        }
        break;
    }
    case MODE_SPIRE_BOSS:
    {
        u16 id = RandomWorldTrainer(local, nl, 4);
        if (id == NO_TRAINER)
            return FALSE;
        m->side[1].trainers = 1;
        AddTrainerMons(&m->side[1], 0, id, 4, 0, 0);
        // de baas is even sterk als de aas van de trainer (plus wat speling); zijn HP-vermenigvuldiger doet de rest
        if (!RandomSpireBoss(&m->side[0], min(100, SideMaxLevel(&m->side[1]) + Random() % 6)))
            return FALSE;
        break;
    }
    }
    for (s = 0; s < 2; s++)
        if (m->side[s].count == 0)
            return FALSE;
    // willekeurig wie links staat (behalve de baas: die speelt altijd de "speler"-kant)
    if (mode != MODE_SPIRE_BOSS && (Random() & 1))
    {
        struct CasinoSide tmp = m->side[0];
        m->side[0] = m->side[1];
        m->side[1] = tmp;
    }
    ComputeOdds(m);
    return TRUE;
}

static void CommitUsed(const struct CasinoMatch *m, u16 *used, u32 *nUsed)
{
    u32 s, k;

    for (s = 0; s < 2; s++)
        for (k = 0; k < m->side[s].trainers && *nUsed < 16; k++)
            used[(*nUsed)++] = m->side[s].trainer[k];
}

// Vier wedstrijden (Jordi): de meeste spannend (50/50 tot ±65/35); ongeveer 1 op 3 kaarten heeft één eenzijdige.
static void GenerateCard(u32 mode)
{
    u16 targets[CASINO_MATCHES], used[16];
    u32 i, nUsed = 0;
    struct CasinoMatch cand;

    for (i = 0; i < CASINO_MATCHES; i++)
        targets[i] = 500 + Random() % 151;
    if (Random() % 3 == 0)
        targets[Random() % CASINO_MATCHES] = 900 + Random() % 80;
    for (i = 0; i < CASINO_MATCHES; i++)
    {
        u32 bestDist = 0xFFFF, attempts;

        memset(&sC.card[i], 0, sizeof(sC.card[i]));
        for (attempts = 0; attempts < 24; attempts++)
        {
            u32 fav, dist;
            if (!GenerateMatch(mode, &cand, used, nUsed))
                continue;
            fav = max(cand.chanceA, 1000 - cand.chanceA);
            dist = (fav > targets[i]) ? fav - targets[i] : targets[i] - fav;
            if (dist < bestDist)
            {
                bestDist = dist;
                sC.card[i] = cand;
            }
            if (dist < 25)
                break;
        }
        PriceMatch(&sC.card[i]);
        CommitUsed(&sC.card[i], used, &nUsed);
    }
    sC.cardValid = TRUE;
    sC.cardMode = mode;
}

static bool32 IsModeUnlocked(u32 mode)
{
    return VarGet(VAR_CASINO_BETS) >= sUnlockBets[mode];
}

static bool32 IsStadiumMode(u32 mode)
{
    return mode == MODE_STADIUM_SINGLES || mode == MODE_STADIUM_DOUBLES;
}

static void GetSideName(const struct CasinoSide *s, u8 *dst)
{
    if (s->trainers == 0)
    {
        StringCopy(dst, Spire_GetBoss(s->mons[0].idx)->name);
        return;
    }
    dst = StringCopy(dst, GetTrainerNameFromId(s->trainer[0]));
    if (s->trainers == 2)
    {
        dst = StringCopy(dst, COMPOUND_STRING(" & "));
        StringCopy(dst, GetTrainerNameFromId(s->trainer[1]));
    }
}

// --- gevecht -------------------------------------------------------------------------------------
static void FillTrainerMon(struct TrainerMon *dst, const struct CasinoSide *s, const struct CasinoMon *cm)
{
    switch (cm->src)
    {
    case SRC_TRAINER:
        *dst = GetTrainerStructFromId(s->trainer[cm->owner])->party[cm->idx];
        break;
    case SRC_FRONTIER:
        *dst = gBattleFrontierMons[cm->idx];
        dst->iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31);
        break;
    case SRC_SPIRE:
    {
        const struct SpireFoe *f = &Spire_GetBoss(cm->idx)->foes[0];
        u32 i;

        memset(dst, 0, sizeof(*dst));
        dst->species = f->species;
        for (i = 0; i < MAX_MON_MOVES; i++)
            dst->moves[i] = f->moves[i];
        dst->ability = f->ability;
        dst->heldItem = f->item;
        dst->iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31);
        dst->nature = NATURE_HARDY;
        break;
    }
    }
    dst->lvl = cm->lvl;
}

// Pokémon van één kant (owner 0xFF = allemaal; bij twee trainers om en om, zodat beide eerst iets laten zien)
static u8 BuildSideParty(struct Pokemon *party, const struct CasinoSide *s, u8 owner)
{
    struct TrainerMon mons[PARTY_SIZE];
    struct Trainer temp;
    u32 i, r, n = 0;

    for (r = 0; r < PARTY_SIZE; r++)
    {
        for (i = 0; i < s->count; i++)
        {
            const struct CasinoMon *cm = &s->mons[i];
            u32 rank = 0, k;

            if (owner != 0xFF && cm->owner != owner)
                continue;
            // rang binnen de eigen trainer
            for (k = 0; k < i; k++)
                if (s->mons[k].owner == cm->owner)
                    rank++;
            if (rank == r)
                FillTrainerMon(&mons[n++], s, cm);
        }
    }
    temp = *GetTrainerStructFromId(s->trainers ? s->trainer[0] : sC.card[sC.match].side[1].trainer[0]);
    temp.party = mons;
    temp.partySize = n;
    temp.poolSize = 0;
    temp.overrideTrainer = 0;
    return CreateNPCTrainerPartyFromTrainer(party, &temp, FALSE, BATTLE_TYPE_TRAINER);
}

// battle_main.c: team van de tegenstander(s)
u8 Casino_BuildEnemyParty(struct Pokemon *party, u16 trainerNum, bool8 firstTrainer)
{
    const struct CasinoSide *s = &sC.card[sC.match].side[1];

    if (firstTrainer)
        ZeroEnemyPartyMons();
    return BuildSideParty(party, s, s->trainers == 2 ? (firstTrainer ? 0 : 1) : 0xFF);
}

static const u8 sDefeat1[] = _("My bookie is going to hear about this.");
static const u8 sDefeat2[] = _("Somebody just won a lot of BP on me\nlosing. I hope they choke on it.");
static const u8 sDefeat3[] = _("Was that on TV? Please say no.");
static const u8 sWin1[] = _("Ka-ching! Somebody out there loves me.");
static const u8 sWin2[] = _("I'd like to thank everyone who bet on\nme. Both of you.");
static const u8 sWin3[] = _("The odds were wrong. I am the odds.");

static const u8 *Casino_DefeatText(u16 trainerId)
{
    if (IsStadiumMode(sC.mode))
        return Stadium_GetDefeatText(trainerId);
    switch (Random() % 3)
    {
    case 0:  return sDefeat1;
    case 1:  return sDefeat2;
    default: return sDefeat3;
    }
}

// battle_message.c: wat een tegenstander zegt als hij wint
const u8 *Casino_GetWinText(u16 trainerId)
{
    if (IsStadiumMode(sC.mode))
        return Stadium_GetWinText(trainerId);
    switch (Random() % 3)
    {
    case 0:  return sWin1;
    case 1:  return sWin2;
    default: return sWin3;
    }
}

// battle_message.c: naam van de "speler"-kant
static EWRAM_DATA u8 sName[40] = {0};

const u8 *Casino_GetPlayerSideName(void)
{
    GetSideName(&sC.card[sC.match].side[0], sName);
    return sName;
}

// battle_controllers.c: de Spire-baas heeft geen trainer, dus geen foto aan de spelerskant
bool32 Casino_HidePlayerTrainerPic(void)
{
    return sC.card[sC.match].side[0].trainers == 0;
}

static void SetupBattle(void)
{
    const struct CasinoMatch *m = &sC.card[sC.match];
    const struct CasinoSide *a = &m->side[0], *b = &m->side[1];

    SavePlayerParty();
    ZeroPlayerPartyMons();
    BuildSideParty(gPlayerParty, a, 0xFF);
    // Spire-baas: HP-vermenigvuldiger (max. 999, dan past het in de levensbalk)
    if (a->trainers == 0)
    {
        u32 hp = min(999, GetMonData(&gPlayerParty[0], MON_DATA_MAX_HP) * a->mons[0].hpMult / 10);
        SetMonData(&gPlayerParty[0], MON_DATA_MAX_HP, &hp);
        SetMonData(&gPlayerParty[0], MON_DATA_HP, &hp);
    }
    CalculatePlayerPartyCount();

    memset(&gTrainerBattleParameter, 0, sizeof(gTrainerBattleParameter));
    TRAINER_BATTLE_PARAM.opponentA = b->trainer[0];
    TRAINER_BATTLE_PARAM.defeatTextA = (u8 *)Casino_DefeatText(b->trainer[0]);
    gBattleTypeFlags = BATTLE_TYPE_TRAINER;
    if (b->trainers == 2 || a->trainers == 2)
        gBattleTypeFlags |= BATTLE_TYPE_DOUBLE;
    if (b->trainers == 2)
    {
        TRAINER_BATTLE_PARAM.opponentB = b->trainer[1];
        TRAINER_BATTLE_PARAM.defeatTextB = (u8 *)Casino_DefeatText(b->trainer[1]);
        gBattleTypeFlags |= BATTLE_TYPE_TWO_OPPONENTS;
    }
    sC.savedPartner = gPartnerTrainerId;
    // AI en trainerfoto van de spelerskant; de baas krijgt de AI van zijn tegenstander
    gPartnerTrainerId = a->trainers ? a->trainer[0] : b->trainer[0];
    FlagSet(FLAG_CASINO_AI_VS_AI);
    gCasinoBattle = TRUE;
}

static void EndBattle(void)
{
    u8 outcome = gBattleOutcome & ~B_OUTCOME_LINK_BATTLE_RAN;

    if (outcome == B_OUTCOME_WON)
        sC.result = 0;
    else if (outcome == B_OUTCOME_DREW)
        sC.result = 2;
    else
        sC.result = 1;
    FlagClear(FLAG_CASINO_AI_VS_AI);
    gCasinoBattle = FALSE;
    gPartnerTrainerId = sC.savedPartner;
    LoadPlayerParty();
    gSpecialVar_Result = CASINO_EXIT_RESULT;
}

static void CB2_EndCasinoBattle(void)
{
    EndBattle();
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void Task_StartArenaBattle(u8 taskId)
{
    if (IsBattleTransitionDone() == TRUE)
    {
        gMain.savedCallback = CB2_EndCasinoBattle;
        SetMainCallback2(CB2_InitBattle);
        DestroyTask(taskId);
    }
}

// --- scherm: de wedstrijdkaart -------------------------------------------------------------------
enum { SCR_CARD, SCR_BET, SCR_TV };

#define PAL_FELT    12
#define PAL_NOISE   13
#define PAL_TEXT    15
#define MAX_PICS    4
#define MAX_ICONS   12
#define TV_FRAMES   34

struct CasinoScreen
{
    u8 state;
    u8 exiting;
    u8 exitTo;      // CASINO_EXIT_* of 0xFE = gevecht
    u8 betIdx;
    u8 timer;
    u8 pics[MAX_PICS];
    u8 picCount;
    u8 icons[MAX_ICONS];
    u8 iconCount;
};

static EWRAM_DATA struct CasinoScreen *sScr = NULL;

static const u32 sFeltTiles[2][8] =
{
    {0x11111111, 0x11211111, 0x11111111, 0x11111112, 0x11111111, 0x12111111, 0x11111111, 0x11111211},
    {0x11111111, 0x11111111, 0x11112111, 0x11111111, 0x21111111, 0x11111111, 0x11111121, 0x11111111},
};
static const u16 sFeltPal[16] = {RGB(3, 12, 6), RGB(3, 12, 6), RGB(2, 10, 5)};
static const u16 sNoisePal[16] = {RGB(2, 2, 3), RGB(5, 5, 6), RGB(12, 12, 13), RGB(20, 20, 21), RGB(28, 28, 29)};

// tekstpalet: 1 = papier, 2/3 donker, 4/5 rood, 6/7 grijs, 8/9 blauw, 10 lijn, 11/12 goud, 13 tv-rand
static const u16 sTextPal[16] =
{
    RGB(31, 30, 26), RGB(31, 30, 26), RGB(6, 5, 4), RGB(24, 23, 19),
    RGB(28, 4, 4), RGB(31, 22, 20), RGB(17, 16, 14), RGB(26, 25, 21),
    RGB(4, 10, 24), RGB(21, 24, 30), RGB(14, 11, 8), RGB(24, 17, 2), RGB(31, 27, 15),
    RGB(8, 8, 9),
};
#define PAPER   1
#define DARK    2
#define RED_INK 4
#define GRAY    6
#define INK     10
#define BEZEL   13
static const u8 sColor_Dark[] = {0, 2, 3};
static const u8 sColor_Red[]  = {0, 4, 5};
static const u8 sColor_Gray[] = {0, 6, 7};
static const u8 sColor_Gold[] = {0, 11, 12};
static const u8 sColor_Tv[]   = {0, 3, 2};

static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 3},
};

static const struct WindowTemplate sWindowTemplates[] =
{
    {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 18, .paletteNum = PAL_TEXT, .baseBlock = 0x001},
    DUMMY_WIN_TEMPLATE,
};
#define WIN 0
#define WX(x) ((x) - 8)
#define WY(y) ((y) - 8)

static void Task_CasinoScreen(u8 taskId);

static void PrintText(u32 font, s32 x, s32 y, const u8 *color, const u8 *str)
{
    AddTextPrinterParameterized3(WIN, font, WX(x), WY(y), color, TEXT_SKIP_DRAW, str);
}

static void Rect(s32 x, s32 y, s32 w, s32 h, s32 t, u8 color)
{
    FillWindowPixelRect(WIN, PIXEL_FILL(color), WX(x), WY(y), w, t);
    FillWindowPixelRect(WIN, PIXEL_FILL(color), WX(x), WY(y + h - t), w, t);
    FillWindowPixelRect(WIN, PIXEL_FILL(color), WX(x), WY(y), t, h);
    FillWindowPixelRect(WIN, PIXEL_FILL(color), WX(x + w - t), WY(y), t, h);
}

#define TAG_PORTRAIT 0x5480
#define TAG_PIC_PAL  0x5490

static const struct OamData sOam_Portrait = {.shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 0};

static u8 Pixel(const u8 *pic, u32 x, u32 y)
{
    u8 b = pic[((y / 8) * 8 + x / 8) * 32 + (y % 8) * 4 + (x % 8) / 2];

    return (x & 1) ? b >> 4 : b & 0xF;
}

// 32x32 rond het hoofd uit de trainerfoto (zelfde aanpak als AddPortrait in stadium_screens.c)
static void AddPortrait(u16 picId, s16 x, s16 y)
{
    u8 slot = sScr->picCount, pal, id, *pic, *out;
    s32 top, minX = 63, maxX = 0, x0, y0, px, py, row;
    struct SpriteSheet sheet;
    struct SpriteTemplate tmpl = {TAG_PORTRAIT + slot, TAG_NONE, &sOam_Portrait, gDummySpriteAnimTable, NULL, gDummySpriteAffineAnimTable, SpriteCallbackDummy};

    if (slot >= MAX_PICS)
        return;
    pal = AllocSpritePalette(TAG_PIC_PAL + slot);
    if (pal == 0xFF)
        return;
    pic = Alloc(64 * 64 / 2);
    out = AllocZeroed(32 * 32 / 2);
    DecompressPicFromTable(&gTrainerSprites[picId].frontPic, pic);
    for (top = 0; top < 64; top++)
    {
        for (px = 0; px < 64 && !Pixel(pic, px, top); px++)
            ;
        if (px < 64)
            break;
    }
    for (row = top; row < top + 16 && row < 64; row++)
    {
        for (px = 0; px < 64; px++)
        {
            if (Pixel(pic, px, row))
            {
                minX = min(minX, px);
                maxX = max(maxX, px);
            }
        }
    }
    x0 = max(0, min(32, (minX + maxX) / 2 - 16));
    y0 = max(0, min(32, top - 2));
    for (py = 0; py < 32; py++)
    {
        for (px = 0; px < 32; px++)
        {
            u8 v = Pixel(pic, x0 + px, y0 + py);
            u8 *b = &out[((py / 8) * 4 + px / 8) * 32 + (py % 8) * 4 + (px % 8) / 2];
            *b |= (px & 1) ? v << 4 : v;
        }
    }
    sheet.data = out;
    sheet.size = 32 * 32 / 2;
    sheet.tag = TAG_PORTRAIT + slot;
    LoadSpriteSheet(&sheet);
    LoadPalette(gTrainerSprites[picId].palette.data, OBJ_PLTT_ID(pal), PLTT_SIZE_4BPP);
    Free(pic);
    Free(out);
    id = CreateSprite(&tmpl, x, y, 0);
    if (id == MAX_SPRITES)
    {
        FreeSpriteTilesByTag(TAG_PORTRAIT + slot);
        FreeSpritePaletteByTag(TAG_PIC_PAL + slot);
        return;
    }
    gSprites[id].oam.paletteNum = pal;
    sScr->pics[sScr->picCount++] = id;
}

static void AddIcon(u16 species, s16 x, s16 y)
{
    u8 id;

    if (sScr->iconCount >= MAX_ICONS)
        return;
    id = CreateMonIcon(species, SpriteCB_MonIcon, x, y, 1, 0);
    if (id == MAX_SPRITES)
        return;
    gSprites[id].oam.priority = 0;
    sScr->icons[sScr->iconCount++] = id;
}

static void FreePics(void)
{
    u32 i;

    for (i = 0; i < sScr->picCount; i++)
    {
        DestroySprite(&gSprites[sScr->pics[i]]);
        FreeSpriteTilesByTag(TAG_PORTRAIT + i);
        FreeSpritePaletteByTag(TAG_PIC_PAL + i);
    }
    sScr->picCount = 0;
    for (i = 0; i < sScr->iconCount; i++)
        FreeAndDestroyMonIconSprite(&gSprites[sScr->icons[i]]);
    sScr->iconCount = 0;
}

static void FormatMult(u8 *dst, u32 mult)
{
    *dst++ = CHAR_x;
    dst = ConvertIntToDecimalStringN(dst, mult / 10, STR_CONV_MODE_LEFT_ALIGN, 2);
    if (mult < 100)     // vanaf x10 zonder decimaal
    {
        *dst++ = CHAR_PERIOD;
        ConvertIntToDecimalStringN(dst, mult % 10, STR_CONV_MODE_LEFT_ALIGN, 1);
    }
}

// Eén kant van de wedstrijd. Singles: portret, klasse, naam, odds, team in twee rijen van drie.
// Doubles: per trainer een rij met portret, naam en drie Pokémon. Levels naast (singles) of boven (doubles) het icoon.
static void DrawPanel(u32 s, s32 x0)
{
    const struct CasinoMatch *m = &sC.card[sC.match];
    const struct CasinoSide *side = &m->side[s];
    bool32 sel = (sC.side == s);
    const u8 *oddsColor = sel ? sColor_Red : sColor_Gold;
    u8 buf[48];
    s32 px = x0 + 4, i, k;

    Rect(x0, 35, 106, 93, sel ? 2 : 1, sel ? RED_INK : INK);
    FormatMult(buf, m->mult[s]);
    if (side->trainers == 2)
    {
        PrintText(FONT_NORMAL, px + 100 - GetStringWidth(FONT_NORMAL, buf, 0), 37, oddsColor, buf);
        for (k = 0; k < 2; k++)
        {
            const struct Trainer *t = GetTrainerStructFromId(side->trainer[k]);
            s32 base = 38 + k * 44, col = 0;

            u32 lo = 100, hi = 1;
            u8 *p;

            AddPortrait(t->trainerPic, px + 16, base + 22);
            PrintText(FONT_SMALL_NARROW, px + 34, base, sColor_Dark, t->trainerName);
            for (i = 0; i < side->count; i++)
            {
                const struct CasinoMon *cm = &side->mons[i];

                if (cm->owner != k)
                    continue;
                AddIcon(cm->species, px + 44 + col * 22, base + 30);
                lo = min(lo, cm->lvl);
                hi = max(hi, cm->lvl);
                col++;
            }
            // levels per trainer als bereik (per icoon past niet naast drie iconen)
            p = StringCopy(buf, COMPOUND_STRING("Lv"));
            p = ConvertIntToDecimalStringN(p, lo, STR_CONV_MODE_LEFT_ALIGN, 3);
            if (hi != lo)
            {
                *p++ = CHAR_HYPHEN;
                ConvertIntToDecimalStringN(p, hi, STR_CONV_MODE_LEFT_ALIGN, 3);
            }
            PrintText(FONT_SMALL, px + 34, base + 9, sColor_Gray, buf);
        }
        return;
    }
    if (side->trainers == 1)
    {
        const struct Trainer *t = GetTrainerStructFromId(side->trainer[0]);
        AddPortrait(t->trainerPic, px + 16, 54);
        PrintText(FONT_SMALL_NARROW, px + 36, 37, sColor_Gray, gTrainerClasses[t->trainerClass].name);
        PrintText(FONT_SMALL_NARROW, px + 36, 47, sColor_Dark, t->trainerName);
    }
    else
    {
        PrintText(FONT_SMALL_NARROW, px, 37, sColor_Gray, sModeName5);
        PrintText(FONT_SMALL_NARROW, px, 47, sColor_Dark, Spire_GetBoss(side->mons[0].idx)->name);
    }
    PrintText(FONT_NORMAL, side->trainers ? px + 36 : px, 57, oddsColor, buf);
    for (i = 0; i < side->count; i++)
    {
        const struct CasinoMon *cm = &side->mons[i];
        s32 ix = px + 12 + (i % 3) * 33, iy = 88 + (i / 3) * 24;

        AddIcon(cm->species, ix, iy);
        ConvertIntToDecimalStringN(buf, cm->lvl, STR_CONV_MODE_LEFT_ALIGN, 3);
        PrintText(FONT_SMALL, ix + 11, iy + 1, sColor_Gray, buf);
    }
}

static u32 BetAmount(void)
{
    return sBets[sScr->betIdx];
}

static void DrawCard(void)
{
    u8 buf[48];
    u32 bp = gSaveBlock2Ptr->frontier.battlePoints, i, modes = 0;

    for (i = 0; i < MODE_COUNT; i++)
        modes += IsModeUnlocked(i);
    PrintText(FONT_NORMAL, 12, 9, sColor_Dark, sModeNames[sC.mode]);
    StringCopy(buf, COMPOUND_STRING("BP "));
    ConvertIntToDecimalStringN(buf + 3, bp, STR_CONV_MODE_LEFT_ALIGN, 4);
    PrintText(FONT_NORMAL, 228 - GetStringWidth(FONT_NORMAL, buf, 0), 9, sColor_Gold, buf);
    StringCopy(buf, COMPOUND_STRING("{UP_ARROW}{DOWN_ARROW} Match "));
    ConvertIntToDecimalStringN(buf + StringLength(buf), sC.match + 1, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringAppend(buf, COMPOUND_STRING(" of 4"));
    PrintText(FONT_SMALL, 12, 24, sColor_Gray, buf);
    if (modes > 1)
        PrintText(FONT_SMALL, 168, 24, sColor_Gray, COMPOUND_STRING("L/R: game"));
    DrawPanel(0, 10);
    DrawPanel(1, 124);
    if (sScr->state == SCR_CARD)
    {
        PrintText(FONT_SMALL, 12, 129, sColor_Dark, COMPOUND_STRING("A: bet on the red side    B: leave"));
        PrintText(FONT_SMALL, 12, 139, sColor_Gray, COMPOUND_STRING("{LEFT_ARROW}{RIGHT_ARROW} side    {UP_ARROW}{DOWN_ARROW} match"));
    }
    else
    {
        u8 *p = StringCopy(buf, COMPOUND_STRING("Bet {LEFT_ARROW} "));
        p = ConvertIntToDecimalStringN(p, BetAmount(), STR_CONV_MODE_LEFT_ALIGN, 3);
        p = StringCopy(p, COMPOUND_STRING(" BP {RIGHT_ARROW}   Pays "));
        p = ConvertIntToDecimalStringN(p, Payout(BetAmount(), sC.card[sC.match].mult[sC.side]), STR_CONV_MODE_LEFT_ALIGN, 4);
        StringCopy(p, COMPOUND_STRING(" BP"));
        PrintText(FONT_SMALL, 12, 129, sColor_Red, buf);
        PrintText(FONT_SMALL, 12, 139, sColor_Gray, COMPOUND_STRING("A: watch   SELECT: result only   B: back"));
    }
}

// tv: donkere kast met een gat erin, daarachter ruis op BG1
#define TV_X0   28
#define TV_Y0   24
#define TV_X1   212
#define TV_Y1   120

static void DrawTv(void)
{
    u8 buf[48];

    FillWindowPixelBuffer(WIN, PIXEL_FILL(BEZEL));
    FillWindowPixelRect(WIN, PIXEL_FILL(0), WX(TV_X0), WY(TV_Y0), TV_X1 - TV_X0, TV_Y1 - TV_Y0);
    Rect(TV_X0 - 3, TV_Y0 - 3, TV_X1 - TV_X0 + 6, TV_Y1 - TV_Y0 + 6, 2, GRAY);
    PrintText(FONT_SMALL, TV_X0, 128, sColor_Tv, COMPOUND_STRING("CASINO TV"));
    PrintText(FONT_SMALL, TV_X1 - 22, 128, sColor_Red, COMPOUND_STRING("LIVE"));
    GetSideName(&sC.card[sC.match].side[0], buf);
    StringAppend(buf, COMPOUND_STRING(" vs "));
    GetSideName(&sC.card[sC.match].side[1], buf + StringLength(buf));
    PrintText(FONT_SMALL_NARROW, TV_X0, 138, sColor_Tv, buf);
    PrintText(FONT_SMALL, TV_X1 - 50, 138, sColor_Tv, COMPOUND_STRING("START: skip"));
}

static void UpdateNoise(void)
{
    u16 *map = GetBgTilemapBuffer(1);
    u32 x, y;

    for (y = TV_Y0 / 8; y < (TV_Y1 + 7) / 8; y++)
        for (x = TV_X0 / 8; x < (TV_X1 + 7) / 8 + 1; x++)
            map[y * 32 + x] = (2 + (Random() & 7)) | ((Random() & 3) << 10) | (PAL_NOISE << 12);
    ScheduleBgCopyTilemapToVram(1);
}

static void LoadNoiseTiles(void)
{
    u32 *tiles = Alloc(8 * 32);
    u32 t, r, x;

    for (t = 0; t < 8; t++)
    {
        for (r = 0; r < 8; r++)
        {
            u32 v = 0;
            for (x = 0; x < 8; x++)
            {
                u32 c = (r & 1) ? 1 + (Random() % 2) : 1 + (Random() % 4);    // donkere oneven lijnen = scanlines
                v |= c << (x * 4);
            }
            tiles[t * 8 + r] = v;
        }
    }
    LoadBgTiles(1, tiles, 8 * 32, 2);
    Free(tiles);
    LoadPalette(sNoisePal, BG_PLTT_ID(PAL_NOISE), PLTT_SIZE_4BPP);
}

static void Redraw(void)
{
    FreePics();
    if (sScr->state == SCR_TV)
    {
        DrawTv();
    }
    else
    {
        FillWindowPixelBuffer(WIN, PIXEL_FILL(PAPER));
        DrawCard();
    }
    CopyWindowToVram(WIN, COPYWIN_FULL);
}

static void VBlankCB_Casino(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_Casino(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    RunTextPrinters();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void OpenScreen(void)
{
    u16 *tilemap;
    u32 x, y;

    sScr = AllocZeroed(sizeof(*sScr));
    SetVBlankCallback(NULL);
    ScanlineEffect_Stop();
    ResetPaletteFade();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetAllPicSprites();
    ResetTasks();
    ResetVramOamAndBgCntRegs();
    ResetAllBgsCoordinates();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    SetBgTilemapBuffer(0, AllocZeroed(BG_SCREEN_SIZE));
    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();

    tilemap = AllocZeroed(BG_SCREEN_SIZE);
    LoadBgTiles(1, sFeltTiles, sizeof(sFeltTiles), 0);
    LoadPalette(sFeltPal, BG_PLTT_ID(PAL_FELT), PLTT_SIZE_4BPP);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            tilemap[y * 32 + x] = ((x * 7 + y * 3) % 5 == 0) | (PAL_FELT << 12);
    SetBgTilemapBuffer(1, tilemap);
    ScheduleBgCopyTilemapToVram(1);
    LoadPalette(sTextPal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    PutWindowTilemap(WIN);
    LoadMonIconPalettes();
    Redraw();
    ScheduleBgCopyTilemapToVram(0);

    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON | DISPCNT_BG0_ON | DISPCNT_BG1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_Casino);
    SetMainCallback2(CB2_Casino);
    CreateTask(Task_CasinoScreen, 0);
}

static void FreeScreen(void)
{
    FreePics();
    FreeMonIconPalettes();
    FreeAllWindowBuffers();
    Free(GetBgTilemapBuffer(0));
    Free(GetBgTilemapBuffer(1));
    Free(sScr);
    sScr = NULL;
}

static void Exit(u8 exitTo)
{
    sScr->exiting = TRUE;
    sScr->exitTo = exitTo;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
}

static void ClampBet(void)
{
    u32 bp = gSaveBlock2Ptr->frontier.battlePoints;

    while (sScr->betIdx > 0 && sBets[sScr->betIdx] > bp)
        sScr->betIdx--;
}

static void PlaceBet(void)
{
    gSaveBlock2Ptr->frontier.battlePoints -= BetAmount();
    sC.bet = BetAmount();
}

static void StartTv(void)
{
    sScr->state = SCR_TV;
    sScr->timer = 0;
    sC.skipped = FALSE;
    SetupBattle();
    PlayMapChosenOrBattleBGM(0);
    LoadNoiseTiles();
    UpdateNoise();
    Redraw();
}

static void SwitchMode(s32 dir)
{
    u32 m = sC.mode, i;

    for (i = 0; i < MODE_COUNT; i++)
    {
        m = (m + MODE_COUNT + dir) % MODE_COUNT;
        if (IsModeUnlocked(m))
            break;
    }
    if (m == sC.mode)
        return;
    PlaySE(SE_SELECT);
    sC.mode = m;
    sC.match = 0;
    GenerateCard(m);
    Redraw();
}

static void Task_CasinoScreen(u8 taskId)
{
    if (sScr->state == SCR_TV)
    {
        // ±1 s ruis, beeld wordt lichter, korte witte flits en dan het gevecht
        if (!gPaletteFade.active || sScr->timer < TV_FRAMES)
        {
            sScr->timer++;
            if (sScr->timer % 2)
                UpdateNoise();
            SetGpuReg(REG_OFFSET_BG1HOFS, Random() % 3);
            if (sScr->timer == TV_FRAMES)
            {
                BeginNormalPaletteFade(PALETTES_ALL, -2, 0, 16, RGB_WHITE);
            }
            else if (sScr->timer > TV_FRAMES && !gPaletteFade.active)
            {
                DestroyTask(taskId);
                FreeScreen();
                gMain.savedCallback = CB2_EndCasinoBattle;
                SetMainCallback2(CB2_InitBattle);
            }
        }
        return;
    }
    if (gPaletteFade.active)
        return;
    if (sScr->exiting)
    {
        gSpecialVar_Result = sScr->exitTo;
        DestroyTask(taskId);
        FreeScreen();
        SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
        return;
    }
    if (sScr->state == SCR_CARD)
    {
        if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            Exit(CASINO_EXIT_NONE);
        }
        else if (JOY_NEW(A_BUTTON))
        {
            // lege wedstrijd (geen teams gevonden): niet inzetten
            if (sC.card[sC.match].side[0].count == 0 || sC.card[sC.match].side[1].count == 0)
            {
                PlaySE(SE_FAILURE);
                return;
            }
            PlaySE(SE_SELECT);
            sScr->state = SCR_BET;
            ClampBet();
            Redraw();
        }
        else if (JOY_REPEAT(DPAD_UP | DPAD_DOWN))
        {
            PlaySE(SE_SELECT);
            sC.match = (sC.match + (JOY_REPEAT(DPAD_UP) ? CASINO_MATCHES - 1 : 1)) % CASINO_MATCHES;
            Redraw();
        }
        else if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sC.side ^= 1;
            Redraw();
        }
        else if (JOY_NEW(L_BUTTON))
        {
            SwitchMode(-1);
        }
        else if (JOY_NEW(R_BUTTON))
        {
            SwitchMode(1);
        }
    }
    else
    {
        if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sScr->state = SCR_CARD;
            Redraw();
        }
        else if (JOY_REPEAT(DPAD_LEFT) && sScr->betIdx > 0)
        {
            PlaySE(SE_SELECT);
            sScr->betIdx--;
            Redraw();
        }
        else if (JOY_REPEAT(DPAD_RIGHT) && sScr->betIdx + 1 < ARRAY_COUNT(sBets)
              && sBets[sScr->betIdx + 1] <= gSaveBlock2Ptr->frontier.battlePoints)
        {
            PlaySE(SE_SELECT);
            sScr->betIdx++;
            Redraw();
        }
        else if (JOY_NEW(SELECT_BUTTON))
        {
            // alleen de uitslag: getrokken uit de odds
            PlaySE(SE_SHOP);
            PlaceBet();
            sC.skipped = FALSE;
            sC.result = ((Random() % 1000) < sC.card[sC.match].chanceA) ? 0 : 1;   // echte kans, niet de getoonde
            Exit(CASINO_EXIT_RESULT);
        }
        else if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SHOP);
            PlaceBet();
            if (IsStadiumMode(sC.mode))
                Exit(CASINO_EXIT_ARENA);
            else
                StartTv();
        }
    }
}

// --- specials ------------------------------------------------------------------------------------
// VAR_RESULT = BP over
void Casino_HasBp(void)
{
    gSpecialVar_Result = gSaveBlock2Ptr->frontier.battlePoints != 0;
}

// De kaart; VAR_RESULT = CASINO_EXIT_* (na meekijken met tv: het gevecht is al gespeeld)
void Casino_OpenCard(void)
{
    if (!IsModeUnlocked(sC.mode))
        sC.mode = MODE_WORLD_SINGLES;
    if (!sC.cardValid || sC.cardMode != sC.mode)
    {
        GenerateCard(sC.mode);
        sC.match = 0;
    }
    sC.side &= 1;
    CleanupOverworldWindowsAndTilemaps();
    OpenScreen();
    sScr->betIdx = 2;   // 10 BP
    ClampBet();
}

// In de arena (Stadium-modi): het gevecht, met een korte transitie
void Casino_StartArenaBattle(void)
{
    sC.skipped = FALSE;
    SetupBattle();
    CreateTask(Task_StartArenaBattle, 1);
    PlayMapChosenOrBattleBGM(0);
    BattleTransition_StartOnField(B_TRANSITION_SLICE);
}

// Arena: overworld-sprites van de vier (of twee) deelnemers; VAR_RESULT = STADIUM_SINGLES/DOUBLES
void Casino_SetArenaGfx(void)
{
    const struct CasinoMatch *m = &sC.card[sC.match];
    static const u16 sVars[2][2] = {{VAR_OBJ_GFX_ID_1, VAR_OBJ_GFX_ID_3}, {VAR_OBJ_GFX_ID_0, VAR_OBJ_GFX_ID_2}};
    u32 s, k;

    for (s = 0; s < 2; s++)
    {
        for (k = 0; k < m->side[s].trainers; k++)
        {
            s32 p = PoolIndexOf(m->side[s].trainer[k]);
            VarSet(sVars[s][k], p >= 0 ? Stadium_GetEntrant(p)->gfx : OBJ_EVENT_GFX_BOY_1);
        }
    }
    gSpecialVar_Result = (m->side[0].trainers == 2) ? STADIUM_DOUBLES : STADIUM_SINGLES;
}

// Uitbetalen. VAR_RESULT: 0 = verloren, 1 = gewonnen, 2 = gelijk (inzet terug).
// gStringVar1 = winnaar, gStringVar2 = bedrag, gStringVar3 = nieuw saldo
void Casino_Resolve(void)
{
    u32 bp = gSaveBlock2Ptr->frontier.battlePoints, amount = sC.bet, bets, m;

    if (sC.result == 2)
    {
        bp += sC.bet;
        gSpecialVar_Result = 2;
        StringCopy(gStringVar1, COMPOUND_STRING("nobody"));
    }
    else
    {
        GetSideName(&sC.card[sC.match].side[sC.result], gStringVar1);
        if (sC.result == sC.side)
        {
            amount = Payout(sC.bet, sC.card[sC.match].mult[sC.side]);
            bp += amount;
            gSpecialVar_Result = 1;
        }
        else
        {
            gSpecialVar_Result = 0;
        }
    }
    gSaveBlock2Ptr->frontier.battlePoints = min(bp, MAX_BATTLE_FRONTIER_POINTS);
    ConvertIntToDecimalStringN(gStringVar2, amount, STR_CONV_MODE_LEFT_ALIGN, 4);
    ConvertIntToDecimalStringN(gStringVar3, gSaveBlock2Ptr->frontier.battlePoints, STR_CONV_MODE_LEFT_ALIGN, 4);
    sC.bet = 0;
    bets = VarGet(VAR_CASINO_BETS);
    if (bets < 9999)
        VarSet(VAR_CASINO_BETS, ++bets);
    sC.newUnlock = 0;
    for (m = 1; m < MODE_COUNT; m++)
        if (bets == sUnlockBets[m])
            sC.newUnlock = m;
    sC.cardValid = FALSE;   // na elke wedstrijd een nieuwe kaart
}

// VAR_RESULT = nieuwe modus vrijgespeeld; gStringVar1 = naam
void Casino_CheckUnlock(void)
{
    gSpecialVar_Result = (sC.newUnlock != 0);
    if (sC.newUnlock)
    {
        StringCopy(gStringVar1, sModeNames[sC.newUnlock]);
        sC.mode = sC.newUnlock;
    }
    sC.newUnlock = 0;
}

// Debug: alle modi vrij en minstens 500 BP
void Casino_DebugUnlockAll(void)
{
    VarSet(VAR_CASINO_BETS, sUnlockBets[MODE_COUNT - 1]);
    if (gSaveBlock2Ptr->frontier.battlePoints < 500)
        gSaveBlock2Ptr->frontier.battlePoints = 500;
}

// battle_main.c (BattleMainCB2): START tijdens het meekijken = direct naar de uitslag, getrokken uit de echte kans
bool32 Casino_TrySkipBattle(void)
{
    static const u8 sText_Skip[] = _("Skipping to the result…");

    if (!gCasinoBattle || !JOY_NEW(START_BUTTON) || gBattleOutcome != 0 || sC.skipped)
        return FALSE;
    sC.skipped = TRUE;
    gBattleOutcome = ((Random() % 1000) < sC.card[sC.match].chanceA) ? B_OUTCOME_WON : B_OUTCOME_LOST;
    BattlePutTextOnWindow(sText_Skip, B_WIN_MSG);
    return TRUE;
}

// Bookie met een tip over de huidige kaart. Zit er een verkeerd geprijsde wedstrijd op de kaart, dan wijst hij die
// meestal aan (de kant die echt favoriet is); anders gokt hij zelf maar wat. VAR_RESULT = 1 (tip), 0 (geen kaart).
// gStringVar1 = wedstrijdnummer, gStringVar2 = naam van de kant.
void Casino_GetTip(void)
{
    u32 i, pick = 0xFF, side;

    if (!IsModeUnlocked(sC.mode))
        sC.mode = MODE_WORLD_SINGLES;
    if (!sC.cardValid || sC.cardMode != sC.mode)
    {
        GenerateCard(sC.mode);
        sC.match = 0;
    }
    for (i = 0; i < CASINO_MATCHES; i++)
        if (sC.card[i].mispriced && sC.card[i].side[0].count)
            pick = i;
    if (pick != 0xFF && Random() % 4 != 0)
    {
        side = sC.card[pick].chanceA >= 500 ? 0 : 1;
    }
    else
    {
        pick = Random() % CASINO_MATCHES;
        side = Random() & 1;
    }
    if (sC.card[pick].side[side].count == 0)
    {
        gSpecialVar_Result = 0;
        return;
    }
    ConvertIntToDecimalStringN(gStringVar1, pick + 1, STR_CONV_MODE_LEFT_ALIGN, 1);
    GetSideName(&sC.card[pick].side[side], gStringVar2);
    gSpecialVar_Result = 1;
}
