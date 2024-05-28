import os
from pathlib import Path
import asyncio
import shutil

class DocumentsManager:

    async def find_documents_folder(self):
        return await self.get_documents_folder()

    async def get_documents_folder(self):
        home = Path.home()
        possible_folders = ['Documents', 'Documentos']

        for folder in possible_folders:
            documents_path = home / folder
            if documents_path.is_dir():
                return str(documents_path)
        return None

    async def copy_files_to_documents(self, usb_mount_path):
        src_folder = os.path.join(usb_mount_path, 'files')
        dst_folder = await self.find_documents_folder()

        if not os.path.exists(src_folder):
            raise FileNotFoundError(f"Files folder not found 'files' in {src_folder}")

        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        for item in os.listdir(src_folder):
            src_path = os.path.join(src_folder, item)
            dst_path = os.path.join(dst_folder, item)

            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)

        print(f"Copied Files of {src_folder} to {dst_folder}")

