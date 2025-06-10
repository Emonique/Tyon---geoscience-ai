import pandas as pd
import numpy as np

def load_well_data(filepath, units='metric'):
    """
    Load well data from CSV with flexible column mapping
    Expected columns (case-insensitive):
    - depth
    - porosity
    - permeability
    - lithology (optional)
    - temperature (optional)
    """
    df = pd.read_csv(filepath)
    
    # Normalize column names
    col_map = {}
    for col in df.columns:
        lower_col = col.strip().lower()
        if 'depth' in lower_col:
            col_map[col] = 'depth'
        elif 'poro' in lower_col:
            col_map[col] = 'porosity'
        elif 'perm' in lower_col:
            col_map[col] = 'permeability'
        elif 'lith' in lower_col or 'rock' in lower_col:
            col_map[col] = 'lithology'
        elif 'temp' in lower_col:
            col_map[col] = 'temperature'
    
    df = df.rename(columns=col_map)
    
    # Handle missing lithology
    if 'lithology' not in df.columns:
        df['lithology'] = 'sandstone'
    
    # Convert units if needed
    if units == 'imperial':
        if 'depth' in df.columns:
            df['depth'] *= 0.3048  # Convert feet to meters
        if 'permeability' in df.columns:
            df['permeability'] *= 0.986923  # Convert mD to m² (approx)
    
    return df.to_dict('records')

def load_from_las(filepath):
    """Placeholder for LAS file loader"""
    # This would use lasio library in a real implementation
    return load_well_data('converted.csv')  # Temporary fallback
def load_well_data(filepath, units='metric'):
    # ... existing code ...
    
    # Validate required columns
    required = ['depth', 'porosity', 'permeability']
    if application == 'geothermal':
        required = ['depth', 'temperature']
    
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
    return df.to_dict('records')
