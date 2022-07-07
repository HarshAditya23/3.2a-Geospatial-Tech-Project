import json
import pandas as pd

# Get the Location History from Google Takeout
with open("Records.json", "r") as location_history:
    location_data = json.loads(location_history.read())

df = pd.DataFrame(location_data["locations"])

# Remove unused columns
df.drop(
    columns=[
        "accuracy",
        "activity",
        "altitude",
        "verticalAccuracy",
        "velocity",
        "heading",
    ],
    inplace=True,
)

# Format latitude, longitude, timestamp to the standard formats
df["latitude"] = df["latitudeE7"] / 10000000
df["longitude"] = df["longitudeE7"] / 10000000
timetag   = pd.to_datetime(df['timestamp'])
timeit    = timetag.astype('int64')//(10**6) 
df["ts"] = pd.to_datetime(timeit,unit='ms')

df[["latitude", "longitude", "ts"]].to_csv("clean_data.csv", index=False)

print("Cleaning completed")
