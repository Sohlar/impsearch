import PyPDF2
import openai
import re


class PDFReader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(reader.numPages):
                text += reader.getPage(page_num).extractText()
        return text

    @staticmethod
    def clean_text(text):
        cleaned_text = re.sub(r"[^a-zA-Z0-9.,;:\(\)\[\]\{\}\-\+=\*/ ]", "", text)
        return cleaned_text
    
    def chunk_text(self, text):
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

    def analyze_paper(self, text):
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

    def generate_code(self, summary):
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

def main(pdf_path, openai_api_key):
    #extract and clean text from PDF
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

if __name__ == "__main__":
    pdf_path = "path/to/your/research_paper.pdf"
    openai_api_key = "your_openai_api_key"
    main(pdf_path, openai_api_key)
