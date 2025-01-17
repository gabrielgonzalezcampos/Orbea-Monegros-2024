"""
Módulo para la anonimización y limpieza de datos de ciclistas.
Incluye funcionalidades para anonimizar nombres y filtrar participantes.
"""

from dataclasses import dataclass
from typing import Optional, TypeAlias, Final, NotRequired, TypedDict
import pandas as pd
from faker import Faker
from src.utils import display_table, TableConfig

# Type aliases
DataFrame: TypeAlias = pd.DataFrame
Series: TypeAlias = pd.Series

# Constantes tipadas
DEFAULT_LOCALE: Final[str] = 'en_US'
DEFAULT_TIME: Final[str] = '00:00:00'

class CyclistData(TypedDict):
    """Tipo para los datos de un ciclista."""
    biker: str
    dorsal: int
    time: str
    club: str

class CyclistResult(TypedDict):
    """Tipo para el resultado de búsqueda de un ciclista."""
    found: bool
    data: NotRequired[CyclistData]

@dataclass
class AnonymizationResult:
    """Clase para almacenar resultados de la anonimización."""
    df: DataFrame
    original_count: int
    anonymized_count: int

    def summary(self) -> str:
        """Genera un resumen del proceso de anonimización."""
        return (
            f"Registros originales: {self.original_count}\n"
            f"Registros anonimizados: {self.anonymized_count}"
        )

def validate_dataframe(df: Optional[DataFrame], required_columns: list[str]) -> None:
    """
    Valida que el DataFrame cumpla con los requisitos básicos.

    Args:
        df: DataFrame a validar
        required_columns: Lista de columnas requeridas

    Raises:
        ValueError: Si el DataFrame no cumple los requisitos
    """
    if df is None:
        raise ValueError("El DataFrame no puede ser None")

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Columnas requeridas faltantes: {missing_columns}"
        )

def name_surname(df: DataFrame) -> AnonymizationResult:
    """
    Anonimiza los nombres de los ciclistas usando Faker.

    Args:
        df: DataFrame original con los datos de los ciclistas

    Returns:
        AnonymizationResult con el DataFrame anonimizado y estadísticas

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    validate_dataframe(df, ['biker'])

    # Inicializar Faker con seed para reproducibilidad
    fake = Faker(DEFAULT_LOCALE)
    Faker.seed(12345)

    # Crear copia y anonimizar
    anonymized_df = df.copy()
    anonymized_df['biker'] = [fake.name() for _ in range(len(df))]

    result = AnonymizationResult(
        df=anonymized_df,
        original_count=len(df),
        anonymized_count=len(anonymized_df)
    )

    # Mostrar resultados
    print("\n=== Datos Anonimizados ===")
    display_table(
        anonymized_df,
        "Primeros 5 registros:",
        TableConfig(max_rows=5)
    )

    print(f"\n{result.summary()}")

    return result

def clean_no_time_bikers(df: DataFrame) -> DataFrame:
    """
    Elimina los ciclistas que no han participado (tiempo 00:00:00).

    Args:
        df: DataFrame con los datos de los ciclistas

    Returns:
        DataFrame sin los ciclistas que no han participado

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    validate_dataframe(df, ['time'])

    # Filtrar y contar
    original_count = len(df)
    cleaned_df = df[df['time'] != DEFAULT_TIME]
    cleaned_count = len(cleaned_df)

    # Mostrar resultados
    print("\n=== Limpieza de No Participantes ===")
    print(f"Registros eliminados: {original_count - cleaned_count}")
    print(f"Registros restantes: {cleaned_count}")
    display_table(
        cleaned_df,
        "Primeros 5 registros después de la limpieza:",
        TableConfig(max_rows=5)
    )


    return cleaned_df

def get_cyclist_by_dorsal(df: DataFrame, dorsal: int) -> CyclistResult:
    """
    Recupera los datos de un ciclista por su número de dorsal.

    Args:
        df: DataFrame con los datos de ciclistas
        dorsal: Número de dorsal a buscar

    Returns:
        CyclistResult con los datos del ciclista o indicación de no encontrado

    Raises:
        ValueError: Si el DataFrame es inválido
    """
    validate_dataframe(df, ['dorsal'])

    cyclist_data = df[df['dorsal'] == dorsal]

    if cyclist_data.empty:
        print(f"\nNo se encontró ningún ciclista con dorsal {dorsal}")
        return {'found': False}

    cyclist = cyclist_data.iloc[0]
    result: CyclistResult = {
        'found': True,
        'data': {
            'biker': cyclist['biker'],
            'dorsal': cyclist['dorsal'],
            'time': cyclist['time'],
            'club': cyclist['club']
        }
    }

    display_table(
        [result['data']],
        f"\n=== Datos del Ciclista con dorsal {dorsal} ==="
    )


    return result

def main(df: Optional[DataFrame] = None) -> DataFrame:
    """
    Función principal para ejecutar la anonimización y limpieza de datos.

    Args:
        df: DataFrame a procesar. Si no se proporciona, se debe cargar del ejercicio 1.

    Returns:
        DataFrame procesado y limpio

    Raises:
        ValueError: Si no se proporciona un DataFrame válido
    """
    if df is None:
        raise ValueError("Se requiere un DataFrame válido")

    # Proceso completo
    anonymized_result = name_surname(df)
    cleaned_df = clean_no_time_bikers(anonymized_result.df)
    get_cyclist_by_dorsal(cleaned_df, 1000)

    return cleaned_df
