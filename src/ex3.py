"""
Módulo para el análisis y visualización de la distribución de tiempos
de los ciclistas en la carrera Orbea Monegros 2024.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias, Optional, Final, TypedDict
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import display_table, TableConfig

# Type aliases
DataFrame: TypeAlias = pd.DataFrame
Series: TypeAlias = pd.Series
TimeStr: TypeAlias = str

# Constantes tipadas
DEFAULT_IMG_PATH: Final[Path] = Path("img")
DEFAULT_HIST_NAME: Final[str] = "histograma.png"
FIGURE_SIZE: Final[tuple[int, int]] = (10, 6)

class TimeInterval(TypedDict):
    """Tipo para intervalos de tiempo."""
    hours: int
    minutes: int
    seconds: int

@dataclass
class TimeGroupResult:
    """Clase para almacenar resultados del agrupamiento de tiempos."""
    df: DataFrame
    time_distribution: Series
    total_groups: int

    def summary(self) -> str:
        """Genera un resumen del agrupamiento de tiempos."""
        return (
            f"Total de grupos temporales: {self.total_groups}\n"
            f"Rango de tiempos: {self.time_distribution.index.min()} - "
            f"{self.time_distribution.index.max()}"
        )

def parse_time(time_str: TimeStr) -> Optional[TimeInterval]:
    """
    Parsea un string de tiempo en formato 'hh:mm:ss'.

    Args:
        time_str: Tiempo en formato 'hh:mm:ss'

    Returns:
        TimeInterval con las partes del tiempo o None si es inválido
    """
    if not isinstance(time_str, str):
        return None

    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
        return TimeInterval(hours=hours, minutes=minutes, seconds=seconds)
    except (ValueError, TypeError):
        return None

def minutes_002040(time_str: TimeStr) -> Optional[TimeStr]:
    """
    Agrupa los tiempos en intervalos de 20 minutos.

    Args:
        time_str: Tiempo en formato 'hh:mm:ss'

    Returns:
        Tiempo agrupado en formato 'hh:mm' o None si es inválido

    Examples:
        >>> minutes_002040('06:19:40')
        '06:00'
        >>> minutes_002040('06:29:40')
        '06:20'
        >>> minutes_002040('06:59:40')
        '06:40'
    """
    time_parts = parse_time(time_str)
    if not time_parts:
        return None

    grouped_minutes = (time_parts['minutes'] // 20) * 20
    return f"{time_parts['hours']:02d}:{grouped_minutes:02d}"

def process_time_groups(df: DataFrame) -> DataFrame:
    """
    Procesa los tiempos de los ciclistas y añade columna de tiempos agrupados.

    Args:
        df: DataFrame con datos de ciclistas

    Returns:
        DataFrame con nueva columna de tiempos agrupados

    Raises:
        ValueError: Si el DataFrame es inválido o no tiene columna 'time'
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    if 'time' not in df.columns:
        raise ValueError("El DataFrame debe tener una columna 'time'")

    processed_df = df.copy()
    processed_df['time_grouped'] = processed_df['time'].apply(minutes_002040)

    print("\n=== Tiempos Agrupados ===")
    display_table(
        processed_df,
        "Primeros 15 registros:",
        TableConfig(max_rows=15)
    )

    return processed_df

def group_by_time(df: DataFrame) -> TimeGroupResult:
    """
    Agrupa los ciclistas por intervalos de tiempo.

    Args:
        df: DataFrame con datos de ciclistas

    Returns:
        TimeGroupResult con resultados del agrupamiento

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    if df is None or df.empty:
        raise ValueError("El DataFrame no puede ser None o estar vacío")

    if 'time_grouped' not in df.columns:
        raise ValueError("El DataFrame debe tener una columna 'time_grouped'")

    time_distribution = df['time_grouped'].value_counts().sort_index()

    result = TimeGroupResult(
        df=df,
        time_distribution=time_distribution,
        total_groups=len(time_distribution)
    )

    display_table(
        time_distribution.reset_index(),
        "\n=== Distribución de Tiempos ===",
        TableConfig(headers=['Intervalo de Tiempo', 'Número de Ciclistas'])
    )
    print(f"\n{result.summary()}")

    return result

def create_histogram(time_groups: TimeGroupResult,
                    output_dir: Optional[Path] = None) -> Path:
    """
    Crea y guarda un histograma de la distribución de tiempos.

    Args:
        time_groups: Resultados del agrupamiento de tiempos
        output_dir: Directorio para guardar la imagen

    Returns:
        Path al archivo de imagen guardado
    """
    plt.figure(figsize=FIGURE_SIZE)
    time_groups.time_distribution.plot(kind='bar')

    plt.title('Distribución de Tiempos de Ciclistas')
    plt.xlabel('Intervalo de Tiempo')
    plt.ylabel('Número de Ciclistas')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Preparar directorio y guardar
    img_dir = Path(output_dir or DEFAULT_IMG_PATH)
    img_dir.mkdir(parents=True, exist_ok=True)

    img_path = img_dir / DEFAULT_HIST_NAME
    plt.savefig(img_path)
    plt.close()

    print(f"\nHistograma guardado en: {img_path}")
    return img_path

def main(df: Optional[DataFrame] = None) -> DataFrame:
    """
    Función principal para procesar tiempos y generar histograma.

    Args:
        df: DataFrame a procesar

    Returns:
        DataFrame con tiempos procesados

    Raises:
        ValueError: Si no se proporciona un DataFrame válido
    """
    if df is None:
        raise ValueError("Se requiere un DataFrame válido")

    processed_df = process_time_groups(df)
    time_groups = group_by_time(processed_df)
    create_histogram(time_groups)

    return processed_df
