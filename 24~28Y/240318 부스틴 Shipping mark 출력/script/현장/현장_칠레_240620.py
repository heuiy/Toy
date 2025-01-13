# 일단 글자에 rotate 적용하는 것 준비했음
# 내 노트북에서는 rotate 적용해야 하는데
# 부스틴 현장에서는 rotate 적용 불필요함

from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import black, white
import io
import os
from datetime import datetime


def select_pdf_file():
    # download_folder = "D:\\#.Secure Work Folder\\BIG\\Toy\\24~28Y\\240318 부스틴 Shipping mark 출력\\pdf"
    download_folder = "D:\\#.Secure Work Folder\\Shipping Mark\\pdf"
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


def add_watermark_and_address(input_pdf_path, current_document_number, total_documents, skip_address=False):
    fixed_address = "Almirante Pastene 300, Providencia, Santiago, Chile"
    reader = PdfFileReader(input_pdf_path)
    writer = PdfFileWriter()
    total_pages = reader.getNumPages()

    for i in range(total_pages):
        page = reader.getPage(i)
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=landscape(letter))

        # 페이지 회전 설정
        # can.rotate(90)
        # can.translate(0, -landscape(letter)[1])

        # 페이지 번호 추가
        page_number_text = f"{current_document_number + i}                         {total_documents}"
        can.drawString(234, 45, page_number_text)

        # "2477-B" 글자 추가
        can.setFillColor(white)  # 배경색 흰색으로 설정
        can.rect(201, 120, 500, 15, fill=True, stroke=False)
        can.setFillColor(black)  # 글자색 검정으로 설정
        can.drawString(201, 120, "Registered : N° 2477-B")

        if not skip_address:
            # 주소 및 배경색 추가
            can.setFillColor(white)  # 배경색 흰색으로 설정
            can.rect(201, 456, 500, 23, fill=True, stroke=False)
            can.setFillColor(black)  # 글자색 검정으로 설정
            can.drawString(201, 457, fixed_address)

        # 불필요한 부분 가리기
        can.setFillColor(white)
        can.rect(201, 353, 500, 22, fill=True, stroke=False)

        # 가린 부분에 BOOSTIN 글자 추가
        can.setFillColor(black)
        can.drawString(201, 355, "BOOSTIN ADVANCE")

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

        writer = copy_pages(selected_pdf_file, current_batch_copies)
        if writer is None:
            print("PDF 생성에 실패하였습니다.")
            continue

        temp_pdf_file = os.path.join(
            "D:\\#.Secure Work Folder\\Shipping Mark\\temp", "temp.pdf")
        with open(temp_pdf_file, "wb") as temp_pdf:
            writer.write(temp_pdf)

        writer_with_watermark_and_address = add_watermark_and_address(temp_pdf_file, current_document_number,
                                                                      total_documents)
        new_total_pages = writer_with_watermark_and_address.getNumPages()

        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        output_pdf_file = os.path.join("D:\\#.Secure Work Folder\\Shipping Mark\\out",
                                       f"{input_pdf_filename}_{timestamp}_{current_document_number}.pdf")
        with open(output_pdf_file, "wb") as output_pdf:
            writer_with_watermark_and_address.write(output_pdf)

        output_files.append(output_pdf_file)
        current_document_number += new_total_pages

    combined_writer = PdfFileWriter()
    for pdf_file in output_files:
        reader = PdfFileReader(pdf_file)
        for page_num in range(reader.getNumPages()):
            combined_writer.addPage(reader.getPage(page_num))

    combined_pdf_path = os.path.join("D:\\#.Secure Work Folder\\Shipping Mark\\out",
                                     f"combined_{timestamp}.pdf")
    with open(combined_pdf_path, "wb") as combined_pdf:
        combined_writer.write(combined_pdf)

    print(f"통합된 최종 PDF 파일이 저장되었습니다: {combined_pdf_path}")


if __name__ == "__main__":
    main()

 
