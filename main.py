import os
import subprocess

# 👩‍👦 الصور + النصوص (بدّل الأسماء حسب صورك)
slides = [
    {"image": "1.png", "text": "التعب حاضر… لكن الحب أقوى."},
    {"image": "2.png", "text": "كل يوم فرصة جديدة للتغيير."},
]

# ملف الصوت (حط موسيقى ملهمة mp3)
audio_file = "music.mp3"

# ملف الخط (Lora من Google Fonts)
font_file = "Lora-Regular.ttf"

# الفيديو النهائي
output_video = "final_video.mp4"

# مدة كل صورة (ثواني)
duration_per_image = 5

# إنشاء فيديو مؤقت لكل صورة + نص
temp_videos = []
for i, slide in enumerate(slides):
    temp_output = f"temp_{i}.mp4"
    temp_videos.append(temp_output)

    drawtext = (
        f"drawtext=text='{slide['text']}':"
        f"fontfile={font_file}:"
        f"fontcolor=white:fontsize=42:"
        f"shadowcolor=black:shadowx=2:shadowy=2:"
        f"x=(w-text_w)/2:y=h-120"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", slide["image"],
        "-vf", drawtext,
        "-t", str(duration_per_image),
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        temp_output
    ]
    subprocess.run(cmd)

# تجميع الفيديوهات
with open("videos.txt", "w") as f:
    for v in temp_videos:
        f.write(f"file '{os.path.abspath(v)}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", "videos.txt",
    "-c", "copy", "temp_full.mp4"
])

# إضافة الموسيقى
subprocess.run([
    "ffmpeg", "-y",
    "-i", "temp_full.mp4",
    "-i", audio_file,
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest", output_video
])

print("✅ الفيديو تخدم:", output_video)
