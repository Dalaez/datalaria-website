import shutil
import os

src = r"C:\Users\dalae\.gemini\antigravity\brain\1046490d-4515-4931-bc67-35666eee66f9\cover_obsolescence_chess_1773038521815.png"
dst_es = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\content\es\posts\obs_parte1_intro\cover.png"
dst_en = r"c:\Users\dalae\OneDrive\Emprendiendo\datalaria\content\en\posts\obs_part1_intro\cover.png"

shutil.copy(src, dst_es)
shutil.copy(src, dst_en)

print("Images copied successfully")
