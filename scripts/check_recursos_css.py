with open("assets/css/extended/recursos.css", "r", encoding="utf-8") as f:
    text = f.read()

for idx, line in enumerate(text.splitlines()):
    if "modal-preview" in line:
        print(f"Line {idx+1}: {line}")
