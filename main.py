import json
from pathlib import Path
from datetime import datetime
from diagnostics.logger import setup_logger

from diagnostics.network_config import get_network_configuration
from diagnostics.connectivity import (
    check_gateway_connectivity,
    check_internet_connectivity
)
from diagnostics.dns_check import check_dns_resolution
from diagnostics.port_check import check_port



def run_diagnostics(logger):
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": None,
        "network_configuration": None,
        "gateway_connectivity": None,
        "internet_connectivity": None,
        "dns_diagnostics": None,
        "port_diagnostics": None,
        "errors": []
    }

    def run_check(name, function):
        try:
            result = function()
            logger.info("%s completed successfully.", name)
            return result

        except Exception as error:
            message = f"{name} failed: {error}"
            logger.exception(message)
            report["errors"].append(message)
            return None

    report["network_configuration"] = run_check(
        "Network configuration",
        get_network_configuration
    )

    if report["network_configuration"]:
        report["hostname"] = report["network_configuration"]["hostname"]

    report["gateway_connectivity"] = run_check(
        "Gateway connectivity",
        check_gateway_connectivity
    )

    report["internet_connectivity"] = run_check(
        "Internet connectivity",
        check_internet_connectivity
    )

    report["dns_diagnostics"] = run_check(
        "DNS diagnostics",
        check_dns_resolution
    )

    def run_port_checks():
        ports = {}

        for host, port in [
            ("google.com", 80),
            ("google.com", 443),
            ("github.com", 443)
        ]:
            ports[f"{host}:{port}"] = check_port(host, port)

        return ports

    report["port_diagnostics"] = run_check(
        "Port diagnostics",
        run_port_checks
    )

    return report


def save_report(report):
    reports_directory = Path("reports")
    reports_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_directory / f"network_report_{timestamp}.json"

    with report_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return report_file


def calculate_health(report):
    checks = []

    gateway = report["gateway_connectivity"]
    checks.append(
        gateway is not None and gateway["reachable"]
    )

    internet = report["internet_connectivity"]
    checks.extend(
        internet.values() if internet is not None else [False]
    )

    dns = report["dns_diagnostics"]
    if dns is not None:
        checks.extend(
            result["resolved"] for result in dns.values()
        )
    else:
        checks.append(False)

    ports = report["port_diagnostics"]
    if ports is not None:
        checks.extend(
            result["reachable"] for result in ports.values()
        )
    else:
        checks.append(False)

    passed = sum(checks)
    total = len(checks)

    return {
        "passed": passed,
        "total": total,
        "failed": total - passed,
        "status": "HEALTHY" if passed == total else "ISSUES DETECTED"
    }


def main():
    logger = setup_logger()
    logger.info("Network diagnostics started.")

    report = run_diagnostics(logger)
    health = calculate_health(report)
    report["overall_health"] = health
    report_file = save_report(report)

    logger.info("Network diagnostics completed.")
    logger.info("Report saved: %s", report_file)

    print("\nNETWORK DIAGNOSTICS TOOLKIT")
    print("=" * 50)
    print(f"Diagnostic Time: {report['timestamp']}")
    print(f"Hostname: {report['hostname']}")
    print(f"Gateway Reachable: {report['gateway_connectivity']['reachable']}")

    print("\nInternet Connectivity:")
    for address, reachable in report["internet_connectivity"].items():
        print(f"{address}: {reachable}")

    print("\nDNS Diagnostics:")
    if report["dns_diagnostics"] is not None:
        for domain, result in report["dns_diagnostics"].items():
            print(f"{domain}: {result['resolved']}")
    else:
        print("DNS diagnostics failed.")

    print("\nPort Diagnostics:")
    if report["port_diagnostics"] is not None:
        for destination, result in report["port_diagnostics"].items():
            print(f"{destination}: {result['reachable']}")
    else:
        print("Port diagnostics failed.")
    
    print("\nDiagnostic Errors:")
    if report["errors"]:
        for error in report["errors"]:
            print(f"- {error}")
    else:
        print("No errors detected.")

    print("\nOVERALL NETWORK HEALTH")
    print("=" * 50)
    print(f"Status: {health['status']}")
    print(f"Successful Checks: {health['passed']}/{health['total']}")
    print(f"Failed Checks: {health['failed']}")

    print("\nREPORT SAVED")
    print("=" * 50)
    print(f"Location: {report_file}")



if __name__ == "__main__":
    main()
