"""
Módulo para gestionar el estado y la ejecución secuencial de los ejercicios
del proyecto de análisis de datos de Orbea Monegros 2024.
"""

from typing import Optional, Set
import pandas as pd
from src import ex1, ex2, ex3, ex4, ex5

class ProjectState:
    """
    Clase para mantener el estado de los ejercicios ejecutados y gestionar
    su ejecución secuencial.

    Attributes:
        executed_exercises: Conjunto de ejercicios ya ejecutados
        last_dataframe: Último DataFrame generado
        current_exercise: Ejercicio actualmente en ejecución
    """

    # Descripción de los ejercicios disponibles
    EJERCICIOS = {
        1: "Importación del dataset y EDA (Análisis Exploratorio de Datos)",
        2: "Anonimización de ciclistas y limpieza del dataset",
        3: "Agrupamiento de tiempos de ciclistas e histograma",
        4: "Análisis de clubs ciclistas",
        5: "Análisis específico del Unió Ciclista Sant Cugat (UCSC)"
    }

    def __init__(self) -> None:
        """Inicializa el estado del proyecto."""
        self.executed_exercises: Set[int] = set()
        self.last_dataframe: Optional[pd.DataFrame] = None
        self.current_exercise: Optional[int] = None

    def run_exercise(self, exercise_number: int) -> bool:
        """
        Ejecuta un ejercicio específico de forma secuencial.

        Args:
            exercise_number: Número del ejercicio a ejecutar (1-5)

        Returns:
            True si el ejercicio se ejecutó correctamente, False en caso contrario

        Raises:
            ValueError: Si el número de ejercicio no es válido
        """
        try:
            if exercise_number not in self.EJERCICIOS:
                raise ValueError(f"Ejercicio {exercise_number} no válido")

            # Si es un ejercicio que requiere ejecutar ejercicios previos
            if exercise_number > 1:
                # Guardar el ejercicio actual para evitar recursión infinita
                current_exercise = self.current_exercise
                self.current_exercise = exercise_number

                # Ejecutar ejercicio anterior si no se ha ejecutado
                prev_exercise = exercise_number - 1
                if prev_exercise not in self.executed_exercises:
                    self.run_exercise(prev_exercise)

                # Restaurar el ejercicio actual
                self.current_exercise = current_exercise

            # Imprimir información del ejercicio
            print(f"\n--- EJERCICIO {exercise_number}: {self.EJERCICIOS[exercise_number]} ---")

            # Ejecutar el ejercicio correspondiente
            if exercise_number == 1:
                self.last_dataframe = ex1.main()
            elif exercise_number == 2:
                self.last_dataframe = ex2.main(self.last_dataframe)
            elif exercise_number == 3:
                self.last_dataframe = ex3.main(self.last_dataframe)
            elif exercise_number == 4:
                self.last_dataframe = ex4.main(self.last_dataframe)
            elif exercise_number == 5:
                ex5.main(self.last_dataframe)

            # Marcar el ejercicio como ejecutado
            self.executed_exercises.add(exercise_number)
            return True

        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        except ImportError as e:
            print(f"Error al importar módulo: {e}")
            return False
        except AttributeError as e:
            print(f"Error al acceder a atributo: {e}")
            return False
        except RuntimeError as e:
            print(f"Error de ejecución: {e}")
            return False

    def run_all_exercises(self) -> bool:
        """
        Ejecuta todos los ejercicios secuencialmente.

        Returns:
            True si todos los ejercicios se ejecutaron correctamente,
            False si alguno falló
        """
        self.executed_exercises.clear()
        return all(self.run_exercise(i) for i in range(1, 6))
