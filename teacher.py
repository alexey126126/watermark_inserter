import torch
import torch.optim as optim
from torch import nn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

from model import UNet
from watermark_dataset import WatermarkDataset

# Создаем датасет и загрузчик данных
dataset_dir = 'dataset'  # Путь к вашему датасету
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Измените размер в зависимости от модели
    transforms.ToTensor()
])

dataset = WatermarkDataset(dataset_dir, transform=transform)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)

# Определяем модель
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = UNet().to(device)

# Оптимизатор и функция потерь
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()  # Используем MSE Loss

# Обучение модели
num_epochs = 10  # Выберите количество эпох
losses = []  # Для отслеживания потерь в процессе обучения

for epoch in range(num_epochs):
    model.train()  # Переводим модель в режим обучения
    epoch_loss = 0  # Для отслеживания потерь в текущей эпохе

    for with_watermark, without_watermark in data_loader:
        with_watermark, without_watermark = with_watermark.to(device), without_watermark.to(device)

        output = model(with_watermark)  # Прогон через модель
        loss = criterion(output, without_watermark)  # Вычисляем потери

        optimizer.zero_grad()  # Обнуляем градиенты
        loss.backward()  # Вычисляем градиенты
        optimizer.step()  # Обновляем параметры

        epoch_loss += loss.item()  # Добавляем к общей потере

    avg_epoch_loss = epoch_loss / len(data_loader)  # Средняя потеря за эпоху
    losses.append(avg_epoch_loss)  # Запоминаем потери

    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {avg_epoch_loss}")

# Отображение графика потерь
plt.plot(losses)
plt.xlabel("Эпоха")
plt.ylabel("Потери")
plt.title("График потерь")
plt.show()

# Сохранение обученной модели
torch.save(model, " trained_model/unet_model.pth")  # Убедитесь, что путь указан верно

