import urllib
from datetime import datetime
url = "http://111.67.195.174/sh/db.tar.gz"
file = "db.tar.gz"
_prev = 0
_s = datetime.now()


def reporthook(blocks_read, block_size, total_size):
    global _prev
    if not blocks_read:
        print ("Connection opened")
    if total_size < 0:
        print "Read %d blocks" % blocks_read
    else:
        if blocks_read * block_size * 100 / total_size - _prev > 0.1:
            _prev = blocks_read * block_size * 100 / total_size
            percent = blocks_read * block_size * 100 / total_size
            total = total_size / 1024 / 1024.0
            speed = blocks_read * block_size / 1024 / (datetime.now() - _s).seconds
            print "%d percents of %d MB, speed: %dKB/s, left time: %d min %d second" % (percent, total, speed, total * 1024 / speed / 60, total * 1024 / speed % 60)

if __name__ == '__main__':
    urllib.urlretrieve(url, file, reporthook)
