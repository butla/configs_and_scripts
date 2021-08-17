set -e

EFI_PARTITION=/dev/nvme0n1p1
# get this from `sudo blkid`
CRYPT_PARTITION_ID=050a93bf-d0d3-4d01-83c7-b65d060d2cc5

function log() {
    echo '---' $(date --iso-8601=seconds) $@ '---'
}

log "Setting up crypttab and fstab with proper partition IDs..."

# cat reads input from the "here document", redirects it to sudoed tee (it needs to write root files).
# Since we don't want the output it's redirected to /dev/null
cat <<EOF | sudo tee /mnt/etc/crypttab > /dev/null
# /etc/crypttab: mappings for encrypted partitions.
#
# Each mapped device will be created in /dev/mapper, so your /etc/fstab
# should use the /dev/mapper/<name> paths for encrypted devices.
#
# See crypttab(5) for the supported syntax.
#
# NOTE: Do not list your root (/) partition here, it must be set up
#       beforehand by the initramfs (/etc/mkinitcpio.conf). The same applies
#       to encrypted swap, which should be set up with mkinitcpio-openswap
#       for resume support.
#
# <name>	<device>			<password>	<options>
crypt		UUID=$CRYPT_PARTITION_ID	none		luks
EOF

# the only thing I'm changing here is the root (/) UUID
cat <<EOF | sudo tee /mnt/etc/fstab > /dev/null
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a device; this may
# be used with UUID= as a more robust way to name devices that works even if
# disks are added and removed. See fstab(5).
#
# <file system>             <mount point>  <type>  <options>  <dump>  <pass>
UUID=7E5B-9C2C                            /boot/efi      vfat    defaults,noatime 0 2
UUID=4f3c8672-650d-4a8b-9697-1817ec53bb78 /boot          ext4    defaults,noatime,discard 0 2
/dev/vg0/manjaro			  /              ext4    defaults,noatime,discard 0 1
tmpfs                                     /tmp           tmpfs   defaults,noatime,mode=1777 0 0
/swapfile 				  none 		 swap 	 defaults 0 0
EOF

log "Sending commands to the Manjaro install through chroot"
sudo chroot /mnt <<EOF

# Modify grub config.
# I'm stealing the stuff from the new Manjaro installing in an encrypted partition right now.
# I definitely don't want it with "quiet". I want to get logs. I'll see if something is off that way.
sed -i -E 's|GRUB_CMDLINE_LINUX_DEFAULT=".+"|GRUB_CMDLINE_LINUX_DEFAULT="apparmor=1 security=apparmor udev.log_priority=3"|' /etc/default/grub

# This is needed so that grub config and install will work.
# If you're writing typing this and not copying it, notice there's efivarFs and efivars.
mount -t efivarfs efivarfs /sys/firmware/efi/efivars

# preparing the config for grub
grub-mkconfig -o /boot/grub/grub.cfg  

# installing grub
grub-install $EFI_PARTITION
EOF

log "Success!"
