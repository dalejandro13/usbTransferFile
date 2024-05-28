from documents_manager import DocumentsManager
from usb_manager import UsbManager
import asyncio

doc_folder = DocumentsManager()
usb_manager = UsbManager(doc_folder)

# Tested on Ubuntu 22.04.4 LTS

if __name__ == "__main__":
    try:
        asyncio.run(usb_manager.read_usb())
    except KeyboardInterrupt:
        print("finalizando el monitoreo de usb")
    
    
    
    
