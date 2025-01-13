# QR 코드 이미지 추가
# 예시 코드임 
# 실제로는 수정해야함

from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, white
import io
import os
from datetime import datetime

def select_pdf_file():
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

    # 첫 페이지만 여러 장 복사
    if total_pages == 2:
        # 2페이지짜리인 경우, 첫 번째 페이지를 복사할 횟수는 입력받은 수 - 1
        first_copies -= 1

    for _ in range(first_copies):
        writer.addPage(reader.getPage(0))

    # 2페이지짜리인 경우 두 번째 페이지 추가
    if total_pages == 2:
        writer.addPage(reader.getPage(1))

    return writer

def add_watermark_and_address(input_pdf_path,
                              current_document_number,
                              total_documents,
                              batch_number,
                              skip_address=False,
                              qr_image_path=None):
    """
    input_pdf_path: PDF 파일 경로
    current_document_number: 현재 문서(박스) 번호
    total_documents: 전체 문서(박스) 수
    batch_number: 배치 번호(사용자 입력)
    skip_address: 주소 추가를 스킵할지 여부(False일 때 주소 추가)
    qr_image_path: QR 코드 이미지 경로(문자열)
    """
    fixed_address = "SAO PAULO - BRAZIL RUAEDGAR MARCHIORI, 255"
    reader = PdfFileReader(input_pdf_path)
    writer = PdfFileWriter()
    total_pages = reader.getNumPages()

    for i in range(total_pages):
        page = reader.getPage(i)
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # ---------------------------
        # 1) 페이지 번호 추가
        # ---------------------------
        page_number_text = f"{current_document_number + i}                        {total_documents}"
        can.drawString(238, 45, page_number_text)

        # ---------------------------
        # 2) 배치 번호 추가
        # ---------------------------
        batch_number_text = f"(  {batch_number}  )"
        can.drawString(286, 289, batch_number_text)

        # ---------------------------
        # 3) 주소 추가 (skip_address가 False일 때만)
        # ---------------------------
        if not skip_address:
            can.setFillColor(white)  # 배경색 흰색
            can.rect(201, 458, 500, 15, fill=True, stroke=False)
            can.setFillColor(black)  # 글자색 검정
            can.drawString(201, 458, fixed_address)

        # ---------------------------
        # 4) 불필요한 부분 가리기 & BOOSTIN 텍스트 추가
        # ---------------------------
        can.setFillColor(white)
        can.rect(266, 353, 500, 15, fill=True, stroke=False)

        can.setFillColor(black)
        can.drawString(266, 353, "BOOSTIN")

        # ---------------------------
        # 5) QR 코드 추가
        # ---------------------------
        if qr_image_path and os.path.exists(qr_image_path):
            # 테스트를 위해 임의의 위치, 크기로 설정했습니다.
            # 필요에 따라 x, y, width, height를 조절해주세요.
            x_position = 50   # 좌측에서 50pt
            y_position = 500  # 하단에서 500pt
            qr_width = 80     # QR 코드 폭
            qr_height = 80    # QR 코드 높이

            can.drawImage(qr_image_path,
                          x_position,
                          y_position,
                          width=qr_width,
                          height=qr_height,
                          preserveAspectRatio=True,
                          mask='auto')

        # ---------------------------
        # PDF 페이지 머지
        # ---------------------------
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

    # QR 코드 이미지 경로 (PC 내에 실제 QR 코드 파일이 위치한 경로로 변경하세요)
    qr_image_path = "D:\\#.Secure Work Folder\\Shipping Mark\\qr\\qrcode.png"

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
        with open(temp_pdf_file, "wb") as temp_pdf:
            writer.write(temp_pdf)

        # QR 코드 포함 워터마크(주소, BOOSTIN 등) 삽입
        writer_with_watermark_and_address = add_watermark_and_address(
            temp_pdf_file,
            current_document_number,
            total_documents,
            batch_number,
            skip_address=False,
            qr_image_path=qr_image_path
        )

        new_total_pages = writer_with_watermark_and_address.getNumPages()

        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        output_pdf_file = os.path.join(
            "D:\\#.Secure Work Folder\\Shipping Mark\\out",
            f"{input_pdf_filename}_{timestamp}_{current_document_number}.pdf"
        )
        with open(output_pdf_file, "wb") as output_pdf:
            writer_with_watermark_and_address.write(output_pdf)

        output_files.append(output_pdf_file)
        current_document_number += new_total_pages

    # 모든 PDF 파일을 합쳐서 최종 PDF 생성
    combined_writer = PdfFileWriter()
    for pdf_file in output_files:
        reader = PdfFileReader(pdf_file)
        for page_num in range(reader.getNumPages()):
            combined_writer.addPage(reader.getPage(page_num))

    # 통합 PDF 저장
    # 가장 마지막 반복의 timestamp를 사용하거나, 여기서 다시 현재 시간으로 생성하셔도 됩니다.
    combined_pdf_path = os.path.join(
        "D:\\#.Secure Work Folder\\Shipping Mark\\out",
        f"combined_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
    )
    with open(combined_pdf_path, "wb") as combined_pdf:
        combined_writer.write(combined_pdf)

    print(f"통합된 최종 PDF 파일이 저장되었습니다: {combined_pdf_path}")

if __name__ == "__main__":
    main()
