import pandas as pd
import numpy as np


def nat_gas_consumption_data(
    file_netconnect = "~/Desktop/TP Modéco/data/nc_consumption.csv",
    file_gaspool = "~/Desktop/TP Modéco/data/gaspool_consumption.csv",
    file_the = "~/Desktop/TP Modéco/data/the_consumption.csv",
):
    ## Important to understand :
    """
    On the 1st October 2021,
    the two gasmarket areas NCG and Gaspool in Germany will be merged
    and the Trading Hub Europe (THE) will be created.
    This will further improve the competitive conditions in Germany.
    Find all fundamental Information on the new Market Area here in our 10 Q&As.


    """
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

    consumption_data = pd.concat([ncg_consumption_aggregated.sort_index().add(gaspool_consumption_aggregated.sort_index(), fill_value=0), 
                                the_consumption_aggregated.sort_index()])


    return ncg_consumption_aggregated.sort_index(),gaspool_consumption_aggregated.sort_index(),the_consumption_aggregated.sort_index(),consumption_data



#https://open-meteo.com/en/docs/historical-weather-api#start_date=2000-01-01&hourly=&daily=temperature_2m_max,temperature_2m_min,sunshine_duration,wind_speed_10m_max&timezone=Europe%2FBerlin&temporal_resolution=native

def nat_gas_weather_data(
    file_netconnect = "~/Desktop/TP Modéco/data/open-meteo-52.55N13.41E38m.csv"
):

    data=pd.read_csv(file_netconnect, sep=",",skiprows=2, header=0)
    data["sunshine_duration (s)"]=data["sunshine_duration (s)"]/3600
    data = data.rename(columns={"sunshine_duration (s)": "sunshine_duration (h)"})
    data = data.rename(columns={"time": "Date"})
    data["Date"] = pd.to_datetime(data["Date"]).dt.strftime("%Y/%m/%d")
    data.set_index("Date", inplace=True)

    return data

