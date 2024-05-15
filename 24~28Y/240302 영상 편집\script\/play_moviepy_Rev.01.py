from moviepy.editor import VideoFileClip

# 영상 파일 경로
# video_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\youtube\전국민이 16강을 기원했지만 아 또 뜨네요! 황선홍의 축구 인생을 바꿔놓은 그 경기! 1994 월드컵 볼리비아전!!.mp4'
# video_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\히스토리\240301 최종 적용 준비된 영상\Knight_Day_Chase_원본.mp4'
video_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\video\[문제적남자] 창의력 강화 NASA의 핵심 기출문제! 스펙 끝판왕 풀윤 교수가 본 문남 중 NASA형 인재는  Diggle_trimmed.mp4'

# 비디오 클립 객체 생성
video_clip = VideoFileClip(video_path)

# 비디오와 오디오 함께 재생
video_clip.preview()
