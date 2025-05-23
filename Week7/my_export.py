from datetime import datetime
import httpx
import matplotlib.pyplot as plt
import numpy

from prefect import flow, task
from tiled.client import from_profile, from_uri
from tiled.server import SimpleTiledServer


BEAMLINE_ACRONYM = "tst"
# IS_SUBFLOW should be False when running my_export.py
# Change IS_SUBFLOW to True when running full_workflow.py
IS_SUBFLOW=False
tiled_client = from_profile("nsls2")[BEAMLINE_ACRONYM]["raw"]

if IS_SUBFLOW:
    print(f"Don't create a SimpleTiledServer")
else:
    # Start up a simple tiled server to write data to
    # This will create a directory called tiled_data and
    #     store the data there
    simple_local_server = SimpleTiledServer(directory="tiled_data/")
    local_server_client = from_uri(simple_local_server.uri)


@task
def get_weather(
        latitude,
        longitude,
        date,
        weather_past_or_present,
    ):
    """Get hourly temps and sunrise/set for a location."""
    if weather_past_or_present == "past":
        # This url gives archived weather data
        base_url = "https://archive-api.open-meteo.com/v1/archive"
    elif weather_past_or_present == "present":
        # This url gives future or present weather data
        base_url = "https://api.open-meteo.com/v1/forecast/"
    print(f"Getting weather for date {date}")
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "daily": ["sunrise", "sunset"],  # get sunrise and set
        "hourly": "temperature_2m",  # get hourly temperatures
        "timezone": "America/New_York",
        "temperature_unit": "fahrenheit",
    }
    return httpx.get(base_url, params=params)


@task
def format_weather(data):
    """Format weather data."""
    if data.status_code != 200:
        print(f"Bad weather data, status code {data.status_code}")
        return
    data = data.json()
    hourly_times = data["hourly"]["time"]
    hourly_times = [hour.split("T")[-1] for hour in hourly_times]
    hourly_times = numpy.array(hourly_times)
    hourly_temp = data["hourly"]["temperature_2m"]
    # Convert hourly temps to an array
    hourly_temp = numpy.array(hourly_temp)
    # Get some info about the hourly temps
    min_temp = hourly_temp.min()
    max_temp = hourly_temp.max()
    mean_temp = hourly_temp.mean()

    # Format the sunrise and set
    sunrise = data["daily"]["sunrise"][0]
    sunrise = str(datetime.fromisoformat(sunrise))
    sunset = data["daily"]["sunset"][0]
    sunset = str(datetime.fromisoformat(sunset))

    # Return all this formatted weather
    formatted_weather = {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "timezone": data["timezone"].replace("_", " "),
        "hourly_times": hourly_times,
        "hourly_temps": hourly_temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "mean_temp": mean_temp,
        "temp_units": data["hourly_units"]["temperature_2m"],
        "sunrise": sunrise,
        "sunset": sunset,
    }
    return formatted_weather


def save_temp_plot(data, date):
    """Create a temperature plot."""
    # Do not make this a task, matplotlib does not like being used
    # outside the main thread
    plt.figure()
    plt.xlabel("Time")
    plt.ylabel(f"Temp in {data['temp_units']}")
    plt.title(f"Temperature in {data['temp_units']} for {date}")
    plt.plot(data["hourly_times"], data["hourly_temps"])
    plt.savefig("temperature_plot.png")
    plt.close()


@task
def get_tiled_data(ref):
    """Get some data from Tiled."""
    run = tiled_client[ref]
    start_doc = run.start
    scan_id = start_doc.get("scan_id")
    scan_uid = start_doc.get("uid")
    plan_name = start_doc.get("plan_name")
    return scan_id, scan_uid, plan_name


@task
def write_data_to_tiled(data, md):
    """Write the hourly temperatures to Tiled."""
    try:
        processed_array_client = local_server_client.write_array(data, metadata=md)
    except NameError:
        print("SimpleTiledServer is not defined. This is probably a subflow")
        return
    # return the uid of the new entry in Tiled so we can access it later if needed
    return processed_array_client.item["id"]


@flow(log_prints=True)
def export(ref, lat=40.86, lon=-72.87, date="2025-05-20"):
    try:
        date = str(datetime.strptime(date, "%Y-%m-%d")).split(" ")[0]
    except ValueError:
        print(f"Date {date} can not be converted into yyyy-mm-dd format")
        date = "2014-10-23"  # date of first light
        print(f"Using date {date}")
    if (datetime.today() - datetime.strptime(date, "%Y-%m-%d")).days < 5:
        weather_past_or_present = "present"
    else:
        weather_past_or_present = "past"
    weather = get_weather(
        latitude=lat,
        longitude=lon,
        date=date,
        weather_past_or_present=weather_past_or_present
    )
    formatted_weather = format_weather(weather)
    if formatted_weather is None:
        print("Weather could not be formatted. Not exporting.")
        return
    # Save temperature plot as a png
    save_temp_plot(formatted_weather, date)
    # Export data to a text file
    scan_id, scan_uid, plan_name = get_tiled_data(ref)
    print(f"Exporting uid: {scan_uid}")
    print(f"Scan {scan_id}")
    if plan_name in ["scan", "count"]:
        print(f"{plan_name = }")
    else:
        print(f"Plan name {plan_name} is not a supported plan for export. Not exporting.")
        return
    filename = f"scan_{scan_id}_{plan_name}.txt"
    with open(filename, "w") as file:
        file.write(f"UID: {scan_uid}\nScan id: {scan_id}\nPlan name: {plan_name}")
        file.write("\n\nAnd now for the weather...\n")
        temp_units = formatted_weather.pop("temp_units")
        for key, value in formatted_weather.items():
            if key in ["min_temp", "max_temp", "mean_temp"]:
                value = f"{value:.1f} {temp_units}"
            file.write(f"\n{key.capitalize().replace('_', ' ')}: {value}")

    # Add the raw_uid of the scan we are exporting so we can find it later
    md = {"raw_uid": scan_uid}

    # TODO: add some more metadata to the temperature data we will write to tiled
    ...

    # Now write the hourly temps to tiled
    processed_uid = write_data_to_tiled(
        data=formatted_weather["hourly_temps"],
        md=md
    )
    print(f"{processed_uid = }")
    if processed_uid is not None:
        print(f"{local_server_client[processed_uid]}")
