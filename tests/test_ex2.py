"""Tests para el módulo de anonimización y limpieza de datos."""

import pytest
import pandas as pd
from faker import Faker
import io
from contextlib import redirect_stdout

from src.ex2 import (
    main,
    name_surname,
    clean_no_time_bikers,
    get_cyclist_by_dorsal,
    AnonymizationResult,
    CyclistData,
    CyclistResult,
    validate_dataframe
)

# Fixtures
@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba."""
    return pd.DataFrame({
        'biker': ['John Doe', 'Jane Doe', 'Jim Doe'],
        'dorsal': [1, 2, 3],
        'time': ['05:30:00', '00:00:00', '06:30:00'],
        'club': ['Club A', 'Club B', 'Club C']
    })

@pytest.fixture
def fake() -> Faker:
    """Fixture que proporciona una instancia de Faker con seed fijo."""
    faker = Faker()
    Faker.seed(12345)
    return faker

# Tests para validate_dataframe
def test_validate_dataframe_none():
    """Test que verifica la validación de DataFrame None."""
    with pytest.raises(ValueError) as exc_info:
        validate_dataframe(None, ['biker'])
    assert "DataFrame no puede ser None" in str(exc_info.value)

def test_validate_dataframe_missing_columns(sample_df):
    """Test que verifica la validación de columnas faltantes."""
    with pytest.raises(ValueError) as exc_info:
        validate_dataframe(sample_df, ['non_existent'])
    assert "Columnas requeridas faltantes" in str(exc_info.value)

# Tests para name_surname
def test_name_surname_success(sample_df):
    """Test que verifica la anonimización exitosa."""
    result = name_surname(sample_df)
    
    assert isinstance(result, AnonymizationResult)
    assert len(result.df) == len(sample_df)
    assert list(result.df['biker']) != list(sample_df['biker'])
    assert result.original_count == result.anonymized_count
    assert all(isinstance(name, str) for name in result.df['biker'])

def test_name_surname_reproducibility(sample_df, fake):
    """Test que verifica la reproducibilidad de la anonimización."""
    result1 = name_surname(sample_df)
    Faker.seed(12345)
    result2 = name_surname(sample_df)
    
    assert list(result1.df['biker']) == list(result2.df['biker'])

# Tests para clean_no_time_bikers
def test_clean_no_time_bikers_success(sample_df):
    """Test que verifica la limpieza exitosa de no participantes."""
    result = clean_no_time_bikers(sample_df)
    
    assert len(result) == 2  # Solo quedan los que tienen tiempo != 00:00:00
    assert '00:00:00' not in result['time'].values
    assert all(time != '00:00:00' for time in result['time'])

def test_clean_no_time_bikers_no_changes():
    """Test que verifica el caso donde no hay registros para limpiar."""
    df = pd.DataFrame({
        'biker': ['John Doe'],
        'time': ['05:30:00']
    })
    result = clean_no_time_bikers(df)
    assert len(result) == len(df)

# Tests para get_cyclist_by_dorsal
def test_get_cyclist_by_dorsal_found(sample_df):
    """Test que verifica la búsqueda exitosa de un ciclista."""
    result = get_cyclist_by_dorsal(sample_df, 1)
    
    assert isinstance(result, dict)
    assert result['found'] is True
    assert isinstance(result['data'], dict)
    assert result['data']['dorsal'] == 1
    assert result['data']['biker'] == 'John Doe'

def test_get_cyclist_by_dorsal_not_found(sample_df):
    """Test que verifica el caso de ciclista no encontrado."""
    result = get_cyclist_by_dorsal(sample_df, 999)
    
    assert isinstance(result, dict)
    assert result['found'] is False
    assert 'data' not in result

# Tests de tipos
def test_cyclist_data_type():
    """Test que verifica la estructura del tipo CyclistData."""
    data: CyclistData = {
        'biker': 'John Doe',
        'dorsal': 1,
        'time': '05:30:00',
        'club': 'Club A'
    }
    # Si no hay error de tipo, la estructura es correcta

def test_cyclist_result_type():
    """Test que verifica la estructura del tipo CyclistResult."""
    # Caso encontrado
    result_found: CyclistResult = {
        'found': True,
        'data': {
            'biker': 'John Doe',
            'dorsal': 1,
            'time': '05:30:00',
            'club': 'Club A'
        }
    }
    
    # Caso no encontrado
    result_not_found: CyclistResult = {
        'found': False
    }
    # Si no hay error de tipo, las estructuras son correctas

# Test de salida
def test_output_formatting(sample_df):
    """Test que verifica el formato de la salida."""
    output = io.StringIO()
    with redirect_stdout(output):
        name_surname(sample_df)
        
    output_text = output.getvalue()
    assert "=== Datos Anonimizados ===" in output_text
    assert "Primeros 5 registros" in output_text
    assert "Registros originales" in output_text

# Test para main
def test_main_without_df():
    """Test que verifica el manejo de DataFrame no proporcionado."""
    with pytest.raises(ValueError, match="Se requiere un DataFrame válido"):
        main(None)

def test_main_empty_df():
    """Test que verifica el manejo de DataFrame vacío."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="Columnas requeridas faltantes"):
        main(empty_df)

def test_main_success(sample_df, fake):
    """Test que verifica la ejecución exitosa del main."""
    output = io.StringIO()
    with redirect_stdout(output):
        result_df = main(sample_df)
    
    assert isinstance(result_df, pd.DataFrame)
    # Verificar que se han anonimizado los nombres
    assert all(name not in result_df['biker'].values 
              for name in ['John Doe', 'Jane Doe', 'Jim Doe'])
    # Verificar que se han eliminado los registros con tiempo 00:00:00
    assert '00:00:00' not in result_df['time'].values
    # Verificar que se mantienen las columnas originales
    assert list(result_df.columns) == ['biker', 'dorsal', 'time', 'club']
    # Verificar que solo quedan 2 registros (se eliminó el 00:00:00)
    assert len(result_df) == 2

def test_main_output_format(sample_df, fake):
    """Test que verifica el formato de la salida del main."""
    output = io.StringIO()
    with redirect_stdout(output):
        main(sample_df)
    
    output_text = output.getvalue()
    # Verificar las secciones de salida
    assert "=== Datos Anonimizados ===" in output_text
    assert "Primeros 5 registros" in output_text

def test_main_data_consistency(sample_df, fake):
    """Test que verifica la consistencia de los datos procesados."""
    result_df = main(sample_df)
    
    # Verificar que el dorsal y club se mantienen para los registros válidos
    valid_mask = sample_df['time'] != '00:00:00'
    valid_input = sample_df[valid_mask].reset_index(drop=True)
    valid_result = result_df.reset_index(drop=True)
    
    # Verificar que los datos que no deben cambiar se mantienen
    pd.testing.assert_series_equal(valid_result['dorsal'], valid_input['dorsal'])
    pd.testing.assert_series_equal(valid_result['club'], valid_input['club'])
    pd.testing.assert_series_equal(valid_result['time'], valid_input['time'])
    
    # Verificar que los nombres sí han cambiado
    assert not any(name in result_df['biker'].values 
                  for name in ['John Doe', 'Jane Doe', 'Jim Doe'])

if __name__ == '__main__':
    pytest.main(['-v', __file__])