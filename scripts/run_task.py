#%%
import pandas as pd 
import geopandas as gpd 
import numpy as np
import requests
import os 
import fire 
from pattern_steps.crops import process_crop
from pattern_steps.soil import process_soil
from pattern_steps.spectral import process_spectral
from pattern_steps.weather import process_weather
from pattern_steps.crops import CROP_YEAR
#%%
def process_pattern(input_dir, output_dir, year=CROP_YEAR):
    process_crop(base_path=input_dir, output_path=output_dir, YEAR=CROP_YEAR)
    process_soil(base_path=input_dir, output_path=output_dir)
    process_spectral(base_path=input_dir, output_path=output_dir, YEAR=CROP_YEAR)
    process_weather(base_path=input_dir, output_path=output_dir)

#%%
if __name__ == '__main__':
    fire.Fire(process_pattern)
# %%
