import httplib
import json
import threading


class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret


pusher = StaticFlowPusher('127.0.0.1')
# flow tables for s1
# use s1-s2
flow1_left_4 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-left",
    "cookie": "0",
    "priority": "2",
    "active": "true",
    "actions": "output=4"
}
# use s1-s3
flow1_left_5 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-left",
    "cookie": "0",
    "priority": "2",
    "active": "true",
    "actions": "output=5"
}
# use s1-s4
flow1_left_6 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-left",
    "cookie": "0",
    "priority": "2",
    "active": "true",
    "actions": "output=6"
}
# to h1
flow1_right_1 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-right-1",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "00:00:00:00:00:01",
    "active": "true",
    "actions": "output=1"
}
# to h2
flow1_right_2 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-right-2",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "00:00:00:00:00:02",
    "active": "true",
    "actions": "output=2"
}
# to h3
flow1_right_3 = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-right-3",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "00:00:00:00:00:03",
    "active": "true",
    "actions": "output=3"
}
# handle the ARP packet
flow1_right_broadcast = {
    'switch': "00:00:00:00:00:00:00:01",
    "name": "1-right-broadcast",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "ff:ff:ff:ff:ff:ff",
    "active": "true",
    "actions": "output=flood"
}

# flow tables for s5
# use s2-s5
flow5_right_4 = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-right",
    "cookie": "0",
    "priority": "2",
    "active": "true",
    "actions": "output=4"
}
# use s3-s5
flow5_right_5 = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-right",
    "cookie": "0",
    "priority": "2",
    "active": "true",
    "actions": "output=5"
}
# use s4-s5
flow5_right_6 = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-right",
    "cookie": "0",
    "priority": "2",
    "active": "true",
    "actions": "output=6"
}
# to h4
flow5_left_1 = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-left-1",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "00:00:00:00:00:04",
    "active": "true",
    "actions": "output=1"
}
# to h5
flow5_left_2 = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-left-2",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "00:00:00:00:00:05",
    "active": "true",
    "actions": "output=2"
}
# to h6
flow5_left_3 = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-left-3",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "00:00:00:00:00:06",
    "active": "true",
    "actions": "output=3"
}
# handle ARP packet
flow5_left_broadcast = {
    'switch': "00:00:00:00:00:00:00:05",
    "name": "5-left-broadcast",
    "cookie": "0",
    "priority": "3",
    "eth_dst": "ff:ff:ff:ff:ff:ff",
    "active": "true",
    "actions": "output=flood"
}

pusher.set(flow1_left_4)
pusher.set(flow1_right_1)
pusher.set(flow1_right_2)
pusher.set(flow1_right_3)
pusher.set(flow1_right_broadcast)

pusher.set(flow5_right_4)
pusher.set(flow5_left_1)
pusher.set(flow5_left_2)
pusher.set(flow5_left_3)
pusher.set(flow5_left_broadcast)

# s2 table
# from 1 to 2 and from 2 to 1
flow2_right = {
    'switch': "00:00:00:00:00:00:00:02",
    "name": "2-right",
    "cookie": "0",
    "priority": "32768",
    "in_port": "1",
    "active": "true",
    "actions": "output=2"
}
flow2_left = {
    'switch': "00:00:00:00:00:00:00:02",
    "name": "2-left",
    "cookie": "0",
    "priority": "32768",
    "in_port": "2",
    "active": "true",
    "actions": "output=1"
}
# s3 table
# from 1 to 2 and from 2 to 1
flow3_right = {
    'switch': "00:00:00:00:00:00:00:03",
    "name": "3-right",
    "cookie": "0",
    "priority": "32768",
    "in_port": "1",
    "active": "true",
    "actions": "output=2"
}
flow3_left = {
    'switch': "00:00:00:00:00:00:00:03",
    "name": "3-left",
    "cookie": "0",
    "priority": "32768",
    "in_port": "2",
    "active": "true",
    "actions": "output=1"
}
# s4 table
# from 1 to 2 and from 2 to 1
flow4_right = {
    'switch': "00:00:00:00:00:00:00:04",
    "name": "4-right",
    "cookie": "0",
    "priority": "32768",
    "in_port": "1",
    "active": "true",
    "actions": "output=2"
}
flow4_left = {
    'switch': "00:00:00:00:00:00:00:04",
    "name": "4-left",
    "cookie": "0",
    "priority": "32768",
    "in_port": "2",
    "active": "true",
    "actions": "output=1"
}

intro = 2


# change the flow tables
def fun_timer():
    global intro
    if intro == 1:
        # set s1-s2
        pusher.set(flow1_left_4)
        pusher.set(flow5_right_4)
        # guarantee s2 is the only way to pass
        pusher.remove(flow4_left)
        pusher.remove(flow4_right)
        pusher.set(flow2_left)
        pusher.set(flow2_right)
        intro = 2
    elif intro == 2:
        pusher.set(flow1_left_5)
        pusher.set(flow5_right_5)
        # guarantee s3 is the only way to pass
        pusher.remove(flow2_left)
        pusher.remove(flow2_right)
        pusher.set(flow3_left)
        pusher.set(flow3_right)
        intro = 3
    elif intro == 3:
        pusher.set(flow1_left_6)
        pusher.set(flow5_right_6)
        # guarantee s4 is the only way to pass
        pusher.remove(flow3_left)
        pusher.remove(flow3_right)
        pusher.set(flow4_left)
        pusher.set(flow4_right)
        intro = 1
    global timer
    timer = threading.Timer(30, fun_timer)
    timer.start()


pusher.set(flow2_left)
pusher.set(flow2_right)
timer = threading.Timer(30, fun_timer)
timer.start()
