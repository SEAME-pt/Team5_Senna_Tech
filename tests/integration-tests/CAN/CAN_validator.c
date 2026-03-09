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
#include <math.h>

#define TEST_DURATION_SEC 120
#define CAN_INTERFACE "can0"
#define CAN_BITRATE   500000.0
#define MAX_BUS_LOAD_ALLOWED 70.0
#define REQ_ID_BUS_LOAD "EXP-100"

typedef struct {
    canid_t id;
    char name[15];
    char req_id[10];
    int expected_ms;
    int tolerance_ms;
    
    long long last_seen;
    long long min_delta;
    long long max_delta;
    long long sum_delta;
    double sum_delta_sq;
    long count_samples;
} CanRule;

// Rule definitions based on hardware and user requirements
CanRule rules[] = {
    // ID,   NAME,         REQ ID,    EXP, TOL
    {0x010, "SPEED",      "EXP-101", 200,  20, 0, 0, 0, 9999, 0, 0, 0, 0},
    {0x100, "MOTOR_PWR",  "EXP-101", 200,  20, 0, 0, 0, 9999, 0, 0, 0, 0},
    {0x110, "STEER",      "EXP-101", 200,  20, 0, 0, 0, 9999, 0, 0, 0, 0},
    {0x005, "HEARTBEAT",  "EXP-102",  1000, 100, 0, 0, 0, 9999, 0, 0, 0, 0},
    {0x200, "BATTERY",    "EXP-102", 1000, 100, 0, 0, 0, 9999, 0, 0, 0, 0},
    {0x210, "TEMP",       "EXP-102", 1000, 100, 0, 0, 0, 9999, 0, 0, 0, 0}
};

#define NUM_RULES (sizeof(rules) / sizeof(rules[0]))

// Global Variables
int running = 1;
long long total_bits = 0;
long long start_test_time = 0;
FILE *logfile = NULL;

// Handle Ctrl+C to save logs
void sig_handler(int signo) { if (signo == SIGINT) running = 0; }

// Get timestamp in milliseconds
long long current_timestamp() {
    struct timespec te; 
    clock_gettime(CLOCK_MONOTONIC, &te);
    return te.tv_sec * 1000LL + te.tv_nsec / 1000000;
}

// Log to both console and file
#define NUM_RULES (sizeof(rules) / sizeof(rules[0]))

int running = 1;
long long total_bits = 0;
long long start_test_time = 0;
FILE *logfile = NULL;

void sig_handler(int signo) { if (signo == SIGINT) running = 0; }

long long current_timestamp() {
    struct timespec te; 
    clock_gettime(CLOCK_MONOTONIC, &te);
    return te.tv_sec * 1000LL + te.tv_nsec / 1000000;
}

void log_output(const char *format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
    if (logfile) {
        va_start(args, format);
        vfprintf(logfile, format, args);
        va_end(args);
        fflush(logfile);
    }
}

// Print final summary report
void print_summary_table(double bus_load) {
    log_output("\n"
               "========================================================================================\n"
               "                                CAN BUS PERFORMANCE REPORT                              \n"
               "========================================================================================\n");
    
    // Validação do Requisito de Carga de Barramento (EXP-100)
    char *bus_status = (bus_load <= MAX_BUS_LOAD_ALLOWED) ? "PASS" : "FAIL";
    log_output("| %-17s | %-8s | %-6s | %-37s | %-6s |\n", 
               "PARAMETER", "REQ ID", "TARGET", "", "STATUS");
    log_output("| %-11s: %4.2f%% | %-8s | <%-5.0f%% | %-37s | %-6s |\n", 
               "BUS LOAD", bus_load, "EXP-100", MAX_BUS_LOAD_ALLOWED, "", bus_status);
    
    log_output("|--------------|----------|--------|--------|--------|--------|---------|--------|\n");
    log_output("| %-12s | %-8s | %-6s | %-6s | %-6s | %-6s | %-7s | %-6s |\n", 
               "MESSAGE", "REQ ID", "TARGET", "AVG", "MIN", "MAX", "JITTER", "STATUS");
    log_output("|--------------|----------|--------|--------|--------|--------|---------|--------|\n");

    for (int i = 0; i < NUM_RULES; i++) {
        double avg = 0, jitter = 0;
        char *status = "FAIL";

        if (rules[i].count_samples > 1) {
            avg = (double)rules[i].sum_delta / rules[i].count_samples;
            double variance = (rules[i].sum_delta_sq / rules[i].count_samples) - (avg * avg);
            jitter = sqrt(variance < 0 ? 0 : variance);
            
            if (avg >= (rules[i].expected_ms - rules[i].tolerance_ms) && 
                avg <= (rules[i].expected_ms + rules[i].tolerance_ms)) {
                status = "PASS";
            }
        } else if (rules[i].count_samples == 0) {
            status = "STALE";
        }

        log_output("| %-12s | %-8s | %4dms | %6.1f | %4lldms | %4lldms | %6.2f  | %-6s |\n",
            rules[i].name, rules[i].req_id, rules[i].expected_ms, avg,
            rules[i].min_delta == 9999 ? 0 : rules[i].min_delta,
            rules[i].max_delta, jitter, status);
    }
    log_output("========================================================================================\n");
}

int main() {
    signal(SIGINT, sig_handler);
    int s; struct sockaddr_can addr; struct ifreq ifr; struct can_frame frame;
    char filename[100];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    
    strftime(filename, sizeof(filename), "evidence_%Y-%m-%d_%H-%M-%S.txt", t);
    printf("--> Log File: %s\n", filename);
    logfile = fopen(filename, "w");
    
    if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) return 1;

    strcpy(ifr.ifr_name, CAN_INTERFACE);
    ioctl(s, SIOCGIFINDEX, &ifr);
    addr.can_family = AF_CAN; 
    addr.can_ifindex = ifr.ifr_ifindex;
    bind(s, (struct sockaddr *)&addr, sizeof(addr));

    start_test_time = current_timestamp();
    log_output("Starting Validation...\n");

    while (running) {
        if ((current_timestamp() - start_test_time) > (TEST_DURATION_SEC * 1000)) break;

        struct timeval tv = {0, 50000};
        fd_set fds; FD_ZERO(&fds); FD_SET(s, &fds);
        if (select(s + 1, &fds, NULL, NULL, &tv) <= 0) continue;

        if (read(s, &frame, sizeof(struct can_frame)) < 0) break;

        long long current_time = current_timestamp();
        total_bits += (47 + (frame.can_dlc * 8));

        for (int i = 0; i < NUM_RULES; i++) {
            if (frame.can_id == rules[i].id) {
                if (rules[i].last_seen != 0) {
                    long long delta = current_time - rules[i].last_seen;
                    if (delta < rules[i].min_delta) rules[i].min_delta = delta;
                    if (delta > rules[i].max_delta) rules[i].max_delta = delta;
                    rules[i].sum_delta += delta;
                    rules[i].sum_delta_sq += (double)delta * delta;
                    rules[i].count_samples++;
                }
                rules[i].last_seen = current_time;
                break;
            }
        }
    }

    double duration_sec = (current_timestamp() - start_test_time) / 1000.0;
    double bus_load = (total_bits / (duration_sec * CAN_BITRATE)) * 100.0;
    
    print_summary_table(bus_load);

    if (logfile) fclose(logfile);
    close(s);
    return 0;
}