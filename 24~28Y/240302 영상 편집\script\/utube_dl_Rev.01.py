import yt_dlp as youtube_dl

# video_url = 'https://youtu.be/ky8B_zlDyx8?si=I5BEeAA4HmqOHQv7'
video_url = 'https://www.facebook.com/reel/1532673957509633?mibextid=Nif5oz'

# 저장 경로 설정, 여기서 '%(title)s'는 동영상 제목으로 대체됩니다.
save_path = r'D:\회사_더샵\BIG\Toy\24~28Y\240302 영상 편집\youtube\%(title)s.%(ext)s'

ydl_opts = {
    'format': 'best',
    # 'outtmpl': save_path,
    'outtmpl': 'D:/회사_더샵/BIG/Toy/24~28Y/240302 영상 편집/youtube/video.mp4', # 파일명에 이모티콘 있을 경우
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

