#%%
import os
import pandas as pd 
import geopandas as gpd 
CROP_YEAR=2021

# %%
def load_spectral(base_path : str) -> pd.DataFrame:
    '''
    reads in spectral.csv, assuming it is stored at $(base_path)/spectral.csv,
    processes the date too 
    Parameters
    --------------------------------
    input: base_path for a directory
    Outputs
    --------------------------------
    output: pd.Dataframe of spectral
    '''

    spectral = pd.read_csv(os.path.join(base_path, 'spectral.csv'))
    spectral['date'] = pd.to_datetime(spectral['date'])
    return spectral 

def ndvi(nir : float , red : float) -> float:
    '''
    calculates ndvi as (nir - red) / (nir + red)
    Parameters
    ------------
    nir: float
    red: float
    Outputs
    ---------
    ndvi: float
    '''
    return (nir - red) / (nir + red)



def transform_spectral(spectral : pd.DataFrame, CROP_YEAR : int) -> pd.DataFrame:
    '''
    Subsets spectral to a CROP_YEAR,
    calculates ndvi,
    finds peak of season value for each tile
    and the date that occured
    And writes it back out without the year column

    Parameters
    -----------
    crop: pd.Dataframe
    Outputs
    ------------
    Processed dataframe of crop 

    '''
    # subset to year, this will makae calculating ndvi faster
    spectral = spectral[spectral['date'].dt.year==CROP_YEAR]
    # calculate ndvi
    spectral['ndvi'] = spectral.apply(lambda x: ndvi(x.nir, x.red), axis =1)
    # find max ndvi by tile
    spectral = (
        spectral.loc[spectral.groupby('tile_id')['ndvi']
        .idxmax(),
        ['tile_id', 'tile_geometry', 'ndvi', 'date']]
    )
    # rename columns to match output
    spectral = spectral.rename(columns={"ndvi": "pos", "date": "pos_date"})


    return spectral

def write_spectral(spectral : pd.DataFrame, output_path : str) -> None:
    '''
    writes processed crop to $(output_path)/spectral.csv
    '''
    spectral.to_csv(os.path.join(output_path, 'spectral.csv'))


# %%

def process_spectral(base_path : str, output_path : str, YEAR : int) -> None:
    spectral = load_spectral(base_path)
    spectral = transform_spectral(spectral, CROP_YEAR)
    write_spectral(spectral, output_path)

