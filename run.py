import PyPDF2
import openai
import re
import requests
from io import BytesIO

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print("Failed to download the PDF. Please check the URL.")
        return None

def extract_text(pdf_stream):
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def chunk_text( text) -> str:
    section_keywords = [
        "Introduction",
        "Background",
        "Related Work",
        "Method",
        "Methodology",
        "Approach",
        "Algorithm",
        "Implementation",
        "Experiment",
        "Evaluation",
        "Results",
        "Discussion",
        "Conclusion",
        "Future Work",
    ]
    section_pattern = re.compile(
        r"\b(?:{})\b".format("|".join(re.escape(kw) for kw in section_keywords)),
        re.IGNORECASE,
    )
    # Split the text into sections
    sections = []
    current_section = []
    for line in text.splitlines():
        if section_pattern.search(line):
            if current_section:
                sections.append("\n".join(current_section))
                current_section = []
        current_section.append(line)
    if current_section:
        sections.append("\n".join(current_section))
    return sections

class OpenAIAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def analyze_paper(self, text) -> str:
        prompt = f"Understand the following research paper and provide a summary of the main concepts and algorithms, and how they can be implemented in Python:\n{text}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text

    def generate_code(self, summary) -> str:
        prompt = f"Based on the following summary of a research paper, generate Python code snippets implementing the main concepts and algorithms:\n{summary}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text
    
    def organize_code():
        pass



""" def main(pdf_path, openai_api_key):
    #extract and clean text from PDF

    response = requests.get(pdf_path)

    if response.status_code == 200:
        pdf_data = BytesIO(response.content)
        pdf_reader = PDFReader(pdf_data)
        chunks = PDFReader.chunk_text(pdf_data)


    pdf_reader = PDFReader(pdf_path)
    raw_text = pdf_reader.extract_text()
    chunks = PDFReader.chunk_text(cleaned_text)
    cleaned_text = PDFReader.clean_text(raw_text)
    

    #analyze paper and generate code snippets
    openai_analyzer = OpenAIAnalyzer(openai_api_key)
    summary = openai_analyzer.analyze_paper(cleaned_text)
    code_snippets = openai_analyzer.generate_code(summary)

    print("Summary of the paper:")
    print(summary)
    print("\nPython code snippets:")
    print(code_snippets)
 """
def main():
    url = input("Enter the PDF URL: ")
    pdf_stream = download_pdf(url)
    if pdf_stream:
        text = extract_text(pdf_stream)
        chunk_text_t = chunk_text(text)
        print("Extracted text from the PDF:")
        print(text)
    else:
        print("Could not extract text from the PDF.")

if __name__ == "__main__":
    main()
