'''
Query a Minecraft server using its UDP Query protocol.
Details on Query protocal: https://wiki.vg/Query.
The Query protocal is disabled on the servers by default.
'''


import socket
import struct


import settings


BUFFER_SIZE = 4096
ITEMS_META = [
    {'name': 'MOTD', 'key': 'hostname', 'type': lambda s: s.decode(), 'default': ''},
    {'name': 'Version', 'key': 'version', 'type': lambda s: s.decode(), 'default': ''},
    {'name': 'Plugins', 'key': 'plugins', 'type': lambda s: s.decode(), 'default': 'No plugins'},
    {'name': 'Map', 'key': 'map', 'type': lambda s: s.decode(), 'default': ''},
    {'name': 'Number of online players', 'key': 'numplayers', 'type': lambda s: int(s.decode()), 'default': ''},
    {'name': 'Max number of players', 'key': 'maxplayers', 'type': lambda s: int(s.decode()), 'default': ''},
]


def get_status():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((settings.MC_SERVER, settings.QUERY_PORT))


    # Handshake
    request = b'\xFE\xFD' + struct.pack('!Bi', 9, 1)
    s.send(request)
    response = s.recv(BUFFER_SIZE)
    token = int(response[5: -1])


    # Full stat
    request = b'\xFE\xFD'  + struct.pack('!Bii', 0, 1, token) +  b'\x00\x00\x00\x00'
    s.send(request)
    response = s.recv(BUFFER_SIZE)
    response = response[16:]
    kv, players = response.split(b'\x00\x00\x01\x70\x6C\x61\x79\x65\x72\x5F\x00\x00')
    kv = kv.split(b'\x00')
    kv = dict(zip(map(lambda s: s.decode(), kv[::2]), kv[1::2]))
    items = dict()
    for item_meta in ITEMS_META:
        value = item_meta['type'](kv[item_meta['key']])
        items[item_meta['name']] = value if value is not '' else item_meta['default']
    players = list(map(lambda s: s.decode(), players.split(b'\x00')[:-2]))
    items['Players'] = players


    return items
