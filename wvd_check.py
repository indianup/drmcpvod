import os
import glob

def wvd_check():
    wvd_files = glob.glob(f'{os.getcwd()}/WVDs/*.wvd')
    if not wvd_files:
        raise FileNotFoundError("No .wvd file found in the WVDs directory")
    return wvd_files[0]
