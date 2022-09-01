#%%
import os
import pandas as pd 
import geopandas as gpd 
import numpy as np
import requests

def load_crop(base_path : str) -> gpd.GeoDataFrame:
    '''
    reads in crop.csv, assuming it is stored at $(base_path)/crops.csv
    Parameters
    --------------------------------
    input: base_path for a directory
    Outputs
    --------------------------------
    output: pd.Dataframe of crop
    '''

    crop = pd.read_csv(os.path.join(base_path, 'crop.csv'))
    crop['geometry'] = gpd.GeoSeries.from_wkt(crop['field_geometry'])
    crop = gpd.GeoDataFrame(crop)

    return crop 

def load_weather(base_path : str) -> pd.DataFrame:
    '''
    reads in weather.csv, assuming it is stored at $(base_path)/spectral.csv,
    Parameters
    --------------------------------
    input: base_path for a directory
    Outputs
    --------------------------------
    output: pd.Dataframe of weather, gpd.Dataframe of fields
    '''

    weather = pd.read_csv(os.path.join(base_path, 'weather.csv'), dtype= {'fips_code' : object})
    fields = load_crop(base_path)
    
    return weather, fields 

def lookup_fips(lat, lon):
    '''
    looks up lat lon --> fips code
    Parameters
    --------------
    lat
    lon
    Outputs
    ------------
    fips
    
    '''
    url = 'https://geo.fcc.gov/api/census/block/find?latitude=%s&longitude=%s&format=json' % (lat, lon)
    response = requests.get(url)
    data = response.json()
    state = data['State']['FIPS']
    county = data['County']['FIPS'][2:]
    return str(state) + str(county)




#%%
def transform_weather(weather : pd.DataFrame, fields : gpd.GeoDataFrame) -> pd.DataFrame:
    '''
    takes in weather and fields, geocodes fields

    Parameters
    ----------
    Weather
    Fields
    --------
    Output 
    Fields with weather data
    '''
    fields = fields[['field_id', 'geometry']].drop_duplicates()
    weather = weather[weather['year']==2021]
    weather = (weather
        .groupby('fips_code', as_index=False)
        .agg(precip = ('precip', 'sum'),
         max_temp = ('temp', 'max'),
         mean_temp = ('temp', 'mean'))
    )
    fields["lon"] = fields.centroid.x
    fields["lat"] = fields.centroid.y
    fields['fips_code'] = fields.apply(lambda x: lookup_fips(x.lat, x.lon), axis =1)

    joined_fields = fields[['field_id', 'fips_code']].merge(weather, left_on = 'fips_code', right_on = 'fips_code')
    return joined_fields



def write_weather(weather : pd.DataFrame, output_path : str) -> None:
    '''
    writes processed soil to $(output_path)/spectral.csv
    '''
    weather.to_csv(os.path.join(output_path, 'weather.csv'))

# %%

def process_weather(base_path : str, output_path : str) -> None:
    weather, fields = load_weather(base_path)
    weather = transform_weather(weather, fields)
    write_weather(weather, output_path)
