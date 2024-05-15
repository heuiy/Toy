from moviepy.editor import VideoFileClip
import os

# 영상 파일 경로
# source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\히스토리\240301 최종 적용 준비된 영상\Knight_Day_Chase_원본.mp4"
source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\24년 3월 3일 주일 오전 예배_trimmed.mp4"
# source_path = r"D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\youtube\24년 3월 3일 주일 오전 예배.mp4"

# 잘라낼 영상의 시작과 끝 시간 (초 단위)
start_time = 125 # 2분 5초
end_time = 159 # 2분 39초

# 영상 클립 불러오기 및 잘라내기
video_clip = VideoFileClip(source_path).subclip(start_time, end_time)

# 영상 해상도 조절 (예: 원본의 70% 크기)
video_clip = video_clip.resize(1.0)

# 파일명 추출 (확장자 제외)
file_name = os.path.splitext(os.path.basename(source_path))[0]

# 잘라낸 영상 저장할 경로와 파일명 설정
output_path = f"D:\\회사_더샵\\BIG\\Toy\\24~28Y\\240302 영상 편집\\video\\{file_name}_trimmed.mp4"

# 잘라낸 영상 저장
video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
