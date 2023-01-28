import requests
import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter


collegiate = 1
shutil.rmtree("pdf_files", ignore_errors=True, onerror=None)
os.makedirs("pdf_files")

while collegiate < 888:
    coll_url = f"{collegiate:03}"
    url = 'http://matricula.ufba.br/{}_alocacao_vagas.pdf'.format(collegiate)
    resp = requests.get(url)
    if resp.status_code == 200:
        print("reading collegiate no {}".format(coll_url))
        with open("pdf_files\\Collegiate_{}.pdf".format(coll_url), "wb") as f:
            f.write(resp.content)

    collegiate += 1