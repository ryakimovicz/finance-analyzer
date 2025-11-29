import pandas as pd
import matplotlib.pyplot as plt

# --- Configuración ---
FILE_PATH = "gastos.csv"
IMG_PATH = "grafico_gastos.png"

# --- Lógica de Análisis ---

def load_data(file_name):
    """Carga el CSV y convierte tipos de datos."""
    try:
        df = pd.read_csv(file_name)
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{file_name}' no existe.")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def analyze_data(df):
    """Calcula totales y agrupamientos."""
    total_spent = df['monto'].sum()
    category_expenses = df.groupby('categoria')['monto'].sum()
    
    return total_spent, category_expenses

def generate_plot(category_expenses):
    """Genera y guarda un gráfico de torta."""
    plt.figure(figsize=(8, 6))
    
    # Crear gráfico de torta
    plt.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
    plt.title('Distribución de Gastos por Categoría')
    
    # Guardar imagen
    plt.savefig(IMG_PATH)
    plt.close()
    print(f"📊 Gráfico guardado exitosamente como '{IMG_PATH}'")

# --- Ejecución ---

if __name__ == "__main__":
    print("🔄 Cargando datos...")
    df = load_data(FILE_PATH)
    
    if df is not None:
        print("✅ Datos cargados.\n")
        
        # Análisis
        total, por_categoria = analyze_data(df)
        
        print(f"💰 Total Gastado: ${total:,.2f}")
        print("\n📊 Gastos por Categoría:")
        print(por_categoria)
        
        # Generar Gráfico
        print("\n🎨 Generando gráfico...")
        generate_plot(por_categoria)