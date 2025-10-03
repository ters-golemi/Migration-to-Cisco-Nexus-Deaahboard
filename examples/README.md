# Example Configurations and Scripts

This directory contains example configurations, templates, and automation scripts to support the migration to Cisco Nexus Dashboard.

## Directory Structure

```
examples/
├── switch-configs/      # Example switch configurations
├── ndfc-templates/      # Nexus Dashboard Fabric Controller templates
├── scripts/            # Automation scripts
└── README.md          # This file
```

## Switch Configurations

### switch-configs/

Contains example configurations for different switch roles in a VXLAN EVPN fabric:

- **spine-config-example.txt**: Example spine switch configuration
  - BGP EVPN Route Reflector
  - OSPF underlay
  - PIM for multicast (if using multicast replication)
  - Features enabled for NDFC management

- **leaf-config-example.txt**: Example leaf switch configuration
  - VXLAN VTEP
  - BGP EVPN
  - vPC configuration
  - VRF and network configuration
  - Anycast gateway

### Usage

These configurations serve as reference examples. **DO NOT** copy directly to production switches without:

1. Customizing IP addresses for your environment
2. Adjusting BGP AS numbers
3. Updating interface numbers
4. Configuring appropriate VLANs and VNIs
5. Setting correct passwords and secrets
6. Reviewing all settings for your specific requirements

## NDFC Templates

### ndfc-templates/

Contains JSON templates for configuring fabrics in Nexus Dashboard Fabric Controller:

- **fabric-settings.json**: Fabric-wide settings
  - BGP configuration
  - VNI ranges
  - Underlay/overlay settings
  - NTP, DNS, Syslog configuration

- **network-template.json**: Network (VLAN/VNI) definitions
  - Layer 2 networks
  - Gateway configurations
  - VRF assignments
  - Multicast groups

- **vrf-template.json**: VRF definitions
  - L3 VNI configuration
  - Route targets
  - BGP settings
  - Switch attachments

### Usage

These templates can be:
1. Imported into NDFC via the GUI
2. Applied via REST API
3. Used as reference for manual configuration

To use via API:
```bash
curl -X POST https://<ndfc-ip>/api/v1/fabric/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d @fabric-settings.json
```

## Automation Scripts

### scripts/

Python scripts for common migration tasks:

#### backup-all-switches.py

**Purpose**: Backup configurations from all fabric switches

**Features**:
- Connects to all switches via SSH
- Saves running-config, startup-config, version, and inventory
- Creates timestamped backup directory
- Generates backup summary report
- Logs all operations

**Requirements**:
```bash
pip install paramiko netmiko
```

**Usage**:
```bash
python backup-all-switches.py
```

The script will:
1. Prompt for SSH credentials
2. Create a backup directory with timestamp
3. Connect to each switch
4. Save all configurations
5. Generate a summary report

**Output**:
```
backups/
└── 20240115_143022/
    ├── spine-01_running-config.txt
    ├── spine-01_startup-config.txt
    ├── spine-01_version.txt
    ├── spine-01_inventory.txt
    ├── leaf-01_running-config.txt
    ├── ...
    └── backup_summary.txt
```

#### verify-fabric-health.py

**Purpose**: Verify fabric health before/after migration

**Features**:
- Checks BGP EVPN sessions
- Verifies VXLAN tunnel status
- Validates vPC status
- Monitors system resources (CPU, memory)
- Checks for interface errors

**Requirements**:
```bash
pip install paramiko netmiko
```

**Usage**:
```bash
python verify-fabric-health.py
```

**Example Output**:
```
Verifying spine-01 (spine)
  ✓ BGP EVPN: 4/4 sessions Established
  ✓ CPU: 12.5%
  ✓ Memory: 45.2%
  ✓ Interfaces: No errors detected
  Overall Status: HEALTHY
```

## Customization Guide

### Switch Inventory

Update the `SWITCHES` list in both scripts to match your environment:

```python
SWITCHES = [
    {'hostname': 'your-spine-01', 'ip': '10.1.1.1', 'role': 'spine'},
    {'hostname': 'your-leaf-01', 'ip': '10.1.1.11', 'role': 'leaf'},
    # Add your switches here
]
```

### Credentials

**Option 1**: Interactive prompt (default)
- Scripts will prompt for credentials at runtime
- Most secure for production

**Option 2**: Environment variables
```bash
export SWITCH_USERNAME="admin"
export SWITCH_PASSWORD="password"
```

Then modify scripts to read from environment:
```python
import os
username = os.environ.get('SWITCH_USERNAME')
password = os.environ.get('SWITCH_PASSWORD')
```

**Option 3**: Credential file (least secure)
- Create a `.credentials` file (add to .gitignore)
- Use with caution

### Adding More Scripts

Consider creating additional scripts for:
- Pre-migration validation
- Post-migration testing
- Configuration comparison
- Traffic testing
- Performance monitoring

## Security Considerations

### Credential Management
- **Never** commit credentials to version control
- Use environment variables or secure vaults
- Implement credential rotation
- Use SSH keys where possible

### Script Execution
- Review scripts before execution
- Test in lab environment first
- Use read-only credentials when possible
- Log all operations for audit

### File Permissions
```bash
# Secure script files
chmod 750 *.py

# Secure backup directory
chmod 700 backups/

# Secure credential files (if used)
chmod 600 .credentials
```

## Best Practices

### Before Using Scripts

1. **Test in Lab**
   - Always test scripts in non-production first
   - Verify output matches expectations
   - Validate error handling

2. **Backup Everything**
   - Run backup script before any changes
   - Keep multiple backup copies
   - Store backups off-site

3. **Review Logs**
   - Check script logs for errors
   - Verify all operations completed
   - Document any issues

### During Migration

1. **Run Pre-Migration Backup**
   ```bash
   python backup-all-switches.py
   ```

2. **Verify Fabric Health**
   ```bash
   python verify-fabric-health.py
   ```

3. **Save Results**
   - Store backup files securely
   - Save health check results
   - Document baseline metrics

### After Migration

1. **Run Post-Migration Backup**
   ```bash
   python backup-all-switches.py
   ```

2. **Verify Health Again**
   ```bash
   python verify-fabric-health.py
   ```

3. **Compare Results**
   - Compare pre/post configurations
   - Verify no unexpected changes
   - Document any differences

## Troubleshooting

### Connection Issues

**Problem**: Script cannot connect to switches

**Solutions**:
- Verify IP addresses are correct
- Check firewall rules
- Ensure SSH is enabled on switches
- Verify credentials are correct
- Check network connectivity

### Timeout Issues

**Problem**: Script times out during execution

**Solutions**:
- Increase timeout in device configuration
- Check network latency
- Verify switch is responsive
- Try connecting manually via SSH

### Authentication Issues

**Problem**: Authentication fails

**Solutions**:
- Verify username/password
- Check AAA configuration on switches
- Try local authentication
- Verify user has correct privileges

## Additional Resources

- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Paramiko Documentation](http://www.paramiko.org/)
- [Cisco NX-OS API Documentation](https://developer.cisco.com/docs/nexus/)
- [Python Network Automation](https://github.com/ktbyers/pynet)

## Contributing

To contribute additional examples or scripts:

1. Follow existing code style
2. Include documentation
3. Add error handling
4. Test thoroughly
5. Submit pull request

## Support

For issues or questions:
1. Review the main [Troubleshooting Guide](../docs/troubleshooting.md)
2. Check script logs
3. Verify environment setup
4. Contact your Cisco support team

## License

These examples are provided as-is for educational purposes. Test thoroughly before using in production environments.
