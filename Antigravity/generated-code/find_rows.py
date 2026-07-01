from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_tr = False
        self.in_cell = False
        self.current_table = None
        self.current_row = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table" and attrs_dict.get("id") == "row":
            self.in_table = True
            self.current_table = []
            self.tables.append(self.current_table)
        elif tag == "tr" and self.in_table:
            self.in_tr = True
            self.current_row = []
            self.current_table.append(self.current_row)
        elif tag in ("td", "th") and self.in_tr:
            self.in_cell = True
            self.cell_data = ""

    def handle_data(self, data):
        if self.in_cell:
            self.cell_data += data

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif tag == "tr" and self.in_table:
            self.in_tr = False
        elif tag in ("td", "th") and self.in_tr:
            self.in_cell = False
            self.current_row.append(self.cell_data.strip())

with open("C:\\Users\\Guilherme\\.gemini\\antigravity\\brain\\dfe1eb06-5940-4b05-80d0-b157521e1600\\scratch\\search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

parser = TableParser()
parser.feed(html)

print("Rows in table 'row':", len(parser.tables[0]))
for i, row in enumerate(parser.tables[0]):
    row_str = " ".join([f.strip() for f in row if f.strip()])
    if any(k in row_str.lower() for k in ["collembola", "springtail", "podura", "isotomidae"]):
        print(f"Row {i}: {row_str}")
