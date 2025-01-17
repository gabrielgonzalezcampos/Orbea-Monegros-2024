"""
Tests para el módulo de carga y análisis del dataset de Orbea Monegros 2024.
"""

import pytest
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import patch, Mock
import io
from contextlib import redirect_stdout

from src.ex1 import (
    main,
    load_dataset,
    analyze_dataset,
    DatasetInfo,
    DEFAULT_SEPARATOR
)

# Fixtures
@pytest.fixture
def sample_data() -> str:
    """Fixture que proporciona datos de ejemplo en formato CSV."""
    return (
        "biker;dorsal;time;club\n"
        "Ciclista 1;1;05:30:00;Club A\n"
        "Ciclista 2;2;06:00:00;Club B\n"
        "Ciclista 3;3;06:30:00;Club C\n"
    )

@pytest.fixture
def sample_df(sample_data) -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba."""
    return pd.read_csv(
        io.StringIO(sample_data),
        sep=DEFAULT_SEPARATOR
    )

@pytest.fixture
def temp_csv_file(tmp_path: Path, sample_data: str) -> Path:
    """Fixture que crea un archivo CSV temporal con datos de prueba."""
    csv_file = tmp_path / "test_dataset.csv"
    csv_file.write_text(sample_data)
    return csv_file

@pytest.fixture
def mock_read_csv():
    """Fixture que simula la lectura de un CSV."""
    data = {
        'biker': ['Ciclista 1', 'Ciclista 2', 'Ciclista 3'],
        'dorsal': [1, 2, 3],
        'time': ['05:30:00', '06:00:00', '06:30:00'],
        'club': ['Club A', 'Club B', 'Club C']
    }
    with patch('pandas.read_csv') as mock_read:
        mock_read.return_value = pd.DataFrame(data)
        yield mock_read

@pytest.fixture
def expected_df():
    """Fixture que proporciona el DataFrame esperado."""
    return pd.DataFrame({
        'biker': ['Ciclista 1', 'Ciclista 2', 'Ciclista 3'],
        'dorsal': [1, 2, 3],
        'time': ['05:30:00', '06:00:00', '06:30:00'],
        'club': ['Club A', 'Club B', 'Club C']
    })

# Tests para load_dataset
def test_load_dataset_success(temp_csv_file: Path):
    """Test que verifica la carga exitosa del dataset."""
    df = load_dataset(temp_csv_file)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ['biker', 'dorsal', 'time', 'club']

def test_load_dataset_file_not_found():
    """Test que verifica el manejo de archivo no encontrado."""
    with pytest.raises(FileNotFoundError) as exc_info:
        load_dataset('nonexistent.csv')
    assert "Archivo no encontrado" in str(exc_info.value)

def test_load_dataset_empty_file(tmp_path: Path):
    """Test que verifica el manejo de archivo vacío."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    
    with pytest.raises(pd.errors.EmptyDataError) as exc_info:
        load_dataset(empty_file)
    assert "El dataset está vacío" in str(exc_info.value)

def test_load_dataset_invalid_format(tmp_path: Path):
    """Test que verifica el manejo de formato inválido."""
    invalid_file = tmp_path / "invalid.csv"
    # Crear un CSV con número incorrecto de columnas
    invalid_file.write_text(
        "biker;dorsal;time;club\n"
        "Ciclista 1;1;05:30:00\n"  # Falta una columna
        "Ciclista 2;2;06:00:00;Club B;Extra"  # Columna extra
    )

# Tests para analyze_dataset
def test_analyze_dataset_success(sample_df: pd.DataFrame):
    """Test que verifica el análisis exitoso del dataset."""
    result = analyze_dataset(sample_df)
    
    assert isinstance(result, DatasetInfo)
    assert result.total_participants == 3
    assert result.columns == ['biker', 'dorsal', 'time', 'club']
    assert_frame_equal(result.df, sample_df)

def test_analyze_dataset_empty_df():
    """Test que verifica el manejo de DataFrame vacío."""
    empty_df = pd.DataFrame()
    
    with pytest.raises(ValueError) as exc_info:
        analyze_dataset(empty_df)
    assert "DataFrame no puede ser None o estar vacío" in str(exc_info.value)

def test_analyze_dataset_none_df():
    """Test que verifica el manejo de DataFrame None."""
    with pytest.raises(ValueError) as exc_info:
        analyze_dataset(None)
    assert "DataFrame no puede ser None o estar vacío" in str(exc_info.value)

def test_dataset_info_summary(sample_df: pd.DataFrame):
    """Test que verifica la generación del resumen del DatasetInfo."""
    info = DatasetInfo(
        df=sample_df,
        total_participants=3,
        columns=['biker', 'dorsal', 'time', 'club']
    )
    
    summary = info.summary
    assert isinstance(summary, dict)
    assert summary['total_participants'] == 3
    assert summary['columns'] == ['biker', 'dorsal', 'time', 'club']
    assert_frame_equal(summary['head_data'], sample_df.head())

def test_analyze_dataset_output(sample_df: pd.DataFrame):
    """Test que verifica la salida impresa del análisis."""
    output = io.StringIO()
    with redirect_stdout(output):
        analyze_dataset(sample_df)
    
    printed_output = output.getvalue()
    assert "Análisis Exploratorio de Datos" in printed_output
    assert "Primeros 5 registros" in printed_output
    assert "Número total de participantes" in printed_output
    assert "Columnas disponibles" in printed_output

# Test para el main
def test_main_success(mock_read_csv, expected_df):
    """Test que verifica la ejecución exitosa del main."""
    output = io.StringIO()
    with redirect_stdout(output):
        result_df = main()

    # Verificar que el DataFrame devuelto es correcto
    pd.testing.assert_frame_equal(result_df, expected_df)
    
    # Verificar la salida
    output_text = output.getvalue()
    assert "=== Análisis Exploratorio de Datos ===" in output_text
    assert "Primeros 5 registros" in output_text
    # Verifica la presencia de las columnas
    assert "biker" in output_text
    assert "dorsal" in output_text
    assert "time" in output_text
    assert "club" in output_text
    # Verifica la presencia de los tipos de datos
    assert "Tipos de datos por columna" in output_text

def test_main_file_not_found(mock_read_csv):
    """Test que verifica el manejo de archivo no encontrado."""
    mock_read_csv.side_effect = FileNotFoundError("Test error")
    
    with pytest.raises(FileNotFoundError):
        main()

def test_main_empty_file(mock_read_csv):
    """Test que verifica el manejo de archivo vacío."""
    mock_read_csv.return_value = pd.DataFrame()
    
    with pytest.raises(pd.errors.EmptyDataError):
        main()

def test_main_parsing_error(mock_read_csv):
    """Test que verifica el manejo de errores de parsing."""
    mock_read_csv.side_effect = pd.errors.ParserError("Test error")
    
    with pytest.raises(ValueError):
        main()

def test_main_output_format(mock_read_csv, expected_df):
    """Test que verifica el formato detallado de la salida."""
    output = io.StringIO()
    with redirect_stdout(output):
        main()
    
    output_text = output.getvalue().split('\n')
    
    # Verificar secciones específicas de la salida
    headers = [line for line in output_text if "===" in line]
    assert len(headers) > 0  # Al menos una sección con encabezado
    
    # Verificar que se muestran los datos correctos
    assert any('Ciclista 1' in line for line in output_text)
    assert any('Club A' in line for line in output_text)
    assert any('dorsal' in line.lower() for line in output_text)
    
    # Verificar tipos de datos
    assert any('Tipos de datos por columna' in line for line in output_text)
    assert any('object' in line for line in output_text)
    assert any('int64' in line for line in output_text)

if __name__ == '__main__':
    pytest.main(['-v', __file__])