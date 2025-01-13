# 제품명 가리기!!! 추가, 버전 1

# (배치번호 / 연도) 추가
# 주소 설정 생략, 브라질 고정
# 현재까지 Best

# 위치 설정 Tip1
# 좌,하가 0,0 임

# # 주소 및 배경색 추가
# can.setFillColor(white)  # 배경색 흰색으로 설정
# can.rect(394, 125, 150, 201, fill=True, stroke=False)  # 너비를 150으로 증가
# can.setFillColor(black)  # 글자색 검정으로 설정
# can.drawString(394, 350, address)  # y 좌표를 350으로 변경하여 주소 위치를 위로 이동
# 하지만 좀 더 디테일한 수정 필요함

# rect(x, y, width, height, ...): (x, y)는 사각형의 좌측 하단 모서리의 위치를 나타내고, width와 height는 각각 사각형의 너비와 높이입니다.
# drawString(x, y, string): (x, y)는 문자열이 시작되는 위치입니다.

# Merck Sharp & Dohme Saúde Animal Ltda. Vinhedo - SP - Brazil 브라질
# RUC: 20109333159 AV. DE LAS ARTES NORTE NRO. 310, SAN BORJA, LIMA - PERU 페루
# ALLMED FZCO.   P.O. BOX No. 261257 JAFZA, Dubai, U.A.E. 우즈벡
# SMARK FZE JEBAL ALI JAFZA SOUTH LIU10, BD 06, P.O. Box 18076, DUBAI, UAE 오만
# ZALAND SARSABZ LTD.  1st floor, Kabul Plaza Jadai Maiwand closed to kochi Barana, Kabul Afghanistan 아프간
# Av. San Jerónimo #369, Col. La Otra, Del. Alvaro Obregón, C.P 01090, Ciudad de México, México 멕시코
# 남아공, 케냐는 MDM 주소 와 실수령지 주소 동일

from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, white
import io
import os
from datetime import datetime

def select_pdf_file():
  download_folder = "D:\\#.Secure Work Folder\\Shipping Mark\\pdf"
#  download_folder = "D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\pdf"
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

def add_watermark_and_address(input_pdf_path, current_document_number, total_documents, batch_number, skip_address=False):
#   fixed_address = "LG Chem, Ltd."
   fixed_address = "SAO PAULO - BRAZIL RUAEDGAR MARCHIORI, 255"             # 240530 주소 수정함!!!!
   reader = PdfFileReader(input_pdf_path)
   writer = PdfFileWriter()
   total_pages = reader.getNumPages()

   for i in range(total_pages):
       page = reader.getPage(i)
       packet = io.BytesIO()
       can = canvas.Canvas(packet, pagesize=letter)

       # 페이지 번호 추가
       page_number_text = f"{current_document_number + i}                        {total_documents}"
#       can.drawString(230, 44, page_number_text)
#       can.drawString(238, 50, page_number_text)
#       can.drawString(238, 51, page_number_text)
       can.drawString(238, 45, page_number_text)                     # 240530 페이지 번호 위치 수정

       # 배치 번호 추가
       batch_number_text = f"(  {batch_number}  )"
#       can.drawString(276, 293, batch_number_text)  # 배치 번호 위치 (250, 200)
#       can.drawString(286, 290, batch_number_text)  # 배치 번호 위치 (250, 200)
#       can.drawString(286, 284, batch_number_text)  # 배치 번호 위치 (250, 200)
       can.drawString(286, 289, batch_number_text)  # 배치 번호 위치 (250, 200)   # 240530 배치 삽입 위치 수정

       if not skip_address:
           # 주소 및 배경색 추가
           can.setFillColor(white)  # 배경색 흰색으로 설정
#           can.rect(200, 450, 600, 30, fill=True, stroke=False)
#           can.rect(218, 409, 500, 15, fill=True, stroke=False)
           can.rect(201, 458, 500, 15, fill=True, stroke=False)     # 240530 흰색 배경 위치 수정
           can.setFillColor(black)  # 글자색 검정으로 설정
#           can.drawString(205, 460, fixed_address)  # 주소 추가
#           can.drawString(218, 409, fixed_address)  # 주소 추가
           can.drawString(201, 458, fixed_address)                # 240530 주소 위치 수정

       can.save()
       packet.seek(0)
       new_pdf = PdfFileReader(packet)
       page.mergePage(new_pdf.getPage(0))
       writer.addPage(page)

   return writer

def main():
   total_documents = int(input("전체 박스 개수를 입력하세요 (예: 30): "))
   current_document_number = 1
   output_files = []

   while current_document_number <= total_documents:
       remaining_documents = total_documents - current_document_number + 1
       print(f"남은 박스 수: {remaining_documents}")

       current_batch_copies = int(input(f"{current_document_number}부터 시작하는 현재 배치를 몇 장으로 할까요? "))
       if current_batch_copies > remaining_documents:
           print("입력한 박스 수가 남은 박스 수량보다 많을 수 없습니다. 다시 입력해주세요.")
           continue

       selected_pdf_file = select_pdf_file()
       input_pdf_filename = os.path.splitext(os.path.basename(selected_pdf_file))[0]

       # 사용자로부터 배치 번호를 입력받습니다.
       batch_number = input("이 PDF 파일에 삽입할 배치 번호와 연도를 입력하세요: ")

       writer = copy_pages(selected_pdf_file, current_batch_copies)
       if writer is None:
           print("PDF 생성에 실패하였습니다.")
           continue

       temp_pdf_file = os.path.join("D:\\#.Secure Work Folder\\Shipping Mark\\temp", "temp.pdf")
#       temp_pdf_file = os.path.join("D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\pdf\\temp", "temp.pdf")
       with open(temp_pdf_file, "wb") as temp_pdf:
           writer.write(temp_pdf)

       writer_with_watermark_and_address = add_watermark_and_address(temp_pdf_file, current_document_number, total_documents, batch_number)
       new_total_pages = writer_with_watermark_and_address.getNumPages()

       timestamp = datetime.now().strftime("%Y%m%d%H%M")
#       output_pdf_file = os.path.join("D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\out", f"{input_pdf_filename}_{timestamp}_{current_document_number}.pdf")
       output_pdf_file = os.path.join("D:\\#.Secure Work Folder\\Shipping Mark\\out", f"{input_pdf_filename}_{timestamp}_{current_document_number}.pdf")
       with open(output_pdf_file, "wb") as output_pdf:
           writer_with_watermark_and_address.write(output_pdf)

       output_files.append(output_pdf_file)
       current_document_number += new_total_pages

   combined_writer = PdfFileWriter()
   for pdf_file in output_files:
       reader = PdfFileReader(pdf_file)
       for page_num in range(reader.getNumPages()):
           combined_writer.addPage(reader.getPage(page_num))

#   combined_pdf_path = os.path.join("D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\out", f"combined_{timestamp}.pdf")
   combined_pdf_path = os.path.join("D:\\#.Secure Work Folder\\Shipping Mark\\out", f"combined_{timestamp}.pdf")
   with open(combined_pdf_path, "wb") as combined_pdf:
       combined_writer.write(combined_pdf)

   print(f"통합된 최종 PDF 파일이 저장되었습니다: {combined_pdf_path}")

if __name__ == "__main__":
   main()

 
