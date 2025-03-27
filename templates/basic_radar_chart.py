import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Исходные данные
categories = ['Скорость', 'Сила', 'Интеллект', 'Выносливость', 'Ловкость']
values = [4, 3, 5, 2, 4]

# Замыкаем данные (добавляем первый элемент в конец)
closed_values = values + [values[0]]

# Углы для основных категорий (без дублирования!)
n = len(categories)
base_angles = np.linspace(0, 2*np.pi, n, endpoint=False)
closed_angles = np.append(base_angles, base_angles[0])

# Углы для интерполяции (100 точек + замыкание)
interp_angles = np.linspace(0, 2*np.pi, 100, endpoint=True)

# Периодическая интерполяция (учитываем зацикленность данных)
interp_func = interp1d(
    closed_angles,
    closed_values,
    kind='cubic',
    fill_value='extrapolate'  # Разрешаем экстраполяцию
)

# Сглаженные значения
smooth_values = interp_func(interp_angles)

# Создаем график
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})

# Отрисовка
ax.plot(interp_angles, smooth_values, linewidth=2)
ax.fill(interp_angles, smooth_values, alpha=0.25)

# Настройки осей
ax.set_xticks(base_angles)
ax.set_xticklabels(categories)
ax.set_ylim(0, max(values)+1)

plt.title('Сглаженная паутинная диаграмма')
plt.show()
