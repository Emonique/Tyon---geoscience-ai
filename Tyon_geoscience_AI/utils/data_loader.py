 import pandas as pd
import numpy as np

def detect_application(df):
    """Infer application type based on column presence."""
    cols = df.columns.str.lower()
    if cols.str.contains('temperature').any():
        return 'geothermal'
    if cols.str.contains('contaminant|risk').any():
        return 'contamination'
    if cols.str.contains('hydraulic|aquifer').any():
        return 'groundwater'
    if cols.str.contains('porosity').any() and cols.str.contains('permeability').any():
        return 'hydrocarbon'
    return 'unknown'

def load_well_data(filepath, application=None, units='metric'):
    """
    Load well data from CSV with flexible column mapping and auto-detect application type if needed.
    Returns a list of dictionaries.
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
        elif 'hydraulic' in lower_col and 'conductivity' in lower_col:
            col_map[col] = 'hydraulic_conductivity'
        elif 'contaminant' in lower_col or 'risk' in lower_col:
            col_map[col] = 'contaminant_risk'

    df.rename(columns=col_map, inplace=True)

    # Fill in default lithology if missing
    if 'lithology' not in df.columns:
        df['lithology'] = 'sandstone'

    # Convert units
    if units == 'imperial':
        if 'depth' in df.columns:
            df['depth'] = df['depth'] * 0.3048  # ft to m
        if 'permeability' in df.columns:
            df['permeability'] = df['permeability'] * 0.986923e-15  # mD to m²
        if 'temperature' in df.columns:
            df['temperature'] = (df['temperature'] - 32) * 5 / 9  # °F to °C

    # Auto-detect application if needed
    if application is None or application == 'auto':
        application = detect_application(df)
        print(f"Detected application: {application}")

    # Define required columns
    required_columns = {
        'geothermal': ['depth', 'temperature'],
        'contamination': ['depth', 'porosity', 'permeability'],
        'groundwater': ['depth', 'porosity', 'permeability'],
        'hydrocarbon': ['depth', 'porosity', 'permeability']
    }

    if application not in required_columns:
        raise ValueError(f"Could not detect a valid application type. Columns: {list(df.columns)}")

    missing = [col for col in required_columns[application] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for {application} analysis: {', '.join(missing)}")

    return df.to_dict('records')
