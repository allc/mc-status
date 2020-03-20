import socket
import struct


SERVER = 'localhost'
PORT = 25565


BUFFER_SIZE = 4096
ITEMS_META = [
    {'name': 'MOTD', 'key': 'hostname', 'type': lambda s: s.decode(), 'default': ''},
    {'name': 'Version', 'key': 'version', 'type': lambda s: s.decode(), 'default': ''},
    {'name': 'Plugins', 'key': 'plugins', 'type': lambda s: s.decode(), 'default': 'No plugins'},
    {'name': 'Map', 'key': 'map', 'type': lambda s: s.decode(), 'default': ''},
    {'name': 'Number of online players', 'key': 'numplayers', 'type': lambda s: int(s.decode()), 'default': ''},
    {'name': 'Max number of players', 'key': 'maxplayers', 'type': lambda s: int(s.decode()), 'default': ''},
]


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((SERVER, PORT))


# Handshake
request = b'\xFE\xFD' + struct.pack('!Bi', 9, 1)
print('Handshake request: ', request)
s.send(request)
response = s.recv(BUFFER_SIZE)
print('Handshake response: ', response)
token = int(response[5: -1])
print('Challenge token:', token)


# Full stat
request = b'\xFE\xFD'  + struct.pack('!Bii', 0, 1, token) +  b'\x00\x00\x00\x00'
print('Full stat request: ', request)
s.send(request)
response = s.recv(BUFFER_SIZE)
print('Full stat response: ', response)
response = response[16:]
kv, players = response.split(b'\x00\x00\x01\x70\x6C\x61\x79\x65\x72\x5F\x00\x00')
kv = kv.split(b'\x00')
kv = dict(zip(map(lambda s: s.decode(), kv[::2]), kv[1::2]))
items = dict()
for item_meta in ITEMS_META:
    value = item_meta['type'](kv[item_meta['key']])
    items[item_meta['name']] = value if value is not '' else item_meta['default']
print('status:', items)
players = list(map(lambda s: s.decode(), players.split(b'\x00')[:-2]))
print('players: ', players)
if len(players) == 1:
    print('{} is the only player on this server and might feel lonely.'.format(players[0]))
