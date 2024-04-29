import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import numpy as np


# Функция разбивки изображения на блоки
def split_into_blocks(image, block_size):
    image_width, image_height = image.size
    blocks = []
    for y in range(0, image_height, block_size):
        for x in range(0, image_width, block_size):
            end_x = min(x + block_size, image_width)
            end_y = min(y + block_size, image_height)
            block = image.crop((x, y, end_x, end_y))
            blocks.append(((x, y), block))
    return blocks


# Функция нахождения блока с наибольшей изменчивостью цвета
def find_block_with_max_color_change(blocks):
    max_variance = 0
    target_position = None

    for position, block in blocks:
        block_np = np.array(block.convert("L"))  # Преобразуем в черно-белое
        variance = np.var(block_np)  # Измеряем дисперсию

        if variance > max_variance:
            max_variance = variance
            target_position = position

    return target_position


# Функция встраивания водяного знака
def embed_watermark(input_image_path, output_image_path, watermark_text, block_position, block_size):
    image = Image.open(input_image_path).convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # Используем фиксированный размер шрифта
    font_path = "arial.ttf"  # Убедитесь, что файл шрифта существует
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    x, y = block_position
    position = (x + block_size // 2, y + block_size // 2)  # Центрируем текст

    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

    # Объединяем оригинальное изображение с водяным знаком
    watermarked_image = Image.alpha_composite(image, watermark_layer)
    watermarked_image.save(output_image_path)


# Класс приложения на tkinter
class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")

        # Компоненты интерфейса
        self.load_button = tk.Button(self, text="Выбрать директорию с изображениями", command=self.load_directory)
        self.load_button.pack(pady=10)

        self.watermark_entry = tk.Entry(self)
        self.watermark_entry.insert(0, "WATERMARK")
        self.watermark_entry.pack(pady=10)

        self.save_directory_button = tk.Button(self, text="Выбрать директорию для сохранения",
                                               command=self.choose_save_directory)
        self.save_directory_button.pack(pady=10)

        self.embed_button = tk.Button(self, text="Встроить водяные знаки во все изображения",
                                      command=self.embed_watermarks_in_all_images)
        self.embed_button.pack(pady=10)

        self.image_directory = None
        self.save_directory = None

    def load_directory(self):
        self.image_directory = filedialog.askdirectory(title="Выберите директорию с изображениями")
        if not self.image_directory:
            messagebox.showwarning("Предупреждение", "Директория с изображениями не выбрана")

    def choose_save_directory(self):
        self.save_directory = filedialog.askdirectory(title="Выберите директорию для сохранения")
        if not self.save_directory:
            messagebox.showwarning("Предупреждение", "Директория для сохранения не выбрана")

    def embed_watermarks_in_all_images(self):
        if not self.image_directory:
            messagebox.showwarning("Предупреждение", "Выберите директорию с изображениями")
            return

        if not self.save_directory:
            messagebox.showwarning("Предупреждение", "Выберите директорию для сохранения")
            return

        watermark_text = self.watermark_entry.get()
        block_size = 100

        image_files = [f for f in os.listdir(self.image_directory) if f.endswith((".png", ".jpg", ".jpeg"))]
        if not image_files:
            messagebox.showwarning("Предупреждение", "В директории нет изображений")
            return

        for image_file in image_files:
            image_path = os.path.join(self.image_directory, image_file)
            image = Image.open(image_path)
            blocks = split_into_blocks(image, block_size)
            block_position = find_block_with_max_color_change(blocks)

            if block_position is not None:
                output_image_path = os.path.join(self.save_directory, image_file)
                embed_watermark(image_path, output_image_path, watermark_text, block_position, block_size)
            else:
                messagebox.showerror("Ошибка", "Не удалось найти блок с наибольшим изменением")

        messagebox.showinfo("Успех", "Все изображения обработаны")


# Запуск приложения
if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
