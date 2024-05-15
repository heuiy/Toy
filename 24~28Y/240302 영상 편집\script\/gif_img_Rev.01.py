from moviepy.editor import ImageSequenceClip
import os

# 이미지가 있는 경로
image_folder = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\img\240109엔도톡신\\'

# 이미지 파일들을 불러오기
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".jpg")]

# 이미지 시퀀스 클립 생성 (fps를 낮추어 이미지 전환 속도 조절)
clip = ImageSequenceClip(images, fps=0.002)
# fps = 0.5 는 2초에 이미지 1장 전환 (빠름)
# fps = 0.25 는 4초에 이미지 1장 전환 (느림)

# GIF 저장할 경로와 파일명 설정
gif_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\gif_img\image_sequence.gif'

# GIF로 저장
clip.write_gif(gif_path)
