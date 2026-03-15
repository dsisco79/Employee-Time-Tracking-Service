# ============================================================
#  TIMECLOCK CONFIGURATION FILE (SCRUBBED / REPO-SAFE)
#  Copy this file and fill in ALL values marked <-- CHANGE THIS
#  IMPORTANT: Do NOT commit your real credentials or employee list.
# ============================================================

# ── I2C LCD Settings ─────────────────────────────────────────
# Run: i2cdetect -y 1   to confirm your address (0x27 or 0x3F)
LCD_I2C_ADDRESS = 0x27       # <-- CHANGE THIS if yours shows 0x3F
LCD_I2C_PORT    = 1
LCD_COLS        = 20
LCD_ROWS        = 4

# ── Matrix Keypad GPIO Pins (BCM numbering) ───────────────────
# Keypad connector order (left to right): C2 R1 C1 R4 C3 R3 R2
KEYPAD_ROW_PINS = [18, 25, 24, 23]   # R1, R2, R3, R4  (BCM)
KEYPAD_COL_PINS = [17, 27, 22]       # C2, C1, C3      (BCM)

# ── Keypad Layout ─────────────────────────────────────────────
# NOTE: This keypad has a non-standard connector order.
# Columns 1 and 2 are physically swapped, corrected here.
# Run keytest.py to verify your specific keypad.
KEYPAD_LAYOUT = [
    ['2', '1', '3'],
    ['5', '4', '6'],
    ['8', '7', '9'],
    ['*', '0', '#'],
]

# ── Special Keys ──────────────────────────────────────────────
KEY_ENTER = '#'
KEY_CLEAR = '*'

# ── File Paths ────────────────────────────────────────────────
DATA_DIR   = '/home/timeclock/timeclock/data'
EXPORT_DIR = '/home/timeclock/timeclock/exports'

# ── Admin Export Code ─────────────────────────────────────────
# Enter this 4-digit code + # on the keypad to trigger a manual export.
# IMPORTANT: Change this from the default before going live.
EXPORT_CODE = '0000'   # <-- CHANGE THIS

# ── Windows 11 Network Share (SMB) ────────────────────────────
# Run ipconfig on your Windows PC to find its IPv4 address.
SMB_SERVER   = '192.168.1.XXX'       # <-- CHANGE THIS
SMB_SHARE    = 'YourSharedFolder'    # <-- CHANGE THIS
SMB_USERNAME = 'YourWindowsUsername' # <-- CHANGE THIS
SMB_PASSWORD = 'YourWindowsPassword' # <-- CHANGE THIS

# ── Email Settings (Gmail) ────────────────────────────────────
# Requires a Gmail App Password — NOT your regular Gmail password.
# Setup: myaccount.google.com -> Security -> App Passwords
EMAIL_SENDER     = 'your-gmail@gmail.com'  # <-- CHANGE THIS
EMAIL_APP_PASS   = 'xxxx xxxx xxxx xxxx'   # <-- CHANGE THIS (16-char App Password)
EMAIL_RECIPIENTS = [
    'recipient1@example.com',  # <-- CHANGE THIS
    'recipient2@example.com',  # <-- CHANGE THIS
    'recipient3@example.com',  # <-- CHANGE THIS
]

# ── Pay Period Anchor ─────────────────────────────────────────
# Must be a SATURDAY. All 14-day pay periods are calculated from this date.
# Example: '2026-01-03' is a Saturday.
PAY_PERIOD_ANCHOR = '2026-01-03'   # <-- CHANGE THIS if needed

# ── Employee Database ─────────────────────────────────────────
# Format:  'CODE': {'name': 'Full Name', 'id': 'EMP-###'}
# CODE must be exactly 4 digits. Codes must be unique.
# Add up to 30 employees.
EMPLOYEES = {
    '1001': {'name': 'Employee One',   'id': 'EMP-001'},
    '1002': {'name': 'Employee Two',   'id': 'EMP-002'},
    '1003': {'name': 'Employee Three', 'id': 'EMP-003'},
    # Add more employees here...
}