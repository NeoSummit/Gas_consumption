import pandas as pd
import numpy as np

def read_consumption(
    file_netconnect: str = "data\AggregatedConsumptionData NetConnect.csv",
    file_gaspool: str = "data\Aggregated Consumption Date Market Area GASPOOL.csv",
    file_the: str = "data\AggregatedConsumptionData Trading Hub.csv",
) -> tuple([pd.Series, pd.Series, pd.Series]):
    """Reads historic natural gas consumption in MWh and returns them as a tuple of pandas series."""

    # Read NetConnect Germany CSV file
    ncg_consumption = pd.read_csv(file_netconnect, sep=";", index_col="DayOfUse")

    ncg_consumption.index = pd.to_datetime(ncg_consumption.index, format="%d.%m.%Y")

    # Convert kWh to MWh and aggregate different measurement types
    ncg_consumption = ncg_consumption.select_dtypes("number") / 1000
    ncg_consumption_aggregated = ncg_consumption.sum(axis="columns")

    # Read GASPOOL CSV file
    gaspool_consumption = pd.read_csv(file_gaspool, sep=";", index_col="Datum")

    gaspool_consumption.index = pd.to_datetime(
        gaspool_consumption.index, format="%d.%m.%Y"
    )
    gaspool_consumption_aggregated = gaspool_consumption.sum(axis="columns")

    # Read Trading Hub Europe CSV file
    the_consumption = pd.read_csv(file_the, sep=";", thousands=",", index_col="Gasday")

    the_consumption.index = pd.to_datetime(the_consumption.index, format="%d/%m/%Y")

    # Convert kWh to MWh and aggregate different measurement types
    the_consumption = the_consumption.select_dtypes("number") / 1000
    the_consumption_aggregated = the_consumption.sum(axis="columns")

    return tuple(
        [
            ncg_consumption_aggregated.sort_index(),
            gaspool_consumption_aggregated.sort_index(),
            the_consumption_aggregated.sort_index(),
        ]
    )


def read_weather(file: str = "data/open-meteo-52.55N13.41E38m.csv") -> pd.Series:
    """Reads ERA5 temperature data from a CSV file and returns a pandas Series with temperature in Celsius."""
    
    # Load the data
    data = pd.read_csv(file, sep=",", skiprows=2, header=0)

    # Convert sunshine duration from seconds to hours
    data["sunshine_duration (s)"] = data["sunshine_duration (s)"] / 3600
    data = data.rename(columns={"sunshine_duration (s)": "sunshine_duration (h)"})
    
    # Rename and format the date column
    data = data.rename(columns={"time": "Date"})
    data["Date"] = pd.to_datetime(data["Date"])
    
    # Set the date column as the index
    data.set_index("Date", inplace=True)
    
    return data