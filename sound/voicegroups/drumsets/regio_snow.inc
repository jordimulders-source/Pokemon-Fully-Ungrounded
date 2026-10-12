@ Project Grounded: drumkit voor regio_theme.py (sneeuw). Alleen stock-samples, geen PSG.
@ 36 kick, 37 rimsnare, 38 sleebelletjes, 39 triangel.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_snow_drumset, 36
	voice_directsound 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 170
	voice_directsound 68, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 140
	voice_directsound 60, 80, DirectSoundWaveData_sc88pro_jingle_bell, 255, 0, 255, 150
	voice_directsound 74, 44, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 160
