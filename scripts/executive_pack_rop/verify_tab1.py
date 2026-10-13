import openpyxl
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def verify_file(lang, path):
    print(f"\n==========================================")
    print(f"VERIFICANDO: {lang} -> {path}")
    print(f"==========================================")
    wb = openpyxl.load_workbook(path, data_only=False)
    
    t1_name = "Dashboard Ejecutivo" if lang == "ES" else "Executive Dashboard"
    t2_name = "Matriz SKU & Datos Operativos" if lang == "ES" else "SKU Matrix & Operational Inputs"
    
    ws1 = wb[t1_name]
    ws2 = wb[t2_name]
    
    print("--- TAB 1: PARAMETER SCORECARD ---")
    j10 = ws1['J10']
    print(f"  J10 (SKU Selector): value='{j10.value}', locked={j10.protection.locked}, fill={j10.fill.fgColor.rgb}")
    l10 = ws1['L10']
    print(f"  L10 (Description): formula='{l10.value}', locked={l10.protection.locked}")
    j13 = ws1['J13']
    print(f"  J13 (ROP Scorecard): formula='{j13.value}', locked={j13.protection.locked}")
    k13 = ws1['K13']
    print(f"  K13 (SS Scorecard): formula='{k13.value}', locked={k13.protection.locked}")
    
    print("\n--- TAB 1: HEADERS ROW 15 ---")
    for col in ['I', 'J', 'K', 'L', 'M']:
        c = ws1[f"{col}15"]
        w = ws1.column_dimensions[col].width
        print(f"  Col {col} (width {w}): '{c.value}' | wrap={c.alignment.wrap_text} | bg={c.fill.fgColor.rgb} | font_color={c.font.color.rgb if c.font and c.font.color else 'N/A'}")
        
    print("\n--- TAB 1: SIMULATION ROWS 16-20 ---")
    for r in range(16, 21):
        day = ws1[f"I{r}"].value
        inv = ws1[f"J{r}"].value
        rop = ws1[f"K{r}"].value
        ss = ws1[f"L{r}"].value
        stat = ws1[f"M{r}"].value
        print(f"  Row {r}: Day={day} | Inv={inv} | ROP={rop} | SS={ss} | Stat={stat[:35]}...")
        
    print("\n--- TAB 2: EDITABLE INPUT CELLS ---")
    c11 = ws2['C11']
    print(f"  C11 (SKU Description): value='{c11.value}', locked={c11.protection.locked}, fill={c11.fill.fgColor.rgb}")
    e11 = ws2['E11']
    print(f"  E11 (Daily Demand): value='{e11.value}', locked={e11.protection.locked}, fill={e11.fill.fgColor.rgb}")

verify_file("ES", "packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[ES]_Stock_Seguridad_ROP/Calculadora_Stock_Seguridad_ROP_ES.xlsx")
verify_file("EN", "packages/Suite_03_Control_Operativo/05_Stock_Seguridad_ROP/[EN]_Safety_Stock_ROP/Safety_Stock_ROP_Calculator_EN.xlsx")
print("\nVerificación completada.")
