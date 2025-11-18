import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Проверяем доступность GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

# Загрузка данных
df = pd.read_parquet('data_for_tests/data_from_moex5/_5IMOEXF_1_1763448583.parquet')

# Выбираем признаки для обучения
features = ['open', 'high', 'low', 'vol_coin', 'volume', 'direction', 
           'middle']
target = 'close'

# Создаем копию датафрейма для работы
data = df[features + [target]].copy()

# Масштабирование данных
scaler_features = StandardScaler()
scaler_target = StandardScaler()

scaled_features = scaler_features.fit_transform(data[features])
scaled_target = scaler_target.fit_transform(data[[target]])

# Функция для создания последовательностей
def create_sequences(features, target, sequence_length=60):
    X, y = [], []
    for i in range(sequence_length, len(features)):
        X.append(features[i-sequence_length:i])
        y.append(target[i])
    return np.array(X), np.array(y)

# Параметры последовательности
SEQ_LENGTH = 60

# Создаем последовательности
X, y = create_sequences(scaled_features, scaled_target, SEQ_LENGTH)

# Преобразуем в тензоры PyTorch
X_tensor = torch.FloatTensor(X)
y_tensor = torch.FloatTensor(y)

print(f"Форма X: {X_tensor.shape}")  # (samples, sequence_length, features)
print(f"Форма y: {y_tensor.shape}")  # (samples, 1)

# Разделяем данные
split_index = int(0.5 * len(X_tensor))
split_val_index = int(0.7 * len(X_tensor))
X_train, X_val, X_test = X_tensor[:split_index], X_tensor[split_index:split_val_index], X_tensor[split_val_index:]
y_train, y_val, y_test = y_tensor[:split_index], y_tensor[split_index:split_val_index], y_tensor[split_val_index:]

# Создаем Dataset и DataLoader
train_dataset = TensorDataset(X_train, y_train)
val_dataset = TensorDataset(X_val,y_val)
test_dataset = TensorDataset(X_test, y_test)

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(f"Тренировочные данные: {X_train.shape}, {y_train.shape}")
print(f"Валидационные данные: {X_val.shape}, {y_val.shape}")
print(f"Тестовые данные: {X_test.shape}, {y_test.shape}")

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, dropout_rate=0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm1 = nn.LSTM(input_size, hidden_size, num_layers, 
                            batch_first=True, dropout=dropout_rate)
        self.lstm2 = nn.LSTM(hidden_size, hidden_size, num_layers, 
                            batch_first=True, dropout=dropout_rate)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc1 = nn.Linear(hidden_size, 25)
        self.fc2 = nn.Linear(25, output_size)
        
    def forward(self, x):
        # Инициализация скрытых состояний
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        
        # Проход через LSTM слои
        out, _ = self.lstm1(x, (h0, c0))
        out, _ = self.lstm2(out)
        
        # Берем только последний выход последовательности
        out = out[:, -1, :]
        
        # Полносвязные слои
        out = self.dropout(out)
        out = torch.relu(self.fc1(out))
        out = self.fc2(out)
        
        return out

# Параметры модели
input_size = len(features)
hidden_size = 50
num_layers = 2
output_size = 1

# Создаем модель
model = LSTMModel(input_size, hidden_size, num_layers, output_size).to(device)

print(model)

# Функция потерь и оптимизатор
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Для отслеживания потерь
train_losses = []
val_losses = []

# Обучение
num_epochs = 50

for epoch in range(num_epochs):
    # Тренировочный режим
    model.train()
    train_loss = 0.0
    
    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        # Forward pass
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
    
    # Валидация
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for batch_X, batch_y in val_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            outputs = model(batch_X)
            val_loss += criterion(outputs, batch_y).item()
    
    # Средние потери за эпоху
    train_loss = train_loss / len(train_loader)
    val_loss = val_loss / len(val_loader)
    
    train_losses.append(train_loss)
    val_losses.append(val_loss)
    
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}')

print("Обучение завершено!")

# Графики потерь
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Training Loss')
plt.plot(val_losses, label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()

# Предсказания на тестовых данных
model.eval()
all_predictions = []
all_targets = []

with torch.no_grad():
    for batch_X, batch_y in test_loader:
        batch_X = batch_X.to(device)
        outputs = model(batch_X)
        all_predictions.extend(outputs.cpu().numpy())
        all_targets.extend(batch_y.numpy())

all_predictions = np.array(all_predictions)
all_targets = np.array(all_targets)

# Обратное масштабирование
predictions_original = scaler_target.inverse_transform(all_predictions)
targets_original = scaler_target.inverse_transform(all_targets)

# Метрики
mae = mean_absolute_error(targets_original, predictions_original)
mse = mean_squared_error(targets_original, predictions_original)
rmse = np.sqrt(mse)
r2 = r2_score(targets_original, predictions_original)

print(f"MAE: {mae:.4f}")
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²: {r2:.4f}")

# Визуализация предсказаний
plt.subplot(1, 2, 2)
plot_range = min(200, len(targets_original))
plt.plot(targets_original[-plot_range:], label='Actual Close', alpha=0.7, linewidth=2)
plt.plot(predictions_original[-plot_range:], label='Predicted Close', alpha=0.7, linewidth=2)
plt.title('Фактические vs Предсказанные значения')
plt.xlabel('Время')
plt.ylabel('Close Price')
plt.legend()

plt.tight_layout()
plt.show()

def predict_future_torch(model, last_sequence, n_steps, device):
    """Предсказание на несколько шагов вперед"""
    model.eval()
    predictions = []
    current_sequence = last_sequence.clone().to(device)
    
    with torch.no_grad():
        for _ in range(n_steps):
            # Предсказываем следующий шаг
            next_pred = model(current_sequence.unsqueeze(0))
            predictions.append(next_pred.cpu().numpy()[0, 0])
            
            # Обновляем последовательность (упрощенный подход)
            # В реальности нужно обновлять все признаки
            current_sequence = torch.roll(current_sequence, -1, 0)
            # Здесь можно добавить логику обновления признаков
            
    return np.array(predictions)

# Пример предсказания на 10 шагов
last_sequence = X_test[-1].to(device)
future_predictions_scaled = predict_future_torch(model, last_sequence, 10, device)
future_predictions = scaler_target.inverse_transform(future_predictions_scaled.reshape(-1, 1))

print("Предсказания на следующие 10 периодов:")
for i, pred in enumerate(future_predictions, 1):
    print(f"Шаг {i}: {pred[0]:.2f}")

# Сохранение модели
# torch.save(model.state_dict(), 'lstm_model.pth')
# print("Модель сохранена как 'lstm_model.pth'")