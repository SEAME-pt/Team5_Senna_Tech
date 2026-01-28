#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <time.h>
#include <stdarg.h>

// --- TEST CONFIGURATION ---
#define TEST_DURATION_SEC 120  // 2 minutes
#define LOG_FILE_PATH "evidence_log.txt"

// IDs for Latency (EXP-103) [not configured yet]
#define ID_REQ_ESTOP  0x001    
#define ID_ACK_ESTOP  0x002    

// Updated structure with Requirement ID (EXP-XXX)
typedef struct {
    canid_t id;
    char name[20];
    char req_id[10];//EXP-XXX
    int expected_ms;
    int tolerance_ms;
    long long last_seen;
    int consecutive_samples;
    int req_passed;      
} CanRule;

CanRule rules[] = {
    // EXP-101: Fast Messages (50ms)
    {0x010, "SPEED",     "EXP-101", 50,   10, 0, 0, 0},
    {0x100, "MOTOR_PWR", "EXP-101", 50,   10, 0, 0, 0},
    {0x110, "STEER",     "EXP-101", 50,   10, 0, 0, 0},
    
    // EXP-102: Slow Messages (1000ms)
    {0x200, "BATTERY",   "EXP-102", 1000, 100, 0, 0, 0},
    {0x210, "TEMP",      "EXP-102", 1000, 100, 0, 0, 0}
};

#define NUM_RULES (sizeof(rules) / sizeof(rules[0]))

// Global Variables
long long latency_req_time = 0;
long long total_bits = 0;
long long start_test_time = 0;
int exp103_passed = 0; // Control to log EXP-103 only once

// --- AUXILIARY FUNCTIONS ---
long long current_timestamp() {
    struct timespec te; 
    clock_gettime(CLOCK_MONOTONIC, &te);
    return te.tv_sec * 1000LL + te.tv_nsec / 1000000;
}

void log_output(FILE *fp, const char *format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
    if (fp != NULL) {
        va_start(args, format);
        vfprintf(fp, format, args);
        va_end(args);
        fflush(fp); 
    }
}

long read_sys_errors() {
    FILE *f = fopen("/sys/class/net/can0/statistics/rx_errors", "r");
    long errors = 0;
    if (f) {
        fscanf(f, "%ld", &errors);
        fclose(f);
    }
    return errors;
}

int main() {
    int s;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;
    long long current_time, delta;
    FILE *logfile = fopen(LOG_FILE_PATH, "w");

    start_test_time = current_timestamp();
    long initial_errors = read_sys_errors();

    if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) return 1;
    strcpy(ifr.ifr_name, "can0");
    ioctl(s, SIOCGIFINDEX, &ifr);
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) return 1;

    log_output(logfile, "--- EXP VALIDATION (%ds) ---\n", TEST_DURATION_SEC);

    while (1) {
        if ((current_timestamp() - start_test_time) > (TEST_DURATION_SEC * 1000)) break;

        struct timeval tv = {0, 10000}; 
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(s, &fds);
        if (select(s + 1, &fds, NULL, NULL, &tv) <= 0) continue;

        if (read(s, &frame, sizeof(struct can_frame)) < 0) break;

        current_time = current_timestamp();
        total_bits += (47 + (frame.can_dlc * 8));

        // --- EXP-103: LATENCY (Software Check) ---
        if (frame.can_id == ID_REQ_ESTOP) latency_req_time = current_time;
        else if (frame.can_id == ID_ACK_ESTOP) {
            if (latency_req_time != 0) {
                long long lat = current_time - latency_req_time;
                if (lat < 20) {
                    // Log only if not yet passed
                    if (!exp103_passed) {
                         log_output(logfile, "[PASS] EXP-103 (LATENCY) | %lld ms\n", lat);
                         exp103_passed = 1;
                    }
                } else {
                    log_output(logfile, "[FAIL] EXP-103 (LATENCY) | %lld ms\n", lat);
                }
                latency_req_time = 0;
            }
        }

        // --- EXP-101 and EXP-102: CYCLES ---
        for (int i = 0; i < NUM_RULES; i++) {
            if (frame.can_id == rules[i].id) {
                if (rules[i].last_seen != 0) {
                    delta = current_time - rules[i].last_seen;
                    int min = rules[i].expected_ms - rules[i].tolerance_ms;
                    int max = rules[i].expected_ms + rules[i].tolerance_ms;

                    if (delta >= min && delta <= max) {
                        rules[i].consecutive_samples++;
                    } else {
                        rules[i].consecutive_samples = 0; 
                    }

                    if (rules[i].consecutive_samples >= 100 && rules[i].req_passed == 0) {
                        // GENERATE LOG IN CORRECT FORMAT FOR VALIDATOR
                        log_output(logfile, "[PASS] %s (%s)\n", rules[i].req_id, rules[i].name);
                        rules[i].req_passed = 1;
                    }
                }
                rules[i].last_seen = current_time;
                break;
            }
        }
    }

    // --- EXP-100: NETWORK AND LOAD ---
    long final_errors = read_sys_errors();
    long total_errors = final_errors - initial_errors;
    double duration_sec = (current_timestamp() - start_test_time) / 1000.0;
    double bus_load_percent = (total_bits / (duration_sec * 500000.0)) * 100.0;

    log_output(logfile, "\n--- FINAL RESULT ---\n");
    
    // Validate Error and Load together for EXP-100
    if (total_errors == 0 && bus_load_percent < 70.0) {
        log_output(logfile, "[PASS] EXP-100 (INTEGRITY)\n");
        log_output(logfile, "       - Errors: %ld\n", total_errors);
        log_output(logfile, "       - Load: %.2f%%\n", bus_load_percent);
    } else {
        log_output(logfile, "[FAIL] EXP-100 (INTEGRITY)\n");
    }

    fclose(logfile);
    close(s);
    return 0;
}