import PyPDF2
import io

async def extract(file):
    try:
        content = await file.read()
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF content: {str(e)}")