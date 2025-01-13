# 부스틴 서식 유형 하나임
# 별도로 서식 선택할 필요 없음
# 주소 추가됨
# 현재까지 Best
# PDF 합하지 않고, 개별 출력했을 때 Best

# 위치 설정 Tip
# 좌,하가 0,0 임

# # 주소 및 배경색 추가
# can.setFillColor(white)  # 배경색 흰색으로 설정
# can.rect(394, 125, 150, 201, fill=True, stroke=False)  # 너비를 150으로 증가
# can.setFillColor(black)  # 글자색 검정으로 설정
# can.drawString(394, 350, address)  # y 좌표를 350으로 변경하여 주소 위치를 위로 이동
# 하지만 좀 더 디테일한 수정 필요함

# rect(x, y, width, height, ...): (x, y)는 사각형의 좌측 하단 모서리의 위치를 나타내고, width와 height는 각각 사각형의 너비와 높이입니다.
# drawString(x, y, string): (x, y)는 문자열이 시작되는 위치입니다.

# Johnson & Johnson: One Johnson & Johnson Plaza, New Brunswick, NJ 08933, USA.
# Pfizer Inc.: 235 East 42nd Street, New York, NY 10017, USA.
# Merck & Co., Inc.: 2000 Galloping Hill Road, Kenilworth, NJ 07033, USA.
# Roche Group: Grenzacherstrasse 124, 4070 Basel, Switzerland.
# AbbVie Inc.: 1 North Waukegan Road, North Chicago, IL 60064, USA.
# Novartis: Lichtstrasse 35, 4056 Basel, Switzerland.
# Bristol-Myers Squibb (BMS): 430 East 29th Street, 14th Floor, New York, NY 10016, USA.
# Sanofi: 54 Rue La Boétie, 75008 Paris, France.
# AstraZeneca: 1 Francis Crick Avenue, Cambridge Biomedical Campus, Cambridge, CB2 0AA, UK.
# GlaxoSmithKline (GSK): 980 Great West Road, Brentford, Middlesex, TW8 9GS, UK.

from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, white
import io
import os
from datetime import datetime

def select_pdf_file():
   download_folder = "D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\pdf"
   pdf_files = [f for f in os.listdir(download_folder) if f.endswith('.pdf')]
   print("사용 가능한 PDF 파일:")
   for idx, file in enumerate(pdf_files):
       print(f"{idx + 1}. {file}")
   choice = int(input("선택할 PDF 파일 번호를 입력하세요: ")) - 1
   return os.path.join(download_folder, pdf_files[choice])

def copy_pages(input_pdf_path, first_copies):
   reader = PdfFileReader(input_pdf_path)
   writer = PdfFileWriter()
   total_pages = reader.getNumPages()

   if total_pages not in [1, 2]:
       print("지원하지 않는 페이지 수입니다. 1페이지 또는 2페이지의 PDF만 지원됩니다.")
       return None

   if total_pages == 2:
       first_copies -= 1

   for _ in range(first_copies):
       writer.addPage(reader.getPage(0))
   if total_pages == 2:
       writer.addPage(reader.getPage(1))

   return writer

def add_watermark_and_address(input_pdf_path, current_document_number, total_documents, address):
   reader = PdfFileReader(input_pdf_path)
   writer = PdfFileWriter()
   total_pages = reader.getNumPages()

   for i in range(total_pages):
       page = reader.getPage(i)
       packet = io.BytesIO()
       can = canvas.Canvas(packet, pagesize=letter)

       # 페이지 번호 추가
       page_number_text = f"{current_document_number + i}                        {total_documents}"
       can.drawString(230, 44, page_number_text)

       # 주소 및 배경색 추가
       can.setFillColor(white)  # 배경색 흰색으로 설정
       # can.rect(200, 500, 600, 30, fill=True, stroke=False)
       can.rect(200, 450, 600, 30, fill=True, stroke=False)
       can.setFillColor(black)  # 글자색 검정으로 설정
       can.drawString(205, 460, address)  # 주소 추가

       can.save()
       packet.seek(0)
       new_pdf = PdfFileReader(packet)
       page.mergePage(new_pdf.getPage(0))
       writer.addPage(page)

   return writer

def select_address():
   addresses = [
       "Johnson & Johnson: One Johnson & Johnson Plaza, New Brunswick, NJ 08933, USA.",
       "Pfizer Inc.: 235 East 42nd Street, New York, NY 10017, USA.",
       "Merck & Co., Inc.: 2000 Galloping Hill Road, Kenilworth, NJ 07033, USA.",
       "Roche Group: Grenzacherstrasse 124, 4070 Basel, Switzerland.",
       "AbbVie Inc.: 1 North Waukegan Road, North Chicago, IL 60064, USA.",
       "Novartis: Lichtstrasse 35, 4056 Basel, Switzerland.",
       "Bristol-Myers Squibb (BMS): 430 East 29th Street, 14th Floor, New York, NY 10016, USA.",
       "Sanofi: 54 Rue La Boétie, 75008 Paris, France.",
       "AstraZeneca: 1 Francis Crick Avenue, Cambridge Biomedical Campus, Cambridge, CB2 0AA, UK.",
       "GlaxoSmithKline (GSK): 980 Great West Road, Brentford, Middlesex, TW8 9GS, UK."
   ]
   print("사용할 주소를 선택하세요:")
   for idx, address in enumerate(addresses):
       print(f"{idx + 1}. {address}")
   choice = int(input("주소 번호를 입력하세요: ")) - 1
   return addresses[choice]

def main():
   total_documents = int(input("전체 문서 번호를 입력하세요 (예: 30): "))
   current_document_number = 1

   while current_document_number <= total_documents:
       remaining_documents = total_documents - current_document_number + 1
       print(f"남은 문서 수: {remaining_documents}")

       current_batch_copies = int(input(f"{current_document_number}부터 시작하는 현재 배치를 몇 장으로 할까요? "))
       if current_batch_copies > remaining_documents:
           print("입력한 배치 페이지 수가 남은 문서 수보다 클 수 없습니다. 다시 시도해주세요.")
           continue

       selected_pdf_file = select_pdf_file()
       input_pdf_filename = os.path.splitext(os.path.basename(selected_pdf_file))[0]
       writer = copy_pages(selected_pdf_file, current_batch_copies)

       if writer is None:
           print("PDF 생성에 실패하였습니다.")
           continue

       selected_address = select_address()

       temp_pdf_file = os.path.join("D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\pdf\\temp", f"temp.pdf")
       with open(temp_pdf_file, "wb") as temp_pdf:
           writer.write(temp_pdf)

       writer_with_watermark_and_address = add_watermark_and_address(temp_pdf_file, current_document_number, total_documents, selected_address)
       new_total_pages = writer_with_watermark_and_address.getNumPages()

       timestamp = datetime.now().strftime("%Y%m%d%H%M")
       output_pdf_file = os.path.join("D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\out",
                                      f"{input_pdf_filename}_{timestamp}_{current_document_number}.pdf")
       with open(output_pdf_file, "wb") as output_pdf:
           writer_with_watermark_and_address.write(output_pdf)

       print(f"주소가 추가된 파일이 저장되었습니다: {output_pdf_file}")

       current_document_number += new_total_pages

   print("모든 문서 번호가 추가되었습니다.")

if __name__ == "__main__":
   main()
