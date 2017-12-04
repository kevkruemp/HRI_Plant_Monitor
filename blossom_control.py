import urllib2
blossom_add = 'http://10.156.9.99:5555/s/'

def cmd_blossom(blossom_s, blossom_idle=''):
    # command blossom
    blossom_cmd = blossom_add+blossom_s+'/'+blossom_idle
    try:
        urllib2.urlopen(blossom_cmd,timeout=1)
    except:
        pass