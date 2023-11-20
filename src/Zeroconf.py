from zeroconf import ServiceBrowser, Zeroconf
import socket

class OSCQueryServiceProfile:
    def __init__(self, name, address, port, service_type):
        self.name = name
        self.address = address
        self.port = port
        self.service_type = service_type

class MyListener:
    def __init__(self):
        self.oscQueryServices = set()
        self.oscServices = set()

    def remove_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        profile = OSCQueryServiceProfile(info.name, socket.inet_ntoa(info.addresses[0]), info.port, service_type)
        if service_type == "_osc._udp.local.":
            self.oscServices.remove(profile)
        elif service_type == "_oscjson._tcp.local.":
            self.oscQueryServices.remove(profile)

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        profile = OSCQueryServiceProfile(info.name, socket.inet_ntoa(info.addresses[0]), info.port, service_type)
        if service_type == "_osc._udp.local.":
            self.oscServices.add(profile)
        elif service_type == "_oscjson._tcp.local.":
            self.oscQueryServices.add(profile)

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, ["_osc._udp.local.", "_oscjson._tcp.local."], listener)

# use the services
print("OSCQueryServices:", listener.oscQueryServices)
print("OSCServices:", listener.oscServices)

zeroconf.close()
