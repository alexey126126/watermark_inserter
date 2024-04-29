import torch
from application import WatermarkApp


# Загрузка обученной модели
model_path = "path/to/your/unet_model.pth"
model = torch.load(model_path, map_location=torch.device("cpu"))  # Если используется CPU
model.eval()  # Переводим модель в режим инференса

# Запуск приложения
if __name__ == "__main__":
    app = WatermarkApp(model)
    app.mainloop()
