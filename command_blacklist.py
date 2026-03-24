# Command Blacklist for Security
# Keep your system from imploding

COMMAND_BLACKLIST = [
    "rm -rf /",                    # Deletes everything
    "rm -rf ~",                    # Deletes home directory
    "rm -rf *",                    # Deletes current directory contents
    ":(){ :|:& };:",               # Fork bomb
    "dd if=/dev/zero of=/dev/sda", # Overwrites disk
    "dd if=/dev/urandom of=/dev/sda", # Random overwrite
    "mkfs",                        # Format filesystem
    "mkfs.ext4",                   # Format ext4
    "mkfs.xfs",                    # Format XFS
    "format",                      # Windows format command
    "chmod 777 -R /",              # Open all permissions recursively
    "chmod 777 -R /etc",           # Open /etc permissions
    "chmod 777 -R /root",          # Open root permissions
    "shutdown",                    # Shutdown system
    "shutdown -h now",             # Immediate shutdown
    "reboot",                      # Reboot system
    "init 0",                      # Runlevel 0 (halt)
    "init 6",                      # Runlevel 6 (reboot)
    "poweroff",                    # Power off
    "iptables -F",                 # Flush firewall rules
    "iptables -X",                 # Delete custom chains
    "iptables -t nat -F",          # Flush NAT table
    "useradd",                     # Create users
    "usermod",                     # Modify users
    "passwd",                      # Change passwords
    "echo > /proc/*",              # Mess with kernel params
    "echo 1 > /proc/sys/kernel/panic", # Kernel panic settings
    "wget * | sh",                 # Run random scripts
    "curl * | sh",                 # Run random scripts
    "curl * | bash",               # Run random bash scripts
    "wget * | bash",               # Run random bash scripts
    "python -c 'import os; os.system(\"rm -rf /\")'", # Python delete
    "perl -e 'system(\"rm -rf /\")'", # Perl delete
    "find / -delete",              # Delete everything via find
    "nohup rm -rf / &",            # Background delete
    "history -c",                  # Clear command history (suspicious)
    "setenforce 0",                # Disable SELinux
    "apparmor_status",             # Mess with AppArmor
    "umount -a",                   # Unmount all filesystems
    "umount /",                    # Unmount root
    "swapoff -a",                  # Disable all swap
    "sysctl -w kernel.panic=0",    # Disable kernel panic reboot
    "pkill -9",                    # Kill all processes
    "killall -9",                  # Kill all by name
    "fstrim -av",                  # Aggressive SSD trim
    "hdparm --security-erase",     # Secure erase drives
    "cryptsetup luksFormat",       # Format encrypted volumes
]

# Usage: Check if command in COMMAND_BLACKLIST before execution
# if user_command in COMMAND_BLACKLIST:
#     raise SecurityError("Command blacklisted!")
