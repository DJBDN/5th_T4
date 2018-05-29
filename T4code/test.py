import httplib
import json
import threading


class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    # get the list of all flow tables
    def get(self):
        ret = self.get_all({}, 'GET')
        return json.loads(ret[2])

    def get_all(self, data, action):
        path = '/wm/staticentrypusher/list/all/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret


# the links of that topo
links = {
    "S1": ["null", "H1", "H2", "H3", "S2", "S3", "S4"],
    "S2": ["null", "S1", "S5"],
    "S3": ["null", "S1", "S5"],
    "S4": ["null", "S1", "S5"],
    "S5": ["null", "H4", "H5", "H6", "S2", "S3", "S4"]
}

pusher = StaticFlowPusher('127.0.0.1')


# get host name by ip
def get_name(ip):
    if ip == "10.0.0.1":
        return "H1"
    elif ip == "10.0.0.2":
        return "H2"
    elif ip == "10.0.0.3":
        return "H3"
    elif ip == "10.0.0.4":
        return "H4"
    elif ip == "10.0.0.5":
        return "H5"
    elif ip == "10.0.0.6":
        return "H6"
    else:
        return "null"


# find the path between src_ip and dst_ip
def find_path(src_ip, dst_ip):
    # invalid input
    if get_name(src_ip) == "null":
        print "invalid ipv4 address"
        exit(1)
    if get_name(dst_ip) == "null":
        print "invalid ipv4 address"
        exit(1)

    print get_name(src_ip),

    # get the flow table
    switches = pusher.get()
    if len(switches) == 0:
        print "->null"
        return

    for switch in links.keys():
        if get_name(src_ip) in links[switch] and get_name(dst_ip) in links[switch]:
            print "->",
            print switch,
            print "->",
            print get_name(dst_ip)
            return

    for switch in links.keys():
        if get_name(src_ip) in links[switch]:
            print "->",
            print switch,
            break
    print "->",

    if "00:00:00:00:00:00:00:02" in switches.keys() and len(switches["00:00:00:00:00:00:00:02"]) != 0:
        print "S2",
    elif "00:00:00:00:00:00:00:03" in switches.keys() and len(switches["00:00:00:00:00:00:00:03"]) != 0:
        print "S3",
    elif "00:00:00:00:00:00:00:04" in switches.keys() and len(switches["00:00:00:00:00:00:00:04"]) != 0:
        print "S4",

    for switch in links.keys():
        if get_name(dst_ip) in links[switch]:
            print "->",
            print switch,
            break
    print "->",
    print get_name(dst_ip)


# timer function
# sleep by 10 seconds and find path
def fun_timer():
    find_path(src, dst)
    global timer
    timer = threading.Timer(10, fun_timer)
    timer.start()


# start the test
print "----------test start-----------"
# show the host name and its ip
print "host--ip"
print "h1----10.0.0.1"
print "h2----10.0.0.2"
print "h3----10.0.0.3"
print "h4----10.0.0.4"
print "h5----10.0.0.5"
print "h6----10.0.0.6"
# input src ip and dst ip
src = raw_input("src ip:")
dst = raw_input("dst ip:")
# start to print path of packet sent per 10 seconds
find_path(src, dst)
timer = threading.Timer(10, fun_timer)
timer.start()
