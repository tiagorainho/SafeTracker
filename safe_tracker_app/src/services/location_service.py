from __future__ import annotations
from typing import Mapping, List
import numpy as np, math
from beacontools import BeaconScanner, EddystoneTLMFrame, BluetoothAddressType, EddystoneUIDFrame
from time import time


signals_buffer: Mapping[str, List[Signal]]
buffer_max_size = 10
buffer_time_limit = 10
tran_pow=pow(10,-66/10)/1000
Area=.8*pow(10,-2)
earthR = 6371


class Localization:
    lat: float
    lon: float
    height: float

    def __init__(self, lat: float, lon: float, height: float = 0):
        self.lat = lat
        self.lon = lon
        self.height = height

class Beacon:
    localization: Localization
    power_sent: float

    def __init__(self, localization: Localization, power_sent: float) -> None:
        self.localization = localization
        self.power_sent = power_sent

class Signal:
    beacon_id: str
    power_received: float
    timestamp: float

    def __init__(self, beacon_id: str, power_received:float, timestamp: float = 0) -> None:
        self.beacon_id = beacon_id
        self.power_received = power_received
        self.timestamp = timestamp


registered_beacons: Mapping[str, Beacon] = {
    "a"*20: Beacon(localization=Localization(40.623851, -8.656939), power_sent=tran_pow),
    "b"*20: Beacon(Localization=Localization(40.623897, -8.656820), power_sent=tran_pow), 
    "c"*20: Beacon(localization=Localization(40.624074,-8.656998), power_sent=tran_pow)
}


def triangulate_position_with_3_points(signals: List[Signal]):

    for i, signal in enumerate(signals):
        print(f"{signal.beacon_id}: {distances[i]*1000}")

    connected_beacons = [registered_beacons[signal.beacon_id] for signal in signals]

    distances = [(registered_beacons[signal.beacon_id].power_sent/(4*np.pi * signal.power_received))**(1/2) * Area for signal in signals]
    
    # Point 1
    xA = (earthR) *(math.cos(math.radians(connected_beacons[0].localization.lat)) * math.cos(math.radians(connected_beacons[0].localization.lon)))
    yA = (earthR) *(math.cos(math.radians(connected_beacons[0].localization.lat)) * math.sin(math.radians(connected_beacons[0].localization.lon)))
    zA = (earthR) *(math.sin(math.radians(connected_beacons[0].localization.lat)))

    # Point 2
    xB = (earthR) *(math.cos(math.radians(connected_beacons[1].localization.lat)) * math.cos(math.radians(connected_beacons[1].localization.lon)))
    yB = (earthR) *(math.cos(math.radians(connected_beacons[1].localization.lat)) * math.sin(math.radians(connected_beacons[1].localization.lon)))
    zB = (earthR) *(math.sin(math.radians(connected_beacons[1].localization.lat)))

    # Point 3
    xC = (earthR) *(math.cos(math.radians(connected_beacons[2].localization.lat)) * math.cos(math.radians(connected_beacons[2].localization.lon)))
    yC = (earthR) *(math.cos(math.radians(connected_beacons[2].localization.lat)) * math.sin(math.radians(connected_beacons[2].localization.lon)))
    zC = (earthR) *(math.sin(math.radians(connected_beacons[2].localization.lat)))

    P1 = np.array([xA, yA, zA])
    P2 = np.array([xB, yB, zB])
    P3 = np.array([xC, yC, zC])

    ex = (P2 - P1)/(np.linalg.norm(P2 - P1))
    i = np.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(np.linalg.norm(P3 - P1 - i*ex))
    ez = np.cross(ex,ey)
    d = np.linalg.norm(P2 - P1)
    j = np.dot(ey, P3 - P1)


    x = (pow(distances[0],2) - pow(distances[1],2) + pow(d,2))/(2*d)
    y = ((pow(distances[0],2) - pow(distances[2],2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)
    z = np.sqrt(pow(distances[0],2) - pow(x,2) - pow(y,2))

    tmp=pow(distances[0],2) - pow(x,2) - pow(y,2)
    if pow(distances[0],2) - pow(x,2) - pow(y,2)>0:
        z=np.sqrt(tmp)


    triPt = P1 + x*ex + y*ey + z*ez
    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1],triPt[0]))

    # take into consideration the height
    new_pos = (
        lat, 
        lon, 
        int(np.average([
            connected_beacons[0].localization.height, 
            connected_beacons[1].localization.height, 
            connected_beacons[2].localization.height
        ]))
    )
    
    return new_pos

def triangulate_position_with_2_points(signals: List[Signal]):

    for i, signal in enumerate(signals):
        print(f"{signal.beacon_id}: {distances[i]*1000}")

    connected_beacons = [registered_beacons[signal.beacon_id] for signal in signals]

    distances = [(registered_beacons[signal.beacon_id].power_sent/(4*np.pi * signal.power_received))**(1/2) * Area for signal in signals]


    xA = (earthR) *(math.cos(math.radians(connected_beacons[0].localization.lat)) * math.cos(math.radians(connected_beacons[0].localization.lon)))
    yA = (earthR) *(math.cos(math.radians(connected_beacons[0].localization.lat)) * math.sin(math.radians(connected_beacons[0].localization.lon)))
    zA = (earthR) *(math.sin(math.radians(connected_beacons[0].localization.lat)))

    xB = (earthR) *(math.cos(math.radians(connected_beacons[1].localization.lat)) * math.cos(math.radians(connected_beacons[1].localization.lon)))
    yB = (earthR) *(math.cos(math.radians(connected_beacons[1].localization.lat)) * math.sin(math.radians(connected_beacons[1].localization.lon)))
    zB = (earthR) *(math.sin(math.radians(connected_beacons[1].localization.lat)))

    x = (distances[1]*xA + distances[0]*xB)/(distances[0]+distances[1])
    y = (distances[1]*yA + distances[0]*yB)/(distances[0]+distances[1])
    z = (distances[1]*zA + distances[0]*zB)/(distances[0]+distances[1])

    lat = math.degrees(math.asin(z / earthR))
    lon = math.degrees(math.atan2(y,x))

    new_pos = (
        lat, 
        lon, 
        int(np.average([
            connected_beacons[0].localization.height, 
            connected_beacons[1].localization.height
        ]))
    )

    return new_pos

def crop_buffer(signals_buffer: Mapping[str, List[Signal]], buffer_max_size: int, buffer_time_limit: float):
    current_time = time()

    for signals in signals_buffer.values():
        # crop by size
        while len(signals) > buffer_max_size:
            signals.pop(0)
        
        # crop by timestamp
        for signal in signals:
            if current_time - signal.timestamp > buffer_time_limit:
                signals.remove(signal)


def send_buffer(signals_buffer: Mapping[str, List[Signal]]):
    # clean buffer
    crop_buffer(signals_buffer=signals_buffer)

    return {beacon_id: np.average([signal.power_received for signal in signals]) for beacon_id, signals in signals_buffer.items()}

def receive_buffer(signals: Mapping[str, float]):

    # crop to only the 3 strongest signals
    while len(signals) > 3:
        weakest_beacon_id = min(signals, key=signals.get)
        del signals[weakest_beacon_id]
    
    if len(signals) == 3:
        triangulate_position_with_3_points(signals=signals)
    elif len(signals) == 2:
        triangulate_position_with_2_points(signals=signals)
    elif len(signals) == 1:
        pass
    else:
        return


def callback(rssi, packet):
    
    watt = pow(10,rssi/10)/1000
    beacon_id = packet.namespace

    # add signal to buffer
    new_signal = Signal(beacon_id=beacon_id, power_received=watt, timestamp=time())
    signals_buffer[beacon_id].append(new_signal)


if __name__ == '__main__':
    # scan for all TLM frames of beacons in the namespace "12345678901234678901"
    scanner = BeaconScanner(
        callback,
        packet_filter=[EddystoneTLMFrame, EddystoneUIDFrame],
        scan_parameters={"address_type": BluetoothAddressType.PUBLIC,"interval_ms":2.5}
    )
    scanner.start()
