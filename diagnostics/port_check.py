
import socket


def check_port(host, port, timeout=3):
    result = {
        "host": host,
        "port": port,
        "reachable": False,
        "error": None
    }

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout
        ):
            result["reachable"] = True

    except (socket.timeout, OSError) as error:
        result["error"] = str(error)

    return result


if __name__ == "__main__":
    tests = [
        ("google.com", 80),
        ("google.com", 443),
        ("github.com", 443)
    ]

    print("\nPORT CONNECTIVITY")
    print("=" * 45)

    for host, port in tests:
        result = check_port(host, port)

        status = "OPEN" if result["reachable"] else "CLOSED / UNREACHABLE"

        print(f"{host}:{port} - {status}")

        if result["error"]:
            print(f"Error: {result['error']}")
