
import socket
import subprocess
import json
import ipaddress


def get_network_configuration():
    """Collect network configuration from Windows."""

    results = {
        "hostname": socket.gethostname(),
        "interfaces": [],
        "default_gateway": None,
        "dns_servers": [],
        "error": None
    }

    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        """
        Get-NetIPConfiguration | ForEach-Object {
            [PSCustomObject]@{
                InterfaceAlias = $_.InterfaceAlias
                IPv4Address = @($_.IPv4Address | ForEach-Object { $_.IPAddress })
                PrefixLength = @($_.IPv4Address | ForEach-Object { $_.PrefixLength })
                Gateway = @($_.IPv4DefaultGateway | ForEach-Object { $_.NextHop })
                DNSServers = @($_.DNSServer | ForEach-Object { $_.ServerAddresses })
            }
        } | ConvertTo-Json -Depth 4
        """
    ]

    try:
        output = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        configurations = json.loads(output.stdout)

        if isinstance(configurations, dict):
            configurations = [configurations]

        for config in configurations:

            interface = {
                "name": config.get("InterfaceAlias"),
                "ipv4_address": config.get("IPv4Address") or [],
                "prefix_length": config.get("PrefixLength") or [],
                "gateway": None,
                "dns_servers": []
            }
            interface["subnet_mask"] = []

            for prefix in interface["prefix_length"]:
                mask = str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)
                interface["subnet_mask"].append(mask)

            gateways = config.get("Gateway") or []
            dns_servers = config.get("DNSServers") or []

            if isinstance(gateways, str):
                gateways = [gateways]

            if isinstance(dns_servers, str):
                dns_servers = [dns_servers]

            interface["gateway"] = next(
                (gateway for gateway in gateways if gateway),
                None
            )

            interface["dns_servers"] = [
                server for server in dns_servers if server
            ]

            results["interfaces"].append(interface)

            if interface["gateway"] and not results["default_gateway"]:
                results["default_gateway"] = interface["gateway"]

            for server in interface["dns_servers"]:
                if server not in results["dns_servers"]:
                    results["dns_servers"].append(server)

    except (
        subprocess.CalledProcessError,
        json.JSONDecodeError,
        OSError
    ) as error:
        results["error"] = str(error)

    return results


if __name__ == "__main__":

    configuration = get_network_configuration()

    print("\nNETWORK CONFIGURATION")
    print("=" * 45)

    print(f"Hostname: {configuration['hostname']}")
    print(f"Default Gateway: {configuration['default_gateway']}")

    for interface in configuration["interfaces"]:

        print(f"\nInterface: {interface['name']}")
        print(f"IPv4 Address: {interface['ipv4_address']}")
        print(f"Prefix Length: {interface['prefix_length']}")
        print(f"Subnet Mask: {interface['subnet_mask']}")
        print(f"Gateway: {interface['gateway']}")
        print(f"DNS Servers: {interface['dns_servers']}")

    if configuration["error"]:
        print(f"\nError: {configuration['error']}")
