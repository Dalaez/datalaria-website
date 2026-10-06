from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

doc = SimpleDocTemplate("scratch/test_output.pdf")
styles = getSampleStyleSheet()

formula_style = ParagraphStyle(
    'Formula',
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#0F172A"),
)

text_es = (
    "<b>FCF<sub>t</sub> = EBIT<sub>t</sub> · (1 - t) + D&amp;A<sub>t</sub> - CAPEX<sub>t</sub> - &Delta;NWC<sub>t</sub></b><br/>"
    "<font size='7.5' color='#475569'>Donde: NOPAT = EBIT·(1-t); &Delta;NWC = NWC<sub>t</sub> - NWC<sub>t-1</sub></font>"
)

p = Paragraph(text_es, formula_style)
doc.build([p])
print("Built successfully!")
