import BAC0

influx_params = {
"name": "InfluxDB",
"url" : "http://localhost",
"port" : 8086,
"token" : "p5Q5iOlbVi_1CaoMshWIi0L6G4wHob5TRbmBW_rP8ai4_QgUjhXMW_ZBpWT9FsEyXh7RRrVNWhidueLCDecffA==",
"org" : "data",
"bucket" : "data"
}

bnet = BAC0.lite('10.47.35.1/24', db_params=influx_params)
bnet.discover()

for (address, device_id) in bnet.discoveredDevices:
    dev = BAC0.device(address, device_id, bnet, poll=10)
