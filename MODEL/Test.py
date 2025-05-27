import fitz

pdf_path = r"C:\Users\User\PycharmProjects\arcai\PDSf\paper1.pdf"
doc = fitz.open(pdf_path)
page = doc[0]

# Highlight a specific text (provide coordinates or search for text)
text = "INTRODUCTION"
areas = page.search_for(text)  # Returns rectangles where the text is found
for area in areas:
    highlight = page.add_highlight_annot(area)

doc.save("highlighted.pdf")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")  # Extract text in natural reading order
        extracted_text += f"--- Page {page_num + 1} ---\n{text}\n"

    doc.close()
    return extracted_text

parsed_text = extract_text_from_pdf(pdf_path)
print(parsed_text)
