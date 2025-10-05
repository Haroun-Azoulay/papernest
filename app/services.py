# import pyproj - it's the package to use the function lamber93 if i change the API.
import pandas
import httpx
from fastapi import HTTPException
from array import array

# Memo
# 2G : 30km
# 3G : 5km
# 4G : 10km


GEO_URL = "https://data.geopf.fr/geocodage/search"


def parsing_coords_gouv(data) -> tuple:
    long = data["features"][0]["properties"]["x"]
    lat = data["features"][0]["properties"]["y"]
    return long, lat


def read_csv(
    x1,
    y1,
    csv_path="app/utils/mobil_coverage_france.csv",
    radii={"2G": 30000, "3G": 5000, "4G": 10000},
    operators=("Orange", "SFR", "Bouygues"),
) -> dict:
    dataFrame = pandas.read_csv(csv_path)

    deltaX = dataFrame["x"] - x1
    deltaY = dataFrame["y"] - y1
    distanceSquared = deltaX * deltaX + deltaY * deltaY

    coverageResult = {
        operator: {tech: False for tech in radii} for operator in operators
    }

    for operator in operators:
        operatorMask = dataFrame["Operateur"].str.contains(
            operator, case=False, na=False
        )
        for tech, radius in radii.items():
            antennaMask = (
                (dataFrame[tech].eq(1))
                & operatorMask
                & (distanceSquared <= radius * radius)
            )
            coverageResult[operator][tech] = bool(antennaMask.any())
    return coverageResult


async def fetch_geocode(address) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(GEO_URL, params={"q": address})
            if len(address) <= 2 or len(address) > 200:
                raise HTTPException(
                    status_code=400,
                    detail="Error : must contain between 3 and 200 chars and start with a number or a letter.",
                )
            try:
                payload = response.json()
            except ValueError:
                raise HTTPException(
                    status_code=502,
                    detail="API gouv returned an invalid JSON response.",
                )
            features = payload.get("features")
            if not features:
                raise HTTPException(status_code=404, detail="No data for this address.")

            return payload

    except httpx.ReadTimeout:
        raise HTTPException(
            status_code=504, detail="Api gouv not respond in time (timeout)."
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error network: {e}.")


def convert_ms(totalMs) -> array:
    h = totalMs // 3600000
    m = (totalMs % 3600000) // 60000
    s = (totalMs % 60000) // 1000
    ms = totalMs % 1000
    return [h, m, s, ms]


# If I don t start with the lambert coordinates and i only use the gps coordinates but I use the gov API so I get lambert back.
# def lamber93_to_gps(x, y):
#     lambert = pyproj.Proj("+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
#     wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
#     long, lat = pyproj.transform(lambert, wgs84, x, y)
#     return long, lat
