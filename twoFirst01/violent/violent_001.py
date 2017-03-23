import nmap
nm = nmap.PortScanner()
nm.scan('10.86.60.107', '20-443')
