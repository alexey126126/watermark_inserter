import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np


# Функция разбивки изображения на блоки
def split_into_blocks(image, block_size):
    image_width, image_height = image.size
    blocks = []
    for y in range(0, image_height, block_size):
        for x in range(0, image_width, block_size):
            block = image.crop((x, y, x + block_size, y + block_size))
            blocks.append(((x, y), block))
    return blocks


# Функция нахождения блока с наибольшим изменением цвета
def find_block_with_max_color_change(blocks):
    max_variance = 0
    target_position = None

    for position, block in blocks:
        block_np = np.array(block.convert("L"))  # Преобразуем в оттенки серого
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

    font = ImageFont.truetype("arial.ttf", 50)
    x, y = block_position
    text_width, text_height = draw.textlength(watermark_text, font)
    position = (x + (block_size - text_width) // 2, y + (block_size - text_height) // 2)

    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

    watermarked_image = Image.alpha_composite(image, watermark_layer)
    watermarked_image.save(output_image_path)


# Функция для удаления водяного знака
def remove_watermark(input_image_path, output_image_path, block_position, block_size):
    image = cv2.imread(input_image_path)

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    x, y = block_position
    mask[y:y + block_size, x + x + block_size] = 255  # Устанавливаем белую область в маске

    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    cv2.imwrite(output_image_path, inpainted_image)


# Класс приложения на tkinter
class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")

        # Компоненты GUI
        self.load_button = tk.Button(self, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=10)

        self.watermark_entry = tk.Entry(self)
        self.watermark_entry.insert(0, "WATERMARK")
        self.watermark_entry.pack(pady=10)

        self.embed_button = tk.Button(self, text="Встроить водяной знак", command=self.embed_watermark)
        self.embed_button.pack(pady=10)

        self.remove_button = tk.Button(self, text="Удалить водяной знак", command=self.remove_watermark)
        self.remove_button.pack(pady=10)

        self.image_path = None

    # Функция загрузки изображения
    def load_image(self):
        self.image_path = filedialog.askopenfilename(title="Выберите изображение",
                                                     filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])

    # Функция для встраивания водяного знака
    def embed_watermark(self):
        if self.image_path:
            watermark_text = self.watermark_entry.get()
            image = Image.open(self.image_path)
            block_size = 100
            blocks = split_into_blocks(image, block_size)
            block_position = find_block_with_max_color_change(blocks)

            output_image_path = "image_with_watermark.jpg"
            embed_watermark(self.image_path, output_image_path, watermark_text, block_position, block_size)
            print("Водяной знак встроен")
        else:
            print("Пожалуйста, загрузите изображение")

    # Функция для удаления водяного знака
    def remove_watermark(self):
        if self.image_path:
            image = Image.open(self.image_path)
            block_size = 100
            blocks = split_into_blocks(image, block_size)
            block_position = find_block_with_max_color_change(blocks)

            output_image_path = "image_without_watermark.jpg"
            remove_watermark("image_with_watermark.jpg", output_image_path, block_position, block_size)
            print("Водяной знак удален")
        else:
            print("Пожалуйста, загрузите изображение")


# Запуск приложения
if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
