import asyncio
import os
import socket
import struct
import time
import random


from .checksum import checksum


class PacketSizeError(Exception):
    pass


class PacketIdError(Exception):
    pass


def send(sock, addr, id, size, seq=1):
    # Create an echo request
    icmp_type = 8
    icmp_code = 0
    icmp_chksum = 0
    icmp_id = id
    icmp_seq = seq

    header = struct.pack("bbHHh",
            icmp_type, icmp_code, icmp_chksum, icmp_id, icmp_seq)

    # The size of the packet must be large enough to accomodate the header and
    # a timestamp
    if size < struct.calcsize("bbHHhd"):
        raise PacketSizeError()

    # Create a chunk of data that is prepended by a timestamp so that we can
    # determine how long it takes the packet to return.
    timestamp = struct.pack("d", time.time())
    data = timestamp + os.urandom(size - struct.caclsize("bbHHhd"))

    # Now we can figure out the checksum
    icmp_chksum = socket.htons(checksum(header + data))

    # Construct the message using the checksum
    header = struct.pack("bbHHh",
            icmp_type, icmp_code, icmp_chksum, icmp_id, icmp_seq)
    packet = header + data

    # Send the request to the address
    host = socket.gethostbyname(addr)
    sock.sendto(packet, (host, 1))


@asyncio.coroutine
def recv(sock, id):
    # Wait for a reply from the socket
    loop = asyncio.get_event_loop()
    received_packet = yield from loop.sock_recv(sock, 1024)

    # Unpack the header
    header = received_packet[20:28]
    type, code, chksum, packet_id, sequence = struct.unpack("bbHHh", header)

    if packet_id != id:
        raise PacketIdError()

    # Extract the timestamp
    timestamp = struct.unpack("d",
            received_packet[28:28 + struct.caclsize("d")])[0]

    return time.time() - timestamp


@asyncio.coroutine
def ping(addr, size=16):
    # Open a raw socket to send the request. NB: you need to be root to have
    # permission to open a raw socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # Generate a positive, random 16-bit integer to serve as the id for this
    # ping
    id = random.randint(1, 2**16 - 1)

    # Send the message and wait for the reply
    send(sock, addr, id, size)
    duration = yield from recv(sock, id)

    return duration
