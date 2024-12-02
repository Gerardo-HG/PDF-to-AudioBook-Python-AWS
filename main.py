import boto3
import os
from pdfminer.high_level import extract_pages, extract_text
from pypdf import PdfReader
from dotenv import load_dotenv
import time

load_dotenv()

ACCESS_KEY = os.getenv('AWS_AK')
SECRET_ACCESS_KEY = os.getenv('AWS_SAK')

polly_client = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_ACCESS_KEY,region_name='us-west-2').client("polly")

def converter_to_audiobook(pdf_file):
    content = read_pdf(pdf_file)
    for page in range(len(content)):
        text_with_ssml = f"<speak><prosody rate='80%'>{content[page][0]}</prosody></speak>"
        response = polly_client.synthesize_speech(
            VoiceId="Joanna",
            OutputFormat='mp3',
            Text=text_with_ssml,
            Engine="neural"
        )
        with open(f"audios/speech_page_{page}.mp3",'wb') as file:
            file.write(response['AudioStream'].read())
            time.sleep(1)

def read_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    all_document = []
    for i in range(reader.get_num_pages()):
        page = reader.pages[i]
        elements_in_page = [page.extract_text()]
        all_document.append(elements_in_page)
    return all_document

converter_to_audiobook("sample_pdf.pdf")