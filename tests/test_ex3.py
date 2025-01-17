"""Tests para el módulo de análisis de tiempos y generación de histogramas."""

import pytest
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo para tests
import io
import os
from contextlib import redirect_stdout

from src.ex3 import (
    main,
    minutes_002040,
    process_time_groups,
    group_by_time,
    create_histogram,
    TimeInterval,
    TimeGroupResult,
    parse_time
)

# Fixtures
@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba."""
    return pd.DataFrame({
        'biker': ['Ciclista 1', 'Ciclista 2', 'Ciclista 3'],
        'time': ['06:19:40', '06:29:40', '06:59:40']
    })

@pytest.fixture
def processed_df(sample_df) -> pd.DataFrame:
    """Fixture que proporciona un DataFrame con tiempos procesados."""
    df = sample_df.copy()
    df['time_grouped'] = df['time'].apply(minutes_002040)
    return df

@pytest.fixture
def temp_img_dir(tmp_path) -> Path:
    """Fixture que proporciona un directorio temporal para imágenes."""
    img_dir = tmp_path / "img"
    img_dir.mkdir()
    return img_dir

# Tests para parse_time
def test_parse_time_valid():
    """Test que verifica el parsing correcto de tiempo."""
    result = parse_time("06:19:40")
    assert isinstance(result, dict)
    assert result['hours'] == 6
    assert result['minutes'] == 19
    assert result['seconds'] == 40

def test_parse_time_invalid():
    """Test que verifica el manejo de tiempos inválidos."""
    assert parse_time("invalid") is None
    assert parse_time("") is None
    assert parse_time(None) is None
    assert parse_time("06:19") is None

# Tests para minutes_002040
def test_minutes_002040_examples():
    """Test que verifica los ejemplos de la documentación."""
    assert minutes_002040('06:19:40') == '06:00'
    assert minutes_002040('06:29:40') == '06:20'
    assert minutes_002040('06:59:40') == '06:40'

def test_minutes_002040_invalid():
    """Test que verifica el manejo de entradas inválidas."""
    assert minutes_002040("invalid") is None
    assert minutes_002040("") is None
    assert minutes_002040(None) is None

def test_minutes_002040_edge_cases():
    """Test que verifica casos límite."""
    assert minutes_002040('00:00:00') == '00:00'
    assert minutes_002040('23:59:59') == '23:40'

# Tests para process_time_groups
def test_process_time_groups_success(sample_df):
    """Test que verifica el procesamiento exitoso de grupos de tiempo."""
    result = process_time_groups(sample_df)
    
    assert 'time_grouped' in result.columns
    assert len(result) == len(sample_df)
    assert all(isinstance(t, str) for t in result['time_grouped'])

def test_process_time_groups_invalid_df():
    """Test que verifica el manejo de DataFrames inválidos."""
    with pytest.raises(ValueError, match="DataFrame no puede ser None o estar vacío"):
        process_time_groups(None)
    
    with pytest.raises(ValueError, match="DataFrame no puede ser None o estar vacío"):
        process_time_groups(pd.DataFrame())

def test_process_time_groups_missing_column():
    """Test que verifica el manejo de columnas faltantes."""
    df = pd.DataFrame({'wrong_column': [1,2,3]})
    with pytest.raises(ValueError, match="debe tener una columna 'time'"):
        process_time_groups(df)

# Tests para group_by_time
def test_group_by_time_success(processed_df):
    """Test que verifica el agrupamiento exitoso por tiempo."""
    result = group_by_time(processed_df)
    
    assert isinstance(result, TimeGroupResult)
    assert isinstance(result.time_distribution, pd.Series)
    assert result.total_groups > 0
    assert result.df is processed_df

def test_group_by_time_invalid_df():
    """Test que verifica el manejo de DataFrames inválidos."""
    with pytest.raises(ValueError):
        group_by_time(None)
    
    with pytest.raises(ValueError):
        group_by_time(pd.DataFrame())

# Tests para create_histogram
def test_create_histogram(processed_df, temp_img_dir):
    """Test que verifica la creación exitosa del histograma."""
    time_groups = group_by_time(processed_df)
    img_path = create_histogram(time_groups, temp_img_dir)
    
    assert img_path.exists()
    assert img_path.suffix == '.png'

# Tests de salida
def test_output_formatting(sample_df):
    """Test que verifica el formato de la salida."""
    output = io.StringIO()
    with redirect_stdout(output):
        process_time_groups(sample_df)
        
    output_text = output.getvalue()
    assert "=== Tiempos Agrupados ===" in output_text
    assert "Primeros 15 registros" in output_text

# Tests de tipos
def test_time_interval_type():
    """Test que verifica la estructura del tipo TimeInterval."""
    time: TimeInterval = {
        'hours': 6,
        'minutes': 19,
        'seconds': 40
    }
    # Si no hay error de tipo, la estructura es correcta

#Test de main
def test_main_without_df():
    """Test que verifica el manejo de DataFrame no proporcionado."""
    with pytest.raises(ValueError, match="Se requiere un DataFrame válido"):
        main(None)

def test_main_empty_df():
    """Test que verifica el manejo de DataFrame vacío."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        main(empty_df)

def test_main_success(sample_df, temp_img_dir):
    """Test que verifica la ejecución exitosa del main."""
    output = io.StringIO()
    with redirect_stdout(output):
        result_df = main(sample_df)
    
    assert isinstance(result_df, pd.DataFrame)
    # Verificar que se ha añadido la columna de tiempos agrupados
    assert 'time_grouped' in result_df.columns
    # Verificar que se mantienen las columnas originales
    assert all(col in result_df.columns for col in sample_df.columns)
    # Verificar que se ha creado el histograma
    assert os.path.exists('img/histograma.png')

def test_main_data_integrity(sample_df, temp_img_dir):
    """Test que verifica la integridad de los datos procesados."""
    result_df = main(sample_df)
    
    # Verificar que no se han perdido registros
    assert len(result_df) == len(sample_df)
    
    # Verificar que los tiempos agrupados siguen el formato correcto
    time_groups = result_df['time_grouped'].unique()
    for time in time_groups:
        hours, minutes = time.split(':')
        assert int(hours) >= 0 and int(hours) <= 23
        assert int(minutes) in [0, 20, 40]
    
    # Verificar que los datos originales no han cambiado
    pd.testing.assert_series_equal(result_df['time'], sample_df['time'])
    pd.testing.assert_series_equal(result_df['biker'], sample_df['biker'])

if __name__ == '__main__':
    pytest.main(['-v', __file__])