# HelmOS Debian Live-Build Profile

This profile builds a bootable ISO that autologins on TTY1 and auto-starts the HelmOS keyboard palette.

## Host prerequisites (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install -y live-build syslinux-utils xorriso squashfs-tools rsync

Prepare app files

Copies the repo's HelmOS/ into the live image under /opt/HelmOS:

cd os/debian-live
./prepare.sh

Build the ISO
./build.sh


Result: live-image-amd64.hybrid.iso in this directory.

Notes

The image autologins as user live on TTY1 and runs HelmOS.

HelmOS persists runtime data in /home/live/.local/share/helmos/ (logs, memory).

To customize packages, edit config/package-lists/helmos.list.chroot.

To change autostart/service behavior, edit config/includes.chroot/etc/systemd/system/helmos.service.
