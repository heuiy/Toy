from moviepy.editor import VideoFileClip
import os

# MP4 영상 파일 경로
# source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\2023 LG 트윈스 우승 8초.mp4"
# source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\히스토리\240301 YOLO\LG_smaller_YOLO.mp4"
# source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\히스토리\240301 R-CNN\Shiri_원본_cv01.mp4"
source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\e6ca8e1754ba8a0f0164275e0575ea95.mp4"

# 영상 클립 불러오기
video_clip = VideoFileClip(source_path)

# 재생 속도 조절 (예: 1.5배 빠르게)
# video_clip = video_clip.speedx(factor=1.5)
video_clip = video_clip.speedx(factor=1.0)

# 해상도 줄이기 (예: 원본의 50% 크기)
video_clip = video_clip.resize(0.5)
# video_clip = video_clip.resize(1.0)

# 파일명 추출 (확장자 제외)
file_name = os.path.splitext(os.path.basename(source_path))[0]

# GIF로 저장할 경로와 파일명
output_path = f"D:\\회사_더샵\\BIG\\Toy\\24~28Y\\240302 영상 편집\\gif\\{file_name}.gif"

# GIF로 변환하여 저장 (프레임 속도 조정 가능)
video_clip.write_gif(output_path, fps=10)