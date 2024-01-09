import PyPDF2
import requests
from docx import Document
from rest_framework.views import APIView
from rest_framework.response import Response


class PdfView(APIView):

    def read_pdf(self, pdf_url):
        # Download the PDF content
        response = requests.get(pdf_url)
        response.raise_for_status()

        with open('file/pdf/downloaded_resume.pdf', 'wb') as pdf_file:
            pdf_file.write(response.content)

        # Open the downloaded PDF file
        with open('file/pdf/downloaded_resume.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages

            data = ""
            for page_number in range(num_pages):
                page = pdf_reader.getPage(page_number)
                text = page.extractText()
                data = data + text

        return data


    def read_doc(self, docx_url):
        response = requests.get(docx_url)
        response.raise_for_status()

        # Save the downloaded DOCX content to a local file
        with open('file/docs/downloaded_document.docx', 'wb') as docx_file:
            docx_file.write(response.content)

        # Read the content of the local DOCX file
        doc = Document('file/docs/downloaded_document.docx')

        content = []
        # Read paragraphs
        for paragraph in doc.paragraphs:
            content.append(paragraph.text)

        # Read tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    content.append(cell.text)

        return '\n'.join(content)


    def post(self, request):
        url = request.data.get('url', None)
        file_type = request.data.get('file_type', None)
        if file_type == "pdf":
            data = self.read_pdf(url)
            return Response({"data":data})
        elif file_type == "docx":
            data = self.read_doc(url)
            return Response({"data":data})