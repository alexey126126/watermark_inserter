import os
from PIL import Image

# Укажите путь к директории, где находятся изображения
input_dir = "dataset/without_watermark/cropped/"  # Например, "images/"

# Создать целевую директорию для конвертированных изображений
output_dir = "dataset/without_watermark/converted/"  # Папка для сохранения сконвертированных изображений
os.makedirs(output_dir, exist_ok=True)

# Обойти все файлы в директории
for file_name in os.listdir(input_dir):
    # Проверить, является ли файл изображением (по расширению)
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")):
        # Полный путь к изображению
        file_path = os.path.join(input_dir, file_name)

        # Открыть изображение
        with Image.open(file_path) as img:
            # Конвертировать в формат RGBA
            rgba_img = img.convert("RGBA")

            # Путь для сохранения
            output_path = os.path.join(output_dir, file_name)

            # Сохранить изображение в формате RGBA
            rgba_img.save(output_path)

print("Конвертация завершена. Все изображения сохранены в формате RGBA.")