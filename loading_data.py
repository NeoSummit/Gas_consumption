import pandas as pd
import numpy as np

def load_gas_consumption_data(
    file_ncg: str = r"data/AggregatedConsumptionData NetConnect.csv",
    file_gaspool: str = r"data/Aggregated Consumption Date Market Area GASPOOL.csv",
    file_the: str = r"data/AggregatedConsumptionData Trading Hub.csv",
) -> pd.DataFrame:
    """Loads historical natural gas consumption in MWh and returns it as a pandas DataFrame."""

    for file in [file_ncg, file_gaspool, file_the]:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")

    # Read NetConnect Germany CSV file
    ncg_data = pd.read_csv(file_ncg, sep=";", index_col="DayOfUse")
    ncg_data.index = pd.to_datetime(ncg_data.index, format="%d.%m.%Y")
    ncg_data = ncg_data.select_dtypes("number").fillna(0) / 1000  # Convert kWh to MWh
    ncg_aggregated = ncg_data.sum(axis="columns").sort_index()

    # Read GASPOOL CSV file
    gaspool_data = pd.read_csv(file_gaspool, sep=";", index_col="Datum")
    gaspool_data.index = pd.to_datetime(gaspool_data.index, format="%d.%m.%Y")
    gaspool_aggregated = gaspool_data.sum(axis="columns").sort_index()

    # Read Trading Hub Europe CSV file
    the_data = pd.read_csv(file_the, sep=";", thousands=",", index_col="Gasday")
    the_data.index = pd.to_datetime(the_data.index, format="%d/%m/%Y")
    the_data = the_data.select_dtypes("number").fillna(0) / 1000
    the_aggregated = the_data.sum(axis="columns").sort_index()

    # Combine all data
    total_consumption = pd.concat(
        [
            ncg_aggregated.add(gaspool_aggregated, fill_value=0),
            the_aggregated,
        ]
    )
    total_consumption = pd.DataFrame(total_consumption, columns=["consumption (MWh)"])
    return total_consumption




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
    
    return data.sort_index()
