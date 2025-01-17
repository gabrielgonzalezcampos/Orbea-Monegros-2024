"""Tests para el módulo de gestión del estado del proyecto."""

import pytest
import pandas as pd
import io
from unittest.mock import patch, MagicMock
from contextlib import redirect_stdout

from src.project_state import ProjectState

# Fixtures
@pytest.fixture
def project() -> ProjectState:
    """Fixture que proporciona una instancia limpia de ProjectState."""
    return ProjectState()

@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Fixture que proporciona un DataFrame de prueba."""
    return pd.DataFrame({'test': [1, 2, 3]})

# Mock de los módulos de ejercicios
@pytest.fixture
def mock_exercises():
    """Fixture que proporciona mocks para todos los módulos de ejercicios."""
    with patch('src.project_state.ex1') as mock_ex1, \
         patch('src.project_state.ex2') as mock_ex2, \
         patch('src.project_state.ex3') as mock_ex3, \
         patch('src.project_state.ex4') as mock_ex4, \
         patch('src.project_state.ex5') as mock_ex5:
        
        # Configurar los mocks para devolver un DataFrame
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_ex1.main.return_value = mock_df
        mock_ex2.main.return_value = mock_df
        mock_ex3.main.return_value = mock_df
        mock_ex4.main.return_value = mock_df
        mock_ex5.main.return_value = None
        
        yield {
            'ex1': mock_ex1,
            'ex2': mock_ex2,
            'ex3': mock_ex3,
            'ex4': mock_ex4,
            'ex5': mock_ex5
        }

# Tests de inicialización
def test_init(project):
    """Test que verifica la inicialización correcta de ProjectState."""
    assert project.executed_exercises == set()
    assert project.last_dataframe is None
    assert project.current_exercise is None
    assert isinstance(project.EJERCICIOS, dict)
    assert len(project.EJERCICIOS) == 5

# Tests de run_exercise
def test_run_exercise_invalid_number(project):
    """Test que verifica el manejo de números de ejercicio inválidos."""
    output = io.StringIO()
    with redirect_stdout(output):
        result = project.run_exercise(0)
    
    assert result is False
    assert "Error de validación" in output.getvalue()

def test_run_exercise_valid(project, mock_exercises):
    """Test que verifica la ejecución exitosa de un ejercicio."""
    output = io.StringIO()
    with redirect_stdout(output):
        result = project.run_exercise(1)
    
    assert result is True
    assert 1 in project.executed_exercises
    assert project.last_dataframe is not None
    assert "EJERCICIO 1" in output.getvalue()
    mock_exercises['ex1'].main.assert_called_once()

def test_run_exercise_sequential(project, mock_exercises):
    """Test que verifica la ejecución secuencial de ejercicios."""
    # Ejecutar ejercicio 3 debería ejecutar 1 y 2 primero
    output = io.StringIO()
    with redirect_stdout(output):
        result = project.run_exercise(3)
    
    assert result is True
    assert project.executed_exercises == {1, 2, 3}
    assert "EJERCICIO 1" in output.getvalue()
    assert "EJERCICIO 2" in output.getvalue()
    assert "EJERCICIO 3" in output.getvalue()
    
    mock_exercises['ex1'].main.assert_called_once()
    mock_exercises['ex2'].main.assert_called_once()
    mock_exercises['ex3'].main.assert_called_once()

def test_run_exercise_error_handling(project):
    """Test que verifica el manejo de errores en la ejecución."""
    with patch('src.project_state.ex1') as mock_ex1:
        mock_ex1.main.side_effect = RuntimeError("Test error")
        
        output = io.StringIO()
        with redirect_stdout(output):
            result = project.run_exercise(1)
        
        assert result is False
        assert "Error de ejecución" in output.getvalue()
        assert 1 not in project.executed_exercises

# Tests de run_all_exercises
def test_run_all_exercises_success(project, mock_exercises):
    """Test que verifica la ejecución exitosa de todos los ejercicios."""
    output = io.StringIO()
    with redirect_stdout(output):
        result = project.run_all_exercises()
    
    assert result is True
    assert project.executed_exercises == {1, 2, 3, 4, 5}
    assert project.last_dataframe is not None
    
    # Verificar que todos los ejercicios fueron llamados
    for mock in mock_exercises.values():
        mock.main.assert_called_once()

def test_run_all_exercises_with_error(project, mock_exercises):
    """Test que verifica el manejo de errores al ejecutar todos los ejercicios."""
    mock_exercises['ex3'].main.side_effect = RuntimeError("Test error")
    
    output = io.StringIO()
    with redirect_stdout(output):
        result = project.run_all_exercises()
    
    assert result is False
    assert 3 not in project.executed_exercises
    assert "Error de ejecución" in output.getvalue()

# Test de caso de uso completo
def test_full_workflow(project, mock_exercises):
    """Test que verifica un flujo de trabajo completo."""
    # Ejecutar algunos ejercicios individualmente
    project.run_exercise(1)
    project.run_exercise(3)
    
    assert project.executed_exercises == {1, 2, 3}
    
    # Limpiar y ejecutar todos
    output = io.StringIO()
    with redirect_stdout(output):
        result = project.run_all_exercises()
    
    assert result is True
    assert project.executed_exercises == {1, 2, 3, 4, 5}
    output_text = output.getvalue()
    for i in range(1, 6):
        assert f"EJERCICIO {i}" in output_text

if __name__ == '__main__':
    pytest.main(['-v', __file__])