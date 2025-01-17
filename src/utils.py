"""
Módulo de utilidades compartidas para el proyecto de análisis de Orbea Monegros.
"""

from typing import Optional, Union, Dict
from dataclasses import dataclass
import pandas as pd
from tabulate import tabulate

DataFrame = pd.DataFrame

@dataclass
class TableConfig:
    """Configuración para el formato de tablas."""
    headers: Union[str, Dict[str, str]] = 'keys'
    table_format: str = 'pretty'
    show_index: bool = False
    num_align: str = 'right'
    max_rows: Optional[int] = None

def display_table(
    data: DataFrame,
    title: str,
    config: Optional[TableConfig] = None
) -> None:
    """
    Muestra una tabla formateada con los datos proporcionados.

    Args:
        data: DataFrame con los datos a mostrar
        title: Título de la tabla
        config: Configuración opcional para el formato
    """
    if config is None:
        config = TableConfig()

    # Si se especifica max_rows, limitar los datos
    display_data = data.head(config.max_rows) if config.max_rows else data

    print(title)
    print(tabulate(
        display_data,
        headers=config.headers,
        tablefmt=config.table_format,
        showindex=config.show_index,
        numalign=config.num_align
    ))
