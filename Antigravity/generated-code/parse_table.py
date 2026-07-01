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
        self.table_attrs = []
        self.cell_data = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table":
            self.in_table = True
            self.current_table = []
            self.tables.append(self.current_table)
            self.table_attrs.append(attrs_dict)
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
            self.current_table = None
        elif tag == "tr" and self.in_table:
            self.in_tr = False
        elif tag in ("td", "th") and self.in_tr:
            self.in_cell = False
            self.current_row.append(self.cell_data.strip())

with open("C:\\Users\\Guilherme\\.gemini\\antigravity\\brain\\dfe1eb06-5940-4b05-80d0-b157521e1600\\scratch\\search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

parser = TableParser()
parser.feed(html)

print(f"Found {len(parser.tables)} tables")
for idx, table in enumerate(parser.tables):
    attrs = parser.table_attrs[idx]
    print(f"\nTable {idx}: id={attrs.get('id')}, class={attrs.get('class')}")
    print(f"  Rows count: {len(table)}")
    for r_idx, row in enumerate(table[:20]):
        # clean row fields
        clean_row = [field.replace('\n', ' ').strip() for field in row if field.strip()]
        if clean_row:
            print(f"    Row {r_idx}: {clean_row}")
