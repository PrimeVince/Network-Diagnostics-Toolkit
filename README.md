# Network Diagnostics Toolkit

A Python-based network troubleshooting utility that automates common connectivity checks, collects network configuration details, and generates diagnostic reports.

## Features

- **Network Configuration:** Retrieves hostname, network interfaces, IPv4 addresses, subnet masks, default gateway, and DNS servers.
- **Gateway Connectivity:** Tests connectivity to the default gateway using ICMP.
- **Internet Connectivity:** Checks external connectivity using Google and Cloudflare public IP addresses.
- **DNS Diagnostics:** Tests domain name resolution for selected websites.
- **Port Connectivity:** Tests TCP connections to common service ports.
- **Diagnostic Reporting:** Generates timestamped JSON reports containing diagnostic results.
- **Logging:** Records diagnostic activity and errors.
- **Error Handling:** Allows individual diagnostic failures to be recorded without terminating the entire application.
- **Network Health Assessment:** Calculates an overall health status based on diagnostic results.

## Technologies Used

- Python 3
- PowerShell
- Python Standard Library:
  - `socket`
  - `subprocess`
  - `json`
  - `logging`
  - `datetime`
  - `pathlib`
  - `ipaddress`

## Project Structure

```text
Network-Diagnostics-Toolkit/
│
├── diagnostics/
│   ├── __init__.py
│   ├── connectivity.py
│   ├── dns_check.py
│   ├── logger.py
│   ├── network_config.py
│   └── port_check.py
│
├── logs/
├── reports/
│
├── main.py
├── README.md
└── .gitignore
```

## Requirements

- Windows operating system
- Python 3.10 or later
- Windows PowerShell with the `Get-NetIPConfiguration` cmdlet

No third-party Python packages are required.

## Installation

Clone the repository:

```powershell
git clone https://github.com/PrimeVince/Network-Diagnostics-Toolkit.git
```

Navigate into the project directory:

```powershell
cd Network-Diagnostics-Toolkit
```

## Usage

Run the toolkit from the project root:

```powershell
py main.py
```

The application performs the configured network diagnostics and displays the results in the terminal.

## Diagnostic Reports

Each execution generates a timestamped JSON report inside the `reports/` directory.

Example:

```text
reports/
    network_report_20261123_132950.json
```

## Logging

Application activity is recorded in:

```text
logs/network_toolkit.log
```

The log records diagnostic execution, successful completion, report generation, and errors.

## Testing

The toolkit has been tested on a Windows environment.

Verified functionality includes:

- Network configuration retrieval.
- Gateway and external connectivity checks.
- DNS resolution.
- TCP port connectivity.
- JSON report generation.
- Logging.
- Controlled diagnostic failure and recovery.
- Dynamic network health assessment.

## Limitations

- Network configuration retrieval currently relies on Windows PowerShell.
- ICMP tests may be affected by firewall restrictions.
- TCP connection failures may indicate filtering or network restrictions rather than a confirmed closed port.
- The diagnostic targets and ports are currently predefined.

## Author

**Vincent Mathu**

Information Technology graduate interested in networking, IT support, cybersecurity, and automation.

GitHub: [PrimeVince](https://github.com/PrimeVince)