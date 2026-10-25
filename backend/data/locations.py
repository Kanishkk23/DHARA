from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MonitoredLocation:
    id: str
    name: str
    district: str
    state: str
    latitude: float
    longitude: float
    river_name: Optional[str]
    river_station: Optional[str]


MONITORED_LOCATIONS: tuple[MonitoredLocation, ...] = (
    MonitoredLocation(
        id="kullu",
        name="Kullu & Manali Valley",
        district="Kullu",
        state="Himachal Pradesh",
        latitude=31.9579,
        longitude=77.1095,
        river_name="Beas River",
        river_station="Kullu Hydro Gauge",
    ),
    MonitoredLocation(
        id="kedarnath",
        name="Kedarnath & Mandakini Valley",
        district="Rudraprayag",
        state="Uttarakhand",
        latitude=30.7346,
        longitude=79.0669,
        river_name="Mandakini River",
        river_station="Rudraprayag Confluence",
    ),
    MonitoredLocation(
        id="chamoli",
        name="Chamoli & Joshimath",
        district="Chamoli",
        state="Uttarakhand",
        latitude=30.5562,
        longitude=79.5667,
        river_name="Alaknanda River",
        river_station="Joshimath Station",
    ),
    MonitoredLocation(
        id="wayanad",
        name="Wayanad Hill Tracts",
        district="Wayanad",
        state="Kerala",
        latitude=11.6854,
        longitude=76.1320,
        river_name="Kabini / Chaliyar",
        river_station="Meppadi Station",
    ),
    MonitoredLocation(
        id="kinnaur",
        name="Shimla & Kinnaur",
        district="Kinnaur",
        state="Himachal Pradesh",
        latitude=31.6510,
        longitude=78.4752,
        river_name="Satluj River",
        river_station="Reckong Peo Gauge",
    ),
    MonitoredLocation(
        id="munnar",
        name="Munnar & Idukki Hills",
        district="Idukki",
        state="Kerala",
        latitude=10.0889,
        longitude=77.0595,
        river_name="Muthirapuzha / Periyar",
        river_station="Munnar Basin Site",
    ),
    MonitoredLocation(
        id="chiplun",
        name="Chiplun & Mahabaleshwar Ghats",
        district="Ratnagiri",
        state="Maharashtra",
        latitude=17.5323,
        longitude=73.5186,
        river_name="Vashishti River",
        river_station="Chiplun Town Bridge",
    ),
    MonitoredLocation(
        id="teesta",
        name="Teesta Valley & Lachen",
        district="Mangan",
        state="Sikkim",
        latitude=27.7167,
        longitude=88.5500,
        river_name="Teesta River",
        river_station="Chungthang Dam Gauge",
    ),
    MonitoredLocation(
        id="dharamsala",
        name="Dharamsala & Kangra",
        district="Kangra",
        state="Himachal Pradesh",
        latitude=32.2190,
        longitude=76.3234,
        river_name="Manjhi Khad / Beas",
        river_station="Kangra Valley Site",
    ),
    MonitoredLocation(
        id="dimahasao",
        name="Dima Hasao Hills",
        district="Dima Hasao",
        state="Assam",
        latitude=25.1833,
        longitude=93.0167,
        river_name="Jatinga / Kopili",
        river_station="Haflong Station",
    ),
    MonitoredLocation(
        id="guwahati",
        name="Guwahati",
        district="Kamrup Metropolitan",
        state="Assam",
        latitude=26.1445,
        longitude=91.7362,
        river_name="Brahmaputra",
        river_station="Guwahati DC Court",
    ),
    MonitoredLocation(
        id="cuttack",
        name="Cuttack (Naraj)",
        district="Cuttack",
        state="Odisha",
        latitude=20.4625,
        longitude=85.8828,
        river_name="Mahanadi",
        river_station="Naraj Barrage",
    ),
)


def get_all_locations() -> list[MonitoredLocation]:
    return list(MONITORED_LOCATIONS)


def get_location_by_id(
    location_id: str,
) -> Optional[MonitoredLocation]:
    normalized_id = location_id.strip().lower()

    for location in MONITORED_LOCATIONS:
        if location.id == normalized_id:
            return location

    return None