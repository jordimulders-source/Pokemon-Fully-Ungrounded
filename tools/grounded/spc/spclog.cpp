// Speelt een SPC af en logt elke DSP-schrijfactie: "ms reg waarde" (stdout) + WAV van de mix (optioneel).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
static long g_ms = 0;
static FILE *g_log;
#define SPC_DSP_WRITE_HOOK(t, r, v) fprintf(g_log, "%ld %d %d\n", g_ms, (int)(r), (int)(v))
#include "Snes_Spc.cpp"
#include "Spc_Cpu.cpp"
#include "Spc_Dsp.cpp"
#include "Spc_Filter.cpp"
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "spclog in.spc seconden log.txt [uit.raw]\n"); return 1; }
    FILE *f = fopen(argv[1], "rb"); std::vector<char> d(70000); long n = fread(d.data(), 1, d.size(), f); fclose(f);
    g_log = fopen(argv[3], "w");
    Snes_Spc spc; spc.init(); if (spc.load_spc(d.data(), n)) { fprintf(stderr, "load faalt\n"); return 1; }
    spc.clear_echo();
    FILE *raw = argc > 4 ? fopen(argv[4], "wb") : 0;
    long total = atol(argv[2]) * 1000;
    short buf[64];
    for (g_ms = 0; g_ms < total; g_ms++) { spc.play(64, buf); if (raw) fwrite(buf, 2, 64, raw); }   // 32 stereo-samples = 1 ms
    fclose(g_log); if (raw) fclose(raw);
    return 0;
}
