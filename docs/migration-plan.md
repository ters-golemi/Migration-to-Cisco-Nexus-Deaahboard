# Migration Plan: Traditional Nexus Fabric to Nexus Dashboard

## Table of Contents
1. [Migration Overview](#migration-overview)
2. [Migration Strategies](#migration-strategies)
3. [Timeline and Phases](#timeline-and-phases)
4. [Detailed Migration Steps](#detailed-migration-steps)
5. [Risk Mitigation](#risk-mitigation)
6. [Communication Plan](#communication-plan)

## Migration Overview

### Migration Approach
This migration plan supports two approaches:

1. **Greenfield Migration**: Deploy new fabric under Nexus Dashboard management
2. **Brownfield Migration**: Import existing fabric into Nexus Dashboard (Recommended)

### Migration Scope
- Import existing VXLAN EVPN fabric
- Transition management from CLI/DCNM to Nexus Dashboard
- Preserve all existing services and configurations
- Minimal to zero downtime

### Success Criteria
- All switches successfully managed by Nexus Dashboard
- No traffic disruption or packet loss
- All VLANs, VNIs, and VRFs operational
- Complete configuration visibility
- Policy enforcement operational

## Migration Strategies

### Strategy 1: Brownfield In-Place Migration (Recommended)

**Description**: Import existing fabric into Nexus Dashboard while maintaining current configuration.

**Pros**:
- Minimal risk
- No service disruption
- Gradual transition
- Easy rollback

**Cons**:
- Requires careful discovery
- Configuration drift must be resolved
- Legacy configurations may need cleanup

**Best For**: Production environments with zero downtime requirements

### Strategy 2: Greenfield Side-by-Side Migration

**Description**: Build new fabric alongside existing, then migrate workloads.

**Pros**:
- Clean configuration
- Full testing before cutover
- Easy rollback

**Cons**:
- Requires additional hardware
- More complex workload migration
- Higher cost

**Best For**: Major redesigns or upgrades

## Timeline and Phases

### Phase 1: Planning and Preparation (Week 1-2)
**Duration**: 1-2 weeks

**Activities**:
- Complete prerequisite validation
- Inventory current environment
- Document existing configuration
- Create detailed migration runbook
- Set up Nexus Dashboard cluster
- Test connectivity
- Train team members

**Deliverables**:
- Current state documentation
- Migration runbook
- Risk assessment
- Rollback procedures
- Team training completion

### Phase 2: Nexus Dashboard Deployment (Week 2-3)
**Duration**: 1 week

**Activities**:
- Install Nexus Dashboard nodes
- Form cluster
- Configure management network
- Install Nexus Dashboard Fabric Controller
- Configure AAA integration
- Set up backup and monitoring
- Perform initial testing

**Deliverables**:
- Operational Nexus Dashboard cluster
- NDFC application running
- Management connectivity verified
- Backup procedures tested

### Phase 3: Fabric Discovery and Import (Week 3-4)
**Duration**: 1 week

**Activities**:
- Discover existing fabric
- Import switches into NDFC
- Validate configuration compliance
- Resolve configuration drift
- Establish policy baselines
- Configure monitoring

**Deliverables**:
- All switches discovered and imported
- Configuration compliance verified
- Policy templates created
- Monitoring dashboards configured

### Phase 4: Validation and Optimization (Week 4-5)
**Duration**: 1 week

**Activities**:
- Full fabric validation
- Performance testing
- Policy enforcement testing
- Automation workflow testing
- Documentation updates
- Team knowledge transfer

**Deliverables**:
- Validated fabric operation
- Performance baseline
- Updated documentation
- Trained operations team

### Phase 5: Cutover and Steady State (Week 5-6)
**Duration**: 1 week

**Activities**:
- Transition to production management
- Enable automated policies
- Decommission legacy tools
- Final documentation
- Post-migration review

**Deliverables**:
- Production operations via Nexus Dashboard
- Legacy tools decommissioned
- Complete documentation
- Lessons learned document

## Detailed Migration Steps

### Pre-Migration Steps

#### Step 1: Environment Assessment
```bash
# Document current state
# On each switch:

show version
show running-config
show vpc status
show nve peers
show bgp l2vpn evpn summary
show vlan
show vni
show vrf

# Save outputs to file
```

#### Step 2: Backup Configurations
```bash
# Backup all switch configurations
# Using CLI:
copy running-config tftp://backup-server/switch1-backup.cfg

# Using Python/Ansible (recommended):
# See examples/backup-script.py
```

#### Step 3: Verify Network Connectivity
```bash
# From Nexus Dashboard node, verify SSH access
ssh admin@<switch-ip>

# Test HTTPS access
curl -k https://<switch-ip>

# Verify NTP sync
show ntp status
```

### Nexus Dashboard Deployment Steps

#### Step 1: Deploy Nexus Dashboard Nodes

**For Physical Appliance**:
1. Rack and cable appliances
2. Connect management and data network ports
3. Power on nodes
4. Access console for initial configuration

**For Virtual Appliance**:
1. Deploy OVA in vCenter
2. Configure network adapters
3. Power on VM
4. Access console for initial configuration

#### Step 2: Initial Node Configuration
```bash
# On each node console:

# Set hostname
setup
hostname nexus-dashboard-node1

# Configure management IP
interface mgmt0
  ip address <ip-address>/<prefix>
  gateway <gateway-ip>

# Configure DNS
dns server <dns-server-ip>

# Configure NTP
ntp server <ntp-server-ip>

# Save configuration
copy running-config startup-config
```

#### Step 3: Form Nexus Dashboard Cluster

**From Primary Node**:
1. Access Web GUI: https://<primary-node-ip>
2. Complete initial setup wizard
3. Create admin account
4. Add secondary nodes
5. Verify cluster formation

```bash
# Verify cluster status
# From SSH:
acs health
acs cluster status
```

#### Step 4: Install Nexus Dashboard Fabric Controller

1. Navigate to Services > App Store
2. Download NDFC application
3. Install NDFC
4. Allocate resources (CPU, memory)
5. Enable NDFC service
6. Access NDFC GUI
7. Complete NDFC setup wizard

### Fabric Import Steps

#### Step 1: Prepare Fabric for Discovery

**On Each Switch**:
```bash
# Enable required features
feature nxapi
feature bash-shell

# Configure POAP disable (if enabled)
no boot poap enable

# Enable HTTPS
feature https

# Create local user for NDFC (if not using AAA)
username ndfc-admin password <password> role network-admin

# Enable SSH
feature ssh
ssh key rsa 2048

# Configure switch role
system switch-role spine
# or
system switch-role leaf
```

#### Step 2: Create Fabric in NDFC

1. Log in to NDFC GUI
2. Navigate to Fabric Builder
3. Click "Create Fabric"
4. Select "VXLAN EVPN" fabric type
5. Configure fabric settings:
   - Fabric Name
   - BGP ASN
   - Anycast gateway MAC
   - VNI ranges
   - Underlay routing protocol
6. Choose "Easy_Fabric" template
7. Save fabric configuration

#### Step 3: Discover Switches

**Method 1: Seed IP Discovery**
```bash
# In NDFC:
# Fabric > Inventory > Discover
# Enter seed IP or IP range
# Provide credentials
# Select switches to import
# Click "Import"
```

**Method 2: POAP Discovery**
```bash
# For new switches:
# Configure DHCP server with POAP options
# Boot switches
# NDFC will discover via POAP
```

#### Step 4: Import Existing Configuration

1. In NDFC, navigate to Fabric > Inventory
2. Select discovered switches
3. Click "Import Config"
4. NDFC will analyze existing configuration
5. Review configuration compliance
6. Accept or modify policies
7. Complete import process

#### Step 5: Validate Configuration

```bash
# In NDFC:
# Check switch status (all should be "In-Sync")
# Review topology visualization
# Verify all VLANs/VNIs present
# Check VRF configuration
# Validate BGP peering
# Review overlay network status
```

### Post-Import Configuration

#### Step 1: Reconcile Configuration Drift

1. Navigate to Fabric > Configuration Compliance
2. Review any "Out-of-Sync" items
3. For each drift:
   - Analyze differences
   - Decide: Accept current or push policy
   - Document decision
4. Bring all switches to "In-Sync" state

#### Step 2: Create Policy Templates

1. Navigate to Fabric > Policies
2. Create templates for common configurations:
   - Interface policies
   - VLAN policies
   - VRF policies
   - QoS policies
3. Associate templates with switches
4. Validate policy deployment

#### Step 3: Configure Monitoring

1. Enable telemetry streaming
2. Configure alerts and notifications
3. Set up dashboards
4. Configure SNMP traps
5. Enable syslog forwarding

### Validation Steps

#### Step 1: Connectivity Validation

```bash
# From NDFC:
# Operations > Topology
# Verify all links up
# Check for any isolated nodes

# From switches:
show vpc status
show nve peers
show bgp l2vpn evpn summary
show forwarding distribution multicast route
```

#### Step 2: Traffic Validation

```bash
# Verify control plane
show bgp l2vpn evpn
show nve peers detail

# Verify data plane
ping <remote-host> vrf <vrf-name>
traceroute <remote-host> vrf <vrf-name>

# Check traffic flow
show interface counters
show hardware internal tah counters
```

#### Step 3: Policy Validation

1. Deploy test policy
2. Verify policy push success
3. Validate on switch
4. Test policy enforcement
5. Verify compliance reporting

### Cutover Steps

#### Step 1: Enable Read-Write Management

1. Review all validation results
2. Obtain change control approval
3. Switch NDFC to read-write mode
4. Test configuration changes
5. Verify change audit trail

#### Step 2: Enable Automation

1. Configure automated compliance checks
2. Enable auto-remediation (if desired)
3. Set up configuration backup automation
4. Enable automated health monitoring

#### Step 3: Decommission Legacy Tools

1. Disable access to legacy management tools
2. Archive old configurations
3. Update documentation
4. Update runbooks and procedures

## Risk Mitigation

### Risk 1: Configuration Loss
**Mitigation**:
- Complete backups before import
- Test import in lab environment
- Keep CLI access available
- Maintain rollback procedures

### Risk 2: Service Disruption
**Mitigation**:
- Import existing configuration (no push)
- Validate before enabling write mode
- Perform during maintenance window
- Have rollback plan ready

### Risk 3: Configuration Drift
**Mitigation**:
- Document all drift before import
- Create baseline policies
- Test compliance checks
- Gradual drift resolution

### Risk 4: Authentication Failures
**Mitigation**:
- Test AAA integration before import
- Keep local accounts active
- Have backup authentication method
- Document credential locations

### Risk 5: Incomplete Discovery
**Mitigation**:
- Verify network connectivity
- Check credentials on all switches
- Enable required features
- Manual addition if needed

## Communication Plan

### Stakeholder Communication

**Before Migration**:
- 2 weeks: Initial notification
- 1 week: Detailed plan distribution
- 3 days: Pre-migration briefing
- 1 day: Final confirmation

**During Migration**:
- Hourly status updates
- Immediate escalation of issues
- Real-time communication channel (Teams/Slack)

**After Migration**:
- Completion notification
- Summary report
- Lessons learned session
- Knowledge transfer

### Escalation Path

**Level 1**: Network Engineers (first responders)
**Level 2**: Network Architects (complex issues)
**Level 3**: Cisco TAC (product issues)
**Level 4**: Management (business decisions)

## Rollback Procedures

See [Rollback Procedures](rollback-procedures.md) for detailed rollback steps.

### Quick Rollback Triggers

Initiate rollback if:
- Unable to discover more than 25% of switches
- Critical service outage occurs
- Configuration corruption detected
- Unable to validate fabric health
- Management access lost to switches

### Rollback Time Estimate

- Configuration restore: 1-2 hours
- Full fabric verification: 2-4 hours
- Total rollback time: 4-6 hours

## Success Metrics

### Technical Metrics
- 100% switch discovery rate
- 0% packet loss during migration
- <5 minutes downtime per switch
- 100% configuration compliance
- All services operational

### Operational Metrics
- Reduced configuration time
- Faster troubleshooting
- Improved visibility
- Automated compliance checking
- Centralized management

## Post-Migration Activities

### Week 1 After Migration
- Daily health checks
- Monitor for issues
- Gather team feedback
- Document lessons learned

### Month 1 After Migration
- Weekly health reviews
- Optimize policies
- Expand automation
- Train additional staff

### Ongoing
- Quarterly policy reviews
- Regular backup verification
- Continuous optimization
- Stay current with updates

## Next Steps

After completing migration:
1. [Post-Migration Validation](post-migration-validation.md)
2. [Operational Procedures](../README.md)
3. [Troubleshooting Guide](troubleshooting.md)

## References

- [Nexus Dashboard Fabric Controller Configuration Guide](https://www.cisco.com/c/en/us/support/cloud-systems-management/prime-data-center-network-manager/series.html)
- [VXLAN EVPN Design Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/vxlan_evpn/guide/b_Nexus_9000_VXLAN_EVPN_Configuration_Guide.html)
- [Cisco Nexus Dashboard Operations Guide](https://www.cisco.com/c/en/us/td/docs/dcn/nd/2x/operations/cisco-nexus-dashboard-operations-guide.html)
