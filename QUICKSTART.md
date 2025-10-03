# Quick Start Guide

## Welcome!

This repository contains a comprehensive guide for migrating from a traditional Nexus NX-OS VxLAN-based Data Center Fabric to Cisco Nexus Dashboard deployment.

## Getting Started in 5 Minutes

### 1. Understand Your Migration Journey

Your migration will follow this path:
```
Current State          →    Migration Process    →    Target State
├─ Traditional Nexus       ├─ Plan & Prepare         ├─ Nexus Dashboard
├─ CLI Management          ├─ Deploy ND Cluster      ├─ Centralized Mgmt
├─ Manual Config           ├─ Install NDFC           ├─ Policy-Based
└─ Limited Visibility      └─ Import Fabric          └─ Full Analytics
```

### 2. Check Prerequisites (15 minutes)

Before you start, quickly verify:
- [ ] Nexus switches on compatible NX-OS version (9.3(7)+ for N9K)
- [ ] Nexus Dashboard hardware/virtual appliances available
- [ ] Management network connectivity established
- [ ] DNS and NTP services operational
- [ ] Admin access to all switches
- [ ] Complete configuration backups

**→ Full details:** [Prerequisites](docs/prerequisites.md)

### 3. Complete Pre-Migration Checklist (1-2 hours)

Work through the checklist to ensure readiness:
- [ ] Document current environment
- [ ] Backup all configurations
- [ ] Verify fabric health
- [ ] Schedule maintenance window
- [ ] Get team approval

**→ Full checklist:** [Pre-Migration Checklist](docs/pre-migration-checklist.md)

### 4. Follow the Migration Plan (4-6 weeks)

The migration is divided into manageable phases:

**Week 1-2: Planning**
- Complete documentation
- Set up Nexus Dashboard
- Test connectivity

**Week 2-3: Deployment**
- Install Nexus Dashboard
- Form cluster
- Install NDFC application

**Week 3-4: Import**
- Discover switches
- Import configurations
- Validate compliance

**Week 4-5: Validation**
- Test all functionality
- Performance validation
- Team training

**Week 5-6: Production**
- Cutover to production
- Enable automation
- Decommission legacy tools

**→ Detailed plan:** [Migration Plan](docs/migration-plan.md)

### 5. Configure and Validate

- **Configuration:** [Configuration Guide](docs/configuration-guide.md)
- **Validation:** [Post-Migration Validation](docs/post-migration-validation.md)
- **Troubleshooting:** [Troubleshooting Guide](docs/troubleshooting.md)

## Document Navigation

### For Planning Teams
Start here to understand scope and requirements:
1. [README.md](README.md) - Overview and benefits
2. [Prerequisites](docs/prerequisites.md) - System requirements
3. [Migration Plan](docs/migration-plan.md) - Timeline and phases

### For Implementation Teams
Step-by-step technical guides:
1. [Pre-Migration Checklist](docs/pre-migration-checklist.md) - Preparation
2. [Configuration Guide](docs/configuration-guide.md) - Setup instructions
3. [Post-Migration Validation](docs/post-migration-validation.md) - Testing

### For Operations Teams
Ongoing management resources:
1. [Troubleshooting Guide](docs/troubleshooting.md) - Problem resolution
2. [Rollback Procedures](docs/rollback-procedures.md) - Emergency procedures
3. [Example Configurations](examples/) - Reference examples

## Quick Reference Commands

### Backup Configuration (Pre-Migration)
```bash
# Run backup script
python examples/scripts/backup-all-switches.py

# Or manually on each switch
copy running-config tftp://server/backup.cfg
```

### Verify Fabric Health
```bash
# Run health check script
python examples/scripts/verify-fabric-health.py

# Or manually
show bgp l2vpn evpn summary
show nve peers
show vpc status
```

### Check Nexus Dashboard Status
```bash
# SSH to Nexus Dashboard node
ssh admin@<nd-ip>

# Check cluster health
acs health
acs cluster status
```

### Verify NDFC Operation
```bash
# Via GUI
https://<nd-ip>
# Navigate to Services > NDFC

# Check switch status
# Fabric > Inventory
# All switches should show "In-Sync"
```

## Migration Approaches

### Brownfield (Recommended for Production)
**Best for:** Existing fabrics with minimal downtime requirements

**Steps:**
1. Deploy Nexus Dashboard alongside existing fabric
2. Discover and import switches (no config changes)
3. Validate configuration compliance
4. Gradually enable management features
5. Minimal to zero downtime

**→ Details:** [Migration Plan - Strategy 1](docs/migration-plan.md#strategy-1-brownfield-in-place-migration-recommended)

### Greenfield (Best for Major Redesign)
**Best for:** New deployments or complete redesigns

**Steps:**
1. Build new fabric with Nexus Dashboard from start
2. Configure via NDFC policies
3. Migrate workloads from old fabric
4. Decommission old fabric
5. Requires workload migration window

**→ Details:** [Migration Plan - Strategy 2](docs/migration-plan.md#strategy-2-greenfield-side-by-side-migration)

## Common Scenarios

### "I need to migrate quickly"
Fastest path:
1. Skip to [Pre-Migration Checklist](docs/pre-migration-checklist.md)
2. Run [backup script](examples/scripts/backup-all-switches.py)
3. Follow [Migration Plan - Brownfield](docs/migration-plan.md)
4. Use [example configs](examples/) as reference

### "I'm troubleshooting an issue"
Go directly to:
1. [Troubleshooting Guide](docs/troubleshooting.md)
2. Find your issue category
3. Follow diagnostic steps
4. Apply solution

### "Something went wrong, need to rollback"
Emergency procedures:
1. [Rollback Procedures](docs/rollback-procedures.md)
2. Follow emergency rollback steps
3. Restore from backups
4. Validate fabric health

## Support Resources

### Documentation
- **In this repository:** Complete migration guide
- **Cisco.com:** [Nexus Dashboard Documentation](https://www.cisco.com/c/en/us/support/data-center-analytics/nexus-dashboard/series.html)
- **DevNet:** [Nexus Dashboard DevNet](https://developer.cisco.com/nexus-dashboard/)

### Getting Help
1. **Check documentation:** Start with [Troubleshooting Guide](docs/troubleshooting.md)
2. **Review examples:** See [examples/](examples/) directory
3. **Cisco TAC:** 1-800-553-2447 (for urgent issues)
4. **Community:** [Cisco Community Forums](https://community.cisco.com/)

### Training
- Cisco Nexus Dashboard training courses
- VXLAN EVPN fundamentals
- CCNP Data Center certification

## Best Practices

### Before You Start
- Test in lab environment first
- Complete all backups
- Document current state
- Get team buy-in
- Schedule adequate time

### During Migration
- Follow the plan
- Validate each step
- Keep stakeholders informed
- Document changes
- Have rollback ready

### After Migration
- Complete validation
- Monitor for 24 hours
- Train operations team
- Update documentation
- Conduct lessons learned

## Success Criteria

Your migration is successful when:
- [ ] All switches managed by Nexus Dashboard
- [ ] Zero unplanned downtime
- [ ] All services operational
- [ ] Configuration compliance 100%
- [ ] Team trained and confident
- [ ] Monitoring and alerts working
- [ ] Backup procedures validated
- [ ] Documentation complete

## Next Steps

Choose your path:

###  Ready to Start?
→ Go to [Prerequisites](docs/prerequisites.md)

###  Need to Plan?
→ Go to [Migration Plan](docs/migration-plan.md)

###  Ready to Configure?
→ Go to [Configuration Guide](docs/configuration-guide.md)

###  Have Questions?
→ Go to [Troubleshooting Guide](docs/troubleshooting.md)

###  Need to Rollback?
→ Go to [Rollback Procedures](docs/rollback-procedures.md)

## Document Updates

This documentation is continuously improved based on user feedback and new product features.

**Current Version:** 1.0  
**Last Updated:** 2024

## Feedback

Found an issue or have a suggestion? Please:
1. Open an issue in this repository
2. Submit a pull request with improvements
3. Contact the documentation team

---

**Good luck with your migration!** 

Remember: Take your time, validate each step, and don't hesitate to ask for help when needed.
