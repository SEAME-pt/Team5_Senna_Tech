#include "sensors/microphone.h"

#define MICROPHONE_BLOCK_SAMPLES 160U
#define MICROPHONE_DEBUG_PERIOD_MS 1000U

extern MDF_HandleTypeDef AdfHandle0;
extern MDF_FilterConfigTypeDef AdfFilterConfig0;

static int16_t microphone_raw_to_pcm16(int32_t raw)
{
	int32_t shifted;
	ULONG abs_raw;

	abs_raw = (raw < 0) ? (ULONG)(-raw) : (ULONG)raw;
	if (abs_raw <= 32767)
		shifted = raw;
	else
		shifted = raw >> 8;
	if (shifted > 32767)
		shifted = 32767;
	else if (shifted < -32768)
		shifted = -32768;

	return (int16_t)shifted;
}

static float microphone_absf(float v)
{
	return (v < 0.0f) ? -v : v;
}

void Microphone_DefaultConfig(MicrophoneConfig_t *cfg)
{
	if (cfg == (void *)0)
		return ;

	cfg->noise_alpha = 0.98f;
	cfg->dc_alpha = 0.995f;
	cfg->threshold_factor = 2.2f;
	cfg->min_peak = 700.0f;
	cfg->min_rms = 120.0f;
	cfg->refractory_ms = 90U;
	cfg->warmup_blocks = 4U;
	cfg->rearm_ratio = 0.6f;
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
	state->processed_blocks = 0U;
	state->initialized = true;
	state->armed = true;
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

	if (state->noise_floor < state->cfg.min_rms)
		state->noise_floor = state->cfg.min_rms;

	dynamic_threshold = state->noise_floor * state->cfg.threshold_factor;
	if (dynamic_threshold < state->cfg.min_peak)
		dynamic_threshold = state->cfg.min_peak;

	state->last_peak_abs  = peak_abs;
	state->last_avg_abs   = avg_abs;
	state->last_threshold = dynamic_threshold;

	if (state->processed_blocks < state->cfg.warmup_blocks) {
		state->processed_blocks++;
		return false;
	}

	if (!state->armed) {
		/* ainda em cooldown: só volta a armar quando o som sossegar */
		if (peak_abs < (dynamic_threshold * state->cfg.rearm_ratio))
			state->armed = true;
		return false;
	}

	if ((now_ms - state->last_clap_ms) < state->cfg.refractory_ms)
		return false;

	if (peak_abs >= dynamic_threshold && avg_abs >= state->cfg.min_rms) {
		state->last_clap_ms = now_ms;
		state->armed = false;
		uart_send("Clap detected!\r\n");
		return true;
	}

	return false;
}

void Microphone_PrintDebug(const MicrophoneState_t *state)
{
	if (state == (void *)0 || !state->initialized)
		return ;

	uart_send("peak=");
	uart_send_int((ULONG)state->last_peak_abs);
	uart_send(" avg=");
	uart_send_int((ULONG)state->last_avg_abs);
	uart_send(" floor=");
	uart_send_int((ULONG)state->noise_floor);
	uart_send(" thr=");
	uart_send_int((ULONG)state->last_threshold);
	uart_send("\r\n");
}

void microphone_thread_entry(ULONG thread_input)
{
	MicrophoneState_t mic_state;
	MicrophoneConfig_t mic_cfg;
	int16_t sample_block[MICROPHONE_BLOCK_SAMPLES];
	ULONG sample_index = 0U;
	int32_t raw_sample = 0;
	int16_t pcm_sample;
	HAL_StatusTypeDef status;

	CAN_Frame frame;
	frame.id = CAN_ID_MODE_MOVEMENT;
	frame.data[0] = 0;

	(void)thread_input;

	Microphone_DefaultConfig(&mic_cfg);
	Microphone_Init(&mic_state, &mic_cfg);

	uart_send("Microphone thread started\r\n");

	status = HAL_MDF_AcqStart(&AdfHandle0, &AdfFilterConfig0);
	if (status != HAL_OK) {
		uart_send("ADF acquisition start failed\r\n");
		while (1) {
			tx_thread_sleep(100);
		}
	}
	uart_send("ADF acquisition started\r\n");

	while (1) {
		status = HAL_MDF_PollForAcq(&AdfHandle0, 0U);
		if (status == HAL_OK) {
			if (HAL_MDF_GetAcqValue(&AdfHandle0, &raw_sample) == HAL_OK) {
				if (raw_sample != (int32_t)0x80000000) {
					pcm_sample = microphone_raw_to_pcm16(raw_sample);
					sample_block[sample_index++] = pcm_sample;

					if (sample_index >= MICROPHONE_BLOCK_SAMPLES) {
						if (Microphone_ProcessBlock(&mic_state,
											sample_block,
											MICROPHONE_BLOCK_SAMPLES,
											HAL_GetTick())) {
							if (tx_queue_send(&g_rx_data_queue, &frame, TX_NO_WAIT) != TX_SUCCESS)
								uart_send("Failed to send clap detection frame, probably full :(\r\n");
						}
						sample_index = 0U;
					}
				}
			}
		} else {
			tx_thread_sleep(5);
		}
	}
}
