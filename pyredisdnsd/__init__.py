import dnslib

from gevent.server import DatagramServer
from dnslib import DNSRecord, DNSHeader, RR


class Store(object):
    def __init__(self, conn):
        self.conn = conn

    def lookup(self, qname, qtype):
        """Look up a record in redis"""

        key = "%s:%s" % (qname, qtype)
        return self.conn.get(key)


class DNSServer(DatagramServer):
    def __init__(self, listen, store, *args, **kwargs):
        self.store = store
        DatagramServer.__init__(self, listen, *args, **kwargs)

    def response_from_request(self, request, *args, **kwargs):
        """Create a DNSRecord response based on the original request"""

        return DNSRecord(DNSHeader(id=request.header.id, *args, **kwargs))

    def create_result(self, qname, qtype, value):
        """Create a result response for a question"""

        record_class = getattr(dnslib, qtype)
        return RR(
            rname=qname,
            rtype=dnslib.QTYPE[qtype],
            rdata=record_class(value)
        )

    def handle(self, data, address):
        print("DEBUG Received request from %s" % (address[0]))
        request = DNSRecord.parse(data)
        response = self.response_from_request(request, qr=1, aa=1, ra=1)

        for question in request.questions:
            qname = question.qname
            qtype = dnslib.QTYPE[question.qtype]

            return_value = self.store.lookup(qname, qtype)
            if return_value is None:
                response.header.rcode = 2
            else:
                response.add_answer(self.create_result(
                    qname, qtype, return_value
                ))

            response.add_question(question)

        print("DEBUG Response: \n%s" % response)
        self.socket.sendto(response.pack(), address)
