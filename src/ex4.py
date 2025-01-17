"""
Módulo para el análisis y limpieza de datos de clubes ciclistas.
Incluye funcionalidades para normalizar nombres de clubes y análisis de participación.
"""

import re
from dataclasses import dataclass
from typing import TypeAlias, Final, Optional, TypedDict
import pandas as pd
from src.utils import display_table, TableConfig

# Type aliases
DataFrame: TypeAlias = pd.DataFrame
Series: TypeAlias = pd.Series

# Constantes para patrones regex y reemplazos
PREFIX_PATTERNS: Final[list[str]] = [
    r'^C\.C\. ',
    r'^C\.C ',
    r'^CC ',
    r'^C\.D\. ',
    r'^C\.D ',
    r'^CD ',
    r'^A\.C\. ',
    r'^A\.C ',
    r'^AC ',
    r'^A\.D\. ',
    r'^A\.D ',
    r'^AD ',
    r'^A\.E\. ',
    r'^A\.E ',
    r'^AE ',
    r'^E\.C\. ',
    r'^E\.C ',
    r'^EC ',
    r'^S\.C\. ',
    r'^S\.C ',
    r'^SC ',
    r'^S\.D\. ',
    r'^S\.D ',
    r'^SD '
]

SUFFIX_PATTERNS: Final[list[str]] = [
    r' T\.T\.$',
    r' T\.T$',
    r' TT$',
    r' T\.E\.$',
    r' T\.E$',
    r' TE$',
    r' C\.C\.$',
    r' C\.C$',
    r' CC$',
    r' C\.D\.$',
    r' C\.D$',
    r' CD$',
    r' A\.D\.$',
    r' A\.D$',
    r' AD$',
    r' A\.C\.$',
    r' A\.C$',
    r' AC$'
]

REPLACE_PATTERNS: Final[list[tuple[str, str]]] = [
    ('PEÑA CICLISTA', ''),
    ('PENYA CICLISTA', ''),
    ('AGRUPACIÓN CICLISTA', ''),
    ('AGRUPACION CICLISTA', ''),
    ('AGRUPACIÓ CICLISTA', ''),
    ('AGRUPACIO CICLISTA', ''),
    ('CLUB CICLISTA', ''),
    ('CLUB', '')
]

class ClubStats(TypedDict):
    """Tipo para estadísticas de un club."""
    total_members: int
    name: str
    position: int

@dataclass
class ClubAnalysis:
    """Clase para almacenar resultados del análisis de clubes."""
    df: DataFrame
    total_clubs: int
    unique_clubs: int
    top_clubs: list[str]

    def summary(self) -> str:
        """Genera un resumen del análisis de clubes."""
        return (
            f"Total de clubes analizados: {self.total_clubs}\n"
            f"Clubes únicos: {self.unique_clubs}\n"
            f"Top 3 clubes: {', '.join(self.top_clubs[:3])}"
        )

def clean_club_name(club_name: str) -> str:
    """
    Limpia y normaliza el nombre de un club ciclista.

    Args:
        club_name: Nombre del club a limpiar

    Returns:
        Nombre del club limpio y normalizado

    Examples:
        >>> clean_club_name('C.C. Huesca')
        'HUESCA'
        >>> clean_club_name('Club Ciclista Barcelona')
        'BARCELONA'
    """
    if not isinstance(club_name, str):
        return 'INDEPENDIENTE'

    # Convertir a mayúsculas
    name = club_name.upper().strip()

    # Aplicar patrones de reemplazo
    for pattern, replacement in REPLACE_PATTERNS:
        name = name.replace(pattern, replacement).strip()

    # Eliminar prefijos usando regex
    for pattern in PREFIX_PATTERNS:
        name = re.sub(pattern, '', name).strip()

    # Eliminar sufijos usando regex
    for pattern in SUFFIX_PATTERNS:
        name = re.sub(pattern, '', name).strip()

    # Limpiar espacios extra
    name = ' '.join(name.split())

    return name if name else 'INDEPENDIENTE'

def process_club_names(df: DataFrame) -> DataFrame:
    """
    Procesa los nombres de los clubes en el DataFrame.

    Args:
        df: DataFrame con datos de ciclistas

    Returns:
        DataFrame con nombres de clubes limpiados

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    if 'club' not in df.columns:
        raise ValueError("El DataFrame debe tener una columna 'club'")

    result_df = df.copy()
    result_df['club_clean'] = result_df['club'].apply(clean_club_name)

    print("\n=== Nombres de Clubes Procesados ===")
    display_table(
        result_df,
        "Primeros 15 registros:",
        TableConfig(max_rows=15)
    )

    return result_df

def analyze_club_participation(df: DataFrame) -> ClubAnalysis:
    """
    Analiza la participación por clubes.

    Args:
        df: DataFrame con datos de clubes limpios

    Returns:
        ClubAnalysis con resultados del análisis

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    if 'club_clean' not in df.columns:
        raise ValueError("El DataFrame debe tener una columna 'club_clean'")

    # Agrupar y contar
    club_counts = df['club_clean'].value_counts()

    result = ClubAnalysis(
        df=df,
        total_clubs=len(df),
        unique_clubs=len(club_counts),
        top_clubs=club_counts.index.tolist()
    )

    display_table(
        club_counts.reset_index(),
        "\n=== Análisis de Participación por Club ===",
        TableConfig(max_rows=10)
    )
    print(f"\n{result.summary()}")

    return result

def main(df: Optional[DataFrame] = None) -> DataFrame:
    """
    Función principal para procesar y analizar clubes.

    Args:
        df: DataFrame a procesar

    Returns:
        Tupla con DataFrame procesado y análisis de clubes

    Raises:
        ValueError: Si no se proporciona un DataFrame válido
    """
    if df is None:
        raise ValueError("Se requiere un DataFrame válido")

    processed_df = process_club_names(df)
    analyze_club_participation(processed_df)

    return processed_df
