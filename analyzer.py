import pandas as pd

# --- Configuración ---
FILE_PATH = "gastos.csv"

def analyze_data():
    try:
        # 1. Cargar el CSV en un DataFrame (una tabla inteligente)
        df = pd.read_csv(FILE_PATH)
        
        # 2. Convertir la columna 'fecha' a objetos de fecha reales
        # Esto es vital para poder ordenar o filtrar por mes/año después
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        print("\n--- RESUMEN DE DATOS ---")
        print(df.info())  # Muestra qué tipo de datos detectó
        
        # 3. Calcular el total gastado
        total_spent = df['monto'].sum()
        print(f"\n💰 Total Gastado: ${total_spent:,.2f}")
        
        # 4. Agrupar gastos por categoría (como una Tabla Dinámica de Excel)
        category_stats = df.groupby('categoria')['monto'].sum().sort_values(ascending=False)
        
        print("\n📊 Gastos por Categoría:")
        print(category_stats)
        
        return df, category_stats

    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo gastos.csv")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    analyze_data()