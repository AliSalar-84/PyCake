import socket
from concurrent.futures import ThreadPoolExecutor

# ✅ Load subdomains from file
with open("SubStar.txt", "r") as f:
    COMMON_SUBDOMAINS = [line.strip() for line in f if line.strip()]

def find_subdomains(domain, wordlist):
    found = []

    def resolve(sub):
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            return f"✅ {subdomain} -> {ip}"
        except socket.gaierror:
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(resolve, wordlist)

    for result in results:
        if result:
            found.append(result)

    return found

if __name__ == "__main__":
    target = input("Enter a domain: ").strip()
    results = find_subdomains(target, COMMON_SUBDOMAINS)

    if results:
        print(f"\n[+] Found {len(results)} active subdomains:\n")
        for res in results:
            print(res)
    else:
        print("[-] No active subdomains found.")
