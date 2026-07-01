with open("C:\\Users\\Guilherme\\.gemini\\antigravity\\brain\\dfe1eb06-5940-4b05-80d0-b157521e1600\\scratch\\search_result.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "collembola" in line.lower():
        print(f"Line {i}: {line.strip()}")
        # print 5 lines before and after
        start = max(0, i-5)
        end = min(len(lines), i+6)
        print("Context:")
        for j in range(start, end):
            print(f"  {j}: {lines[j].strip()}")
        print("-" * 40)
