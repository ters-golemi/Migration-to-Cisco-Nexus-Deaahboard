#!/usr/bin/env python3
"""
Fabric Health Verification Script

This script verifies the health of a VXLAN EVPN fabric by checking:
- BGP EVPN sessions
- VXLAN tunnel status
- vPC status (if applicable)
- Control plane health
- Data plane health

Requirements:
    pip install paramiko netmiko

Usage:
    python verify-fabric-health.py
"""

import sys
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import re

# Switch inventory
SWITCHES = [
    {'hostname': 'spine-01', 'ip': '192.168.1.1', 'role': 'spine'},
    {'hostname': 'spine-02', 'ip': '192.168.1.2', 'role': 'spine'},
    {'hostname': 'leaf-01', 'ip': '192.168.1.11', 'role': 'leaf'},
    {'hostname': 'leaf-02', 'ip': '192.168.1.12', 'role': 'leaf'},
    {'hostname': 'leaf-03', 'ip': '192.168.1.13', 'role': 'leaf'},
    {'hostname': 'leaf-04', 'ip': '192.168.1.14', 'role': 'leaf'},
]


def connect_to_switch(switch_info, username, password):
    """Connect to a switch"""
    device = {
        'device_type': 'cisco_nxos',
        'host': switch_info['ip'],
        'username': username,
        'password': password,
        'timeout': 60
    }
    
    try:
        connection = ConnectHandler(**device)
        return connection
    except Exception as e:
        print(f"  ✗ Connection failed: {str(e)}")
        return None


def check_bgp_evpn(connection, hostname):
    """Check BGP EVPN sessions"""
    print(f"\n  Checking BGP EVPN sessions on {hostname}...")
    
    try:
        output = connection.send_command('show bgp l2vpn evpn summary')
        
        # Count established sessions
        established = len(re.findall(r'\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+Established', output))
        total_lines = len([line for line in output.split('\n') if re.match(r'^\d+\.\d+\.\d+\.\d+', line)])
        
        if established == total_lines and total_lines > 0:
            print(f"    ✓ BGP EVPN: {established}/{total_lines} sessions Established")
            return True
        else:
            print(f"    ✗ BGP EVPN: {established}/{total_lines} sessions Established")
            return False
            
    except Exception as e:
        print(f"    ✗ Error checking BGP: {str(e)}")
        return False


def check_nve_peers(connection, hostname):
    """Check NVE peers (VXLAN tunnels)"""
    print(f"\n  Checking NVE peers on {hostname}...")
    
    try:
        output = connection.send_command('show nve peers')
        
        # Count UP peers
        up_peers = len(re.findall(r'UP', output))
        
        if up_peers > 0:
            print(f"    ✓ NVE Peers: {up_peers} peers UP")
            return True
        else:
            print(f"    ⚠ NVE Peers: No peers found (may be spine)")
            return True  # Spines don't have NVE peers
            
    except Exception as e:
        print(f"    ✗ Error checking NVE peers: {str(e)}")
        return False


def check_vpc_status(connection, hostname):
    """Check vPC status"""
    print(f"\n  Checking vPC status on {hostname}...")
    
    try:
        output = connection.send_command('show vpc')
        
        if 'vPC domain id' in output:
            # vPC is configured
            if 'vPC peer-link is up' in output:
                print(f"    ✓ vPC: Peer-link is UP")
                
                # Check peer-keepalive
                if 'peer is alive' in output:
                    print(f"    ✓ vPC: Peer-keepalive is alive")
                    return True
                else:
                    print(f"    ✗ vPC: Peer-keepalive issue detected")
                    return False
            else:
                print(f"    ✗ vPC: Peer-link is DOWN")
                return False
        else:
            print(f"    ⓘ vPC: Not configured on this switch")
            return True  # Not an error if vPC not configured
            
    except Exception as e:
        print(f"    ⓘ vPC: {str(e)}")
        return True  # Not critical


def check_system_resources(connection, hostname):
    """Check system resources"""
    print(f"\n  Checking system resources on {hostname}...")
    
    try:
        output = connection.send_command('show system resources')
        
        # Extract CPU and memory usage
        cpu_match = re.search(r'CPU states\s+:\s+(\d+\.\d+)% user', output)
        mem_match = re.search(r'Memory usage:\s+(\d+)K total,\s+(\d+)K used', output)
        
        issues = []
        
        if cpu_match:
            cpu_usage = float(cpu_match.group(1))
            if cpu_usage > 80:
                print(f"    ⚠ CPU: {cpu_usage}% (HIGH)")
                issues.append('cpu')
            else:
                print(f"    ✓ CPU: {cpu_usage}%")
        
        if mem_match:
            total_mem = int(mem_match.group(1))
            used_mem = int(mem_match.group(2))
            mem_percent = (used_mem / total_mem) * 100
            
            if mem_percent > 90:
                print(f"    ⚠ Memory: {mem_percent:.1f}% (HIGH)")
                issues.append('memory')
            else:
                print(f"    ✓ Memory: {mem_percent:.1f}%")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"    ✗ Error checking resources: {str(e)}")
        return False


def check_interface_errors(connection, hostname):
    """Check for interface errors"""
    print(f"\n  Checking interface errors on {hostname}...")
    
    try:
        output = connection.send_command('show interface status | include connected')
        connected_interfaces = len(output.split('\n'))
        
        error_output = connection.send_command('show interface counters errors | exclude 0')
        error_lines = [line for line in error_output.split('\n') if re.match(r'^\S+\s+\d+', line)]
        
        if len(error_lines) > 1:  # More than header
            print(f"    ⚠ Interfaces: {len(error_lines)} interfaces with errors")
            return False
        else:
            print(f"    ✓ Interfaces: No errors detected")
            return True
            
    except Exception as e:
        print(f"    ✗ Error checking interfaces: {str(e)}")
        return False


def verify_switch(switch_info, username, password):
    """Verify health of a single switch"""
    hostname = switch_info['hostname']
    role = switch_info['role']
    
    print("\n" + "=" * 60)
    print(f"Verifying {hostname} ({role})")
    print("=" * 60)
    
    # Connect to switch
    connection = connect_to_switch(switch_info, username, password)
    if not connection:
        return {'hostname': hostname, 'status': 'UNREACHABLE', 'checks': {}}
    
    # Run checks
    checks = {
        'bgp_evpn': check_bgp_evpn(connection, hostname),
        'nve_peers': check_nve_peers(connection, hostname),
        'vpc': check_vpc_status(connection, hostname),
        'resources': check_system_resources(connection, hostname),
        'interfaces': check_interface_errors(connection, hostname)
    }
    
    # Disconnect
    connection.disconnect()
    
    # Determine overall status
    all_passed = all(checks.values())
    status = 'HEALTHY' if all_passed else 'ISSUES'
    
    print(f"\n  Overall Status: {status}")
    
    return {'hostname': hostname, 'status': status, 'checks': checks}


def main():
    """Main function"""
    print("=" * 60)
    print("Fabric Health Verification Script")
    print("=" * 60)
    
    # Get credentials
    username = input("\nEnter SSH username: ")
    password = getpass("Enter SSH password: ")
    
    # Verify each switch
    results = []
    for switch in SWITCHES:
        result = verify_switch(switch, username, password)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    healthy = [r for r in results if r['status'] == 'HEALTHY']
    issues = [r for r in results if r['status'] == 'ISSUES']
    unreachable = [r for r in results if r['status'] == 'UNREACHABLE']
    
    print(f"\nTotal switches: {len(SWITCHES)}")
    print(f"Healthy: {len(healthy)}")
    print(f"With issues: {len(issues)}")
    print(f"Unreachable: {len(unreachable)}")
    
    if healthy:
        print("\n✓ Healthy switches:")
        for r in healthy:
            print(f"  - {r['hostname']}")
    
    if issues:
        print("\n⚠ Switches with issues:")
        for r in issues:
            print(f"  - {r['hostname']}")
            failed_checks = [k for k, v in r['checks'].items() if not v]
            if failed_checks:
                print(f"    Failed checks: {', '.join(failed_checks)}")
    
    if unreachable:
        print("\n✗ Unreachable switches:")
        for r in unreachable:
            print(f"  - {r['hostname']}")
    
    print()
    
    # Exit with appropriate code
    sys.exit(0 if len(issues) == 0 and len(unreachable) == 0 else 1)


if __name__ == '__main__':
    main()
