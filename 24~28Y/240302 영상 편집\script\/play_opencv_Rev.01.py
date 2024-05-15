import cv2

# 영상 파일 경로
video_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\youtube\전국민이 16강을 기원했지만 아 또 뜨네요! 황선홍의 축구 인생을 바꿔놓은 그 경기! 1994 월드컵 볼리비아전!!.mp4'

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 영상이 열렸는지 확인
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 영상 재생
while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video', frame)

    # 'q'를 누르면 종료
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
