"""
Módulo para la carga y análisis exploratorio del dataset de la carrera Orbea Monegros 2024.
Incluye funcionalidades para cargar, validar y analizar los datos de la carrera.
"""

from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import TypeAlias, Optional, TypedDict, Final
import pandas as pd
from src.utils import display_table, TableConfig

# Type aliases
DataFrame: TypeAlias = pd.DataFrame
PathType: TypeAlias = str | PathLike[str] | Path

# Constantes tipadas
DEFAULT_DATA_PATH: Final[Path] = Path('data') / 'dataset.csv'
DEFAULT_ENCODING: Final[str] = 'utf-8'
DEFAULT_SEPARATOR: Final[str] = ';'

class DatasetAnalysis(TypedDict):
    """Tipo para los resultados del análisis del dataset."""
    total_participants: int
    columns: list[str]
    head_data: DataFrame

@dataclass
class DatasetInfo:
    """Clase para almacenar información del dataset."""
    df: DataFrame
    total_participants: int
    columns: list[str]

    @property
    def summary(self) -> DatasetAnalysis:
        """Genera un resumen del dataset en formato diccionario."""
        return {
            'total_participants': self.total_participants,
            'columns': self.columns,
            'head_data': self.df.head()
        }

def load_dataset(data_path: Optional[PathType] = None) -> DataFrame:
    """
    Carga el dataset de la carrera Orbea Monegros 2024.

    Args:
        data_path: Ruta opcional al archivo de datos. Si no se proporciona,
                  se usa la ruta por defecto.

    Returns:
        DataFrame con los datos de la carrera.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo de datos.
        pd.errors.EmptyDataError: Si el archivo está vacío.
        pd.errors.ParserError: Si hay problemas al parsear el CSV.
        ValueError: Para otros errores en la carga del dataset.
    """
    file_path = Path(data_path or DEFAULT_DATA_PATH)

    try:
        df = pd.read_csv(
            file_path,
            encoding=DEFAULT_ENCODING,
            sep=DEFAULT_SEPARATOR
        )

        if df.empty:
            raise pd.errors.EmptyDataError("El dataset está vacío")

        return df

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("El dataset está vacío") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error al parsear el CSV: {e}") from e
    except OSError as e:
        # Capturamos errores del sistema operativo (permisos, etc.)
        raise ValueError(f"Error de sistema al acceder al archivo: {e}") from e

def analyze_dataset(df: DataFrame) -> DatasetInfo:
    """
    Realiza un análisis exploratorio básico del dataset.

    Args:
        df: DataFrame con los datos de la carrera.

    Returns:
        DatasetInfo con la información básica del dataset.

    Raises:
        ValueError: Si el DataFrame es None o está vacío.
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    print("\n=== Análisis Exploratorio de Datos ===")

    # Mostrar primeros registros
    display_table(
        df,
        "Primeros 5 registros:",
        TableConfig(max_rows=5)
    )

    # Información sobre participantes
    total_participants = len(df)
    print(f"\nNúmero total de participantes: {total_participants:,}")

    # Información sobre columnas
    columns = list(df.columns)
    print("\nColumnas disponibles:")
    for col in columns:
        print(f"  - {col}")

    return DatasetInfo(
        df=df,
        total_participants=total_participants,
        columns=columns
    )

def main() -> DataFrame:
    """
    Función principal para ejecutar el análisis del dataset.

    Returns:
        DataFrame con los datos de la carrera.
    """
    df = load_dataset()
    analyze_dataset(df)

    # Información adicional sobre tipos de datos
    print("\nTipos de datos por columna:")
    for col, dtype in df.dtypes.items():
        print(f"  - {col}: {dtype}")

    return df
