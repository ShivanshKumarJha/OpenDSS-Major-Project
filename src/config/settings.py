import os

# Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# OpenDSS Configuration
OPENDSS_SETTINGS = {
    'base_frequency': 50,  # Assuming 50 Hz system
    'base_voltage': 11000,  # Base HV voltage
    'default_line_length': 0.1,  # Default line length in km
}

# Circuit Settings for OpenDSS Model
CIRCUIT_SETTINGS = {
    'base_kv': 11,  # Base kilovoltage
    'pu': 1.0,      # Per-unit voltage 
    'mvasc3': 100,  # 3-phase short circuit MVA
    'mvasc1': 80,   # 1-phase short circuit MVA
}

# Coordinate Settings
COORDINATE_SETTINGS = {
    'projection': 'WGS84',
    'reference_point': {
        'latitude': 29.945176,
        'longitude': 76.817828
    }
}