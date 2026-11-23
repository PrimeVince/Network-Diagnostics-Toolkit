
import subprocess

from diagnostics.network_config import get_network_configuration


def check_gateway_connectivity():
    configuration = get_network_configuration()
    gateway = configuration["default_gateway"]

    result = {
        "gateway": gateway,
        "reachable": False,
        "response": None,
        "error": None
    }

    if not gateway:
        result["error"] = "No default gateway found."
        return result

    try:
        response = subprocess.run(
            ["ping", "-n", "4", gateway],
            capture_output=True,
            text=True,
            timeout=15
        )

        result["response"] = response.stdout
        result["reachable"] = response.returncode == 0

        if not result["reachable"]:
            result["error"] = "Gateway did not respond successfully."

    except subprocess.TimeoutExpired:
        result["error"] = "Gateway ping timed out."

    except OSError as error:
        result["error"] = str(error)

    return result

def check_internet_connectivity():
    targets = ["8.8.8.8", "1.1.1.1"]
    results = {}
    

    for target in targets:
        try:
            response = subprocess.run(
                ["ping", "-n", "4", target],
                capture_output=True,
                text=True,
                timeout=15
            )

            results[target] = response.returncode == 0

        except subprocess.TimeoutExpired:
            results[target] = False

        except OSError:
            results[target] = False

    return results


if __name__ == "__main__":
    gateway_result = check_gateway_connectivity()

    print("\nGATEWAY CONNECTIVITY")
    print("=" * 45)
    print(f"Gateway: {gateway_result['gateway']}")
    print(f"Reachable: {gateway_result['reachable']}")

    if gateway_result["error"]:
        print(f"Error: {gateway_result['error']}")

    if gateway_result["response"]:
        print("\nPING DETAILS")
        print(gateway_result["response"])
        internet_result = check_internet_connectivity()

    print("\nINTERNET CONNECTIVITY")
    print("=" * 45)

    for target, reachable in internet_result.items():
        print(f"{target}: {'Reachable' if reachable else 'Unreachable'}")