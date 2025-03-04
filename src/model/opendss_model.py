import pandas as pd
import os
from pathlib import Path
from ..utils.file_utils import ensure_directory
from ..config.settings import CIRCUIT_SETTINGS, OPENDSS_SETTINGS

class OpenDSSGISModel:
    def __init__(self, dss_path=None):
        self.dss_commands = []
        self.bus_coords = []
        self.dss_path = dss_path
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ensure_directory(dss_path)

    # Add this missing method
    def load_substations_from_csv(self, csv_path):
        """Load substations from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            df.columns = df.columns.str.strip()
            for idx, row in df.iterrows():
                self._create_substation(idx, row)
        except Exception as e:
            raise Exception(f"Error loading substations: {str(e)}")

    def _create_substation(self, idx, data):
        """Create substation transformer"""
        sub_name = f"SubXfmr_{idx+1}"
        hv_kv = data['HVVoltage'] / 1000  # V -> kV
        lv_kv = data['LVVoltage'] / 1000
        
        self.dss_commands.append(
            f"New Transformer.{sub_name} "
            f"Phases=3 Windings=2 "
            f"Xhl={data.get('XHL', 5.75)} "
            f"kVA={data.get('kVA', 1600)} "
            f"Conns=[Delta Wye] "
            f"Buses=[{data['HVBus']} {data['LVBus']}] "
            f"kVs=[{hv_kv} {lv_kv}]\n"  # Use converted kV values
        )
        self._add_bus_coordinates(data['HVBus'], data['Longitude'], data['Latitude'])
        self._add_bus_coordinates(data['LVBus'], data['Longitude'], data['Latitude'])

    # Rest of your existing methods
    def load_transformers_from_csv(self, csv_path):
        """Load distribution transformers from CSV"""
        try:
            df = pd.read_csv(csv_path)
            df.columns = df.columns.str.strip()
            # Clean string data
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            for idx, row in df.iterrows():
                self._create_transformer(idx, row)
        except Exception as e:
            raise Exception(f"Error loading transformers: {str(e)}")

    def _create_transformer(self, idx, data):
        """Create distribution transformer"""
        xfmr_name = f"XFMR{idx+1}"
        config = data['Configuration'].split('-')
        primary_conn = config[0].replace('Star', 'Wye')
        secondary_conn = config[1].replace('Star', 'Wye')
        
        # Convert voltages to kV for OpenDSS
        primary_kv = data['PrimaryVoltage'] / 1000  # V -> kV
        secondary_kv = data['SecondaryVoltage'] / 1000
        
        self.dss_commands.append(
            f"New Transformer.{xfmr_name} "
            f"Phases=3 Windings=2 "
            f"Xhl={data['XHL']} "
            f"kVA={data['kVA']} "
            f"Conns=[{primary_conn} {secondary_conn}] "
            f"Buses=[{data['PrimaryBus']} {data['SecondaryBus']}] "
            f"kVs=[{primary_kv} {secondary_kv}]\n"  # Use converted kV values
        )
        self._add_bus_coordinates(data['PrimaryBus'], data['Longitude'], data['Latitude'])
        self._add_bus_coordinates(data['SecondaryBus'], data['Longitude'], data['Latitude'])

    def _add_bus_coordinates(self, bus_name, lon, lat):
        """Add coordinates with proper bus name formatting"""
        # Clean bus name and ensure string type
        clean_name = str(bus_name).strip()
        self.bus_coords.append(f"BusCoords {clean_name} {lon} {lat}\n")

    def create_base_circuit(self, circuit_name):
        """Initialize base circuit"""
        settings = CIRCUIT_SETTINGS
        self.dss_commands.insert(0,  # Add at beginning of commands
            f"New Circuit.{circuit_name} "
            f"basekv={settings['base_kv']} "
            f"pu={settings['pu']} "
            f"MVAsc3={settings['mvasc3']} "
            f"MVAsc1={settings['mvasc1']}\n"
        )

    def save_dss_files(self):
        """Save generated DSS files"""
        with open(os.path.join(self.dss_path, "Network.dss"), 'w') as f:
            f.writelines(self.dss_commands)
        
        with open(os.path.join(self.dss_path, "BusCoords.dss"), 'w') as f:
            f.writelines(self.bus_coords)

    def create_master_file(self):
        """Create master control file"""
        master_content = f"""Clear
Redirect Network.dss
Redirect BusCoords.dss
Solve
"""
        with open(os.path.join(self.dss_path, "Master.dss"), 'w') as f:
            f.write(master_content)