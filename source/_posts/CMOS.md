---
title: CMOS
date: 2021-01-21 19:21:47
tags: OS
---

## CMOS

"CMOS" is a tiny bit of very low power static memory that lives on the same chip as the Real-Time Clock (RTC). 

CMOS 只能从端口0x70和0x71访问

CMOS的作用是在计算机关机时为BIOS保存50 (or 114) bytes of "Setup" information ，因为它有一个单独的电池。

CMOS 值一次访问一个字节，每个字节可以单独寻址。

每个CMOS地址被称为一个寄存器

<!--More-->

The first 14 CMOS registers access and control the Real-Time Clock,其他的没用。

## Non-Maskable Interrupts

不可屏蔽的中断

NMI is meant to communicate a "panic" status from the hardware to the CPU in a way that the CPU cannot ignore. It is typically used to signal memory errors.

每当向IO端口0x70发送一个字节, the high order bit tells the hardware whether to disable NMIs from reaching the CPU.

 If the bit is on, NMI is disabled (until the next time you send a byte to Port 0x70). The low order 7 bits of any byte sent to Port 0x70 are used to address CMOS registers.

## CMOS Registers

### Accessing CMOS Registers

you "select" a CMOS register (for reading or writing) by sending the register number to IO Port 0x70. Since the 0x80 bit of Port 0x70 controls NMI, you always end up setting that, too. So your CMOS controller always needs to know whether your OS wants NMI to be enabled or not. Selecting a CMOS register is done as follows:

```c
outb (0x70, (NMI_disable_bit << 7) | (selected CMOS register number));
```



Once a register is selected, you either read the value of that register on Port 0x71 (with inb or an equivalent function), or you write a new value to that register -- also on Port 0x71 (with outb, for example):

```c
val_8bit = inb (0x71);
```

*  Reading or writing Port 0x71 seems to default the "selected register" back to 0xD. So you need to **reselect** the register every single time you want to access a CMOS register.

## RTC Update In Progress

RTC电路慢，时间的更新有延迟，如果在RTC更新期间读取时间和日期，会得到不正确的值。

设置了一个"Update in progress" flag在0x0A寄存器。

* The first alternative is to rely on the "update interrupt". When the RTC finishes an update it generates an "update interrupt" (if it's enabled), and the IRQ handler can safely read the time and date registers without worrying about the update at all (and without checking the "Update in progress" flag); as long as the IRQ handler doesn't take almost a full second to do it. In this case you're not wasting up to 1 second of CPU time waiting/polling, but it may still take a full second before the time and date has been read. Despite this it can be a useful technique during OS boot - e.g. setup the "update interrupt" and its IRQ handler as early as you can and then do other things (e.g. loading files from disk), in the hope that the IRQ occurs before you need the time and date.
* The second alternative is to be prepared for dodgy/inconsistent values and cope with them if they occur. To do this, make sure the "Update in progress" flag is clear (e.g. "*while(update_in_progress_flag != clear)*") then read all the time and date registers; then make sure the "Update in progress" flag is clear again (e.g. "*while(update_in_progress_flag != clear)*") and read all the time and date registers again. If the values that were read the first time are the same as the value that were read the second time then the values must be correct. If any of the values are different you need to do it again, and keep doing it again until the newest values are the same as the previous values.

```c
#define CURRENT_YEAR        2020                            // Change this each year!
 
int century_register = 0x00;                                // Set by ACPI table parsing code if possible
 
unsigned char second;
unsigned char minute;
unsigned char hour;
unsigned char day;
unsigned char month;
unsigned int year;
 
void out_byte(int port, int value);
int in_byte(int port);
 
enum {
      cmos_address = 0x70,
      cmos_data    = 0x71
};
 
int get_update_in_progress_flag() {
      out_byte(cmos_address, 0x0A);
      return (in_byte(cmos_data) & 0x80);
}
 
unsigned char get_RTC_register(int reg) {
      out_byte(cmos_address, reg);
      return in_byte(cmos_data);
}
 
void read_rtc() {
      unsigned char century;
      unsigned char last_second;
      unsigned char last_minute;
      unsigned char last_hour;
      unsigned char last_day;
      unsigned char last_month;
      unsigned char last_year;
      unsigned char last_century;
      unsigned char registerB;
 
      // Note: This uses the "read registers until you get the same values twice in a row" technique
      //       to avoid getting dodgy/inconsistent values due to RTC updates
 
      while (get_update_in_progress_flag());                // Make sure an update isn't in progress
      second = get_RTC_register(0x00);
      minute = get_RTC_register(0x02);
      hour = get_RTC_register(0x04);
      day = get_RTC_register(0x07);
      month = get_RTC_register(0x08);
      year = get_RTC_register(0x09);
      if(century_register != 0) {
            century = get_RTC_register(century_register);
      }
 
      do {
            last_second = second;
            last_minute = minute;
            last_hour = hour;
            last_day = day;
            last_month = month;
            last_year = year;
            last_century = century;
 
            while (get_update_in_progress_flag());           // Make sure an update isn't in progress
            second = get_RTC_register(0x00);
            minute = get_RTC_register(0x02);
            hour = get_RTC_register(0x04);
            day = get_RTC_register(0x07);
            month = get_RTC_register(0x08);
            year = get_RTC_register(0x09);
            if(century_register != 0) {
                  century = get_RTC_register(century_register);
            }
      } while( (last_second != second) || (last_minute != minute) || (last_hour != hour) ||
               (last_day != day) || (last_month != month) || (last_year != year) ||
               (last_century != century) );
 
      registerB = get_RTC_register(0x0B);
 
      // Convert BCD to binary values if necessary
 
      if (!(registerB & 0x04)) {
            second = (second & 0x0F) + ((second / 16) * 10);
            minute = (minute & 0x0F) + ((minute / 16) * 10);
            hour = ( (hour & 0x0F) + (((hour & 0x70) / 16) * 10) ) | (hour & 0x80);
            day = (day & 0x0F) + ((day / 16) * 10);
            month = (month & 0x0F) + ((month / 16) * 10);
            year = (year & 0x0F) + ((year / 16) * 10);
            if(century_register != 0) {
                  century = (century & 0x0F) + ((century / 16) * 10);
            }
      }
 
      // Convert 12 hour clock to 24 hour clock if necessary
 
      if (!(registerB & 0x02) && (hour & 0x80)) {
            hour = ((hour & 0x7F) + 12) % 24;
      }
 
      // Calculate the full (4-digit) year
 
      if(century_register != 0) {
            year += century * 100;
      } else {
            year += (CURRENT_YEAR / 100) * 100;
            if(year < CURRENT_YEAR) year += 100;
      }
}
```



