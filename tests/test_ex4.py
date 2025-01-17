"""Tests para el módulo de análisis de clubes ciclistas."""

import pytest
import pandas as pd
import io
from contextlib import redirect_stdout

from src.ex4 import (
    clean_club_name,
    process_club_names,
    analyze_club_participation,
    ClubAnalysis
)

# Fixtures
@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba."""
    return pd.DataFrame({
        'biker': ['Ciclista 1', 'Ciclista 2', 'Ciclista 3', 'Ciclista 4'],
        'club': [
            'C.C. Huesca',
            'Club Ciclista Barcelona',
            'Peña Ciclista Madrid',
            'A.D. Valencia'
        ]
    })

@pytest.fixture
def processed_df(sample_df) -> pd.DataFrame:
    """Fixture que proporciona un DataFrame con clubes procesados."""
    df = sample_df.copy()
    df['club_clean'] = df['club'].apply(clean_club_name)
    return df

# Tests para clean_club_name
@pytest.mark.parametrize("input_name,expected", [
    ('C.C. Huesca', 'HUESCA'),
    ('Club Ciclista Barcelona', 'BARCELONA'),
    ('Peña Ciclista Madrid', 'MADRID'),
    ('A.D. Valencia', 'VALENCIA'),
    ('C.D. Zaragoza T.T.', 'ZARAGOZA'),
    ('', 'INDEPENDIENTE'),
    (None, 'INDEPENDIENTE'),
    ('INDEPENDIENTE', 'INDEPENDIENTE'),
])
def test_clean_club_name(input_name: str, expected: str):
    """Test que verifica la limpieza de nombres de clubes."""
    assert clean_club_name(input_name) == expected

def test_clean_club_name_prefixes():
    """Test que verifica la eliminación de prefijos."""
    prefixes = ['C.C.', 'C.D.', 'A.D.', 'A.C.', 'S.C.']
    for prefix in prefixes:
        assert clean_club_name(f"{prefix} Test") == 'TEST'

def test_clean_club_name_suffixes():
    """Test que verifica la eliminación de sufijos."""
    suffixes = ['T.T.', 'C.C.', 'A.D.']
    for suffix in suffixes:
        assert clean_club_name(f"Test {suffix}") == 'TEST'

# Tests para process_club_names
def test_process_club_names_success(sample_df):
    """Test que verifica el procesamiento exitoso de nombres de clubes."""
    result = process_club_names(sample_df)
    
    assert 'club_clean' in result.columns
    assert len(result) == len(sample_df)
    assert all(isinstance(name, str) for name in result['club_clean'])
    assert all(name.isupper() for name in result['club_clean'])

def test_process_club_names_no_data():
    """Test que verifica el manejo de DataFrame vacío."""
    df = pd.DataFrame({'club': []})
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        process_club_names(df)

def test_process_club_names_wrong_columns():
    """Test que verifica el manejo de columnas incorrectas."""
    df = pd.DataFrame({'wrong_col': ['test']})
    with pytest.raises(ValueError):
        process_club_names(df)

# Tests para analyze_club_participation
def test_analyze_club_participation_success(processed_df):
    """Test que verifica el análisis exitoso de participación."""
    result = analyze_club_participation(processed_df)
    
    assert isinstance(result, ClubAnalysis)
    assert result.total_clubs == len(processed_df)
    assert result.unique_clubs > 0
    assert len(result.top_clubs) > 0
    assert all(club.isupper() for club in result.top_clubs)

def test_analyze_club_participation_no_data():
    """Test que verifica el manejo de DataFrame vacío."""
    df = pd.DataFrame({'club_clean': []})
    with pytest.raises(ValueError, match="El DataFrame no puede ser None o estar vacío"):
        analyze_club_participation(df)

def test_analyze_club_participation_wrong_columns():
    """Test que verifica el manejo de columnas incorrectas."""
    df = pd.DataFrame({'wrong_col': ['test']})
    with pytest.raises(ValueError):
        analyze_club_participation(df)

# Test de valores en la salida
def test_tabulate_output_clubs(sample_df):
    """Test que verifica los nombres de clubes en la salida."""
    output = io.StringIO()
    with redirect_stdout(output):
        process_club_names(sample_df)
    
    output_text = output.getvalue()
    # Verificar que los nombres de clubes aparecen en la salida
    assert 'HUESCA' in output_text
    assert 'BARCELONA' in output_text
    assert 'MADRID' in output_text

def test_tabulate_output_analysis(processed_df):
    """Test que verifica el análisis en la salida."""
    output = io.StringIO()
    with redirect_stdout(output):
        analyze_club_participation(processed_df)
    
    output_text = output.getvalue()
    assert "=== Análisis de Participación por Club ===" in output_text
    assert "Total de clubes analizados:" in output_text
    assert "Clubes únicos:" in output_text

# Test de integración
def test_full_process_flow(sample_df):
    """Test que verifica el flujo completo del proceso."""
    processed = process_club_names(sample_df)
    analysis = analyze_club_participation(processed)
    
    assert isinstance(analysis, ClubAnalysis)
    assert len(processed) == len(sample_df)
    assert 'club_clean' in processed.columns
    assert analysis.total_clubs == len(processed)

if __name__ == '__main__':
    pytest.main(['-v', __file__])