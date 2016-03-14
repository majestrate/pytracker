import bencodepy
import hashlib
from binascii import hexlify

def parseTorrent(fd):
    """
    parse a torrent from a file descriptor
    return dict that was bencoded
    will raise of parse error
    """
    data = fd.read()
    return bencodepy.decode(data)

def dumpTorrent(tdict, fd):
    """
    dump a parsed torrent into a file
    """
    data = bencodepy.encode(tdict)
    fd.write(data)

def validate(tdict):
    """
    check if this torrent dict is valid
    return true if it is valid otherwise return false
    """
    return tdict is not None and b'info' in tdict and b'name' in tdict[b'info']

def infohash(tdict):
    """
    given a decoded torrent file compute the infohash
    """
    return hashlib.sha1(bencodepy.encode(tdict[b'info'])).digest()

def infohash_hex(tdict):
    """
    given a decoded torrent file compute the infohash
    return hexstring
    """
    return hexlify(infohash(tdict)).decode('ascii')



def torrentName(tdict):
    """
    get the name of a torrent
    """
    return tdict[b'info'][b'name'].decode("utf-8")
