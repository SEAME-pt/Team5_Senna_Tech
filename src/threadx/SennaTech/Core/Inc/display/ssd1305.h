#ifndef SSD1305_H
#define SSD1305_H

#include "utils.h"

#define SSD1305_WIDTH   128
#define SSD1305_HEIGHT  32
#define SSD1305_PAGES   4
#define SSD1305_BUF_SIZE (SSD1305_WIDTH * SSD1305_PAGES)

extern SPI_HandleTypeDef hspi3;

void ssd1305_init();
void ssd1305_clear(void);
void ssd1305_fill(uint8_t value);
void ssd1305_update(void);
void ssd1305_draw_pixel(uint8_t x, uint8_t y, uint8_t color);
void ssd1305_draw_line(uint8_t x, uint8_t y,
        uint8_t len, uint8_t color);
void ssd1305_fill_ellipse(uint8_t cx, uint8_t cy,
        uint8_t rx, uint8_t ry, uint8_t color);

// eye designs
void ssd1305_draw_happy_eyes(UINT frame);

void ssd1305_draw_cute_eyes(void);
void ssd1305_draw_half_closed_eyes(void);
void ssd1305_draw_closed_eyes(void);

void ssd1305_draw_sleep_face(UINT frame);

#endif
