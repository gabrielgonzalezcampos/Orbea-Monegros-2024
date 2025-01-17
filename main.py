#!/usr/bin/env python3
import argparse

# Descripción de los ejercicios
# EJERCICIOS = {
#     1: "Importación del dataset y EDA (Análisis Exploratorio de Datos)",
#     2: "Anonimización de ciclistas y limpieza del dataset",
#     3: "Agrupamiento de tiempos de ciclistas e histograma",
#     4: "Análisis de clubs ciclistas",
#     5: "Análisis específico del Unió Ciclista Sant Cugat (UCSC)"
# }

from src.project_state import ProjectState

def interactive_menu():
    """Muestra un menú interactivo para ejecutar ejercicios."""
    project_state = ProjectState()
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("0. Salir")
        print("1. Ejecutar todos los ejercicios")
        print("2. Ejecutar un ejercicio específico")
        
        try:
            choice = input("Seleccione una opción: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                project_state.run_all_exercises()
            elif choice == '2':
                while True:
                    print("\n--- SELECIÓN DE EJERCICIO ---")
                    print("0. Atrás")
                    for num, desc in project_state.EJERCICIOS.items():
                        print(f"{num}. Ejercicio {num}: {desc}")
                    exercise = input("Seleccione una opción: ").strip()
                    if exercise == '0':
                        break
                    try:
                        ex_num = int(exercise) - 1
                        if 0 <= ex_num < len(project_state.EJERCICIOS):
                            project_state.run_exercise(ex_num + 1)
                        else:
                            print("Número de ejercicio inválido. Debe estar entre 0 y 5.")
                    except ValueError:
                        print("Por favor, introduzca un número válido.")
            else:
                print("Opción no válida. Intente de nuevo.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

def main():
    """Función principal que maneja los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='Análisis de datos de Orbea Monegros 2024')
    parser.add_argument('--exercise', type=int, choices=range(1, 6), 
                        help='Ejecutar un ejercicio específico')
    parser.add_argument('--interactive', action='store_true',
                        help='Abrir menú interactivo para selección de ejercicios')
    
    project_state = ProjectState()
    
    # Procesa los argumentos de línea de comandos
    args = parser.parse_args()
    
    # Si se usa --interactive, entra al menú interactivo
    if args.interactive:
        interactive_menu()
        return
    
    # Si se especifica un ejercicio, lo ejecuta
    if args.exercise:
        project_state.run_exercise(args.exercise)
    # Si no se especifica nada, ejecuta todos los ejercicios por defecto
    else:
        project_state.run_all_exercises()

if __name__ == '__main__':
    main()