# pytube는 연령 제한이 있는 동영상을 다운로드할 수 없음.
# youtube_dl는 연령 제한 있어도 다운로드 가능

from pytube import YouTube

# 유튜브 동영상 URL
# video_url = 'https://youtu.be/rS4op6MW5qc?si=O9BjF5AGIe9R-JUX'
video_url = 'https://youtu.be/5ZXOV1ma35g?si=8a4L5Eu7vcI7MlDi'

# YouTube 객체 생성
yt = YouTube(video_url)

# 가장 높은 해상도의 스트림 선택
video = yt.streams.get_highest_resolution()

# 동영상 저장 경로 지정
save_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\youtube\\'

# 동영상 다운로드
video.download(save_path)
