# 🔍 Blind SQLi - Binary Search Attack

A fast and efficient Python script that extracts passwords from blind SQL injection vulnerabilities using the binary search algorithm — no manual script editing required.

## ⚡ Performance

| Method                              | Time (approx)      |
| ----------------------------------- | ------------------ |
| Burp Suite Community (Intruder)     | 10-15 minutes      |
| Python - Cluster Bomb (Brute Force) | 2-3 minutes        |
| **Python - Binary Search**          | **~15 seconds** ✅ |

## 📂 Scripts

| Script            | Method                       | Speed   |
| ----------------- | ---------------------------- | ------- |
| `clusterBomb.py`  | Brute force (a-z, 0-9)       | Medium  |
| `binarySearch.py` | Binary search on ASCII range | Fast ⚡ |

## 🛠️ Installation

```bash
git clone https://github.com/Hasrat270/ClusterBombForPortSwiggerLab.git
cd ClusterBombForPortSwiggerLab
pip install requests
```

## 🚀 Usage

Just run the script — it will ask for values dynamically. No need to edit anything manually.

```bash
python binarySearch.py
```

```
=======================================================
        Blind SQLi - Binary Search Attack
=======================================================

[*] URL        : https://YOUR-LAB-URL.net/
[*] Testing connection...
[+] Connected! Status: 200

[*] TrackingId : YOUR_TRACKING_ID
[*] Session    : YOUR_SESSION_COOKIE

[*] Validating cookies...
[+] Cookies OK!

[*] Target   : https://YOUR-LAB-URL.net/
[*] Threads  : 20
[*] Retries  : 3 per request
[*] Starting attack...

[+] Position 01: 'i' | Progress: 1/20  | i???????????????????
[+] Position 07: 'p' | Progress: 2/20  | i?????p?????????????
...
[+] Position 20: 'i' | Progress: 20/20 | ipb53cp6m4yo1vnzp5ki

=======================================================
[*] Final Password : ipb53cp6m4yo1vnzp5ki
[*] Time Taken     : 14.95 seconds
=======================================================
```

### Where to find the values?

Open **Burp Suite → Repeater** and copy from your request:

```
GET / HTTP/2
Host: YOUR-LAB-URL.net
Cookie: TrackingId=YOUR_TRACKING_ID; session=YOUR_SESSION_COOKIE
```

## ⚙️ How It Works

### Binary Search Algorithm

Instead of checking every character one by one (a-z, 0-9), binary search cuts the search space in half with every request:

```
Finding character at position 1:
  ASCII range: 32-126

  Step 1: Is ASCII > 79?  → YES → search 80-126
  Step 2: Is ASCII > 103? → NO  → search 80-103
  Step 3: Is ASCII > 91?  → NO  → search 80-91
  Step 4: Is ASCII > 85?  → NO  → search 80-85
  Step 5: Is ASCII > 82?  → NO  → search 80-82
  Step 6: Is ASCII > 81?  → NO  → ASCII 80 = 'P' ✅

  6 requests vs 36 requests (brute force) — 6x faster
```

All 20 positions run **simultaneously** via parallel threads, making the total attack complete in ~15 seconds.

### Key Features

- ✅ **Dynamic input** — no script editing needed, just run and enter values
- ✅ **Auto URL fix** — adds `https://` automatically if missing
- ✅ **Input validation** — catches empty or invalid inputs
- ✅ **Connection test** — verifies URL is reachable before starting
- ✅ **Session validation** — checks if cookies are valid before attack
- ✅ **Retry logic** — 3 retries per failed request with delay
- ✅ **TCP reuse** — faster connections via requests Session object
- ✅ **20 parallel threads** — all positions searched simultaneously
- ✅ **Partial results** — shows progress on Ctrl+C interrupt

## 📋 Requirements

- Python 3.x
- `requests` library

## ⚠️ Disclaimer

> These scripts are developed **strictly for educational purposes** and for use in legal lab environments only. Do not use on any system without explicit written permission. Unauthorized use is illegal and unethical.

## 👤 Author

**Hasrat Afridi** — [@Hasrat270](https://github.com/Hasrat270)
