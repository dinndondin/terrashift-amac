"""Componente amac.nasa.config; lógica extraída de nasa_api.py."""




BASE_URL = "https://power.larc.nasa.gov/api/temporal"


DEFAULT_PARAMS = [
    "T2M", "T2M_MAX", "T2M_MIN",
    "PRECTOTCORR",
    "RH2M",
    "GWETROOT",
    "ALLSKY_SFC_SW_DWN",
    "WS2M",
    "T2MDEW",
]


_FILL_VALUE = -999.0
