import sys
import copy
import json
import socket

deltas = {
    "updates": [
        {
            "source": {
                "label": "rpi:%s" % socket.gethostname()
            },
            "values": []
        }
    ]
}

d1 = copy.deepcopy(deltas)
d1["updates"][0]["values"].append({
    "path":  "system.stdout",
    "value": "testdata"
})
sys.stdout.write(json.dumps(d1))

d2 = copy.deepcopy(deltas)
d2["updates"][0]["values"].append({
    "path":  "system.stderr",
    "value": "testdata"
})
sys.stderr.write(json.dumps(d2))

d3 = copy.deepcopy(deltas)
d3["updates"][0]["values"].append({
    "path":  "system.__stdout__",
    "value": "testdata"
})
sys.stdout.write(json.dumps(d3))

d4 = copy.deepcopy(deltas)
d4["updates"][0]["values"].append({
    "path":  "system.__stderr__",
    "value": "testdata"
})
sys.__stderr__.write(json.dumps(d4))
