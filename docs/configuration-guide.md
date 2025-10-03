# Configuration Guide: Cisco Nexus Dashboard and NDFC

## Table of Contents
1. [Initial Nexus Dashboard Configuration](#initial-nexus-dashboard-configuration)
2. [Nexus Dashboard Fabric Controller Setup](#nexus-dashboard-fabric-controller-setup)
3. [Fabric Configuration](#fabric-configuration)
4. [Network Configuration](#network-configuration)
5. [Policy Configuration](#policy-configuration)
6. [Security Configuration](#security-configuration)
7. [Monitoring and Analytics](#monitoring-and-analytics)

## Initial Nexus Dashboard Configuration

### Node Configuration

#### Physical Appliance Configuration

**Console Access**:
```bash
# Connect to console port
# Login with default credentials
# Default: admin/admin (must change on first login)

# Run setup utility
setup

# Configure hostname
hostname nexus-dashboard-01

# Configure management interface
interface mgmt0
  ip address 192.168.1.100/24
  no shutdown
exit

# Configure default gateway
ip route 0.0.0.0/0 192.168.1.1

# Configure DNS
dns server 8.8.8.8 8.8.4.4
dns domain-name company.local

# Configure NTP
ntp server 192.168.1.10
ntp server 192.168.1.11

# Save configuration
copy running-config startup-config
```

#### Virtual Appliance Configuration

**Deploy OVA**:
1. Open vSphere Client
2. Right-click on cluster/host
3. Select "Deploy OVF Template"
4. Browse to Nexus Dashboard OVA file
5. Follow deployment wizard:
   - Name: nexus-dashboard-01
   - Storage: Select appropriate datastore
   - Networks: Map networks (management, data)
6. Customize hardware:
   - CPU: 32 vCPUs
   - Memory: 128 GB
   - Disk: 500 GB
7. Power on VM after deployment

**Initial Configuration** (via console):
```bash
# Login to VM console
# Set management IP
config
  interface mgmt0
    ip address 192.168.1.100 255.255.255.0
    no shutdown
  exit
  ip route 0.0.0.0 0.0.0.0 192.168.1.1
exit

# Configure DNS and NTP
dns-server 192.168.1.10
ntp-server 192.168.1.10
```

### Web GUI Initial Setup

**First Login**:
1. Navigate to https://192.168.1.100
2. Accept security warning
3. Login with admin credentials
4. Complete Setup Wizard:
   - Review and accept EULA
   - Set new admin password
   - Configure NTP servers
   - Configure DNS servers
   - Set timezone
   - Upload SSL certificate (optional)

### Cluster Formation

#### Three-Node Cluster (Production)

**On Primary Node**:
1. Login to Web GUI
2. Navigate to Infrastructure > Cluster Configuration
3. Click "Add Node"
4. Enter secondary node details:
   - Hostname: nexus-dashboard-02
   - Management IP: 192.168.1.101
   - Username: admin
   - Password: <password>
5. Click "Add"
6. Repeat for third node
7. Verify cluster status: Infrastructure > Cluster Configuration

**Verify Cluster**:
```bash
# SSH to any node
ssh admin@192.168.1.100

# Check cluster status
acs health
acs cluster status
acs show nodes

# Expected output:
# All nodes should show "healthy"
# Cluster state should be "converged"
```

### Network Configuration

#### Management Network
```bash
# Configure management VLAN (if required)
config
  interface mgmt0
    vlan 100
    ip address 192.168.1.100 255.255.255.0
    no shutdown
  exit
exit
```

#### Data Network
```bash
# Configure data network interfaces
config
  interface eth1/1
    description "Data Network Connection"
    no switchport
    ip address 10.1.1.100/24
    no shutdown
  exit
exit
```

## Nexus Dashboard Fabric Controller Setup

### Install NDFC Application

**Via Web GUI**:
1. Login to Nexus Dashboard
2. Navigate to Services > App Store
3. Locate "Nexus Dashboard Fabric Controller"
4. Click "Download"
5. Wait for download to complete
6. Click "Install"
7. Configure installation:
   - Application Name: NDFC
   - Persistent IP: 192.168.1.105
   - Resource Allocation: Large (for production)
8. Click "Install"
9. Monitor installation progress
10. Wait for status to show "Healthy"

**Resource Allocation Options**:
- **Small**: <50 switches
- **Medium**: 50-100 switches
- **Large**: 100-500 switches
- **X-Large**: >500 switches

### NDFC Initial Configuration

**First Login**:
1. Navigate to Services > Installed Apps
2. Click on "NDFC"
3. Click "Open" to launch NDFC GUI
4. Login with Nexus Dashboard credentials
5. Complete NDFC Setup Wizard:
   - License: Upload license file
   - SMTP: Configure email settings
   - Syslog: Configure syslog server
   - Backup: Configure backup location

### License Configuration

```bash
# Via GUI:
# Settings > Licensing
# Click "Add License"
# Upload license file or paste license key
# Verify license status
```

### AAA Configuration

#### Local User Authentication
```bash
# Settings > User Management > Local Users
# Click "Add User"
# Enter:
#   - Username
#   - Password
#   - Role (network-admin, network-operator, etc.)
# Click "Save"
```

#### TACACS+ Configuration
```bash
# Settings > User Management > AAA
# Select "TACACS+"
# Click "Add Server"
# Enter:
#   - Server IP: 192.168.1.50
#   - Port: 49 (default)
#   - Shared Secret: <secret>
#   - Timeout: 5
# Click "Save"
# Enable TACACS+ authentication
```

#### RADIUS Configuration
```bash
# Settings > User Management > AAA
# Select "RADIUS"
# Click "Add Server"
# Enter:
#   - Server IP: 192.168.1.51
#   - Port: 1812 (default)
#   - Shared Secret: <secret>
#   - Timeout: 5
# Click "Save"
# Enable RADIUS authentication
```

## Fabric Configuration

### Create VXLAN EVPN Fabric

**Easy Fabric Template**:
1. Navigate to Fabric Builder
2. Click "Create Fabric"
3. Enter Fabric Details:
   - **Fabric Name**: DC1-Fabric
   - **Fabric Template**: Easy_Fabric
   - **Fabric Type**: Switch
   - **BGP AS**: 65001
   - **Anycast Gateway MAC**: 0001.0001.0001
   
4. Configure Advanced Settings:
   - **Underlay Routing**: OSPF or IS-IS
   - **Overlay Routing**: EBGP or IBGP
   - **Replication Mode**: Multicast or Ingress Replication
   - **DHCP Server**: IP address (optional)
   - **NTP Server**: IP address
   - **Syslog Server**: IP address

5. Configure VNI Ranges:
   - **L2 VNI Range**: 30000-39999
   - **L3 VNI Range**: 50000-59999
   - **Multicast Group Range**: 239.1.1.0-239.1.1.255

6. Click "Save"

### Fabric Settings Template

```json
{
  "fabricName": "DC1-Fabric",
  "fabricType": "Switch",
  "fabricTemplate": "Easy_Fabric",
  "asn": "65001",
  "replicationMode": "Ingress",
  "anycastGWMac": "0001.0001.0001",
  "enabledFeatures": [
    "VXLAN",
    "EVPN",
    "PIM",
    "VRF-Lite"
  ],
  "underlayRouting": "ospf",
  "overlayRouting": "ebgp",
  "l2VniRange": "30000-39999",
  "l3VniRange": "50000-59999",
  "multicastRange": "239.1.1.0-239.1.1.255"
}
```

### Add Switches to Fabric

#### Seed IP Discovery
1. Navigate to Fabric > Inventory
2. Click "Discover"
3. Enter discovery parameters:
   - **Seed IP**: 10.1.1.1 (first switch)
   - **Username**: admin
   - **Password**: <password>
   - **Discovery Method**: CDP/LLDP
4. Click "Discover"
5. Select discovered switches
6. Assign roles:
   - Spine
   - Leaf
   - Border Leaf
   - Border Gateway
7. Click "Import"

#### Manual Addition
1. Navigate to Fabric > Inventory
2. Click "Add Device"
3. Enter switch details:
   - **IP Address**: 10.1.1.1
   - **Username**: admin
   - **Password**: <password>
   - **Role**: spine/leaf
4. Click "Add"
5. Repeat for all switches

### Configure Fabric Settings

#### Underlay Network - OSPF
```bash
# Settings applied to all switches:

feature ospf

router ospf UNDERLAY
  router-id <loopback-ip>
  
interface loopback0
  description Underlay Router ID
  ip address <router-id>/32
  ip router ospf UNDERLAY area 0.0.0.0

interface Ethernet1/1-X
  description Underlay P2P Link
  no switchport
  mtu 9216
  ip address <p2p-ip>/<prefix>
  ip router ospf UNDERLAY area 0.0.0.0
  no shutdown
```

#### Overlay Network - BGP EVPN
```bash
# Spine configuration:

feature bgp
feature nv overlay

router bgp 65001
  router-id <loopback-ip>
  address-family l2vpn evpn
    retain route-target all
  
  neighbor <leaf-loopback-ip>
    remote-as 65001
    update-source loopback0
    address-family l2vpn evpn
      send-community extended
      route-reflector-client

# Leaf configuration:

router bgp 65001
  router-id <loopback-ip>
  address-family l2vpn evpn
  
  neighbor <spine-loopback-ip>
    remote-as 65001
    update-source loopback0
    address-family l2vpn evpn
      send-community extended
```

#### VXLAN Configuration
```bash
# Enable features
feature vn-segment-vlan-based
feature nv overlay

# Configure NVE interface
interface nve1
  no shutdown
  description VXLAN Overlay
  host-reachability protocol bgp
  source-interface loopback1
  member vni 30001
    mcast-group 239.1.1.1
  member vni 50001 associate-vrf
```

## Network Configuration

### VLAN Configuration

**Via NDFC GUI**:
1. Navigate to Fabric > Networks
2. Click "Add Network"
3. Select "VLAN"
4. Configure:
   - **Network Name**: VLAN_100
   - **VLAN ID**: 100
   - **VNI**: 30100
   - **Subnet**: 10.100.0.0/24
   - **Gateway IP**: 10.100.0.1
   - **VRF**: default or custom VRF
   - **Multicast Group**: 239.1.1.1
5. Select deployment switches
6. Click "Deploy"

**Network Template Example**:
```json
{
  "networkName": "VLAN_100",
  "vlanId": 100,
  "vni": 30100,
  "gatewayIp": "10.100.0.1/24",
  "vrfName": "Tenant-1",
  "mcastGroup": "239.1.1.1",
  "enableIR": true,
  "suppressARP": true,
  "enableL3OnBorder": true,
  "deploymentMode": "perSwitch"
}
```

### VRF Configuration

1. Navigate to Fabric > VRFs
2. Click "Add VRF"
3. Configure:
   - **VRF Name**: Tenant-1
   - **L3 VNI**: 50001
   - **VLAN ID**: 1001 (for L3VNI SVI)
   - **Route Target**: auto or manual
   - **Route Distinguisher**: auto or manual
4. Select deployment switches
5. Click "Deploy"

**VRF Template Example**:
```json
{
  "vrfName": "Tenant-1",
  "l3Vni": 50001,
  "vlanId": 1001,
  "rtAuto": true,
  "rdAuto": true,
  "redistributeStatic": true,
  "redistributeConnected": true,
  "maxBgpPaths": 4,
  "maxIBgpPaths": 2
}
```

### Border Gateway Configuration

**For External Connectivity**:
1. Navigate to Fabric > External Connectivity
2. Click "Add External Network"
3. Configure:
   - **External Network Name**: Internet-VRF
   - **VRF**: Tenant-1
   - **Border Devices**: Select border leafs
   - **External Router IP**: <external-router-ip>
   - **Local AS**: 65001
   - **Remote AS**: 65002
4. Click "Deploy"

## Policy Configuration

### Interface Policies

**Access Port Policy**:
1. Navigate to Policies > Interface Policies
2. Click "Add Policy"
3. Configure:
   - **Policy Name**: Access-Port-Policy
   - **Port Type**: Access
   - **VLAN**: 100
   - **Speed**: 10G
   - **MTU**: 9216
   - **STP**: Edge
4. Save policy

**Trunk Port Policy**:
```json
{
  "policyName": "Trunk-Port-Policy",
  "portType": "trunk",
  "allowedVlans": "100,200,300",
  "nativeVlan": 1,
  "speed": "10G",
  "mtu": 9216,
  "stpType": "edge"
}
```

### QoS Policies

1. Navigate to Policies > QoS
2. Click "Add Policy"
3. Configure:
   - **Policy Name**: QoS-Voice
   - **Class Maps**: Voice, Video, Data
   - **Marking**: DSCP EF for Voice
   - **Queuing**: Priority queue for Voice
4. Apply to interfaces

### Security Policies

**ACL Policy**:
1. Navigate to Policies > Access Control
2. Click "Add ACL"
3. Configure:
   - **ACL Name**: Block-SSH-External
   - **Type**: IPv4
   - **Rules**: 
     - deny tcp any any eq 22
     - permit ip any any
4. Apply to interfaces or VRFs

## Security Configuration

### Certificate Management

**Upload Custom Certificate**:
1. Navigate to Settings > Security > Certificates
2. Click "Import Certificate"
3. Upload:
   - Certificate file (.pem)
   - Private key file
   - CA chain file (if applicable)
4. Click "Import"
5. Enable certificate for HTTPS

### RBAC Configuration

**Create Custom Role**:
1. Navigate to Settings > User Management > Roles
2. Click "Add Role"
3. Configure:
   - **Role Name**: Fabric-Operator
   - **Permissions**:
     - Read: All
     - Write: Networks, Interfaces
     - Deploy: Networks
4. Save role

### SSH Key Management

1. Navigate to Settings > Security > SSH Keys
2. Click "Add Key"
3. Enter:
   - Key Name
   - Public Key
4. Associate with user account

## Monitoring and Analytics

### Enable Telemetry

1. Navigate to Operations > Telemetry
2. Click "Enable Telemetry"
3. Configure:
   - **Collection Interval**: 60 seconds
   - **Metrics**: Interface stats, BGP, VXLAN
   - **Destination**: NDFC (default)
4. Select switches
5. Click "Enable"

### Configure Alerts

1. Navigate to Operations > Alerts
2. Click "Add Alert Rule"
3. Configure:
   - **Rule Name**: High-CPU-Alert
   - **Condition**: CPU > 80%
   - **Duration**: 5 minutes
   - **Severity**: Critical
   - **Actions**: Email, Syslog, SNMP
4. Save rule

### Dashboard Configuration

1. Navigate to Operations > Dashboards
2. Click "Create Dashboard"
3. Add widgets:
   - Fabric topology
   - Interface statistics
   - BGP status
   - VXLAN tunnels
   - Alerts summary
4. Save dashboard

### Backup Configuration

**Automated Backups**:
1. Navigate to Settings > Backup & Restore
2. Configure backup schedule:
   - **Frequency**: Daily
   - **Time**: 02:00 AM
   - **Retention**: 30 days
   - **Location**: SFTP server or local
3. Enter SFTP details:
   - Server IP
   - Username
   - Password/SSH Key
   - Path
4. Test connection
5. Enable scheduled backup

## Best Practices

### Configuration Management
- Always use policies instead of direct CLI
- Document all configuration changes
- Use templates for consistency
- Implement change control process
- Regular configuration backups

### Security
- Change default passwords
- Use TACACS+/RADIUS for authentication
- Enable RBAC
- Use SSH keys
- Regular security audits
- Keep software updated

### Monitoring
- Enable telemetry on all devices
- Configure meaningful alerts
- Regular health checks
- Trend analysis
- Capacity planning

### High Availability
- Deploy 3-node cluster minimum
- Redundant network paths
- Regular backup verification
- Test failover procedures
- Document recovery procedures

## Troubleshooting Commands

```bash
# Nexus Dashboard
acs health
acs cluster status
show tech-support

# NDFC
# Check fabric status
# Operations > Fabric > Health

# Switch verification
show nve peers
show bgp l2vpn evpn summary
show vxlan
show vpc status
show interface status
show system resources
```

## Next Steps

After completing configuration:
1. [Post-Migration Validation](post-migration-validation.md)
2. [Troubleshooting Guide](troubleshooting.md)
3. Begin operational procedures

## References

- [Nexus Dashboard Configuration Guide](https://www.cisco.com/c/en/us/td/docs/dcn/nd/2x/configuration/cisco-nexus-dashboard-configuration-guide.html)
- [NDFC Configuration Guide](https://www.cisco.com/c/en/us/support/cloud-systems-management/prime-data-center-network-manager/series.html)
- [VXLAN EVPN Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/vxlan_evpn/guide/b_Nexus_9000_VXLAN_EVPN_Configuration_Guide.html)
