import gevent
import os
import redis

from pyredisdnsd import Store, DNSServer

# Patch redis to use the gevent socket
redis.connection.socket = gevent.socket

# Get configuration from environment
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = os.environ.get('REDIS_DB', 0)
RDNSD_LISTEN = os.environ.get('RDNSD_LISTEN', ':53')

def main():
    conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    store = Store(conn)
    print "Listening on %s" % DNS_LISTEN
    DNSServer(RDNSD_LISTEN, store=store).serve_forever()

if __name__ == "__main__":
    main()

