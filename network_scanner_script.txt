import nmap
import socket
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

class NetworkScanner:
    def __init__(self, target_network):
        self.target = target_network
        self.nm = nmap.PortScanner()

    def basic_scan(self):
        """
        Perform a basic network scan
        Returns list of active hosts
        """
        try:
            logging.info("Starting basic scan...")
            # Perform ping scan to find active hosts
            self.nm.scan(hosts=self.target, arguments='-sn')
           
            active_hosts = []
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    try:
                        hostname = socket.gethostbyaddr(host)[0]
                    except socket.herror:
                        hostname = "Unknown"
                   
                    active_hosts.append({
                        'ip': host,
                        'hostname': hostname
                    })
           
            logging.info("Basic scan completed successfully.")
            return active_hosts
       
        except Exception as e:
            logging.error(f"Scan error: {e}")
            return []

    def port_scan(self, host):
        """
        Perform detailed port scan on a specific host
        """
        try:
            logging.info(f"Starting port scan for host {host}...")
            self.nm.scan(host, arguments='-sV -sC')
           
            open_ports = []
            for proto in self.nm[host].all_protocols():
                ports = self.nm[host][proto].keys()
                for port in ports:
                    service = self.nm[host][proto][port]
                    open_ports.append({
                        'port': port,
                        'state': service['state'],
                        'service': service.get('name', 'Unknown'),
                        'version': service.get('version', 'Unknown')
                    })
           
            logging.info(f"Port scan for host {host} completed successfully.")
            return open_ports
       
        except Exception as e:
            logging.error(f"Port scan error for host {host}: {e}")
            return []

# Usage Example
def main():
    # Replace with your local network or test environment
    target_network = '192.168.1.0/24'
   
    scanner = NetworkScanner(target_network)
   
    # Perform network discovery
    logging.info("Discovering active hosts...")
    hosts = scanner.basic_scan()
   
    logging.info("\nActive Hosts:")
    for host in hosts:
        logging.info(f"IP: {host['ip']}, Hostname: {host['hostname']}")
       
        # Perform detailed port scan on each host
        logging.info(f"\nScanning ports for {host['ip']}:")
        ports = scanner.port_scan(host['ip'])
       
        for port in ports:
            logging.info(f"Port {port['port']}: {port['service']} ({port['state']}) - Version: {port['version']}")

if __name__ == "__main__":
    main()
