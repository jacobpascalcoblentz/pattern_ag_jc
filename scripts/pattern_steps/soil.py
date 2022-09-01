#%%
import os
import pandas as pd 
import geopandas as gpd 
import numpy as np
# %%
def load_soil(base_path : str) -> gpd.GeoDataFrame:
    '''
    reads in soil.csv, assuming it is stored at $(base_path)/spectral.csv,
    processes the date too 
    Parameters
    --------------------------------
    input: base_path for a directory
    Outputs
    --------------------------------
    output: pd.Dataframe of spectral
    '''

    soil = pd.read_csv(os.path.join(base_path, 'soil.csv'))
    soil['geometry'] = gpd.GeoSeries.from_wkt(soil['mukey_geometry'])
    soil = gpd.GeoDataFrame(soil)
    return soil 

def layer_weights(hzdept : float , hzdepb : float) -> float:
    '''
    calculates ndvi as (nir - red) / (nir + red)
    Parameters
    ------------
    hzdept: float
    hzdepb: float
    Outputs
    ---------
    layer_weights: float
    '''
    return abs(hzdept - hzdepb) / hzdepb


def double_weighted_average(df : pd.DataFrame, col: str):
    '''
    does the double weighted average on the soil datframe
    Parameters
    ----------
    df: a dataframe of soil
    col: string referencing which column to agg
    '''
    # calculate weighted average by cokey
    average1 = (
        df.groupby(['mukey', 'cokey', 'comppct'], as_index= False )
        .apply(lambda x: np.average(x[col],
         weights=x.layer_weights))
         .rename(columns = {None : col})
        )
    # then calculate the weighted average by mukey
    average2 = (
        average1.groupby(['mukey'], as_index= False )
        .apply(lambda x: np.average(x[col], 
        weights=x.comppct))
        .rename(columns = {None : col})
        .set_index('mukey')
        )
    return average2


def transform_soil(soil : pd.DataFrame) -> pd.DataFrame:
    '''
    Calculates weighted average of horizontal layers for each component 
    Then uses that to calculate weighted average of components for each map
            unit 
    Parameters
    -----------
    crop: pd.Dataframe
    Outputs
    ------------
    Processed dataframe of crop 

    '''
    # calculate layer weights
    soil['layer_weights'] = soil.apply(lambda x: layer_weights(x.hzdept, x.hzdepb), axis =1)
    # find double weighted average for om, cec, ph
    cec = double_weighted_average(soil, 'cec')
    ph = double_weighted_average(soil, 'ph')
    om =  double_weighted_average(soil, 'om')
    # join aggregated values here 
    soil_output = (
        pd.DataFrame(soil.set_index(['mukey'])['mukey_geometry'])
        .drop_duplicates()
        .join(om)
        .join(cec)
        .join(ph)
    )

    return soil_output

def write_soil(soil : pd.DataFrame, output_path : str) -> None:
    '''
    writes processed soil to $(output_path)/spectral.csv
    '''
    soil.to_csv(os.path.join(output_path, 'soil.csv'))


# %%

def process_soil(base_path : str, output_path : str) -> None:
    soil = load_soil(base_path)
    soil = transform_soil(soil)
    write_soil(soil, output_path)
