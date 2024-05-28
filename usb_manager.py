import os
import asyncio
import pyudev
from pathlib import Path
import subprocess
import time
import shutil

class UsbManager:
    def __init__(self, documents_manager):
        self.documents_manager = documents_manager

    async def get_mount_path(self, device_node):
        with open('/proc/mounts', 'r') as mounts:
            for line in mounts:
                if device_node in line:
                    return line.split()[1]
        return None

    async def mount_device(self, device_node):
        try:
            subprocess.run(['udisksctl', 'mount', '-b', device_node], check=True)
            await asyncio.sleep(2)  # Wait a moment for the system to complete assembly
            mount_path = await self.get_mount_path(device_node)
            return mount_path
        except subprocess.CalledProcessError as e:
            print(f"Error mounting the device {device_node}: {e}")
            return None

    async def eject_usb(self, device_node):
        try:
            subprocess.run(['udisksctl', 'unmount', '-b', device_node], check=True)
            subprocess.run(['udisksctl', 'power-off', '-b', device_node], check=True)
            print(f"Dispositivo {device_node} expulsado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to eject the device {device_node}: {e}")

    async def read_usb(self):
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='block', device_type='partition')

        print("Waiting for the USB stick connection...")
        for device in iter(monitor.poll, None):
            if device.action == 'add':
                device_path = device.device_node
                mount_path = await self.get_mount_path(device_path)
                if not mount_path:
                    print(f"The device {device_path} it is not assembled. Trying to ride it...")
                    mount_path = await self.mount_device(device_path)

                if mount_path:
                    print(f"Connected devices: {device_path}")
                    print(f"Assembly Path: {mount_path}")
                    try:
                        await self.documents_manager.copy_files_to_documents(mount_path)
                        await asyncio.sleep(2)
                        await self.eject_usb(device_path)
                    except Exception as e:
                        print(f"Error copying files or ejecting the device: {e}")
                        await asyncio.sleep(2)
                        print("Ejecting USB Device")
                        await self.eject_usb(device_path)
                else:
                    print(f"Could not find the mounting path for the device: {device_path}")

