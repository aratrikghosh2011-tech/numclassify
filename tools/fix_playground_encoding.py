#!/usr/bin/env python3
"""
Fix mojibake, remove emoji, fix double CRLF in playground JS/CSS files.
Run once from repo root: python tools/fix_playground_encoding.py
"""
from pathlib import Path


def reverse_double_encode(text):
    """
    Reverse cp1252 double-encoding corruption.
    
    Original UTF-8 bytes were read as cp1252, then saved as UTF-8 again.
    We reverse: decode corrupted chars back to single-byte values, then
    re-decode as proper UTF-8.
    """
    w1252 = {
        0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
        0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
        0x2030: 0x89, 0x0160: 0x8A, 0x2039: 0x8B, 0x0152: 0x8C,
        0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
        0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
        0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x203A: 0x9B,
        0x0153: 0x9C, 0x017E: 0x9E, 0x0178: 0x9F,
    }
    result = bytearray()
    for ch in text:
        cp = ord(ch)
        if cp < 0x80:
            result.append(cp)
        elif cp in w1252:
            result.append(w1252[cp])
        elif 0xA0 <= cp <= 0xFF:
            result.append(cp)
        elif cp in (0x81, 0x8D, 0x8F, 0x90, 0x9D):
            result.append(cp)
        else:
            result.append(ord('?'))
    return result.decode('utf-8', errors='replace')


def fix_file(path):
    raw = path.read_bytes()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    text = raw.decode('utf-8')
    text = reverse_double_encode(text)
    text = text.replace('\r\r\n', '\n').replace('\r\n', '\n')
    return text


# ---- guide.js ----
p = Path('docs/playground-guide.js')
raw = p.read_bytes()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]

# Replace corrupted emoji at byte level before decoding
# 👋 corrupted: F0 9F 91 8B -> double-encoded as C3 B0 C5 B8 E2 80 98 E2 80 B9
raw = raw.replace(b'\xc3\xb0\xc5\xb8\xe2\x80\x98\xe2\x80\xb9', b'')
# → corrupted: E2 86 92 -> double-encoded as C3 A2 E2 80 B0 E2 80 99
raw = raw.replace(b'\xc3\xa2\xe2\x80\xb0\xe2\x80\x99', b'>')
# — corrupted: E2 80 94 -> double-encoded as C3 A2 E2 82 AC E2 80 9D
raw = raw.replace(b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', b' - ')
# ⌨ corrupted: E2 8C A8 -> double-encoded as C3 A2 C5 8C C2 A8
raw = raw.replace(b'\xc3\xa2\xc5\x8c\xc2\xa8', b'keyboard')
# 🎉 corrupted: F0 9F 8E 89 -> double-encoded C3 B0 C5 B8 C5 92 E2 80 B0
# But the actual bytes might differ. Let me check and handle specific patterns.
# The guide.js line 77 has the 🎉 at the end of "classifying. " text
# After removing 👋 above, that should be fine. Let's just handle the remaining .

# Handle specific full-string replacements at byte level
raw = raw.replace(
    b" Hey! I'm Byte, your guide. This is the numclassify playground  -  a live Python environment running in your browser. Let me walk you through it. Takes about 30 seconds.",
    b"Hey! I'm Byte, your guide. This is the numclassify playground - a live Python environment running in your browser. Let me walk you through it. Takes about 30 seconds."
)
# Also handle without the space after 👋 removal (leading space removed)
raw = raw.replace(
    b"Hey! I'm Byte, your guide. This is the numclassify playground  -  a live Python environment running in your browser. Let me walk you through it. Takes about 30 seconds.",
    b"Hey! I'm Byte, your guide. This is the numclassify playground - a live Python environment running in your browser. Let me walk you through it. Takes about 30 seconds."
)

# Fix the "Next →" and "Done ✓" buttons
# ✓ corrupted: E2 9C 93 -> C3 A2 C5 93 E2 80 9C
raw = raw.replace(b"'Done \xc3\xa2\xc5\x93\xe2\x80\x9c'", b"'Done'")
# → corrupted already handled above with the general replacement

# Fix the final guide step text - it has corrupted ⌨ and 🎉
# Find and replace the complete string
raw = raw.replace(
    b"That's everything! The keyboard shortcut overlay (press ?) shows all keyboard shortcuts. Happy classifying. ",
    b"That's everything! Press ? to see all keyboard shortcuts."
)
# Also handle any trailing corruption bytes after the period
raw = raw.replace(b"classifying. \xf0\x9f\x8e\x89", b"classifying.")

text = raw.decode('utf-8')
text = reverse_double_encode(text)
text = text.replace('\r\r\n', '\n').replace('\r\n', '\n')

# Fix remaining em dash in emoji-removed text
text = text.replace(' -  ', ' - ')
text = text.replace('  ', ' ')

p.write_text(text, encoding='utf-8')
print(f"Fixed: {p}")


# ---- core.js ----
p = Path('docs/playground-core.js')
raw = p.read_bytes()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]

text = raw.decode('utf-8')
text = reverse_double_encode(text)
text = text.replace('\r\r\n', '\n').replace('\r\n', '\n')

text = text.replace('\u2014', ' -- ')
text = text.replace('\u25bc', 'v')
text = text.replace('\u25b6', '>')

p.write_text(text, encoding='utf-8')
print(f"Fixed: {p}")


# ---- tabs.js ----
p = Path('docs/playground-tabs.js')
raw = p.read_bytes()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]

# Replace theme toggle line at byte level before decoding
# The corrupted sun emoji contains byte 0x8F which can't roundtrip through cp1252
raw = raw.replace(
    b"$('theme-icon').textContent = next === 'light' ? '\xc3\xa2\xcb\x9c\xe2\x82\xac\xc3\xaf\xc2\xb8\xc2\x8f' : '\xc3\xb0\xc5\xb8\xc5\x92\xe2\x84\xa2';",
    b"$('theme-icon').textContent = next === 'light' ? 'Light' : 'Dark';"
)

text = raw.decode('utf-8')
text = reverse_double_encode(text)
text = text.replace('\r\r\n', '\n').replace('\r\n', '\n')

# Fix em dashes in UI strings
for old, new in [
    ('Cannot copy batch results \u2014 classify a single number first.',
     'Cannot copy batch results. Classify a single number first.'),
    ('Cannot download batch results \u2014 classify a single number first.',
     'Cannot download batch results. Classify a single number first.'),
    ('Copy failed \u2014 try selecting manually.',
     'Copy failed. Try selecting manually.'),
    ('No shared properties \u2014 these numbers are mathematically unrelated.',
     'No shared properties. These numbers have no properties in common.'),
]:
    text = text.replace(old, new)

p.write_text(text, encoding='utf-8')
print(f"Fixed: {p}")


# ---- guide.css ----
p = Path('docs/playground-guide.css')
raw = p.read_bytes()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
text = raw.decode('utf-8')
text = reverse_double_encode(text)
text = text.replace('\r\r\n', '\n').replace('\r\n', '\n')

p.write_text(text, encoding='utf-8')
print(f"Fixed: {p}")


print("\nAll JS/CSS files fixed.")
