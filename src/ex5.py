"""
Módulo para el análisis específico de los ciclistas de la UCSC (Unió Ciclista Sant Cugat).
"""

from dataclasses import dataclass
from typing import TypeAlias, Optional, Final, TypedDict
import pandas as pd
from src.utils import display_table

# Type aliases
DataFrame: TypeAlias = pd.DataFrame
Series: TypeAlias = pd.Series

# Constantes
CLUB_NAME: Final[str] = 'UCSC'

class CyclistPerformance(TypedDict):
    """Tipo para almacenar el rendimiento de un ciclista."""
    name: str
    time: str
    position: int
    total_percentage: float

@dataclass
class UCSCAnalysis:
    """Clase para almacenar el análisis de los ciclistas de UCSC."""
    total_cyclists: int
    best_cyclist: CyclistPerformance
    all_cyclists: DataFrame

    def summary(self) -> str:
        """Genera un resumen del análisis de UCSC."""
        return (
            f"Total ciclistas UCSC: {self.total_cyclists}\n"
            f"Mejor tiempo: {self.best_cyclist['time']} "
            f"({self.best_cyclist['name']})\n"
            f"Posición general: {self.best_cyclist['position']}\n"
            f"Porcentaje: {self.best_cyclist['total_percentage']:.2f}%"
        )

def get_ucsc_cyclists(df: DataFrame) -> DataFrame:
    """
    Obtiene todos los ciclistas de la UCSC.

    Args:
        df: DataFrame con los datos de los ciclistas

    Returns:
        DataFrame con solo los ciclistas de UCSC

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    if 'club_clean' not in df.columns:
        raise ValueError("El DataFrame debe tener una columna 'club_clean'")

    ucsc_cyclists = df[df['club_clean'] == CLUB_NAME].copy()

    if ucsc_cyclists.empty:
        print(f"\nNo se encontraron ciclistas del {CLUB_NAME}")
        return ucsc_cyclists

    display_table(
        ucsc_cyclists,
        f"\n=== Ciclistas del {CLUB_NAME} ==="
    )

    return ucsc_cyclists

def find_best_ucsc_cyclist(df: DataFrame, ucsc_df: DataFrame) -> Optional[CyclistPerformance]:
    """
    Encuentra el ciclista de UCSC con mejor tiempo.

    Args:
        df: DataFrame completo con todos los ciclistas
        ucsc_df: DataFrame con solo ciclistas de UCSC

    Returns:
        Información del mejor ciclista o None si no hay datos

    Raises:
        ValueError: Si algún DataFrame es inválido
    """
    if df is None or df.empty or ucsc_df is None or ucsc_df.empty:
        raise ValueError("Los DataFrames no pueden ser None o estar vacíos")

    if 'time' not in ucsc_df.columns or 'biker' not in ucsc_df.columns:
        raise ValueError("Faltan columnas requeridas en el DataFrame")

    # Encontrar el mejor tiempo
    best_time_idx = ucsc_df['time'].idxmin()
    best_cyclist = ucsc_df.loc[best_time_idx]

    # Encontrar posición general
    df_sorted = df.sort_values('time')
    overall_position = df_sorted.index.get_loc(best_time_idx) + 1

    # Calcular porcentaje
    total_percentage = (overall_position / len(df)) * 100

    result: CyclistPerformance = {
        'name': best_cyclist['biker'],
        'time': best_cyclist['time'],
        'position': overall_position,
        'total_percentage': total_percentage
    }

    print(f"\n=== Mejor Ciclista {CLUB_NAME} ===")
    print(f"Nombre: {result['name']}")
    print(f"Tiempo: {result['time']}")
    print(f"Posición general: {result['position']} de {len(df)}")
    print(f"Porcentaje: {result['total_percentage']:.2f}%")

    return result

def analyze_ucsc(df: DataFrame) -> Optional[UCSCAnalysis]:
    """
    Realiza un análisis completo de los ciclistas de UCSC.

    Args:
        df: DataFrame con todos los datos de ciclistas

    Returns:
        Análisis completo de UCSC o None si no hay datos

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    ucsc_cyclists = get_ucsc_cyclists(df)
    if ucsc_cyclists.empty:
        return None

    best_cyclist = find_best_ucsc_cyclist(df, ucsc_cyclists)
    if not best_cyclist:
        return None

    analysis = UCSCAnalysis(
        total_cyclists=len(ucsc_cyclists),
        best_cyclist=best_cyclist,
        all_cyclists=ucsc_cyclists
    )

    print(f"\n=== Resumen Análisis {CLUB_NAME} ===")
    print(analysis.summary())

    return analysis

def main(df: Optional[DataFrame] = None) -> Optional[UCSCAnalysis]:
    """
    Función principal para analizar los ciclistas de UCSC.

    Args:
        df: DataFrame a analizar

    Returns:
        Resultados del análisis de UCSC

    Raises:
        ValueError: Si no se proporciona un DataFrame válido
    """
    if df is None:
        raise ValueError("Se requiere un DataFrame válido")

    return analyze_ucsc(df)
