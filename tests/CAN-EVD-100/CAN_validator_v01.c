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
#include <signal.h>

// --- TEST CONFIGURATION ---
#define TEST_DURATION_SEC 120
#define LOG_FILE_PATH "evidence_log.txt"
#define CAN_INTERFACE "can0"
#define CAN_BITRATE   500000.0 // 500kbps

// IDs for Event-Driven Latency (Request/Response)
#define ID_REQ_ESTOP  0x001    
#define ID_ACK_ESTOP  0x002    

// Enriched structure with statistics
typedef struct {
    canid_t id;
    char name[20];
    char req_id[10];
    int expected_ms;
    int tolerance_ms;
    
    // Execution control
    long long last_seen;
    int consecutive_samples;
    int req_passed;
    
    // Statistics for Evidence
    long long min_delta;
    long long max_delta;
    long long sum_delta;
    long count_samples;
} CanRule;

CanRule rules[] = {
    //ID, NAME, REQ_ID, EXP_MS, TOL_MS, LAST_SEEN, CONSEC_SAMPS, REQ_PASSED, MIN_DELTA, MAX_DELTA, SUM_DELTA, COUNT_SAMPLES
    // EXP-101: Fast Messages (50ms)
    {0x010, "SPEED",     "EXP-101", 50,   10, 0, 0, 0, 9999, 0, 0, 0},
    {0x100, "MOTOR_PWR", "EXP-101", 50,   10, 0, 0, 0, 9999, 0, 0, 0},
    {0x110, "STEER",     "EXP-101", 50,   10, 0, 0, 0, 9999, 0, 0, 0},
    
    // EXP-102: Slow Messages (1000ms)
    {0x200, "BATTERY",   "EXP-102", 1000, 100, 0, 0, 0, 9999, 0, 0, 0},
    {0x210, "TEMP",      "EXP-102", 1000, 100, 0, 0, 0, 9999, 0, 0, 0}

    // SG-CAN-01: Heartbeat Message (not implemented in yet)
    {0x005, "HEARTBEAT", "SG-01",  100,   20, 0, 0, 0, 9999, 0, 0, 0}, 
};

#define NUM_RULES (sizeof(rules) / sizeof(rules[0]))

// Global Variables
int running = 1;
long long latency_req_time = 0;
long long total_bits = 0;
long long start_test_time = 0;
FILE *logfile = NULL;

// --- AUXILIARY FUNCTIONS ---

// Capture Ctrl+C to close the log correctly
void sig_handler(int signo) {
    if (signo == SIGINT) running = 0;
}

long long current_timestamp() {
    struct timespec te; 
    clock_gettime(CLOCK_MONOTONIC, &te);
    return te.tv_sec * 1000LL + te.tv_nsec / 1000000;
}

void log_output(const char *format, ...) {
    va_list args;
    
    // Print to Console
    va_start(args, format);
    vprintf(format, args);
    va_end(args);

    // Print to File
    if (logfile != NULL) {
        va_start(args, format);
        vfprintf(logfile, format, args);
        va_end(args);
        fflush(logfile); 
    }
}

long read_sys_errors(const char* iface) {
    char path[100];
    sprintf(path, "/sys/class/net/%s/statistics/rx_errors", iface);
    FILE *f = fopen(path, "r");
    long errors = 0;
    if (f) {
        fscanf(f, "%ld", &errors);
        fclose(f);
    }
    return errors;
}

void print_summary_table() {
    log_output("\n===================================================================\n");
    log_output("                       DETAILED STATISTICS                         \n");
    log_output("===================================================================\n");
    log_output("| %-10s | %-8s | %-6s | %-6s | %-6s | %-6s |\n", 
               "NAME", "REQ", "EXP", "AVG", "MIN", "MAX");
    log_output("|------------|----------|--------|--------|--------|--------|\n");

    for (int i = 0; i < NUM_RULES; i++) {
        double avg = 0;
        if (rules[i].count_samples > 0) 
            avg = (double)rules[i].sum_delta / rules[i].count_samples;

        log_output("| %-10s | %-8s | %4dms | %6.1f | %4lldms | %4lldms |\n",
            rules[i].name,
            rules[i].req_id,
            rules[i].expected_ms,
            avg,
            rules[i].min_delta == 9999 ? 0 : rules[i].min_delta,
            rules[i].max_delta
        );
    }
    log_output("===================================================================\n");
}

int main() {
    signal(SIGINT, sig_handler); // Allow exit with Ctrl+C saving the log

    int s;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;
    long long current_time, delta;

    char filename[100];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    
    // Format: evidence_YYYY-MM-DD_HH-MM-SS.txt
    strftime(filename, sizeof(filename), "evidence_%Y-%m-%d_%H-%M-%S.txt", t);
    
    printf("--> Log File Created: %s\n", filename);
    logfile = fopen(filename, "w");
    
    if (!logfile) { 
        perror("Error creating log file"); 
        return 1; 
    }

    start_test_time = current_timestamp();
    long initial_errors = read_sys_errors(CAN_INTERFACE);

    if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) { perror("Socket"); return 1; }
    strcpy(ifr.ifr_name, CAN_INTERFACE);
    ioctl(s, SIOCGIFINDEX, &ifr);
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) { perror("Bind"); return 1; }

    // Evidence Log Header
    time_t rawtime;
    time(&rawtime);
    log_output("TEST EXECUTION REPORT\n");
    log_output("Date: %s", ctime(&rawtime));
    log_output("Interface: %s\n", CAN_INTERFACE);
    log_output("Duration Target: %d sec\n", TEST_DURATION_SEC);
    log_output("----------------------------------------------------------\n");

    while (running) {
        if ((current_timestamp() - start_test_time) > (TEST_DURATION_SEC * 1000)) break;

        struct timeval tv = {0, 10000}; 
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(s, &fds);
        if (select(s + 1, &fds, NULL, NULL, &tv) <= 0) continue;

        if (read(s, &frame, sizeof(struct can_frame)) < 0) break;

        current_time = current_timestamp();
        total_bits += (47 + (frame.can_dlc * 8));

        // --- EXP-103: REQ/RESP LATENCY (Asynchronous) ---
        if (frame.can_id == ID_REQ_ESTOP) {
            latency_req_time = current_time;
        }
        else if (frame.can_id == ID_ACK_ESTOP) {
            if (latency_req_time != 0) {
                long long lat = current_time - latency_req_time;
                if (lat < 20) {
                    log_output("[PASS] EXP-103 (ESTOP_LATENCY) | Actual: %lld ms | Limit: 20 ms\n", lat);
                } else {
                    log_output("[FAIL] EXP-103 (ESTOP_LATENCY) | Actual: %lld ms | Limit: 20 ms\n", lat);
                }
                latency_req_time = 0; // Reset
            }
        }

        // --- EXP-101 and EXP-102: CYCLIC (Complete Statistics) ---
        for (int i = 0; i < NUM_RULES; i++) {
            if (frame.can_id == rules[i].id) {
                if (rules[i].last_seen != 0) {
                    delta = current_time - rules[i].last_seen;

                    // Statistical Collection
                    if (delta < rules[i].min_delta) rules[i].min_delta = delta;
                    if (delta > rules[i].max_delta) rules[i].max_delta = delta;
                    rules[i].sum_delta += delta;
                    rules[i].count_samples++;

                    // Requirement Validation (Moving Window)
                    int min = rules[i].expected_ms - rules[i].tolerance_ms;
                    int max = rules[i].expected_ms + rules[i].tolerance_ms;

                    if (delta >= min && delta <= max) {
                        rules[i].consecutive_samples++;
                    } else {
                        rules[i].consecutive_samples = 0; 
                    }

                    // Requirement Approval (Log once, but continue collecting stats)
                    if (rules[i].consecutive_samples >= 100 && rules[i].req_passed == 0) {
                        double current_avg = (double)rules[i].sum_delta / rules[i].count_samples;
                        log_output("[PASS] %s (%s) | Stable for 100 cycles | Current Avg: %.1f ms\n", 
                                   rules[i].req_id, rules[i].name, current_avg);
                        rules[i].req_passed = 1;
                    }
                }
                rules[i].last_seen = current_time;
                break;
            }
        }
    }

    // --- EXP-100: NETWORK AND LOAD ---
    long final_errors = read_sys_errors(CAN_INTERFACE);
    long total_errors = final_errors - initial_errors;
    double duration_sec = (current_timestamp() - start_test_time) / 1000.0;
    double bus_load_percent = (total_bits / (duration_sec * CAN_BITRATE)) * 100.0;

    log_output("\n--- FINAL METRICS ---\n");
    
    if (total_errors == 0 && bus_load_percent < 70.0) {
        log_output("[PASS] EXP-100 (INTEGRITY) | Errors: %ld | Load: %.2f%% | Duration: %.1fs\n", 
                   total_errors, bus_load_percent, duration_sec);
    } else {
        log_output("[FAIL] EXP-100 (INTEGRITY) | Errors: %ld | Load: %.2f%% | Threshold: 70%%\n", 
                   total_errors, bus_load_percent);
    }

    // Print the detailed table at the end
    print_summary_table();

    if (logfile) fclose(logfile);
    close(s);
    return 0;
}