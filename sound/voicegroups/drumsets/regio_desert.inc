@ Project Grounded: drumkit voor regio_theme.py (woestijn). Alleen stock-samples, geen PSG.
@ 36 dum, 37 tek, 38 ka, 39 riq, 40 lijsttrom, 41 zill, 42 taiko, 43 crash.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_desert_drumset, 36
	voice_directsound 52, 64, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160
	voice_directsound 64, 64, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 140
	voice_directsound 69, 60, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 140
	voice_directsound 60, 72, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 160
	voice_directsound 56, 64, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 170
	voice_directsound 72, 80, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 160
	voice_directsound 52, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 165
