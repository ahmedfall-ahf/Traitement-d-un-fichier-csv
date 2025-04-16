import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

def read_csv_with_any_encoding(filepath):
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    for enc in encodings:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except Exception:
            continue
    raise ValueError("Impossible de lire le fichier avec les encodages standards.")

def process_csv(filepath, filename):
    df = read_csv_with_any_encoding(filepath)

    # 1. Traitement des valeurs manquantes
    df = df.fillna(df.mean(numeric_only=True))

    # 2. Traitement des valeurs aberrantes
    for col in df.select_dtypes(include='number'):
        if df[col].std() != 0:
            z = (df[col] - df[col].mean()) / df[col].std()
            df = df[(z < 3) & (z > -3)]

    # 3. Suppression des doublons
    df = df.drop_duplicates()

    # Vérifie que le DataFrame contient encore des lignes
    if df.shape[0] == 0:
        raise ValueError("Le fichier ne contient plus aucune ligne après nettoyage.")

    # 4. Normalisation
    num_cols = df.select_dtypes(include='number').columns
    if not df[num_cols].empty:
        scaler = MinMaxScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

    # 5. Sauvegarde
    output_path = os.path.join('processed', f'{filename}')
    df.to_csv(output_path, index=False)
    return output_path
