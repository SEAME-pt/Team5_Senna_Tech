#include "sensors/microphone.h"

static float microphone_absf(float v)
{
	return (v < 0.0f) ? -v : v;
}

void Microphone_DefaultConfig(MicrophoneConfig_t *cfg)
{
	if (cfg == (void *)0) {
		return;
	}

	cfg->noise_alpha = 0.98f;
	cfg->dc_alpha = 0.995f;
	cfg->threshold_factor = 4.0f;
	cfg->min_peak = 1800.0f;
	cfg->min_rms = 350.0f;
	cfg->refractory_ms = 180U;
}

void Microphone_Init(MicrophoneState_t *state, const MicrophoneConfig_t *cfg)
{
	MicrophoneConfig_t local_cfg;

	if (state == (void *)0)
		return ;

	if (cfg == (void *)0) {
		Microphone_DefaultConfig(&local_cfg);
		state->cfg = local_cfg;
	} else
		state->cfg = *cfg;

	state->noise_floor = state->cfg.min_rms;
	state->dc_estimate = 0.0f;
	state->last_clap_ms = 0U;
	state->initialized = true;
}

bool Microphone_ProcessBlock(MicrophoneState_t *state,
							const int16_t *samples,
							size_t sample_count,
							ULONG now_ms)
{
	float sum_abs = 0.0f;
	float peak_abs = 0.0f;
	float avg_abs;
	float dynamic_threshold;
	float x;
	float hp;
	size_t i;

	if (state == (void *)0 || samples == (void *)0 || sample_count == 0U || !state->initialized)
		return false;

	for (i = 0U; i < sample_count; i++) {
		x = (float)samples[i];

		state->dc_estimate = (state->cfg.dc_alpha * state->dc_estimate) +
							 ((1.0f - state->cfg.dc_alpha) * x);
		hp = x - state->dc_estimate;

		hp = microphone_absf(hp);
		sum_abs += hp;

		if (hp > peak_abs)
			peak_abs = hp;
	}

	avg_abs = sum_abs / (float)sample_count;

	state->noise_floor = (state->cfg.noise_alpha * state->noise_floor) +
						 ((1.0f - state->cfg.noise_alpha) * avg_abs);

	dynamic_threshold = state->noise_floor * state->cfg.threshold_factor;
	if (dynamic_threshold < state->cfg.min_peak)
		dynamic_threshold = state->cfg.min_peak;

	if ((now_ms - state->last_clap_ms) < state->cfg.refractory_ms)
		return false;

	if (peak_abs >= dynamic_threshold && avg_abs >= state->cfg.min_rms) {
		state->last_clap_ms = now_ms;
		uart_send("Clap detected!\r\n");
		return true;
	}

	return false;
}

void microphone_thread_entry(ULONG thread_input)
{
	MicrophoneState_t mic_state;
	MicrophoneConfig_t mic_cfg;

	(void)thread_input;

	Microphone_DefaultConfig(&mic_cfg);
	Microphone_Init(&mic_state, &mic_cfg);

	uart_send("Microphone thread started\r\n");

	while (1) {
		/*
		 * TODO: integrate real audio capture (PCM) and call
		 * Microphone_ProcessBlock(&mic_state, samples, sample_count, HAL_GetTick()).
		 */
		tx_thread_sleep(10);
	}
}
