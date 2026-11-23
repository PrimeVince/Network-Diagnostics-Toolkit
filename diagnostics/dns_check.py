
import socket


def check_dns_resolution():
    domains = [
        "google.com",
        "cloudflare.com",
        "github.com"
    ]

    results = {}

    for domain in domains:
        try:
            addresses = socket.getaddrinfo(
                domain,
                None,
                socket.AF_INET
            )

            results[domain] = {
                "resolved": True,
                "ip_addresses": sorted({
                    address[4][0] for address in addresses
                }),
                "error": None
            }

        except socket.gaierror as error:
            results[domain] = {
                "resolved": False,
                "ip_addresses": [],
                "error": str(error)
            }

    return results


if __name__ == "__main__":
    dns_results = check_dns_resolution()

    print("\nDNS DIAGNOSTICS")
    print("=" * 45)

    for domain, result in dns_results.items():
        print(f"\nDomain: {domain}")
        print(f"Resolved: {result['resolved']}")
        print(f"IP Addresses: {result['ip_addresses']}")

        if result["error"]:
            print(f"Error: {result['error']}")
