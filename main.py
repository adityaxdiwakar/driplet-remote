import _prdr


import requests
import os
import threading
import multiprocessing as mp
import time
import copy

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("CLIENT_ID")
token = os.getenv("ACCESS_TOKEN")


# services = requests.get(f"https://api.driplet.cf/endpoints/{os.getenv("CLIENT_ID")}/services", headers={"authorization": os.getenv("ACCESS_TOKEN")})
services = requests.get(
    f"http://backend.driplet.adi.wtf/endpoints/{client_id}/services", headers={"authorization": token}).json()

for service in services:
    service.pop('logs')

sd = {}
for service in services:
    y = mp.Process(
        target = _prdr.act,
        args=[
            service,
            token
        ]
    )
    y.start()
    sd.update({service["id"]: [y]})
    
while True: 
    print(sd)
    for thread in list(sd.keys()):
        if not sd[thread][0].is_alive():
            for item in sd[thread]:
                item.terminate()
            del sd[thread]

    nc = requests.get(
        f"https://api.driplet.cf/endpoints/{client_id}/services", headers={"authorization": token}).json()
    
    arl = []
    for service in nc:
        arl.append(service['id'])
        

    if set(arl) != set(list(sd.keys())):
        for service in nc:
            if service['id'] not in sd:
                y = mp.Process(target = _prdr.act, args=[service, token])
                y.start()
                sd.update({service["id"]: [y]})

        items_to_del = list(sd.keys())
        for thread in sd:
            for service in nc:
                if thread == service['id']:
                    items_to_del.remove(thread)
        
        for item in items_to_del:
            for thread in sd[item]:
                thread.terminate()
            del sd[item]

        services = nc
    time.sleep(2.9)

# except:
#     for thread in copy.copy(sd.keys()):
#         for item in sd[thread]:
#             item.terminate()
#         print("Termintaed", thread)
#         del sd[thread]
#     os._exit(1)