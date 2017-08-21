import picoweb
import uasyncio as asyncio
import gc
import network
import socket
import ustruct
import ure as re
import wifi_database
from picoweb.utils import parse_qs
import utime
gc.collect()

class HTTPRequest:

    def __init__(self):
        pass

    def read_form_data(self):
        size = int(self.headers["Content-Length"])
        data = yield from self.reader.readline()
        line = data.decode()
        if line.startswith('------'):
            boundary = line
            chars_read = len(line)
            self.form = {}
            while True:
                data = yield from self.reader.readline()
                line = data.decode()
                chars_read += len(line)
                if line == boundary:
                    continue
                if chars_read >= size or line == boundary.strip() + '--\r\n':
                    break
                elif line.startswith('Content-Disposition: form-data;'):
                    field = re.compile('.*=\"(.*)\"').match(line).group(1)
                elif line != '\r\n':
                    self.form[field] = line.strip()
        else:
            form = parse_qs(line)
            self.form = form

class MyWebApp(picoweb.WebApp):
    def get_task(self, host='0.0.0.0', port=80, debug=False):
        gc.collect()
        self.debug = int(debug)
        self.init()
        if debug:
            print("* Running on http://%s:%s/" % (host, port))
        return asyncio.start_server(self._handle, host, port)


def handle_template(req, resp):
    if req.method == 'POST':
        yield from req.read_form_data()
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, req.url_match.group(1), (req, ))


async def dns_server():
    myip = network.WLAN(network.AP_IF).ifconfig()[0]
    print('binding to', myip)
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mysocket.bind(socket.getaddrinfo(myip, 53)[0][-1])
    while True:
        yield uasyncio.IORead(mysocket)
        mysocket.setblocking(False)
        packet, address = mysocket.recvfrom(256)
        # is query? opcode 0? 1 question?
        if (packet[2] & 0x80 == 0x0 and packet[2] & 0xf0 == 0x0 and packet[4:6] == b'\x00\x01'):
            # we take the request, change a few bits and append the answer
            response = bytearray(packet)
            response[2] |= 0x80 # change from query to response
            response[3] = 0 # recursion not available and responsecode stays 0
            response[7] = 1 # number of answers
            response += b'\xc0\x0c' # stuff
            response += b'\x00\x01' # A entry
            response += b'\x00\x01' # class IN
            response += b'\x00\x00\x00\x00' # TTL 0
            response += b'\x00\x04' # length of address
            response += ustruct.pack('BBBB', *[int(x) for x in myip.split('.')])
            mysocket.sendto(response, address)

ROUTES = [
    ('/', lambda req, resp: (yield from app.sendfile(resp, 'index.html'))),
    (re.compile("^/(.*\.htm[l]?)$"), lambda req, resp: (yield from app.handle_static(req, resp))),
    (re.compile("^/(.*\.css)$"), lambda req, resp: (yield from app.handle_static(req, resp))),
    (re.compile("^/(.+\.tpl)($|\?.*)"), lambda req, resp: (yield from handle_template(req, resp))),
]
app = MyWebApp(pkg='html', serve_static=False, routes=ROUTES)
gc.collect()
app._load_template('wifi-scan.tpl')
app._load_template('wifi-add.tpl')
app._load_template('wifi-status.tpl')
app._load_template('wifi-saved.tpl')
gc.collect()
