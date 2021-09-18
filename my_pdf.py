from fpdf import FPDF

class myPdf(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_font("Times", size = 20)
    def add_title(self, title):
        self.set_font("Times", size = 40)
        self.cell(200, 10, txt = title, ln = 1, align = 'C')
        self.cell(200, 10, txt = "", ln = 1, align = 'C')
    def add_words(self, words):
        txt = words[0] + " = " + words[1]
        self.set_font("Times", size = 20)
        self.cell(200, 10, txt = txt, ln = 1, align = 'C')