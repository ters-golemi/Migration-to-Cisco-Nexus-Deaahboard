# Prerequisites for Nexus Dashboard Migration

## Table of Contents
1. [Hardware Requirements](#hardware-requirements)
2. [Software Requirements](#software-requirements)
3. [Network Requirements](#network-requirements)
4. [Access Requirements](#access-requirements)
5. [Knowledge Requirements](#knowledge-requirements)
6. [Current Environment Assessment](#current-environment-assessment)

## Hardware Requirements

### Nexus Dashboard Physical Appliance
- **Cisco Nexus Dashboard (ND) Physical Node**:
  - CPU: 32 cores (minimum)
  - RAM: 256 GB (minimum)
  - Storage: 3 TB SSD (RAID configuration)
  - Network: 4x 10G/25G ports (minimum)

### Nexus Dashboard Virtual Appliance
- **VMware ESXi Requirements**:
  - vSphere 6.7 or later
  - vCPU: 32 cores
  - vRAM: 128 GB (minimum)
  - vDisk: 500 GB (thin provisioned)
  - vNIC: 4 virtual network adapters

### Cluster Requirements
- Minimum 3 nodes for production (high availability)
- Single node for lab/testing environments
- Maximum latency between nodes: 50ms RTT

## Software Requirements

### Nexus Dashboard
- **Nexus Dashboard Version**: 2.3.x or later (recommended: latest version)
- **Nexus Dashboard Fabric Controller (NDFC)**: 12.1.x or later
- **Nexus Dashboard Insights**: 6.3.x or later (optional)
- **Nexus Dashboard Orchestrator**: 4.2.x or later (for multi-site)

### Existing Nexus Switches
- **Minimum NX-OS Version**: 
  - Nexus 9000 Series: 9.3(7) or later
  - Nexus 3000 Series: 9.3(7) or later
  - Nexus 7000 Series: 8.4(1) or later
- **Supported Switch Models**:
  - Nexus 9300 Series (spine/leaf)
  - Nexus 9500 Series (spine/core)
  - Nexus 3100/3200 Series

### Browser Requirements
- Chrome 90+ (recommended)
- Firefox 88+
- Safari 14+
- Edge 90+

## Network Requirements

### IP Addressing
- **Management Network**: 
  - Dedicated management subnet for Nexus Dashboard cluster
  - IP addresses for each cluster node
  - Default gateway
  - DNS servers (primary and secondary)
  - NTP servers

- **Data Network**:
  - Connectivity to all fabric switches (in-band or out-of-band)
  - VLAN configuration for switch management

### DNS Requirements
- Forward and reverse DNS entries for all Nexus Dashboard nodes
- DNS resolution for external services (if required)

### NTP Requirements
- At least 2 NTP servers (internal or external)
- Time synchronization accuracy: ±1 second
- All fabric switches must sync to same NTP sources

### Firewall Requirements
- **Inbound Ports**:
  - TCP 22 (SSH)
  - TCP 443 (HTTPS)
  - TCP 80 (HTTP - redirects to HTTPS)
  - TCP 8443 (API)
  
- **Outbound Ports**:
  - TCP 22 (SSH to switches)
  - TCP 443 (HTTPS)
  - UDP 123 (NTP)
  - UDP 53 (DNS)
  - TCP 25/587 (SMTP for notifications)

- **Cluster Communication**:
  - All ports between cluster nodes (unrestricted)
  - TCP 2379-2380 (etcd)
  - TCP 6443 (Kubernetes API)

### Bandwidth Requirements
- Minimum 1 Gbps between Nexus Dashboard and switches
- 10 Gbps recommended for large fabrics (>100 switches)

## Access Requirements

### Administrative Access
- **Existing Fabric**:
  - Admin-level access to all Nexus switches
  - TACACS+/RADIUS credentials (if applicable)
  - Enable password/secret

- **Nexus Dashboard**:
  - Local admin account
  - Integration with AAA servers (optional)

### External Services
- **vCenter/ESXi**: Admin access for VM deployment
- **SMTP Server**: For email notifications
- **Syslog Server**: For centralized logging
- **SNMP**: For monitoring integration

### Certificate Requirements
- Valid SSL certificates (optional but recommended)
- CA-signed certificates for production
- Certificate chain files
- Private key files

## Knowledge Requirements

### Technical Skills
- **Networking**:
  - VXLAN EVPN fundamentals
  - BGP configuration and troubleshooting
  - VRF and VRF-Lite
  - Multicast (if using multicast underlay)
  - QoS policies

- **Data Center**:
  - Nexus NX-OS CLI and configuration
  - Data center fabric design
  - Layer 2 and Layer 3 networking
  - High availability concepts

- **Nexus Dashboard**:
  - REST API basics (optional)
  - Intent-based networking concepts
  - Policy management

### Recommended Certifications
- CCNP Data Center
- Cisco VXLAN EVPN training
- Nexus Dashboard training

## Current Environment Assessment

### Documentation Needed
Before starting migration, document your current environment:

1. **Network Topology**:
   - Complete network diagram
   - Switch inventory (models, versions, roles)
   - Physical and logical connectivity
   - Cabling documentation

2. **Configuration Documentation**:
   - Running configurations of all switches
   - Feature set enabled
   - VLANs and VNIs
   - VRFs and route targets
   - BGP AS numbers and peering
   - Anycast gateway configuration

3. **Service Documentation**:
   - Application dependencies
   - Network segmentation policies
   - QoS requirements
   - Multicast requirements
   - External connectivity (Internet, WAN)

4. **Operations Documentation**:
   - Change management procedures
   - Maintenance windows
   - Backup procedures
   - Monitoring and alerting
   - Incident response procedures

### Environment Health Check
Verify the current environment health:

```bash
# Check switch version
show version

# Check fabric health
show nve peers
show bgp l2vpn evpn summary
show vpc status

# Check resource utilization
show system resources
show processes cpu sort
show interface status

# Verify configuration consistency
show running-config
```

### Backup Requirements
- Complete configuration backups of all switches
- Boot variable and kickstart images
- License files
- Certificate files
- Persistent log files

## Pre-Migration Tasks

### Week Before Migration
- [ ] Schedule maintenance window
- [ ] Notify stakeholders
- [ ] Complete all documentation
- [ ] Backup all configurations
- [ ] Install Nexus Dashboard cluster
- [ ] Verify network connectivity
- [ ] Test AAA integration

### Day Before Migration
- [ ] Final configuration backup
- [ ] Verify backup integrity
- [ ] Confirm maintenance window
- [ ] Prepare rollback plan
- [ ] Test communication with switches
- [ ] Verify DNS and NTP
- [ ] Confirm team availability

### Day of Migration
- [ ] Freeze change control
- [ ] Enable enhanced logging
- [ ] Establish communication channels
- [ ] Verify rollback readiness
- [ ] Start screen recording/logging

## Tools and Utilities

### Required Tools
- SSH client (PuTTY, SecureCRT, or terminal)
- TFTP/SFTP server for backups
- Configuration management tool (Ansible, Python)
- Network monitoring tool
- Packet capture tool (Wireshark)

### Optional Tools
- Cisco DCNM (for comparison)
- Python scripts for automation
- Ansible playbooks
- REST API client (Postman)

## Validation Checklist

Before proceeding with migration:

- [ ] All hardware requirements met
- [ ] Software versions compatible
- [ ] Network connectivity verified
- [ ] Access credentials validated
- [ ] Documentation complete
- [ ] Backups verified
- [ ] Team trained and ready
- [ ] Maintenance window approved
- [ ] Rollback plan documented
- [ ] Stakeholders notified

## Next Steps

Once all prerequisites are met, proceed to:
1. [Pre-Migration Checklist](pre-migration-checklist.md)
2. [Migration Plan](migration-plan.md)

## References

- [Cisco Nexus Dashboard Installation Guide](https://www.cisco.com/c/en/us/td/docs/dcn/nd/2x/installation/cisco-nexus-dashboard-installation-guide.html)
- [Nexus Dashboard Fabric Controller Documentation](https://www.cisco.com/c/en/us/support/cloud-systems-management/prime-data-center-network-manager/series.html)
- [NX-OS Software Compatibility Matrix](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/interoperability/guide/b_Cisco_Nexus_9000_Series_NX-OS_Software_Interoperability_Support_Matrix.html)
