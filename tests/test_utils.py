"""Tests para el módulo de utilidades compartidas."""

import pytest
import pandas as pd
import io
from contextlib import redirect_stdout

from src.utils import TableConfig, display_table

# Fixtures
@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba."""
    return pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']
    })

@pytest.fixture
def custom_headers() -> dict[str, str]:
    """Fixture que proporciona headers personalizados."""
    return ['Número', 'Letra']

# Tests para TableConfig
def test_table_config_defaults():
    """Test que verifica los valores por defecto de TableConfig."""
    config = TableConfig()
    assert config.headers == 'keys'
    assert config.table_format == 'pretty'
    assert config.show_index is False
    assert config.num_align == 'right'
    assert config.max_rows is None

def test_table_config_custom():
    """Test que verifica la configuración personalizada de TableConfig."""
    config = TableConfig(
        headers={'a': 'A'},
        table_format='grid',
        show_index=True,
        num_align='center',
        max_rows=5
    )
    assert config.headers == {'a': 'A'}
    assert config.table_format == 'grid'
    assert config.show_index is True
    assert config.num_align == 'center'
    assert config.max_rows == 5

# Tests para display_table
def test_display_table_basic(sample_df):
    """Test que verifica la visualización básica de una tabla."""
    output = io.StringIO()
    with redirect_stdout(output):
        display_table(sample_df, "Test Table")
    
    output_text = output.getvalue()
    assert "Test Table" in output_text
    assert "col1" in output_text
    assert "col2" in output_text
    for val in ['1', '2', '3', 'a', 'b', 'c']:
        assert val in output_text

def test_display_table_custom_config(sample_df, custom_headers):
    """Test que verifica la visualización con configuración personalizada."""
    config = TableConfig(
        headers=custom_headers,
        max_rows=2
    )
    
    output = io.StringIO()
    with redirect_stdout(output):
        display_table(sample_df, "Custom Table", config)
    
    output_text = output.getvalue()
    assert "Custom Table" in output_text
    assert "Número" in output_text
    assert "Letra" in output_text
    # Solo debe mostrar 2 filas
    assert len(output_text.split('\n')) <= 8  # título + headers + 2 filas + líneas de formato

def test_display_table_empty_df():
    """Test que verifica el manejo de DataFrame vacío."""
    empty_df = pd.DataFrame()
    output = io.StringIO()
    with redirect_stdout(output):
        display_table(empty_df, "Empty Table")
    
    output_text = output.getvalue()
    assert "Empty Table" in output_text

if __name__ == '__main__':
    pytest.main(['-v', __file__])