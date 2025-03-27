import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


def category_spider_chart(df, colors=None):
    """
    Рисует радарный график для данных из датафрейма, сгруппированных по категориям.

    Параметры:
    df: Датафрейм с колонками 'Category', 'Subject', 'Score'.
    colors: Список цветов для каждого набора данных.
    """
    # Группируем данные по категориям
    grouped = df.groupby("Category")

    # Извлекаем уникальные категории (метки)
    labels = df["Category"].unique().tolist()

    # Сохраняем порядок предметов из исходного датафрейма
    unique_categories = df["Subject"].unique().tolist()

    # Создаем углы для графика
    angles = np.linspace(0, 2 * np.pi, len(unique_categories), endpoint=False)
    angles = np.append(angles, angles[0])  # Замыкаем круг

    # Подготовка данных для графика
    values_list = []
    for _, group in grouped:
        score_dict = dict(zip(group["Subject"], group["Score"]))  # Создаем словарь {предмет: оценка}
        aligned_scores = [score_dict.get(cat, 0) for cat in unique_categories]  # Заполняем пропуски нулями
        aligned_scores.append(aligned_scores[0])  # Замыкаем круг
        values_list.append(aligned_scores)

    # Создаем график
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Настройка осей
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Настройка радиальных меток
    plt.yticks([71, 86, 100],color="#5d5d61", size=8, alpha=1, fontsize=8,
                ha="center", va="bottom", fontweight="bold", zorder=2)

    # Пунктирная сетка для всех угловых меток
    ax.set_xticks([])  # Устанавливаем метки для всех углов (кроме последнего, который дублирует первый)
    ax.set_xticklabels([])
    # Пунктирные линии для всех осей
    ax.grid(color='#c3c3c7', linestyle='--', linewidth=0.5, alpha=1, zorder=0)

    ax.add_artist(plt.Circle((0, 0), 30, transform=ax.transData._b, color="white", zorder=3))
    ax.text(0, 0, "student_name",
            ha='center', va='center',
            fontsize=10,
            color='#333333', zorder=4)
    ax.set_frame_on(False)


    # Если цвета не переданы, используем стандартную палитру
    if colors is None:
        colors = plt.cm.tab20.colors[:len(labels)]

    # Рисуем данные
    for values, label, color in zip(values_list, labels, colors):
        ax.plot(angles, values, linewidth=0, label=label, color=color)
        ax.fill(angles, values, color=color, alpha=1,  zorder=2)

    # Легенда
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    # Создаем кастомные элементы для легенды
    legend_elements = [Patch(facecolor=color, label=label)
                       for color, label in zip(colors, labels)]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.show()


# Пример использования
df = pd.read_csv('../templates/subjects_scores.csv')

# Вызов функции
category_spider_chart(
    df,
    colors=["#665191", "#a05195", "#d45087", "#f95d6a", "#ff7c43", "#ffa600"]
)