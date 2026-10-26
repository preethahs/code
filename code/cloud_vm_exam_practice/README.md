# Cloud and Distributed Computing Exam Practice

## Python programs
Each question has its own folder. Run the server first where a server/client pair is provided, then run the client in another terminal. Use separate terminals for multiple clients.

Requirements:
- Python 3.10+
- Pyro4 only for Questions 6 and 9: `python -m pip install Pyro4`

All socket examples use `127.0.0.1` for same-computer testing. For separate VMs, replace it with the server VM's reachable private IP and allow the relevant TCP port through the VM firewall/network settings.

### Programs
1. Basic client-server communication: `q01/server.py`, `q01/client.py` (port 5101)
2. Marks, score, pass/fail, rank: `q02/server.py`, `q02/client.py` (port 5102)
3. Serialization/deserialization: `q03/server.py`, `q03/client.py` (port 5103)
4. File statistics: `q04/server.py`, `q04/client.py` (port 5104). Put a test file in the server's current directory.
5. Token Ring: `q05/server.py`, `q05/client.py` (port 5105). Set EXPECTED_CLIENTS to the number of clients you will start.
6. Temperature conversion RMI using Pyro4: `q06/server.py`, `q06/client.py`
7. Berkeley clock synchronization simulation: `q07/berkeley.py`
8. Clock drift simulation: `q08/clock_drift.py`
9. Online shopping RMI using Pyro4: `q09/server.py`, `q09/client.py`
10. Lamport logical clock: `q10/lamport.py`
11. Round-robin task scheduler: `q11/scheduler.py`

## General run commands
Socket server/client:
1. `python server.py`
2. In another terminal: `python client.py`

For Pyro4:
1. `python server.py`
2. In another terminal: `python client.py`
The server prints a URI; enter/paste it into the client if prompted.

## VM practicals: what to do
Use VirtualBox or VMware Workstation, or your institution's cloud VM platform. Create at least two Linux VMs (e.g. Ubuntu Server), connect them to the same private virtual network, and test connectivity with `ping <other-VM-private-IP>`. For socket client/server tasks, run the server on VM1 and client on VM2. Change the client HOST to VM1's private IP and allow the server port in the firewall (e.g. UFW only if enabled). Do not expose test ports to the public internet.

1. Load balancing and fault tolerance:
   - Create VM1 and VM2 as backend web servers; create VM3 as load balancer.
   - Install a web server on each backend and give each a distinct response identifying itself.
   - Install/configure HAProxy or Nginx on VM3 to distribute requests to VM1 and VM2.
   - Test repeatedly with `curl http://<load-balancer-IP>`; responses should come from both backends.
   - Stop one backend and test again. A health-checked load balancer should route to the healthy backend. Restart it and confirm recovery.
2. School fee portal — load balancing and fault tolerance:
   - Use the same 3-VM topology. Deploy a simple fee-portal page on each backend, using the same mock fee records (no real student data).
   - Configure the load balancer with health checks. Repeatedly refresh the portal and verify service continues when one backend is stopped.
   - For a realistic design, keep application state/database outside the individual web VMs or use a shared database; otherwise different backends may show inconsistent records.
3. Physical server consolidation (logical simulation acceptable):
   - List sample physical servers, their CPU/RAM utilization and workloads.
   - Create a consolidation plan mapping workloads to fewer VMs while staying within CPU/RAM capacity and leaving headroom.
   - Optionally create two or three small VMs and deploy separate services, then consolidate them onto fewer VMs and compare resource use.
   - Record before/after VM count, CPU/RAM allocation, utilization, and risks. Do not claim physical consolidation if only a simulation was performed.
4. School exam portal — load balancing:
   - Create two backend VMs serving a mock exam login page and one load-balancer VM.
   - Use dummy users only. Configure round-robin balancing and health checks.
   - Test with repeated requests and shut down one backend to demonstrate the remaining service.
   - Discuss session persistence and database consistency as design considerations.
5. Multiple VMs communicating by IP:
   - Create two VMs on the same private/host-only network.
   - Run `ip addr` on Linux (or `ipconfig` on Windows) to find each VM's private IP.
   - Verify reachability with `ping`.
   - Run a server on VM1 and client on VM2, set HOST to VM1's private IP, and allow the TCP port in the VM firewall.
   - If ping fails, check network mode, subnet, firewall, and that both VMs are running.
6. Online examination portal — load balancing and fault tolerance:
   - Deploy two identical mock exam application servers and a separate load balancer.
   - Use dummy exam data; do not use real student records.
   - Configure health checks, test normal operation, stop one backend, and demonstrate continued access.
   - Discuss protection against duplicate submissions, shared session storage, backups, and database availability.
7. Client-server communication and load balancer:
   - Start two backend servers on separate VMs/ports and a load balancer VM.
   - Configure HAProxy/Nginx to forward client requests to the backends.
   - Test through the load-balancer IP only, then stop one backend and repeat.
   - Include a topology diagram, IP table, commands, screenshots, and observed results in the lab record.

Typical HAProxy architecture:
Client -> Load Balancer VM -> Backend VM1 / Backend VM2.
Use private networking and health checks. Exact setup commands depend on the Linux distribution, network mode, and whether your lab uses VirtualBox, VMware, or a cloud provider.
