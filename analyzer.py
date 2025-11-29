import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# --- Configuración ---
FILE_PATH = "gastos.csv"
IMG_PATH = "grafico_gastos.png"
PDF_PATH = "reporte_gastos.pdf"

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

def generate_pdf(total_spent, category_expenses):
    """Crea un reporte PDF con los datos y el gráfico."""
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Reporte de Gastos Personales", ln=True, align="C")
    pdf.ln(10) # Salto de línea
    
    # Resumen General
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total Gastado: ${total_spent:,.2f}", ln=True)
    pdf.ln(5)
    
    # Detalle por Categoría
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detalle por Categoría:", ln=True)
    pdf.set_font("Arial", "", 12)
    
    for category, amount in category_expenses.items():
        pdf.cell(0, 10, f"- {category}: ${amount:,.2f}", ln=True)
        
    # Insertar Gráfico (Imagen)
    # x=10, y=None (automático), w=100 (ancho)
    pdf.image(IMG_PATH, x=55, w=100)
    
    # Guardar PDF
    pdf.output(PDF_PATH)
    print(f"📄 Reporte PDF generado exitosamente: '{PDF_PATH}'")

# --- Ejecución ---

if __name__ == "__main__":
    print("🔄 Cargando datos...")
    df = load_data(FILE_PATH)
    
    if df is not None:
        print("✅ Datos cargados.\n")
        
        # Análisis
        total, por_categoria = analyze_data(df)
        
        print(f"💰 Total Gastado: ${total:,.2f}")
        
        # Generar Gráfico
        generate_plot(por_categoria)
        
        # Generar Reporte PDF
        print("\n📝 Creando reporte PDF...")
        generate_pdf(total, por_categoria)