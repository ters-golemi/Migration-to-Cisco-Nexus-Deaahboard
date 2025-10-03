# Rollback Procedures

## Table of Contents
1. [Overview](#overview)
2. [Rollback Decision Criteria](#rollback-decision-criteria)
3. [Emergency Rollback](#emergency-rollback)
4. [Planned Rollback](#planned-rollback)
5. [Partial Rollback](#partial-rollback)
6. [Post-Rollback Validation](#post-rollback-validation)
7. [Lessons Learned](#lessons-learned)

---

## Overview

This document provides procedures for rolling back the migration to Nexus Dashboard. Rollback procedures are designed to restore the environment to its pre-migration state with minimal downtime.

### Rollback Objectives
- Restore fabric to operational state
- Minimize service disruption
- Preserve data integrity
- Document issues for resolution

### Rollback Timeline
- **Emergency Rollback**: 2-4 hours
- **Planned Rollback**: 4-6 hours
- **Partial Rollback**: 1-2 hours per switch

### Prerequisites
- Complete configuration backups available
- Team members on standby
- Communication channels open
- Rollback approval obtained (if planned)

---

## Rollback Decision Criteria

### Critical Issues Requiring Immediate Rollback

Initiate emergency rollback if any of the following occur:

1. **Complete Fabric Failure**
   - [ ] Multiple switches unreachable
   - [ ] Control plane completely down
   - [ ] Data plane not forwarding traffic
   - [ ] Critical services offline >15 minutes

2. **Data Loss or Corruption**
   - [ ] Configuration corruption detected
   - [ ] Data plane state inconsistent
   - [ ] MAC/ARP table corruption
   - [ ] Route table corruption

3. **Severe Performance Degradation**
   - [ ] Packet loss >5%
   - [ ] Latency >100ms (intra-DC)
   - [ ] Control plane CPU >95% sustained
   - [ ] Memory exhaustion

4. **Security Breach**
   - [ ] Unauthorized access detected
   - [ ] Configuration tampering
   - [ ] Security policy failure
   - [ ] Credential compromise

5. **Inability to Manage Fabric**
   - [ ] Cannot access >50% of switches
   - [ ] Cannot deploy critical changes
   - [ ] NDFC completely unresponsive
   - [ ] No management access available

### Non-Critical Issues (Troubleshoot First)

Consider troubleshooting before rollback:

- Individual switch discovery failures
- Minor configuration drift
- Non-critical feature issues
- Performance within acceptable limits
- Cosmetic GUI issues

---

## Emergency Rollback

Use this procedure when immediate rollback is required due to critical issues.

### Phase 1: Incident Declaration (5 minutes)

#### Step 1: Assess Situation
```bash
# Quick health checks
show bgp l2vpn evpn summary
show nve peers
show vpc status
show system resources

# Document current state
# Take screenshots
# Save show tech-support
```

#### Step 2: Declare Rollback
- [ ] Notify team via communication channel
- [ ] Activate emergency procedures
- [ ] Assign roles and responsibilities
- [ ] Start incident log

#### Step 3: Get Approval
- [ ] Contact change manager
- [ ] Brief management (if time permits)
- [ ] Document decision rationale

### Phase 2: Disable NDFC Management (10 minutes)

#### Step 1: Set NDFC to Read-Only
```bash
# In NDFC GUI:
# 1. Navigate to Fabric Settings
# 2. Set to "Monitor Mode" or "Read-Only"
# 3. Confirm no pending deployments
```

#### Step 2: Cancel Pending Operations
- [ ] Cancel any in-progress deployments
- [ ] Clear configuration sessions
- [ ] Stop automated tasks

### Phase 3: Restore Switch Configurations (60-90 minutes)

#### Step 1: Prepare for Restoration

```bash
# Verify backup files accessible
ls -l /backup/location/

# Verify TFTP/SCP server reachable
ping <backup-server-ip>

# Calculate restoration order:
# 1. Spine switches first
# 2. Border leaf switches
# 3. Access leaf switches
```

#### Step 2: Restore Configuration Per Switch

**For Each Switch** (in order):

```bash
# 1. Connect to switch via console (preferred) or SSH
ssh admin@<switch-ip>

# 2. Copy backup configuration
copy scp://backup-server/switch1-backup.cfg running-config vrf management

# Or if using TFTP:
copy tftp://backup-server/switch1-backup.cfg running-config vrf management

# 3. Verify configuration loaded
show running-config

# 4. Save to startup
copy running-config startup-config

# 5. Verify services
show bgp l2vpn evpn summary
show nve peers
show vpc status

# 6. Document completion time
```

**Restoration Script** (if using automation):

```python
#!/usr/bin/env python3
# restore_configs.py

import paramiko
import time
from datetime import datetime

switches = [
    {'ip': '10.1.1.1', 'role': 'spine', 'backup': 'spine1-backup.cfg'},
    {'ip': '10.1.1.2', 'role': 'spine', 'backup': 'spine2-backup.cfg'},
    {'ip': '10.1.1.11', 'role': 'leaf', 'backup': 'leaf1-backup.cfg'},
    # Add all switches
]

def restore_switch_config(switch_ip, backup_file):
    """Restore configuration to a switch"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(switch_ip, username='admin', password='password')
        
        # Execute restore command
        command = f'copy scp://server/{backup_file} running-config vrf management'
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Wait for completion
        stdout.channel.recv_exit_status()
        
        # Save configuration
        stdin, stdout, stderr = ssh.exec_command('copy run start')
        stdout.channel.recv_exit_status()
        
        print(f"[{datetime.now()}] Successfully restored {switch_ip}")
        return True
        
    except Exception as e:
        print(f"[{datetime.now()}] Error restoring {switch_ip}: {str(e)}")
        return False
    finally:
        ssh.close()

# Restore in order: spines first, then leafs
for switch in sorted(switches, key=lambda x: x['role']):
    print(f"\nRestoring {switch['ip']} ({switch['role']})...")
    restore_switch_config(switch['ip'], switch['backup'])
    time.sleep(10)  # Wait between switches

print("\n=== Restoration Complete ===")
```

#### Step 3: Verify Fabric Convergence

After restoring all switches:

```bash
# On each spine, verify BGP
show bgp l2vpn evpn summary

# Verify all neighbors in Established state
# Expected: All leaf switches as neighbors

# On each leaf, verify VXLAN
show nve peers

# Verify all expected peers present
# Verify tunnels operational

# Check vPC status (if applicable)
show vpc status

# Verify consistency
show vpc consistency-parameters global
```

### Phase 4: Restore Services (30 minutes)

#### Step 1: Verify Control Plane

```bash
# Check BGP EVPN routes
show bgp l2vpn evpn
show bgp l2vpn evpn summary

# Verify route counts match pre-migration
# Check for any missing routes

# Verify underlay routing
show ip route summary
show ip ospf neighbors
# or
show isis adjacency
```

#### Step 2: Verify Data Plane

```bash
# Test Layer 2 connectivity
# From test host in each VLAN
ping <host-in-same-vlan>

# Test Layer 3 connectivity
ping <host-in-different-vlan>

# Test external connectivity
ping <external-host>

# Verify MAC learning
show mac address-table
show l2route evpn mac all
```

#### Step 3: Verify High Availability

```bash
# Check vPC status
show vpc

# Verify:
# - Peer link operational
# - Role established correctly
# - All vPC ports up
# - Consistency check passed

# Test failover (if time permits)
# Reload one vPC peer
# Verify traffic continues
```

### Phase 5: Validate Rollback (30 minutes)

#### Validation Checklist

- [ ] All switches accessible
- [ ] All BGP sessions established
- [ ] All VXLAN tunnels up
- [ ] All vPC pairs operational
- [ ] Layer 2 connectivity working
- [ ] Layer 3 connectivity working
- [ ] External connectivity working
- [ ] No configuration errors
- [ ] No packet loss
- [ ] Performance acceptable

#### Document Rollback

```bash
# Capture final state
show tech-support > bootflash:post-rollback-tech.txt

# Document:
# - Start time
# - End time
# - Issues encountered
# - Resolution steps
# - Final status
```

---

## Planned Rollback

Use this procedure for non-emergency rollback situations.

### Prerequisites
- Change control approval
- Scheduled maintenance window
- Team availability confirmed
- Communication plan activated

### Rollback Steps

#### Step 1: Preparation (1 hour)

```bash
# 1. Final backup before rollback
# Take snapshot of current state
show tech-support > bootflash:pre-rollback-tech.txt

# 2. Document NDFC state
# Take screenshots of:
# - Fabric topology
# - Switch inventory
# - Configuration compliance
# - Active alerts

# 3. Verify backup files
ls -l /backup/location/
md5sum /backup/location/*.cfg

# 4. Notify stakeholders
# Send notification email
# Update status page
```

#### Step 2: Graceful NDFC Shutdown (30 minutes)

```bash
# 1. Disable automated tasks
# NDFC: Settings > Scheduler
# Disable all scheduled tasks

# 2. Cancel pending deployments
# NDFC: Operations > Deployment History
# Cancel any pending/in-progress deployments

# 3. Export NDFC configuration (optional)
# NDFC: Settings > Backup & Restore
# Create final backup

# 4. Set fabric to read-only
# NDFC: Fabric Settings > Mode: Monitor
```

#### Step 3: Configuration Restoration (2-3 hours)

Follow the same steps as Emergency Rollback Phase 3, but with more time for validation between switches.

**Enhanced Per-Switch Procedure**:

```bash
# For each switch (with extended validation):

# 1. Pre-restoration checks
show running-config | include "hostname|interface|vlan|vrf"

# 2. Restore configuration
copy scp://server/backup.cfg running-config

# 3. Validate specific features
show bgp l2vpn evpn summary
show nve peers
show vlan brief
show vrf

# 4. Test connectivity
ping <next-hop>
ping <test-host>

# 5. Monitor for 5 minutes
# Watch for any instability

# 6. Save configuration
copy running-config startup-config

# 7. Proceed to next switch
```

#### Step 4: Comprehensive Validation (1-2 hours)

Perform thorough validation as documented in [Post-Migration Validation](post-migration-validation.md), including:

- [ ] Control plane validation
- [ ] Data plane validation
- [ ] High availability validation
- [ ] Performance validation
- [ ] Security validation

#### Step 5: NDFC Decommission (optional)

If not reusing Nexus Dashboard:

```bash
# 1. Uninstall NDFC application
# Nexus Dashboard GUI: Services > NDFC > Uninstall

# 2. Remove switch discovery records
# Clean up any NDFC-specific configuration

# 3. Decommission Nexus Dashboard cluster (if desired)
# Power off nodes
# Deallocate resources
```

---

## Partial Rollback

Use when only specific switches or features need rollback.

### Scenario 1: Rollback Single Switch

**When to Use**:
- Single switch issues
- Import failure on one switch
- Configuration corruption on one switch

**Procedure**:

```bash
# 1. Identify problematic switch
# NDFC: Fabric > Inventory
# Note switch with issues

# 2. Remove from NDFC management
# NDFC: Fabric > Inventory > Switch > Delete

# 3. Restore configuration
ssh admin@<switch-ip>
copy scp://server/switch-backup.cfg running-config

# 4. Verify independently
show bgp l2vpn evpn summary
show nve peers

# 5. Re-import to NDFC (if resolved)
# Or leave in CLI management mode
```

### Scenario 2: Rollback Specific Feature

**When to Use**:
- New policy causing issues
- Feature configuration error
- Partial deployment failure

**Procedure**:

```bash
# 1. Identify affected configuration
# Review deployment history
# Identify changes made

# 2. Revert specific configuration
# Option A: Via NDFC (if possible)
# Rollback to previous policy version

# Option B: Via CLI
ssh admin@<switch-ip>
configure terminal
# Remove specific configuration
# Or restore specific section from backup

# 3. Validate feature operation
# Test affected functionality

# 4. Update NDFC (if needed)
# Reconcile configuration
```

### Scenario 3: Rollback Network Changes

**When to Use**:
- VLAN/VNI issues
- VRF configuration problems
- Routing policy issues

**Procedure**:

```bash
# 1. Document current network state
show vlan
show vni
show vrf

# 2. Remove new networks from NDFC
# NDFC: Fabric > Networks > Delete

# 3. Restore previous network configuration
# From backup or via CLI

# 4. Verify network operation
# Test connectivity per VLAN/VRF

# 5. Re-add to NDFC when ready
```

---

## Post-Rollback Validation

### Immediate Validation (0-2 hours)

```bash
# Critical Services Check
- [ ] All switches reachable
- [ ] Control plane operational
- [ ] Data plane forwarding
- [ ] No critical alerts
- [ ] Basic connectivity working

# Quick Tests
ping <test-hosts>
show bgp l2vpn evpn summary
show nve peers
show vpc status
```

### Extended Validation (2-24 hours)

```bash
# Stability Monitoring
- [ ] No BGP flapping
- [ ] No VXLAN tunnel flapping
- [ ] No MAC address flapping
- [ ] Consistent performance
- [ ] No memory leaks
- [ ] No CPU spikes

# Enable Enhanced Monitoring
logging level all 6
terminal monitor
```

### Full Validation (1-7 days)

- [ ] Complete [Post-Migration Validation](post-migration-validation.md) checklist
- [ ] Performance baseline verification
- [ ] All services validated
- [ ] Long-term stability confirmed
- [ ] No recurring issues

---

## Lessons Learned

### Post-Rollback Analysis

After rollback, conduct analysis session:

#### Document Root Cause

```
Issue Description:
_________________________________________________________________

Root Cause:
_________________________________________________________________

Impact Assessment:
_________________________________________________________________

Time to Detect:
_________________________________________________________________

Time to Resolve:
_________________________________________________________________
```

#### Identify Improvements

- [ ] What went wrong?
- [ ] What could have prevented it?
- [ ] What warnings were missed?
- [ ] What validation was inadequate?
- [ ] What training is needed?

#### Action Items

| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| | | | |
| | | | |

### Update Procedures

Based on lessons learned:

- [ ] Update migration plan
- [ ] Enhance validation procedures
- [ ] Add warning indicators
- [ ] Improve backup procedures
- [ ] Update training materials

---

## Communication Templates

### Rollback Notification Email

```
Subject: URGENT - Nexus Dashboard Migration Rollback Initiated

Team,

We have initiated rollback of the Nexus Dashboard migration due to [ISSUE].

Status: IN PROGRESS
Started: [TIME]
Expected Completion: [TIME]
Current Impact: [DESCRIPTION]

Actions:
1. [ACTION 1]
2. [ACTION 2]
3. [ACTION 3]

Bridge Line: [NUMBER]
Status Updates: Every 30 minutes

Contact: [NAME] [PHONE] [EMAIL]
```

### Rollback Completion Email

```
Subject: Nexus Dashboard Migration Rollback Complete

Team,

The rollback of the Nexus Dashboard migration is now complete.

Timeline:
- Rollback Started: [TIME]
- Rollback Completed: [TIME]
- Total Duration: [DURATION]

Current Status:
- All switches: Operational
- Services: Restored
- Impact: Resolved

Validation:
✓ Control plane operational
✓ Data plane operational
✓ All services validated
✓ Performance normal

Next Steps:
1. Continue monitoring for 24 hours
2. Schedule lessons learned session
3. Plan remediation for root cause
4. Schedule retry (if applicable)

Thank you for your support during this incident.

Contact: [NAME] [PHONE] [EMAIL]
```

---

## Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Incident Commander | _____________ | _____________ | _____________ |
| Network Lead | _____________ | _____________ | _____________ |
| Cisco TAC | _____________ | 1-800-553-2447 | _____________ |
| Management | _____________ | _____________ | _____________ |

---

## Rollback Checklist Summary

### Pre-Rollback
- [ ] Rollback decision made
- [ ] Approval obtained
- [ ] Team notified
- [ ] Backup files verified
- [ ] Tools prepared

### During Rollback
- [ ] NDFC disabled
- [ ] Configurations restored
- [ ] Services validated
- [ ] Testing completed
- [ ] Documentation updated

### Post-Rollback
- [ ] Full validation complete
- [ ] Monitoring active
- [ ] Stakeholders notified
- [ ] Incident documented
- [ ] Lessons learned scheduled

---

## References

- [Migration Plan](migration-plan.md)
- [Post-Migration Validation](post-migration-validation.md)
- [Troubleshooting Guide](troubleshooting.md)

---

**Document Version**: 1.0  
**Last Updated**: [Date]  
**Owner**: [Name]
