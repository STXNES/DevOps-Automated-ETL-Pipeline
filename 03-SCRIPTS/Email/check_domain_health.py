import sys
import os
import dns.resolver

def check_txt_record(domain, prefix):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            txt_string = rdata.to_text().strip('"')
            if txt_string.startswith(prefix):
                return txt_string
    except Exception:
        pass
    return None

def main():
    target_domain = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AUDIT_DOMAIN", "google.com")

    print("========================================")
    print(f" DOMAIN HEALTH AUDIT: {target_domain}")
    print("========================================\n")
    
    # 1. SPF Check
    spf = check_txt_record(target_domain, "v=spf1")
    if spf:
        print(f"[OK] SPF Record Found: {spf}")
    else:
        print("[FAIL] SPF Record MISSING! (Add TXT 'v=spf1 include:spf.yourprovider.com ~all')")
        
    # 2. DKIM Check
    dkim_selector = os.environ.get("DKIM_SELECTOR", "default")
    dkim_domain = f"{dkim_selector}._domainkey.{target_domain}"
    dkim = check_txt_record(dkim_domain, "v=DKIM1")
    if dkim:
        print(f"[OK] DKIM Record Found: {dkim[:45]}...")
    else:
        print(f"[WARN] DKIM Record Not Found at '{dkim_domain}'. Verify provider DNS selector.")
        
    # 3. DMARC Check
    dmarc_domain = f"_dmarc.{target_domain}"
    dmarc = check_txt_record(dmarc_domain, "v=DMARC1")
    if dmarc:
        print(f"[OK] DMARC Record Found: {dmarc}")
    else:
        print(f"[FAIL] DMARC Record MISSING! (Add TXT at _dmarc.{target_domain}: 'v=DMARC1; p=none;')")
        
    print("\n========================================")
    print(" AUDIT SUMMARY:")
    if spf and dmarc:
        print(" [OK] Domain DNS deliverability configured properly.")
        print(" Outgoing emails will route to inbox instead of spam quarantine.")
    else:
        print(" [WARN] Deliverability issues detected. Check missing records above.")
    print("========================================\n")

if __name__ == "__main__":
    main()
