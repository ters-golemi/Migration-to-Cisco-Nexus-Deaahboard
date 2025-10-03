#!/usr/bin/env python3
"""
Backup All Switches Configuration Script

This script connects to all switches in the fabric and backs up their
running configurations to a local directory with timestamps.

Requirements:
    pip install paramiko netmiko

Usage:
    python backup-all-switches.py
"""

import os
import sys
from datetime import datetime
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Switch inventory
SWITCHES = [
    {'hostname': 'spine-01', 'ip': '192.168.1.1', 'role': 'spine'},
    {'hostname': 'spine-02', 'ip': '192.168.1.2', 'role': 'spine'},
    {'hostname': 'leaf-01', 'ip': '192.168.1.11', 'role': 'leaf'},
    {'hostname': 'leaf-02', 'ip': '192.168.1.12', 'role': 'leaf'},
    {'hostname': 'leaf-03', 'ip': '192.168.1.13', 'role': 'leaf'},
    {'hostname': 'leaf-04', 'ip': '192.168.1.14', 'role': 'leaf'},
]

# Backup directory
BACKUP_DIR = './backups'


def create_backup_directory():
    """Create backup directory if it doesn't exist"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, timestamp)
    
    try:
        os.makedirs(backup_path, exist_ok=True)
        logger.info(f"Created backup directory: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Failed to create backup directory: {str(e)}")
        sys.exit(1)


def backup_switch_config(switch_info, username, password, backup_path):
    """
    Backup configuration for a single switch
    
    Args:
        switch_info (dict): Dictionary containing switch details
        username (str): SSH username
        password (str): SSH password
        backup_path (str): Path to save backup files
    
    Returns:
        bool: True if successful, False otherwise
    """
    hostname = switch_info['hostname']
    ip = switch_info['ip']
    
    logger.info(f"Backing up {hostname} ({ip})...")
    
    device = {
        'device_type': 'cisco_nxos',
        'host': ip,
        'username': username,
        'password': password,
        'timeout': 60,
        'session_log': f'{backup_path}/{hostname}_session.log'
    }
    
    try:
        # Connect to device
        connection = ConnectHandler(**device)
        logger.info(f"Connected to {hostname}")
        
        # Get running configuration
        running_config = connection.send_command('show running-config')
        
        # Get startup configuration
        startup_config = connection.send_command('show startup-config')
        
        # Get version information
        version = connection.send_command('show version')
        
        # Get inventory
        inventory = connection.send_command('show inventory')
        
        # Save configurations
        running_config_file = os.path.join(backup_path, f'{hostname}_running-config.txt')
        startup_config_file = os.path.join(backup_path, f'{hostname}_startup-config.txt')
        version_file = os.path.join(backup_path, f'{hostname}_version.txt')
        inventory_file = os.path.join(backup_path, f'{hostname}_inventory.txt')
        
        with open(running_config_file, 'w') as f:
            f.write(running_config)
        
        with open(startup_config_file, 'w') as f:
            f.write(startup_config)
        
        with open(version_file, 'w') as f:
            f.write(version)
        
        with open(inventory_file, 'w') as f:
            f.write(inventory)
        
        # Disconnect
        connection.disconnect()
        
        logger.info(f"Successfully backed up {hostname}")
        logger.info(f"  Running config: {running_config_file}")
        logger.info(f"  Startup config: {startup_config_file}")
        logger.info(f"  Version info: {version_file}")
        logger.info(f"  Inventory: {inventory_file}")
        
        return True
        
    except NetmikoTimeoutException:
        logger.error(f"Timeout connecting to {hostname} ({ip})")
        return False
    except NetmikoAuthenticationException:
        logger.error(f"Authentication failed for {hostname} ({ip})")
        return False
    except Exception as e:
        logger.error(f"Error backing up {hostname}: {str(e)}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Switch Configuration Backup Script")
    print("=" * 60)
    print()
    
    # Get credentials
    username = input("Enter SSH username: ")
    password = getpass("Enter SSH password: ")
    
    # Create backup directory
    backup_path = create_backup_directory()
    
    # Backup summary
    successful = []
    failed = []
    
    # Backup each switch
    print()
    print("Starting backup process...")
    print()
    
    for switch in SWITCHES:
        success = backup_switch_config(switch, username, password, backup_path)
        
        if success:
            successful.append(switch['hostname'])
        else:
            failed.append(switch['hostname'])
        
        print()
    
    # Summary
    print("=" * 60)
    print("Backup Summary")
    print("=" * 60)
    print(f"Total switches: {len(SWITCHES)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print()
    
    if successful:
        print("Successfully backed up:")
        for hostname in successful:
            print(f"  ✓ {hostname}")
        print()
    
    if failed:
        print("Failed to backup:")
        for hostname in failed:
            print(f"  ✗ {hostname}")
        print()
    
    print(f"Backup location: {backup_path}")
    print()
    
    # Create summary file
    summary_file = os.path.join(backup_path, 'backup_summary.txt')
    with open(summary_file, 'w') as f:
        f.write("Backup Summary\n")
        f.write("=" * 60 + "\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total switches: {len(SWITCHES)}\n")
        f.write(f"Successful: {len(successful)}\n")
        f.write(f"Failed: {len(failed)}\n")
        f.write("\n")
        
        if successful:
            f.write("Successfully backed up:\n")
            for hostname in successful:
                f.write(f"  {hostname}\n")
            f.write("\n")
        
        if failed:
            f.write("Failed to backup:\n")
            for hostname in failed:
                f.write(f"  {hostname}\n")
    
    logger.info(f"Summary saved to: {summary_file}")
    
    # Exit with appropriate code
    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
