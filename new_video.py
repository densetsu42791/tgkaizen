import subprocess
import os

# Путь к оригинальному видео
original_path = "/home/den/svetache/courses_dnk/интерьерная фотосъемка/original/5. Подготовка к съемке.mp4"

# Папка и имя выходного файла
output_path = os.path.join(os.path.dirname(original_path), "new_video1.mp4")

# Узнаем длительность исходного видео
def get_video_duration(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

# Целевая длительность в секундах
target_duration = 2 * 60 + 2  # 2 минуты и 2 секунды

# Длительность оригинального видео
original_duration = get_video_duration(original_path)

# Сколько секунд нужно черного экрана
black_duration = target_duration - original_duration
if black_duration <= 0:
    raise ValueError("Оригинальное видео уже длиннее или равно 2:02")

# Команда ffmpeg
command = [
    "ffmpeg",
    "-f", "lavfi",
    "-i", f"color=c=black:s=1280x720:d={black_duration}",
    "-i", original_path,
    "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[outv]",
    "-map", "[outv]",
    "-y",
    output_path
]

# Выполняем
subprocess.run(command)
print(f"Готово! Файл сохранён как {output_path}")
