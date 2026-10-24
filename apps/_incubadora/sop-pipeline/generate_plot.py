import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración visual "Cyberpunk/Professional"
plt.style.use('dark_background')
sns.set_context("talk") # Texto más grande para lectura en móvil

def generate_impact_chart():
    print("🎨 Generando gráfica de impacto...")
    
    # 1. Cargar Datos Sucios (Simulación de lo que ve el Excel)
    df = pd.read_csv('dirty_sales_sample.csv')
    
    # Conversión forzada para graficar (lo mismo que hace tu clase Hygiene)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    df = df.dropna(subset=['date', 'qty'])
    
    # 2. Configurar el Canvas (2 Paneles)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # --- PANEL 1: LA MENTIRA (Raw Data) ---
    # Mostramos todo, incluidos los errores masivos
    sns.scatterplot(data=df, x='date', y='qty', ax=ax1, 
                    color='#ff5252', s=100, alpha=0.7, label='Datos "Sucios" (Excel)')
    
    ax1.set_title('❌ REALIDAD: Lo que tu ERP exporta (Ruido + Outliers)', 
                  fontsize=16, fontweight='bold', color='#ff5252')
    ax1.set_ylabel('Unidades Vendidas')
    ax1.grid(True, alpha=0.1)
    ax1.legend(loc='upper right')
    
    # Anotación en el outlier (Asumiendo que hay uno gigante)
    max_val = df['qty'].max()
    max_date = df.loc[df['qty'].idxmax(), 'date']
    ax1.annotate(f'¡ERROR! ({int(max_val)} u.)', 
                 xy=(max_date, max_val), xytext=(max_date, max_val),
                 arrowprops=dict(facecolor='white', shrink=0.05))

    # --- PANEL 2: LA VERDAD (Filtered Data) ---
    # Filtramos los outliers masivos para ver la tendencia real
    # Nota: Usamos un corte simple visual aquí, tu script usa Z-Score matemático
    visual_filter = df[df['qty'] < df['qty'].quantile(0.95)]
    
    sns.lineplot(data=visual_filter, x='date', y='qty', ax=ax2, 
                 color='#00e676', linewidth=3, label='Tendencia Real')
    sns.scatterplot(data=visual_filter, x='date', y='qty', ax=ax2, 
                    color='#00e676', s=50, alpha=0.6)
    
    ax2.set_title('✅ INGENIERÍA: Señal limpia para predicción (S&OP Ready)', 
                  fontsize=16, fontweight='bold', color='#00e676')
    ax2.set_ylabel('Unidades Vendidas')
    ax2.set_xlabel('Fecha de Transacción')
    ax2.grid(True, alpha=0.1)
    
    # Título General
    plt.suptitle('IMPACTO DE LA HIGIENE DE DATOS EN S&OP', 
                 fontsize=22, y=0.98, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('sop_impact_chart.png', dpi=300)
    print("📸 Gráfica guardada: sop_impact_chart.png")

if __name__ == "__main__":
    generate_impact_chart()