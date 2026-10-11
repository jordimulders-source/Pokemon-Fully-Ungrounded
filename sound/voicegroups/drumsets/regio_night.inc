@ Project Grounded: drumkit voor regio_theme.py (nacht). Alleen stock-samples, geen PSG.
@ 36 kick, 37 rimsnare, 38 triangel, 39 bekken.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_night_drumset, 36
	voice_directsound 58, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 170
	voice_directsound 66, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 140
	voice_directsound 72, 84, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 150
	voice_directsound 54, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 120, 235, 0, 150
