# Raspberry Pi Employee Time Clock System

A complete employee time clock system built on a Raspberry Pi 4B with an I2C 20x4 LCD display and a 3x4 matrix keypad. Tracks employee clock in/out times across 14-day pay periods, calculates regular and overtime hours, generates formatted Excel timesheets, and automatically delivers them via Wi-Fi to a Windows 11 PC and by email.

## Features

- Live clock display on 20x4 LCD (12-hour format with date)
- 3x4 matrix keypad for secure 4-digit employee code entry
- Clock in / clock out for up to 30 employees
- 14-day pay period tracking (Saturday to Friday)
- Weekly overtime calculation (hours over 40 per week)
- Excel timesheet export — one tab per employee per pay period
- Automatic export every Friday at 11:59 PM
- Manual export via admin keypad code
- Wi-Fi file transfer to Windows 11 PC via SMB
- Email delivery of timesheet to multiple recipients (Gmail)
- JSON data storage — one file per pay period, never overwritten
- Auto-start on boot via systemd
- Auto-restart after crash or power outage (tested)
- Graceful shutdown on SIGTERM/SIGINT

## Hardware Requirements

| Part | Details |
|------|---------|
| Raspberry Pi 4B | Any RAM version (1GB, 2GB, 4GB, 8GB) |
| MicroSD Card | 16GB or larger, Class 10 or better |
| I2C LCD 20x4 | With PCF8574 I2C backpack — address 0x27 or 0x3F |
| 3x4 Matrix Keypad | 12-key connector style |
| Power Supply | Official Pi 4 USB-C 5V 3A |
| Jumper Wires | Female-to-Female |
| MicroSD Card Reader | To flash OS from your PC |

## Wiring

### LCD to Raspberry Pi (4 wires only)

| LCD Pin | Wire Color | Pi Physical Pin | Pi Function |
|---------|-----------|-----------------|-------------|
| VCC | Red | Pin 2 | 5V Power |
| GND | Black | Pin 6 | Ground |
| SDA | Yellow | Pin 3 | I2C Data |
| SCL | Green | Pin 5 | I2C Clock |

### Keypad to Raspberry Pi

Keypad connector pin order: **C2 R1 C1 R4 C3 R3 R2**

| Keypad Pin | Signal | Pi Physical Pin | BCM GPIO |
|:----------:|:------:|:---------------:|:--------:|
| 1 | NC | Not connected | — |
| 2 | R1 | Pin 12 | GPIO 18 |
| 3 | C1 | Pin 13 | GPIO 27 |
| 4 | R4 | Pin 16 | GPIO 23 |
| 5 | C3 | Pin 15 | GPIO 22 |
| 6 | R3 | Pin 18 | GPIO 24 |
| 7 | R2 | Pin 22 | GPIO 25 |
| 8 | C2 | Pin 11 | GPIO 17 |
| 9 | NC | Not connected | — |

**Note:** This keypad has a non-standard connector pin order. Columns 1 and 2 are physically swapped, which is corrected in the `KEYPAD_LAYOUT` in `config.py`. Always run `keytest.py` to verify your specific keypad before deploying.

## Installation

1. **Download Raspberry Pi Imager** from raspberrypi.com/software and install it on your PC.
2. **Flash Raspberry Pi OS 64-bit.** In the Imager: Choose Device → Raspberry Pi 4, Choose OS → Raspberry Pi OS (64-bit), Choose Storage → your SD card. Click Edit Settings and set: hostname=timeclock, username=timeclock, password=your choice, configure Wi‑Fi, timezone=your timezone, enable SSH with password auth. Click Write.
3. **First boot and SSH in.** Insert SD card, power on Pi, wait 60 seconds, then: `ssh timeclock@timeclock.local`
4. **Enable I2C.** Run `sudo raspi-config` → Interface Options → I2C → Yes → Finish. Then `sudo reboot` and SSH back in.
5. **Wire the hardware** with Pi powered OFF. See wiring tables above.
6. **Verify LCD is detected.** Run `sudo apt install -y i2c-tools` then `i2cdetect -y 1`. You should see `27` (or `3f`) in the grid.
7. **Install system packages:** `sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-pip python3-venv smbclient git`
8. **Create project folders:** `mkdir -p /home/timeclock/timeclock/data && mkdir -p /home/timeclock/timeclock/exports && cd /home/timeclock/timeclock`
9. **Create virtual environment:** `python3 -m venv venv && source venv/bin/activate`
10. **Install Python libraries:** `pip install RPi.GPIO RPLCD smbus2 openpyxl`
11. **Clone this repo or create the files:** `git clone https://github.com/dsisco79/Employee-Time-Tracking-Service.git .` or use `nano` to create each file manually.
12. **Edit config.py** with all your real values. See Configuration Reference below.
13. **Set up Gmail App Password.** Go to myaccount.google.com → Security → App Passwords → create one named “TimeClock” → copy the 16-character password into `EMAIL_APP_PASS` in `config.py`.
14. **Test manually:** `source venv/bin/activate && python timeclock.py` — verify LCD shows clock, keypad works, clock in/out works. Press Ctrl+C when done.
15. **Install the systemd service:** `sudo cp timeclock.service /etc/systemd/system/`
16. **Enable and start the service:** `sudo systemctl daemon-reload && sudo systemctl enable timeclock.service && sudo systemctl start timeclock.service`
17. **Add hardware group permissions:** `sudo usermod -a -G gpio,i2c,spi timeclock && sudo reboot`
18. **Test power outage recovery.** Confirm service is running, unplug the Pi, wait 30 seconds, plug back in. LCD should show the clock within ~35 seconds automatically.

## Configuration Reference

| Setting | Description | Example |
|---------|-------------|---------|
| LCD_I2C_ADDRESS | I2C address from i2cdetect | 0x27 or 0x3F |
| KEYPAD_ROW_PINS | BCM GPIO pins for keypad rows | [18, 25, 24, 23] |
| KEYPAD_COL_PINS | BCM GPIO pins for keypad columns | [17, 27, 22] |
| KEYPAD_LAYOUT | Character map matching physical keys | See config.py |
| DATA_DIR | Where JSON punch data is stored | /home/timeclock/timeclock/data |
| EXPORT_DIR | Where Excel files are saved | /home/timeclock/timeclock/exports |
| EXPORT_CODE | 4-digit admin keypad code to trigger manual export | 4 digits of your choice |
| SMB_SERVER | Windows PC IP address | 192.168.1.105 |
| SMB_SHARE | Windows shared folder name | TimeClock |
| SMB_USERNAME | Windows login username | YourUser |
| SMB_PASSWORD | Windows login password | YourPass |
| EMAIL_SENDER | Gmail address to send from | yourname@gmail.com |
| EMAIL_APP_PASS | 16-character Gmail App Password | xxxx xxxx xxxx xxxx |
| EMAIL_RECIPIENTS | List of email addresses to send to | Up to 30 |
| PAY_PERIOD_ANCHOR | A known Saturday date to anchor pay periods | 2026-01-03 |
| EMPLOYEES | Dict of employee codes, names, and IDs | See config.py |

## Employee Management

- **Add a new employee:** edit `config.py`, add a new entry to `EMPLOYEES`, then restart:
  - `sudo systemctl restart timeclock.service`
- **Remove an employee:** comment out their entry in `config.py` and restart. Historical data remains in `data/`.
- **Change a code:** update the employee’s code key in `config.py` and restart.

## Daily Usage

| Action | How |
|--------|-----|
| Clock in or out | Type 4-digit code + `#` |
| Clear a mistake | Press `*` |
| Trigger manual export | Type admin `EXPORT_CODE` + `#` |

## Useful Commands

| Task | Command |
|------|---------|
| Check service status | `sudo systemctl status timeclock.service` |
| View live log | `sudo journalctl -u timeclock.service -f` |
| View app log | `tail -f /home/timeclock/timeclock/timeclock.log` |
| Restart service | `sudo systemctl restart timeclock.service` |
| Stop service | `sudo systemctl stop timeclock.service` |
| Edit config | `nano /home/timeclock/timeclock/config.py` |
| After any config change | `sudo systemctl restart timeclock.service` |
| View punch data files | `ls /home/timeclock/timeclock/data/` |
| View exported Excel files | `ls /home/timeclock/timeclock/exports/` |
| Test keypad mapping | `python /home/timeclock/timeclock/keytest.py` |
| Check LCD I2C address | `i2cdetect -y 1` |

## Project Structure

```
.
├── timeclock.py          # Main application
├── config.py             # Configuration — fill in your values
├── keytest.py            # Keypad diagnostic utility
├── timeclock.service     # systemd auto-start service file
├── requirements.txt      # Python dependencies
├── .gitignore            # Excludes data, exports, logs, venv
└── README.md             # This file
```

## Security Notes

- Never commit your real `config.py` containing passwords, credentials, or employee names/codes.
- Add `data/`, `exports/`, and `*.log` to `.gitignore` (these contain sensitive employee data).
- Keep your real `config.py` only on the Pi.
- Consider making your repo private if you fork it for internal use.