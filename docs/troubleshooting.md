# Troubleshooting Guide

## Table of Contents
1. [Nexus Dashboard Issues](#nexus-dashboard-issues)
2. [NDFC Application Issues](#ndfc-application-issues)
3. [Switch Discovery Issues](#switch-discovery-issues)
4. [Configuration Sync Issues](#configuration-sync-issues)
5. [Fabric Control Plane Issues](#fabric-control-plane-issues)
6. [VXLAN Data Plane Issues](#vxlan-data-plane-issues)
7. [Performance Issues](#performance-issues)
8. [Authentication and Access Issues](#authentication-and-access-issues)

---

## Nexus Dashboard Issues

### Issue: Node Not Joining Cluster

**Symptoms**:
- Node shows as "unavailable" in cluster
- Cluster formation fails
- Node cannot communicate with other nodes

**Diagnosis**:
```bash
# Check node status
acs health
acs cluster status

# Check connectivity
ping <other-node-ip>

# Check time sync
show ntp status

# Check logs
tail -f /var/log/acs/acs.log
```

**Common Causes and Solutions**:

1. **Network Connectivity Issue**
   - **Solution**: Verify management network connectivity
   ```bash
   # Test connectivity
   ping <other-node-mgmt-ip>
   traceroute <other-node-mgmt-ip>
   
   # Check firewall rules
   # Ensure all ports open between nodes
   ```

2. **Time Synchronization Issue**
   - **Solution**: Sync time with NTP
   ```bash
   # Configure NTP
   ntp-server <ntp-server-ip>
   
   # Verify sync
   show ntp status
   
   # Time difference must be <1 second
   ```

3. **Certificate Issue**
   - **Solution**: Regenerate cluster certificates
   ```bash
   # Contact Cisco TAC for certificate regeneration
   # May require cluster reformation
   ```

### Issue: Service Showing Unhealthy

**Symptoms**:
- `acs health` shows service as unhealthy
- Red status in GUI
- Service not responding

**Diagnosis**:
```bash
# Check service status
acs health

# Check specific service
docker ps -a | grep <service-name>

# Check service logs
docker logs <container-id>
```

**Solutions**:

1. **Restart Service**
   ```bash
   # Restart specific service
   acs service restart <service-name>
   
   # Restart all services (last resort)
   acs service restart all
   ```

2. **Resource Exhaustion**
   ```bash
   # Check resources
   df -h
   free -m
   top
   
   # Solution: Add resources or clean up disk
   ```

3. **Database Corruption**
   ```bash
   # Restore from backup
   # Settings > Backup & Restore > Restore
   ```

### Issue: Unable to Access Web GUI

**Symptoms**:
- Cannot connect to https://<nd-ip>
- Connection timeout
- Certificate errors

**Solutions**:

1. **Check Service Status**
   ```bash
   # Verify HTTPS service running
   acs health
   
   # Check if nginx is running
   docker ps | grep nginx
   ```

2. **Certificate Issue**
   ```bash
   # Check certificate validity
   openssl s_client -connect <nd-ip>:443
   
   # Regenerate self-signed cert if needed
   # Or upload new certificate via CLI
   ```

3. **Firewall Issue**
   ```bash
   # Verify port 443 accessible
   telnet <nd-ip> 443
   
   # Check firewall rules on node
   iptables -L
   ```

---

## NDFC Application Issues

### Issue: NDFC Application Won't Install

**Symptoms**:
- Installation fails
- Installation stuck at certain percentage
- Error message during installation

**Diagnosis**:
```bash
# Check application status
# GUI: Services > Installed Apps

# Check logs
ssh admin@<nd-ip>
tail -f /var/log/acs/acs.log
```

**Solutions**:

1. **Insufficient Resources**
   - **Solution**: Allocate more resources
   ```bash
   # Check available resources
   # GUI: Infrastructure > Cluster Configuration
   
   # Increase resources:
   # - CPU: 32+ cores
   # - Memory: 128+ GB
   # - Disk: 500+ GB
   ```

2. **Corrupted Download**
   - **Solution**: Re-download application
   ```bash
   # Delete corrupted package
   # Re-download from App Store
   # Verify checksum
   ```

3. **Network Connectivity**
   - **Solution**: Check external connectivity
   ```bash
   # If downloading from internet
   ping 8.8.8.8
   
   # Check proxy settings if applicable
   ```

### Issue: NDFC GUI Not Loading

**Symptoms**:
- NDFC application shows "Healthy" but GUI won't load
- Blank page or loading spinner
- JavaScript errors in browser console

**Solutions**:

1. **Clear Browser Cache**
   ```bash
   # Clear browser cache and cookies
   # Try incognito/private mode
   # Try different browser
   ```

2. **Restart NDFC Service**
   ```bash
   # Via GUI: Services > Installed Apps
   # Select NDFC > Actions > Restart
   ```

3. **Check Persistent IP**
   ```bash
   # Verify persistent IP configured correctly
   # GUI: Services > NDFC > Configuration
   # Test connectivity to persistent IP
   ping <ndfc-persistent-ip>
   ```

---

## Switch Discovery Issues

### Issue: Switch Not Discovered

**Symptoms**:
- Switch not appearing in discovery
- Discovery completes but switch missing
- Discovery fails with error

**Diagnosis**:
```bash
# From NDFC:
# Fabric > Inventory > Discover
# Note any error messages

# From switch:
show running-config
show feature
ping <ndfc-ip>
```

**Solutions**:

1. **Connectivity Issue**
   ```bash
   # From NDFC node, test SSH
   ssh admin@<switch-ip>
   
   # From switch, test connectivity
   ping <ndfc-ip>
   
   # Check routing
   show ip route
   ```

2. **Feature Not Enabled**
   ```bash
   # On switch, enable required features
   feature nxapi
   feature ssh
   feature https
   
   # Verify
   show feature | grep enabled
   ```

3. **Credential Issue**
   ```bash
   # Verify credentials are correct
   # Try manual SSH login with same credentials
   ssh <username>@<switch-ip>
   
   # Check switch AAA configuration
   show aaa authentication
   ```

4. **POAP Enabled**
   ```bash
   # Disable POAP
   no boot poap enable
   
   # Save config
   copy running-config startup-config
   ```

### Issue: Switch Import Fails

**Symptoms**:
- Discovery successful but import fails
- Configuration compliance errors
- Switch stuck in "importing" state

**Diagnosis**:
```bash
# Check switch logs
# NDFC: Operations > Logs
# Filter by switch IP

# From switch
show logging last 100
```

**Solutions**:

1. **Configuration Conflict**
   ```bash
   # Review configuration differences
   # NDFC: Fabric > Configuration Compliance
   
   # Options:
   # a) Accept current config
   # b) Push NDFC policy
   # c) Manually resolve conflicts
   ```

2. **Software Version Incompatibility**
   ```bash
   # Check minimum supported version
   # Upgrade switch if needed
   
   # Verify version compatibility
   show version
   
   # Upgrade process:
   install all nxos <image-url>
   ```

3. **License Issue**
   ```bash
   # Check license status
   show license usage
   
   # Install required licenses
   install license <license-file>
   ```

---

## Configuration Sync Issues

### Issue: Switch Showing "Out-of-Sync"

**Symptoms**:
- Switch status: "Out-of-Sync"
- Configuration drift detected
- Deployment fails

**Diagnosis**:
```bash
# In NDFC:
# Fabric > Configuration Compliance
# Click on switch showing out-of-sync
# Review differences

# From switch:
show running-config
show startup-config
```

**Solutions**:

1. **Manual Configuration Change**
   ```bash
   # Someone made changes via CLI
   
   # Option 1: Accept changes
   # NDFC: Reconcile Configuration > Accept Running Config
   
   # Option 2: Revert changes
   # NDFC: Deploy > Push Intended Config
   
   # Option 3: Make changes in NDFC instead
   ```

2. **Deployment Failure**
   ```bash
   # Check deployment history
   # NDFC: Operations > Deployment History
   
   # Retry deployment
   # Fix any errors first
   # Redeploy configuration
   ```

3. **Configuration Drift**
   ```bash
   # Enable configuration monitoring
   # NDFC: Settings > Configuration Compliance
   # Enable drift detection
   
   # Set up alerts for drift
   ```

### Issue: Configuration Deployment Fails

**Symptoms**:
- Deployment fails with error
- Partial deployment
- Rollback occurs

**Diagnosis**:
```bash
# Check deployment logs
# NDFC: Operations > Deployment History
# Click on failed deployment
# Review error messages

# From switch:
show configuration session summary
```

**Solutions**:

1. **Syntax Error in Configuration**
   ```bash
   # Review configuration for errors
   # Test on one switch first
   # Fix syntax and redeploy
   ```

2. **Resource Constraint**
   ```bash
   # Check switch resources
   show system resources
   show hardware capacity
   
   # May need to:
   # - Clear TCAM
   # - Remove unused configs
   # - Upgrade hardware
   ```

3. **Commit Error**
   ```bash
   # Session timeout or conflict
   
   # Clear stale sessions on switch:
   clear config session <session-id>
   
   # Retry deployment
   ```

---

## Fabric Control Plane Issues

### Issue: BGP EVPN Sessions Not Establishing

**Symptoms**:
- BGP neighbor in "Idle" or "Active" state
- Route prefixes not received
- VXLAN tunnels not forming

**Diagnosis**:
```bash
# Check BGP status
show bgp l2vpn evpn summary

# Check BGP neighbor details
show bgp l2vpn evpn neighbors <neighbor-ip>

# Check routing
show ip route <neighbor-loopback>

# Check firewall
telnet <neighbor-ip> 179
```

**Solutions**:

1. **Underlay Routing Issue**
   ```bash
   # Verify underlay reachability
   ping <neighbor-loopback> source <local-loopback>
   
   # Check OSPF/IS-IS
   show ip ospf neighbors
   show isis adjacency
   
   # Fix underlay first
   ```

2. **BGP Configuration Error**
   ```bash
   # Verify BGP config
   show running-config bgp
   
   # Check:
   # - Correct ASN
   # - Correct neighbor IP (loopback)
   # - Correct update-source
   # - Address-family l2vpn evpn enabled
   
   # Fix configuration via NDFC
   ```

3. **Firewall Blocking BGP**
   ```bash
   # Check if TCP 179 is open
   telnet <neighbor-ip> 179
   
   # Check ACLs
   show ip access-lists
   
   # Remove blocking ACL
   ```

### Issue: VXLAN Tunnels Not Forming

**Symptoms**:
- NVE peers not showing up
- `show nve peers` empty
- No VXLAN encapsulation

**Diagnosis**:
```bash
# Check NVE interface
show interface nve1

# Check NVE peers
show nve peers

# Check loopback reachability
ping <remote-loopback> source loopback1

# Check multicast (if using multicast)
show ip mroute
```

**Solutions**:

1. **NVE Interface Down**
   ```bash
   # Check NVE config
   show running-config interface nve1
   
   # Ensure:
   # - no shutdown
   # - source-interface configured
   # - VNI members configured
   
   # Fix configuration
   interface nve1
     no shutdown
     source-interface loopback1
   ```

2. **Loopback Not Reachable**
   ```bash
   # Verify loopback IP reachable
   ping <remote-vtep-ip>
   
   # Check underlay routing
   show ip route <remote-vtep-ip>
   
   # Fix underlay routing
   ```

3. **VNI Configuration Mismatch**
   ```bash
   # Verify VNI configuration
   show nve vni
   
   # Ensure VNI configured on both sides
   # Check multicast group matches
   # Fix VNI configuration via NDFC
   ```

### Issue: MAC Address Not Learning

**Symptoms**:
- Hosts cannot communicate
- MAC address table empty
- Ping fails between hosts

**Diagnosis**:
```bash
# Check local MAC learning
show mac address-table

# Check EVPN MAC learning
show l2route evpn mac all

# Check BGP EVPN routes
show bgp l2vpn evpn

# Check interface status
show interface status
```

**Solutions**:

1. **Interface Issue**
   ```bash
   # Check interface status
   show interface ethernet x/y
   
   # Verify:
   # - Interface up
   # - No errors
   # - VLAN assigned
   
   # Fix interface issue
   ```

2. **VLAN/VNI Mapping Issue**
   ```bash
   # Check VLAN configuration
   show vlan id <vlan-id>
   
   # Check VNI mapping
   vlan <vlan-id>
     vn-segment <vni>
   
   # Ensure consistent across fabric
   ```

3. **BGP EVPN Not Advertising**
   ```bash
   # Check route advertisement
   show bgp l2vpn evpn vni-id <vni>
   
   # Verify route-target
   show bgp l2vpn evpn route-target
   
   # Fix BGP configuration
   ```

---

## VXLAN Data Plane Issues

### Issue: Packet Loss Across VXLAN

**Symptoms**:
- Intermittent packet loss
- High latency
- Connectivity issues

**Diagnosis**:
```bash
# Check interface counters
show interface counters errors

# Check for drops
show hardware internal errors

# Check VXLAN counters
show interface nve1 counters

# Check underlay utilization
show interface ethernet x/y counters
```

**Solutions**:

1. **MTU Mismatch**
   ```bash
   # Check MTU on underlay
   show interface ethernet x/y
   
   # Set to 9216 for jumbo frames
   interface ethernet x/y
     mtu 9216
   
   # Verify end-to-end
   ping <remote-host> df-bit packet-size 9000
   ```

2. **Congestion/Oversubscription**
   ```bash
   # Check interface utilization
   show interface ethernet x/y counters rate
   
   # Check for drops
   show interface counters discards
   
   # Solutions:
   # - Add bandwidth
   # - Enable ECMP for load balancing
   # - Implement QoS
   ```

3. **Hardware Issue**
   ```bash
   # Check for hardware errors
   show hardware internal errors
   show logging | include ERROR
   
   # May need RMA if hardware fault
   # Contact Cisco TAC
   ```

### Issue: Asymmetric Routing

**Symptoms**:
- Traffic works in one direction only
- Traceroute shows different paths
- Session establishment fails

**Diagnosis**:
```bash
# Trace path in both directions
traceroute <destination>
# From destination back to source

# Check routing table
show ip route <destination>

# Check BGP paths
show bgp vrf <vrf> ipv4 unicast <prefix>
```

**Solutions**:

1. **BGP Path Selection**
   ```bash
   # Adjust BGP attributes
   # Use route-maps to prefer certain paths
   
   # Check current selection
   show bgp vrf <vrf> ipv4 unicast <prefix>
   
   # Adjust via NDFC policies
   ```

2. **ECMP Hash Distribution**
   ```bash
   # Verify ECMP enabled
   show feature | include ecmp
   
   # Check hash algorithm
   show port-channel load-balance
   
   # Adjust if needed
   port-channel load-balance src-dst ip-l4port
   ```

---

## Performance Issues

### Issue: High CPU Utilization

**Symptoms**:
- CPU consistently >80%
- Slow response times
- Control plane instability

**Diagnosis**:
```bash
# Check CPU usage
show processes cpu sort

# Check top processes
top

# Check specific features
show system resources
```

**Solutions**:

1. **Control Plane Policing**
   ```bash
   # Check CoPP policies
   show copp status
   
   # Tune CoPP if needed
   # May need to rate-limit certain protocols
   ```

2. **Excessive Logging**
   ```bash
   # Reduce logging level
   logging level <facility> <level>
   
   # Disable debug logging
   no debug all
   ```

3. **Software Bug**
   ```bash
   # Check for known bugs
   # Upgrade to recommended version
   # Open TAC case if needed
   ```

### Issue: High Memory Utilization

**Symptoms**:
- Memory >90%
- Out of memory errors
- Service crashes

**Diagnosis**:
```bash
# Check memory usage
show system resources

# Check memory details
show system internal mem allocator

# Identify memory consumers
show processes memory sort
```

**Solutions**:

1. **Clear Unnecessary Data**
   ```bash
   # Clear logs
   clear logging logfile
   
   # Clear cores
   delete bootflash:core.*
   
   # Clear unused files
   delete bootflash:/*old*
   ```

2. **Reduce Feature Set**
   ```bash
   # Disable unused features
   no feature <feature-name>
   
   # Scale down configurations
   # Review and optimize policies
   ```

---

## Authentication and Access Issues

### Issue: Cannot Login to NDFC

**Symptoms**:
- Login fails
- "Invalid credentials" error
- Account locked

**Solutions**:

1. **Reset Local Password**
   ```bash
   # SSH to Nexus Dashboard
   ssh rescue-user@<nd-ip>
   
   # Reset admin password
   acs password reset admin
   ```

2. **AAA Server Down**
   ```bash
   # Check AAA server connectivity
   ping <aaa-server-ip>
   
   # Use local fallback
   # Login with local admin account
   ```

3. **Account Locked**
   ```bash
   # Unlock account
   # SSH to ND
   acs user unlock <username>
   ```

### Issue: TACACS+ Authentication Failing

**Symptoms**:
- TACACS users cannot login
- Local users can login
- "Authentication failed" error

**Diagnosis**:
```bash
# Check TACACS configuration
show tacacs-server

# Test TACACS connectivity
test aaa server tacacs+ <server-ip>

# Check logs
show logging | include AAA
```

**Solutions**:

1. **Shared Secret Mismatch**
   ```bash
   # Verify shared secret matches
   # On NDFC: Settings > AAA > TACACS+
   # Update shared secret
   
   # On TACACS server: verify secret
   ```

2. **Server Unreachable**
   ```bash
   # Test connectivity
   ping <tacacs-server-ip>
   telnet <tacacs-server-ip> 49
   
   # Check firewall rules
   ```

3. **User Not in TACACS Database**
   ```bash
   # Verify user exists on TACACS server
   # Check group membership
   # Verify privilege level
   ```

---

## Getting Additional Help

### Collect Diagnostic Information

**From Nexus Dashboard**:
```bash
# Generate tech-support
acs support
# File will be saved to /data/acs/

# Download via GUI:
# Settings > Support > Tech Support
```

**From NDFC**:
```bash
# Collect NDFC logs
# GUI: Settings > Support > Collect Support Info
```

**From Switches**:
```bash
# Generate tech-support
show tech-support > bootflash:techsupport.txt

# Copy to NDFC/server
copy bootflash:techsupport.txt scp://<server-ip>/path/
```

### Contact Cisco TAC

**Before Opening Case**:
- Collect all tech-support files
- Document problem symptoms
- Note when problem started
- List any recent changes
- Have contract information ready

**Open TAC Case**:
- Web: https://mycase.cloudapps.cisco.com/case
- Phone: 1-800-553-2447 (US)
- Severity levels:
  - S1: Production down
  - S2: Production severely degraded
  - S3: Non-critical functionality affected
  - S4: Information/enhancement request

---

## Useful Commands Reference

### Nexus Dashboard
```bash
acs health                          # Check cluster health
acs cluster status                  # Check cluster status
acs service restart <service>       # Restart service
acs show nodes                      # List cluster nodes
acs password reset <user>           # Reset password
```

### NDFC Verification
```bash
# Via GUI:
Operations > Fabric > Health        # Fabric health
Fabric > Inventory                  # Switch status
Operations > Topology               # Topology view
Operations > Deployment History     # Deployment logs
```

### Switch Diagnostics
```bash
show bgp l2vpn evpn summary        # BGP EVPN status
show nve peers                      # VXLAN peers
show vpc status                     # vPC status
show vlan                           # VLAN database
show interface status               # Interface status
show system resources               # Resource utilization
show logging last 100               # Recent logs
```

---

## References

- [Nexus Dashboard Troubleshooting Guide](https://www.cisco.com/c/en/us/td/docs/dcn/nd/2x/troubleshooting/cisco-nexus-dashboard-troubleshooting-guide.html)
- [NDFC Troubleshooting Guide](https://www.cisco.com/c/en/us/support/cloud-systems-management/prime-data-center-network-manager/products-troubleshooting-guides-list.html)
- [VXLAN EVPN Troubleshooting](https://www.cisco.com/c/en/us/support/docs/switches/nexus-9000-series-switches/213920-troubleshoot-vxlan-bgp-evpn-control-and.html)
