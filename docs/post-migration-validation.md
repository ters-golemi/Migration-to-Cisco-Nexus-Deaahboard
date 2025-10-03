# Post-Migration Validation Guide

## Table of Contents
1. [Overview](#overview)
2. [Nexus Dashboard Validation](#nexus-dashboard-validation)
3. [Fabric Controller Validation](#fabric-controller-validation)
4. [Fabric Health Validation](#fabric-health-validation)
5. [Network Functionality Validation](#network-functionality-validation)
6. [Performance Validation](#performance-validation)
7. [Security Validation](#security-validation)
8. [Operational Validation](#operational-validation)
9. [Sign-Off Checklist](#sign-off-checklist)

## Overview

This guide provides comprehensive validation procedures to confirm successful migration to Nexus Dashboard. All validations must pass before declaring the migration complete.

### Validation Timeline
- **Immediate** (0-2 hours): Critical functionality checks
- **Short-term** (2-24 hours): Stability and performance monitoring
- **Medium-term** (1-7 days): Ongoing monitoring and optimization
- **Long-term** (7-30 days): Final validation and optimization

---

## Nexus Dashboard Validation

### Cluster Health

#### Check Cluster Status
```bash
# SSH to any Nexus Dashboard node
ssh admin@<nd-node-ip>

# Check overall health
acs health

# Expected output:
# All services: healthy
# All nodes: healthy
# Cluster state: converged
```

**Expected Results**:
- [ ] All services show "healthy"
- [ ] All nodes show "healthy"
- [ ] Cluster state is "converged"
- [ ] No critical alerts

#### Verify Node Communication
```bash
# Check inter-node communication
acs cluster status

# Verify all nodes listed
acs show nodes
```

**Validation Checklist**:
- [ ] All 3 nodes visible in cluster
- [ ] All nodes show "up" status
- [ ] No network partitioning detected
- [ ] Latency between nodes <50ms

### Application Services

#### Verify NDFC Service
1. Login to Nexus Dashboard GUI
2. Navigate to Services > Installed Apps
3. Verify NDFC status

**Expected Results**:
- [ ] NDFC status: "Healthy"
- [ ] NDFC version displayed correctly
- [ ] Resource allocation correct
- [ ] Persistent IP accessible

#### Access NDFC Application
1. Click on NDFC application
2. Click "Open" to launch NDFC GUI
3. Login with credentials

**Validation Checklist**:
- [ ] NDFC GUI accessible
- [ ] Login successful
- [ ] Dashboard loads without errors
- [ ] No JavaScript errors in browser console

---

## Fabric Controller Validation

### Fabric Status

#### Check Fabric Health
1. In NDFC, navigate to Operations > Fabric > Health
2. Review overall fabric health score

**Expected Results**:
- [ ] Fabric health score >90%
- [ ] No critical alarms
- [ ] All fabrics visible
- [ ] Topology diagram complete

#### Verify Switch Inventory
1. Navigate to Fabric > Inventory
2. Review all imported switches

**Validation Checklist**:
- [ ] All switches showing "In-Sync" status
- [ ] Switch roles correct (spine/leaf)
- [ ] Software versions displayed
- [ ] Management IPs correct
- [ ] No switches showing errors

### Configuration Compliance

#### Check Configuration Sync
1. Navigate to Fabric > Configuration Compliance
2. Review compliance status for all switches

**Expected Results**:
- [ ] All switches "In-Sync" with NDFC
- [ ] No configuration drift
- [ ] Intended configuration matches running config
- [ ] No pending configurations

#### Verify Policy Deployment
1. Navigate to Fabric > Policies
2. Check policy deployment status

**Validation Checklist**:
- [ ] All policies deployed successfully
- [ ] No failed policy deployments
- [ ] Policy templates loaded correctly
- [ ] Policy associations correct

---

## Fabric Health Validation

### Control Plane Validation

#### BGP EVPN Status

**From NDFC**:
1. Navigate to Operations > Routing > BGP
2. Verify all BGP sessions

**From Switch CLI**:
```bash
# Check BGP summary
show bgp l2vpn evpn summary

# Verify expected output:
# All neighbors in "Established" state
# Route counts match expected values
```

**Validation Checklist**:
- [ ] All BGP sessions "Established"
- [ ] Route counts stable
- [ ] No BGP flapping detected
- [ ] Prefix advertisements correct

#### VXLAN Control Plane

**From NDFC**:
1. Navigate to Operations > Overlay
2. Check NVE peers status

**From Switch CLI**:
```bash
# Check NVE peers
show nve peers

# Verify all expected peers are UP
# Check peer state
show nve interface nve1

# Verify tunnel status
show nve vni
```

**Expected Results**:
- [ ] All NVE peers showing "UP"
- [ ] Peer count matches expected
- [ ] VNI mappings correct
- [ ] No tunnel flapping

#### Underlay Routing (OSPF/IS-IS)

**From Switch CLI**:
```bash
# For OSPF
show ip ospf neighbors

# For IS-IS
show isis adjacency

# Verify all neighbors in Full/Up state
```

**Validation Checklist**:
- [ ] All underlay neighbors up
- [ ] No adjacency flapping
- [ ] Route counts correct
- [ ] No routing loops detected

### Data Plane Validation

#### VLAN/VNI Mapping

**From NDFC**:
1. Navigate to Fabric > Networks
2. Verify all VLANs/VNIs

**From Switch CLI**:
```bash
# Check VLAN database
show vlan

# Check VNI mappings
show vxlan

# Verify L2VNI
show nve vni

# Verify L3VNI
show bgp l2vpn evpn summary
```

**Expected Results**:
- [ ] All VLANs configured correctly
- [ ] All VNIs mapped to correct VLANs
- [ ] L3VNI operational for each VRF
- [ ] No orphan VNIs or VLANs

#### VRF Configuration

**From NDFC**:
1. Navigate to Fabric > VRFs
2. Verify all VRFs deployed

**From Switch CLI**:
```bash
# Check VRF list
show vrf

# Check VRF routes
show ip route vrf <vrf-name>

# Verify VRF interfaces
show vrf <vrf-name> interface
```

**Validation Checklist**:
- [ ] All VRFs operational
- [ ] L3VNI assigned to each VRF
- [ ] Route targets correct
- [ ] Inter-VRF routing working (if configured)

#### MAC Address Learning

**From Switch CLI**:
```bash
# Check MAC address table
show mac address-table

# Check MAC addresses in VXLAN
show l2route evpn mac all

# Verify MAC sync between peers
show l2route evpn mac-ip all
```

**Expected Results**:
- [ ] MAC addresses learning correctly
- [ ] No duplicate MAC addresses
- [ ] MAC synchronization working
- [ ] No MAC flapping detected

#### ARP/ND Table

**From Switch CLI**:
```bash
# Check ARP table
show ip arp vrf <vrf-name>

# Check IPv6 neighbor discovery
show ipv6 neighbor vrf <vrf-name>

# Verify distributed anycast gateway
show ip arp suppression-cache detail
```

**Validation Checklist**:
- [ ] ARP entries populated
- [ ] Anycast gateway operational
- [ ] ARP suppression working (if enabled)
- [ ] No ARP resolution issues

### High Availability Validation

#### vPC Status

**From Switch CLI**:
```bash
# Check vPC status
show vpc

# Verify vPC consistency
show vpc consistency-parameters global

# Check vPC peer-link
show vpc peer-keepalive

# Verify vPC ports
show vpc brief
```

**Expected Results**:
- [ ] vPC peer-link operational
- [ ] vPC role correctly established
- [ ] All vPC ports up
- [ ] No vPC consistency errors
- [ ] Peer-keepalive active

#### Multi-Site (if applicable)

**From NDFC**:
1. Navigate to Multi-Site view
2. Verify site connectivity

**Validation Checklist**:
- [ ] All sites visible
- [ ] Inter-site links operational
- [ ] DCI connectivity working
- [ ] Stretched VNIs operational

---

## Network Functionality Validation

### Layer 2 Connectivity

#### VLAN Connectivity Test

**Test Procedure**:
1. Select two hosts in same VLAN, different leaf switches
2. Test connectivity

```bash
# From host 1
ping <host-2-ip>

# Verify response
# Expected: 0% packet loss
```

**Validation Matrix**:

| VLAN | Host 1 | Host 2 | Result | Latency |
|------|--------|--------|--------|---------|
| 100  | ✓      | ✓      | PASS   | <1ms    |
| 200  | ✓      | ✓      | PASS   | <1ms    |
| 300  | ✓      | ✓      | PASS   | <1ms    |

**Expected Results**:
- [ ] All VLAN tests pass
- [ ] 0% packet loss
- [ ] Latency acceptable (<2ms intra-DC)
- [ ] MTU size correct (jumbo frames if configured)

### Layer 3 Connectivity

#### Inter-VLAN Routing Test

```bash
# From host in VLAN 100
ping <host-in-vlan-200-ip>

# Verify anycast gateway
traceroute <host-in-vlan-200-ip>

# Expected: First hop is anycast gateway
```

**Validation Checklist**:
- [ ] Inter-VLAN routing working
- [ ] Anycast gateway responding
- [ ] Symmetric IRB working
- [ ] Traffic load-balanced across spines

#### VRF Isolation Test

```bash
# Test isolation between VRFs
# From VRF-1:
ping <host-in-vrf-2> vrf VRF-1

# Expected: No connectivity (unless route-leaking configured)
```

**Expected Results**:
- [ ] VRF isolation working
- [ ] No cross-VRF leaking (unless intended)
- [ ] VRF route leaking working (if configured)

### External Connectivity

#### Border Gateway Test

```bash
# Check external routes
show ip route vrf <vrf-name>

# Verify external BGP
show bgp vrf <vrf-name> ipv4 unicast summary

# Test external connectivity
ping <external-ip> vrf <vrf-name>
```

**Validation Checklist**:
- [ ] External routes learned
- [ ] Border leaf BGP sessions up
- [ ] External connectivity working
- [ ] Route redistribution correct

#### Internet Connectivity Test

```bash
# From end host
ping 8.8.8.8
traceroute 8.8.8.8

# Verify NAT (if applicable)
# Check firewall traversal
```

**Expected Results**:
- [ ] Internet connectivity working
- [ ] NAT operational (if configured)
- [ ] Default route correct
- [ ] Return traffic working

---

## Performance Validation

### Baseline Metrics

#### Capture Performance Baseline

**From NDFC**:
1. Navigate to Operations > Telemetry
2. Capture baseline metrics:
   - Interface throughput
   - CPU utilization
   - Memory utilization
   - Packet rates
   - Latency

**Baseline Checklist**:
- [ ] CPU utilization <50% on all switches
- [ ] Memory utilization <75%
- [ ] Interface utilization <70%
- [ ] No interface errors
- [ ] No packet drops

#### Throughput Testing

**Test Procedure**:
```bash
# Use iperf or similar tool
# Server side:
iperf3 -s

# Client side:
iperf3 -c <server-ip> -t 60 -P 10

# Test various scenarios:
# - Intra-VLAN
# - Inter-VLAN
# - Cross-site (if multi-site)
```

**Performance Targets**:
- [ ] Line-rate throughput achieved
- [ ] No packet loss under load
- [ ] Jitter <1ms
- [ ] CPU impact minimal during testing

### Latency Testing

```bash
# ICMP latency test
ping -c 1000 <remote-host>

# Calculate statistics:
# - Average latency
# - Maximum latency
# - Jitter
```

**Expected Results**:
- [ ] Average latency <1ms (intra-DC)
- [ ] Maximum latency <3ms
- [ ] Jitter <0.5ms
- [ ] No timeout packets

---

## Security Validation

### Access Control

#### Authentication Test

```bash
# Test local authentication
ssh admin@<switch-ip>

# Test AAA authentication
ssh <aaa-user>@<switch-ip>

# Test NDFC authentication
# Login via GUI with different user roles
```

**Validation Checklist**:
- [ ] Local authentication working
- [ ] AAA authentication working
- [ ] TACACS+ authorization working
- [ ] RBAC roles enforced

#### Certificate Validation

**From NDFC**:
1. Check SSL certificate validity
2. Verify certificate chain
3. Test HTTPS connectivity

**Expected Results**:
- [ ] Valid SSL certificate installed
- [ ] Certificate chain complete
- [ ] No certificate warnings
- [ ] Secure connections only

### Policy Enforcement

#### ACL Validation

```bash
# Test ACL enforcement
# From restricted host:
telnet <blocked-ip> <blocked-port>

# Expected: Connection refused/timeout
```

**Validation Checklist**:
- [ ] ACLs deployed correctly
- [ ] Blocked traffic denied
- [ ] Allowed traffic permitted
- [ ] ACL counters incrementing

---

## Operational Validation

### Monitoring and Alerts

#### Telemetry Validation

**From NDFC**:
1. Navigate to Operations > Telemetry
2. Verify data collection

**Validation Checklist**:
- [ ] Telemetry streaming active
- [ ] Metrics being collected
- [ ] No collection errors
- [ ] Historical data available

#### Alert Configuration

```bash
# Trigger test alert
# Example: Generate high CPU alert

# Verify alert received:
# - Email notification
# - Syslog entry
# - SNMP trap
# - Dashboard notification
```

**Expected Results**:
- [ ] Alerts triggering correctly
- [ ] Notifications received
- [ ] Alert severity correct
- [ ] Alert clearing working

### Backup and Restore

#### Configuration Backup

**From NDFC**:
1. Navigate to Settings > Backup & Restore
2. Trigger manual backup
3. Verify backup completion

**Validation Checklist**:
- [ ] Manual backup successful
- [ ] Backup file accessible
- [ ] Backup includes all switches
- [ ] Scheduled backup configured

#### Test Restore (Non-Production)

```bash
# In test environment only:
# Restore from backup
# Verify configuration restored correctly
```

### Change Management

#### Deploy Test Change

**Test Procedure**:
1. Create simple configuration change
2. Deploy via NDFC
3. Verify change applied
4. Check audit trail

**Validation Checklist**:
- [ ] Change deployed successfully
- [ ] Configuration in-sync
- [ ] Audit trail captured
- [ ] Rollback capability verified

---

## Sign-Off Checklist

### Critical Validations (Must Pass)

- [ ] All Nexus Dashboard nodes healthy
- [ ] NDFC application operational
- [ ] All switches discovered and in-sync
- [ ] No configuration drift
- [ ] BGP EVPN sessions established
- [ ] VXLAN tunnels operational
- [ ] All VLANs/VNIs operational
- [ ] Layer 2 connectivity working
- [ ] Layer 3 connectivity working
- [ ] vPC operational (if applicable)
- [ ] External connectivity working
- [ ] No critical alarms
- [ ] Monitoring operational
- [ ] Backup procedures working

### Performance Validations

- [ ] Baseline metrics captured
- [ ] Performance within acceptable range
- [ ] No degradation from pre-migration
- [ ] Throughput testing passed
- [ ] Latency testing passed

### Security Validations

- [ ] Authentication working
- [ ] Authorization working
- [ ] SSL certificates valid
- [ ] ACLs enforced
- [ ] Audit logging active

### Operational Validations

- [ ] Team trained on new system
- [ ] Documentation updated
- [ ] Runbooks updated
- [ ] Monitoring dashboards configured
- [ ] Alert rules configured
- [ ] Backup schedule active

---

## Validation Reports

### Daily Health Check (First Week)

**Checklist**:
- [ ] Review overnight alerts
- [ ] Check switch status
- [ ] Verify BGP stability
- [ ] Check VXLAN tunnels
- [ ] Review configuration compliance
- [ ] Check backup completion
- [ ] Review performance metrics

### Weekly Review (First Month)

**Checklist**:
- [ ] Comprehensive health check
- [ ] Performance trend analysis
- [ ] Capacity planning review
- [ ] Policy compliance review
- [ ] Security audit
- [ ] Backup integrity check
- [ ] Documentation updates

---

## Validation Documentation

### Required Documentation

Create and maintain the following:

1. **Validation Test Results**:
   - All test outputs
   - Screenshots of key validations
   - Performance baseline data
   - Comparison with pre-migration

2. **Issue Log**:
   - Any issues discovered
   - Resolution steps
   - Impact assessment
   - Preventive measures

3. **Sign-Off Document**:
   - Validation completion date
   - Team signatures
   - Outstanding items
   - Recommendations

---

## Troubleshooting Failed Validations

If any validation fails, refer to:
1. [Troubleshooting Guide](troubleshooting.md)
2. [Rollback Procedures](rollback-procedures.md) (if critical)

---

## Sign-Off

### Validation Completion

| Validation Category | Status | Comments | Validated By | Date |
|---------------------|--------|----------|--------------|------|
| Nexus Dashboard | ☐ Pass ☐ Fail | | | |
| Fabric Controller | ☐ Pass ☐ Fail | | | |
| Fabric Health | ☐ Pass ☐ Fail | | | |
| Network Functionality | ☐ Pass ☐ Fail | | | |
| Performance | ☐ Pass ☐ Fail | | | |
| Security | ☐ Pass ☐ Fail | | | |
| Operations | ☐ Pass ☐ Fail | | | |

### Final Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Network Engineer | _____________ | _____________ | __/__/____ |
| Network Architect | _____________ | _____________ | __/__/____ |
| Operations Manager | _____________ | _____________ | __/__/____ |

---

## Next Steps

After successful validation:
1. Transition to normal operations
2. Schedule optimization review (30 days)
3. Conduct lessons learned session
4. Update operational procedures
5. Archive migration documentation

---

**Document Version**: 1.0  
**Last Updated**: [Date]  
**Validated By**: [Name]
