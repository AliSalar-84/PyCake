import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_subdomains_hackertarget(domain):
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print("[-] API request failed.")
            return []
        return [line.split(',')[0] for line in res.text.splitlines()]
    except Exception as e:
        print(f"[-] Exception occurred: {e}")
        return []

def check_subdomain(subdomain):
    try:
        result = subprocess.run(["curl", subdomain, "-v", "--max-time", "5"], capture_output=True, text=True)
        if len(result.stderr) >= 200:
            return f"✅ {subdomain} - responsive"
        else:
            return f"⚠️ {subdomain} - response too short"
    except subprocess.TimeoutExpired:
        return f"⏰ {subdomain} - request timed out"
    except Exception as e:
        return f"❌ {subdomain} - error: {e}"

if __name__ == "__main__":
    domain = input("Please enter a valid domain (e.g., example.com): ").strip()
    subdomains = get_subdomains_hackertarget(domain)

    if not subdomains:
        print("No subdomains found or API error.")
    else:
        print(f"Found {len(subdomains)} subdomains. Checking responsiveness...")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in subdomains]

            for future in as_completed(futures):
                print(future.result())
