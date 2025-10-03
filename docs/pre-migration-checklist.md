# Pre-Migration Checklist

## Overview
This checklist ensures all prerequisites are met before beginning the migration to Nexus Dashboard. Complete all items and verify with checkmarks before proceeding.

---

## 1. Planning and Documentation

### Environment Assessment
- [ ] Complete network topology diagram created
- [ ] All switch models and software versions documented
- [ ] Physical and logical connectivity mapped
- [ ] Cable plant documentation up to date
- [ ] Port assignments documented
- [ ] VLAN database documented
- [ ] VNI assignments documented
- [ ] VRF configuration documented
- [ ] BGP AS numbers and peering documented
- [ ] External connectivity documented

### Current Configuration Backup
- [ ] Running configs backed up for all switches
- [ ] Startup configs backed up for all switches
- [ ] Boot variables documented
- [ ] License files backed up
- [ ] Certificate files backed up
- [ ] Backup integrity verified (can restore if needed)
- [ ] Backups stored in secure location
- [ ] Backup timestamps recorded

### Change Management
- [ ] Change request submitted and approved
- [ ] Maintenance window scheduled
- [ ] Maintenance window communicated to stakeholders
- [ ] Business approval obtained
- [ ] Roll-back procedures documented and approved
- [ ] Emergency contact list created
- [ ] Escalation path defined

---

## 2. Infrastructure Readiness

### Nexus Dashboard Hardware/Virtual Appliance
- [ ] Nexus Dashboard nodes procured/deployed
- [ ] Minimum 3 nodes for production (or 1 for lab)
- [ ] Physical appliances racked and cabled (if applicable)
- [ ] Virtual machines created with proper resources
- [ ] Management network connectivity verified
- [ ] Data network connectivity verified
- [ ] Console access tested
- [ ] Power redundancy verified (for physical)

### Network Infrastructure
- [ ] Management VLAN configured and operational
- [ ] IP addresses allocated for ND nodes
- [ ] Default gateway configured and reachable
- [ ] Firewall rules configured (ports opened)
- [ ] Network latency between nodes <50ms
- [ ] Bandwidth requirements met (1G minimum, 10G recommended)

### Supporting Infrastructure
- [ ] DNS servers operational
- [ ] Forward DNS entries created for ND nodes
- [ ] Reverse DNS entries created for ND nodes
- [ ] NTP servers operational and synchronized
- [ ] SMTP server configured for notifications
- [ ] Syslog server ready for log collection
- [ ] TFTP/SFTP server for backups
- [ ] AAA servers (TACACS+/RADIUS) operational

---

## 3. Software and Licensing

### Nexus Dashboard Software
- [ ] Latest Nexus Dashboard software downloaded
- [ ] NDFC application package downloaded
- [ ] Nexus Dashboard Insights downloaded (if required)
- [ ] Software integrity verified (checksums)
- [ ] Installation media prepared
- [ ] License files obtained
- [ ] License files validated
- [ ] Support contract verified and active

### Switch Software
- [ ] All switches on compatible NX-OS versions
  - Nexus 9000: 9.3(7)+ minimum
  - Nexus 3000: 9.3(7)+ minimum
  - Nexus 7000: 8.4(1)+ minimum
- [ ] All switches same or compatible software versions
- [ ] Required features enabled on switches
- [ ] Software upgrade planned if needed
- [ ] Upgrade images available and verified

---

## 4. Access and Credentials

### Nexus Dashboard Access
- [ ] Admin credentials decided
- [ ] Local user accounts planned
- [ ] AAA integration credentials obtained
- [ ] SSH keys generated (if using key-based auth)
- [ ] Certificate files prepared (if using custom certs)
- [ ] Certificate chain validated

### Switch Access
- [ ] Admin credentials for all switches documented
- [ ] TACACS+/RADIUS credentials verified
- [ ] Enable passwords/secrets documented
- [ ] SSH access tested from ND management network
- [ ] HTTPS access tested from ND management network
- [ ] Console access available as backup
- [ ] All switches accessible from ND nodes

### External Services Access
- [ ] vCenter/ESXi admin credentials (for virtual deployment)
- [ ] AAA server admin credentials
- [ ] SMTP server credentials
- [ ] Backup server credentials
- [ ] Monitoring system credentials

---

## 5. Switch Preparation

### Feature Enablement
On each switch, verify the following features are enabled:
- [ ] `feature nxapi`
- [ ] `feature bash-shell`
- [ ] `feature https`
- [ ] `feature ssh`
- [ ] `feature bgp`
- [ ] `feature nv overlay`
- [ ] `feature vn-segment-vlan-based`
- [ ] `feature interface-vlan`

### Switch Configuration
- [ ] POAP disabled on all switches
- [ ] Switch roles configured (spine/leaf)
- [ ] Management interface configured with correct IP
- [ ] Default gateway configured
- [ ] DNS configured
- [ ] NTP configured and synchronized
- [ ] Hostname configured
- [ ] Domain name configured

### Connectivity Verification
- [ ] SSH connectivity verified from ND to all switches
- [ ] HTTPS connectivity verified from ND to all switches
- [ ] NTP synchronization verified on all switches
- [ ] DNS resolution working on all switches
- [ ] Inter-switch connectivity verified
- [ ] No spanning-tree blocked ports (unexpected)

---

## 6. Fabric Health Check

### Control Plane
- [ ] All BGP sessions in Established state
- [ ] BGP EVPN address family operational
- [ ] No BGP flapping detected
- [ ] OSPF/IS-IS neighbors in Full state
- [ ] No routing loops detected
- [ ] Route counts normal and stable

### Data Plane
- [ ] All NVE peers up
- [ ] VXLAN tunnels established
- [ ] No MAC/IP moves detected
- [ ] ARP/ND tables complete
- [ ] Traffic flows validated
- [ ] No packet loss detected

### High Availability
- [ ] vPC peer-links operational
- [ ] vPC consistency parameters matched
- [ ] vPC role resolution correct
- [ ] No vPC orphan ports
- [ ] All vPC ports in up state
- [ ] MCT links operational

### Resource Utilization
- [ ] CPU utilization <50% on all switches
- [ ] Memory utilization <75% on all switches
- [ ] TCAM utilization <80%
- [ ] No hardware errors detected
- [ ] Interface counters clean (no errors)
- [ ] Temperature within normal range

---

## 7. Testing Environment

### Lab/Test Environment
- [ ] Lab environment available for testing
- [ ] Lab mirrors production topology
- [ ] Test migration performed in lab
- [ ] Test migration documented
- [ ] Issues identified and resolved
- [ ] Test results reviewed with team
- [ ] Test configurations available for reference

### Test Cases
- [ ] Switch discovery tested
- [ ] Configuration import tested
- [ ] Policy deployment tested
- [ ] Rollback procedures tested
- [ ] Failover scenarios tested
- [ ] Performance baseline captured

---

## 8. Team Readiness

### Skills and Training
- [ ] Team trained on Nexus Dashboard
- [ ] Team trained on NDFC
- [ ] VXLAN EVPN knowledge confirmed
- [ ] REST API basics understood (if needed)
- [ ] Troubleshooting procedures reviewed
- [ ] Escalation procedures understood

### Team Availability
- [ ] All required team members available during migration window
- [ ] Backup team members identified
- [ ] On-call support arranged
- [ ] Cisco TAC engaged (if needed)
- [ ] Communication channels established (Teams/Slack)

### Documentation Review
- [ ] All migration documentation reviewed by team
- [ ] Questions and concerns addressed
- [ ] Roles and responsibilities assigned
- [ ] Runbook reviewed and validated
- [ ] Rollback procedures understood

---

## 9. Backup and Recovery

### Configuration Backups
- [ ] All switch configs backed up (within 24 hours)
- [ ] Backup restoration tested
- [ ] Backup files stored securely
- [ ] Multiple backup copies maintained
- [ ] Off-site backup copy available

### System Images
- [ ] Current boot images backed up
- [ ] Kickstart images backed up (if applicable)
- [ ] Image files verified bootable
- [ ] Fallback images available

### Recovery Plan
- [ ] Detailed rollback plan documented
- [ ] Rollback time estimate calculated
- [ ] Rollback triggers defined
- [ ] Recovery procedures tested
- [ ] Emergency procedures documented

---

## 10. Monitoring and Alerting

### Monitoring Tools
- [ ] Network monitoring tools operational
- [ ] Baseline metrics captured
- [ ] Alert thresholds configured
- [ ] Dashboard prepared for migration monitoring
- [ ] Packet capture tool ready (if needed)

### Logging
- [ ] Logging levels increased on switches
- [ ] Syslog capture configured
- [ ] Log retention verified
- [ ] Log analysis tools ready
- [ ] Screen recording/logging prepared

---

## 11. Communication Plan

### Stakeholder Communication
- [ ] Initial notification sent (2 weeks prior)
- [ ] Detailed plan distributed (1 week prior)
- [ ] Pre-migration briefing completed (3 days prior)
- [ ] Final confirmation sent (1 day prior)
- [ ] Impact assessment communicated
- [ ] Expected downtime communicated

### During Migration Communication
- [ ] Communication channel established
- [ ] Status update schedule defined
- [ ] Escalation contacts verified
- [ ] Bridge/conference line reserved
- [ ] Chat room/channel created

---

## 12. Risk Assessment

### Identified Risks
- [ ] All potential risks identified
- [ ] Risk mitigation plans documented
- [ ] Risk severity assessed
- [ ] Risk owners assigned
- [ ] Contingency plans prepared

### Critical Services
- [ ] Critical services identified
- [ ] Service dependencies mapped
- [ ] Service validation procedures defined
- [ ] Service recovery procedures documented

---

## 13. Final Verification (24 hours before)

### Environment Status
- [ ] No recent changes to environment
- [ ] No open incidents affecting migration
- [ ] All prerequisites still met
- [ ] Team members confirmed available
- [ ] Maintenance window confirmed

### Final Backups
- [ ] Final configuration backups completed
- [ ] Final state snapshot captured
- [ ] Backup verification completed
- [ ] Backups accessible by all team members

### Final Checks
- [ ] Change freeze in effect
- [ ] Monitoring alerts suppressed (if appropriate)
- [ ] All documentation printed/accessible
- [ ] Tools and scripts prepared
- [ ] Emergency contact list distributed

---

## 14. Day of Migration

### Pre-Migration Tasks
- [ ] Team check-in completed
- [ ] Communication channels tested
- [ ] Monitoring dashboards displayed
- [ ] Backup procedures reviewed
- [ ] Go/No-Go decision made
- [ ] Migration start time confirmed

### Ready to Begin
- [ ] All checklist items completed
- [ ] Team ready and standing by
- [ ] No blocking issues identified
- [ ] Rollback plan reviewed
- [ ] Authorization to proceed obtained

---

## Sign-Off

### Approvals Required

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Network Architect | _____________ | _____________ | __/__/____ |
| Network Manager | _____________ | _____________ | __/__/____ |
| Change Manager | _____________ | _____________ | __/__/____ |
| Business Owner | _____________ | _____________ | __/__/____ |

### Checklist Completion

- **Total Items**: Count all checkboxes above
- **Completed Items**: Count checked items
- **Completion Percentage**: Calculate percentage
- **Outstanding Items**: List any uncompleted items with justification

---

## Notes and Comments

Use this section to document any deviations from the checklist or additional notes:

```
Date: ___________
Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Next Steps

Once this checklist is 100% complete:
1. Proceed to [Migration Plan](migration-plan.md)
2. Begin Phase 1: Planning and Preparation
3. Follow the detailed migration steps

## Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Team Lead | _____________ | _____________ | _____________ |
| Network Architect | _____________ | _____________ | _____________ |
| Cisco TAC | _____________ | 1-800-553-2447 | _____________ |
| Management | _____________ | _____________ | _____________ |

---

**Document Version**: 1.0  
**Last Updated**: [Date]  
**Prepared By**: [Name]
