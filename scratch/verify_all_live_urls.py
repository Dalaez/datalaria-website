import os

OLD_IDS = [
    "957a4ecf-94d1-45f8-9ff7-ea032e8008af",
    "c9ca2aa7-e707-4789-bdb7-1ba191aa0550",
    "d7c65e14-8717-4e37-8750-1065afa66b4b",
    "4544ff60-2426-46c9-8265-7fa4764990af",
    "8031103e-84d4-40bb-b560-9181f4ec31ea",
    "195836b8-7fe4-4c1b-bd48-f40d9a6ebea1",
    "c6eb00f3-1890-4884-be46-3f76c9922737",
    "c6f4ced0-0117-434f-829d-79ecf8263587",
    "d1f06578-2f17-41e5-b277-83f49fe500a4",
    "761e6a35-2e48-4638-a806-47e6e222c656",
    "b3e9d717-f88a-4b27-ad61-af1eaa92459c",
    "1f2082c2-ea7d-4e6c-9b36-151edc23a5fa",
    "3650d76e-bf47-4fde-92ad-fc00189fc321",
    "4acc69c6-e640-43c6-bfc2-1c4d6b037135",
    "78e1e755-cf85-48fa-8698-4aa3db80cfb1",
    "c4e54cc9-e400-4f22-ad15-31e56f61416b",
    "e5b89ce3-f635-4839-9cd3-97a17f56da44",
    "b4ff4e28-d47a-496c-807e-b9672695d34f",
]

base_dir = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria"
found = 0
for root, dirs, files in os.walk(base_dir):
    if ".git" in root or "__pycache__" in root or "scratch" in root:
        continue
    for f in files:
        if f.endswith((".md", ".html")):
            fp = os.path.join(root, f)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                txt = fh.read()
            for oid in OLD_IDS:
                if oid in txt:
                    print(f"FOUND {oid} in {os.path.relpath(fp, base_dir)}")
                    found += 1

if found == 0:
    print("SUCCESS: ALL 17 PRODUCTS 100% CLEAN! ZERO OLD TEST IDS REMAINING!")
else:
    print(f"Total old IDs found: {found}")
