#%%
import pandas as pd 
import geopandas as gpd 
import os
CROP_YEAR = 2021
#%%
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


def transform_crop(crop : pd.DataFrame, CROP_YEAR : int) -> pd.DataFrame:
    '''
    Subsets crop to a CROP_YEAR
    And writes it back out without the year column

    Parameters
    -----------
    crop: pd.Dataframe
    Outputs
    ------------
    Processed dataframe of crop 

    '''
    # subset to crop year
    crop = crop[crop['year']==CROP_YEAR]
    # remove year column
    crop = crop[['field_id', 'field_geometry', 'crop_type']]
    # write to csv

    return crop

def write_crop(crop : pd.DataFrame, output_path : str) -> None:
    '''
    writes processed crop to $(output_path)/crop.csv
    '''
    crop.to_csv(os.path.join(output_path, 'crop.csv'))

 #%%   
def process_crop(base_path : str, output_path : str, YEAR : int):
    crop = load_crop(base_path)
    crop = transform_crop(crop, CROP_YEAR)
    write_crop(crop, output_path)




# %%
