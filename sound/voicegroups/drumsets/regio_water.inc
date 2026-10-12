@ Project Grounded: drumkit voor regio_theme.py (water). Alleen stock-samples, geen PSG.
@ 36 kick, 37 rimsnare, 38 splash, 39 conga laag, 40 conga hoog, 41 conga open, 42 belletjes, 43 triangel, 44 crash.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_water_drumset, 36
	voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 66, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 150
	voice_directsound 70, 70, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 225, 0, 150
	voice_directsound 57, 52, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160
	voice_directsound 62, 76, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 140
	voice_directsound 65, 76, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_bubbles, 255, 0, 255, 170
	voice_directsound 74, 84, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 150
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
