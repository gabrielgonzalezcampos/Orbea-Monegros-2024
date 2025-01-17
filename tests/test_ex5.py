"""Tests para el módulo de análisis de ciclistas UCSC."""

import pytest
import pandas as pd
import io
from contextlib import redirect_stdout

from src.ex5 import (
    get_ucsc_cyclists,
    find_best_ucsc_cyclist,
    analyze_ucsc,
    UCSCAnalysis,
    CyclistPerformance,
    CLUB_NAME
)

# Fixtures
@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba con ciclistas."""
    return pd.DataFrame({
        'biker': ['Ciclista 1', 'Ciclista 2', 'Ciclista 3', 'Ciclista 4'],
        'time': ['05:30:00', '06:00:00', '05:45:00', '06:15:00'],
        'club_clean': ['UCSC', 'OTRO', 'UCSC', 'OTRO']
    })

@pytest.fixture
def ucsc_df(sample_df) -> pd.DataFrame:
    """Fixture que proporciona solo los ciclistas de UCSC."""
    return sample_df[sample_df['club_clean'] == CLUB_NAME].copy()

# Tests para get_ucsc_cyclists
def test_get_ucsc_cyclists_success(sample_df):
    """Test que verifica la obtención exitosa de ciclistas UCSC."""
    result = get_ucsc_cyclists(sample_df)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert all(result['club_clean'] == CLUB_NAME)
    assert 'Ciclista 1' in result['biker'].values
    assert 'Ciclista 3' in result['biker'].values

def test_get_ucsc_cyclists_no_data():
    """Test que verifica el manejo de DataFrame vacío."""
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        get_ucsc_cyclists(None)
        
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        get_ucsc_cyclists(pd.DataFrame())

def test_get_ucsc_cyclists_wrong_columns():
    """Test que verifica el manejo de columnas incorrectas."""
    df = pd.DataFrame({'wrong_col': ['test']})
    with pytest.raises(ValueError, match="El DataFrame debe tener una columna 'club_clean'"):
        get_ucsc_cyclists(df)

def test_get_ucsc_cyclists_no_members(sample_df):
    """Test que verifica el caso sin miembros de UCSC."""
    df = sample_df.copy()
    df['club_clean'] = 'OTRO'
    result = get_ucsc_cyclists(df)
    assert result.empty

# Tests para find_best_ucsc_cyclist
def test_find_best_ucsc_cyclist_success(sample_df, ucsc_df):
    """Test que verifica la búsqueda exitosa del mejor ciclista."""
    result = find_best_ucsc_cyclist(sample_df, ucsc_df)
    
    assert isinstance(result, dict)
    assert result['name'] == 'Ciclista 1'
    assert result['time'] == '05:30:00'
    assert result['position'] == 1
    assert 0 < result['total_percentage'] <= 100

def test_find_best_ucsc_cyclist_no_data():
    """Test que verifica el manejo de DataFrames vacíos."""
    with pytest.raises(ValueError):
        find_best_ucsc_cyclist(None, pd.DataFrame())
    
    with pytest.raises(ValueError):
        find_best_ucsc_cyclist(pd.DataFrame(), None)

# Tests para analyze_ucsc
def test_analyze_ucsc_success(sample_df):
    """Test que verifica el análisis exitoso de UCSC."""
    result = analyze_ucsc(sample_df)
    
    assert isinstance(result, UCSCAnalysis)
    assert result.total_cyclists == 2
    assert isinstance(result.best_cyclist, dict)
    assert isinstance(result.all_cyclists, pd.DataFrame)
    assert len(result.all_cyclists) == 2

def test_analyze_ucsc_no_data():
    """Test que verifica el manejo de DataFrame vacío."""
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        analyze_ucsc(None)
    
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        analyze_ucsc(pd.DataFrame())

def test_analyze_ucsc_no_members(sample_df):
    """Test que verifica el caso sin miembros de UCSC."""
    df = sample_df.copy()
    df['club_clean'] = 'OTRO'
    result = analyze_ucsc(df)
    assert result is None

# Tests de salida
def test_output_formatting(sample_df):
    """Test que verifica el formato de la salida."""
    output = io.StringIO()
    with redirect_stdout(output):
        analyze_ucsc(sample_df)
        
    output_text = output.getvalue()
    assert f"=== Ciclistas del {CLUB_NAME} ===" in output_text
    assert f"=== Mejor Ciclista {CLUB_NAME} ===" in output_text
    assert f"=== Resumen Análisis {CLUB_NAME} ===" in output_text

# Tests de tipos
def test_cyclist_performance_type():
    """Test que verifica la estructura del tipo CyclistPerformance."""
    performance: CyclistPerformance = {
        'name': 'Test',
        'time': '05:30:00',
        'position': 1,
        'total_percentage': 25.0
    }
    # Si no hay error de tipo, la estructura es correcta

if __name__ == '__main__':
    pytest.main(['-v', __file__])