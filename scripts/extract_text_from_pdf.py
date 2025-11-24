import os
from langchain_community.document_loaders import PyPDFLoader

input_folder = "data/textbook_pdfs"
output_folder = "data/combined_text"

os.makedirs(output_folder, exist_ok=True)

for pdf_file in os.listdir(input_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(input_folder, pdf_file)
        print("Extracting:", pdf_path)

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        full_text = "\n\n".join([d.page_content for d in docs])

        out_name = pdf_file.replace(".pdf", ".txt")
        out_path = os.path.join(output_folder, out_name)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)

print("✅ All PDFs extracted to data/combined_text/")
