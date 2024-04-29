import os
from PIL import Image

# Укажите путь к директории, где находятся изображения
image_dir = "dataset/without_watermark/"  # Например, "images/"

# Создать папку для сохранения обрезанных изображений
output_dir = os.path.join(image_dir, "cropped/")
os.makedirs(output_dir, exist_ok=True)

# Находим минимальный размер среди всех изображений
min_width = float("inf")
min_height = float("inf")

# Первый проход: определить минимальные размеры
for file_name in os.listdir(image_dir):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
        file_path = os.path.join(image_dir, file_name)
        with Image.open(file_path) as img:
            width, height = img.size
            min_width = min(min_width, width)
            min_height = min(min_height, height)

target_size = (min_width, min_height)

# Второй проход: обрезать изображения до минимальных размеров
for file_name in os.listdir(image_dir):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
        file_path = os.path.join(image_dir, file_name)
        with Image.open(file_path) as img:
            width, height = img.size

            # Рассчитываем параметры обрезки, чтобы центрировать обрезку
            left = (width - min_width) / 2
            top = (height - min_height) / 2
            right = left + min_width
            bottom = top + min_height

            # Обрезаем изображение
            cropped_img = img.crop((left, top, right, bottom))

            # Сохраняем в новую директорию
            output_path = os.path.join(output_dir, file_name)
            cropped_img.save(output_path)

print("Обрезка изображений завершена.")