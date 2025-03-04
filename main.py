import os
import win32com.client
from src.model.opendss_model import OpenDSSGISModel

def main():
    try:
        # Path configuration
        base_dir = os.path.join(os.path.dirname(__file__), 'data')
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)  # Create directory if needed
        
        # Initialize model
        model = OpenDSSGISModel(dss_path=output_dir)
        
        # Build network
        model.create_base_circuit("SubstationNetwork")
        model.load_transformers_from_csv(os.path.join(base_dir, 'transformers.csv'))
        model.load_substations_from_csv(os.path.join(base_dir, 'substations.csv'))
        
        # Generate DSS files
        model.save_dss_files()
        model.create_master_file()
        
        # Return output_dir for later use
        return output_dir

    except Exception as e:
        print(f"Error: {e}")
        return None

def run_in_opendss(output_dir):
    """Execute the model using OpenDSS COM interface"""
    if not output_dir:
        print("No output directory provided!")
        return
    
    try:
        dss = win32com.client.Dispatch("OpenDSSEngine.DSS")
        dss.Start(0)
        dss_text = dss.Text
        master_path = os.path.join(output_dir, 'Master.dss')
        
        print(f"Compiling {master_path}...")
        dss_text.Command = f"Compile '{master_path}'"
        
        print("Solving circuit...")
        dss_text.Command = "Solve"
        
        print("Simulation completed successfully!")
        print("\nVoltage Results:")
        dss_text.Command = "Show Voltages"
        
    except Exception as e:
        print(f"OpenDSS execution error: {e}")

if __name__ == "__main__":
    generated_output_dir = main()
    if generated_output_dir:
        run_in_opendss(generated_output_dir)