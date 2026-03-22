# 🔍 Blind SQLi - Binary Search Attack

A fast and efficient Python script that extracts passwords from blind SQL injection vulnerabilities using binary search algorithm.

## ⚡ Performance

| Method                              | Time (approx)      |
| ----------------------------------- | ------------------ |
| Burp Suite Community (Intruder)     | 10-15 minutes      |
| Python - Cluster Bomb (Brute Force) | 2-3 minutes        |
| **Python - Binary Search**          | **~15 seconds** ✅ |

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Hasrat270/ClusterBombForPortSwiggerLab.git

# Navigate to directory
cd ClusterBombForPortSwiggerLab

# Install required library
pip install requests
```

## 📂 Scripts

| Script            | Method                 | Speed   |
| ----------------- | ---------------------- | ------- |
| `clusterBomb.py`  | Brute force (a-z, 0-9) | Medium  |
| `binarySearch.py` | Binary search on ASCII | Fast ⚡ |

## 🚀 Usage

### Binary Search (Recommended)

```bash
python binarySearch.py
```

```
=======================================================
        Blind SQLi - Binary Search Attack
=======================================================

[*] URL        : https://YOUR-LAB-URL.net/
[*] TrackingId : YOUR_TRACKING_ID
[*] Session    : YOUR_SESSION_COOKIE

[*] Validating cookies...
[+] Cookies OK!
[*] Threads  : 20
[*] Retries  : 3 per request
[*] Starting attack...

[+] Position 01: 'i' | Progress: 1/20  | i???????????????????
[+] Position 02: 'p' | Progress: 2/20  | ip??????????????????
...
[+] Position 20: 'i' | Progress: 20/20 | ipb53cp6m4yo1vnzp5ki

=======================================================
[*] Final Password : ipb53cp6m4yo1vnzp5ki
[*] Time Taken     : 14.95 seconds
=======================================================
```

### Cluster Bomb

```bash
python clusterBomb.py
```

## ⚙️ How It Works

### Binary Search Algorithm

Instead of checking every character (a-z, 0-9), binary search cuts the search space in half each time:

```
Finding character at position 1:
  ASCII range: 32-126

  Step 1: Is ASCII > 79?  → YES → search 80-126
  Step 2: Is ASCII > 103? → NO  → search 80-103
  Step 3: Is ASCII > 91?  → NO  → search 80-91
  Step 4: Is ASCII > 85?  → NO  → search 80-85
  Step 5: Is ASCII > 82?  → NO  → search 80-82
  Step 6: Is ASCII > 81?  → NO  → Found: ASCII 80 = 'P' ✅

  Result: 6 requests vs 36 requests (brute force)
```

### Key Features

- ✅ **Auto URL fix** — adds `https://` automatically
- ✅ **Input validation** — catches empty/invalid inputs
- ✅ **Connection test** — verifies URL before attack
- ✅ **Session validation** — checks if cookies are valid
- ✅ **Retry logic** — 3 retries per failed request
- ✅ **TCP reuse** — faster connections via session object
- ✅ **20 parallel threads** — all positions run simultaneously
- ✅ **Partial results** — shows progress on Ctrl+C

## 📋 Requirements

- Python 3.x
- `requests` library

## ⚠️ Disclaimer

> These scripts are developed **strictly for educational purposes** and for use in legal lab environments only. Do not use on any system without explicit permission. Unauthorized use is illegal.

## 👤 Author

**Hasrat Afridi** — [@Hasrat270](https://github.com/Hasrat270)
