# templates/circular_barchart.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_circular_barchart(items, values, groups, ax, show_legend=True, group_colors=None):
    """
    Рисует круговую барчарт-диаграмму.

    Параметры:
    - items: Список названий (предметов).
    - values: Список числовых значений.
    - groups: Список категорий.
    - ax: Ось для рисования графика.
    - show_legend: Если True, отображает легенду, иначе скрывает.
    - group_colors: Словарь с цветами для каждой группы.
    """
    df = pd.DataFrame({"items": items, "values": values, "groups": groups})

    df = df.sort_values(by="groups").reset_index(drop=True)

    # Извлечение данных
    VALUES = df["values"].values
    LABELS = df["items"].values
    GROUP = df["groups"].values

    pad = 1

    if group_colors is None:
        CUSTOM_COLORS = ["#a8e6cf", "#dcedc1", "#ffd3b6", "#ffdca6", "#f2aeae", "#dbdcff"]
        unique_categories = list(dict.fromkeys(GROUP))
        group_colors = {category: CUSTOM_COLORS[i % len(CUSTOM_COLORS)] for i, category in enumerate(unique_categories)}

    # Назначаем цвета, чтобы категории соответствовали цветам
    COLORS = [group_colors[cat] for cat in GROUP]

    # Вычисление углов и индексов
    GROUPS_SIZE = [len(group) for _, group in df.groupby("groups")]
    ANGLES_N = len(VALUES) + pad * len(GROUPS_SIZE)  # Общее количество углов
    ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)  # Углы для всех секторов
    WIDTH = (2 * np.pi) / len(ANGLES)  # Ширина каждого столбца

    # Индексы для непустых столбцов
    IDXS = []
    offset = 0
    for size in GROUPS_SIZE:
        IDXS += list(range(offset + pad, offset + size + pad))
        offset += size + pad

    # Добавление фонового круга
    ax.add_artist(plt.Circle((0, 0), 150, transform=ax.transData._b, color="#fff0f0", zorder=-1))

    # Настройка оси
    ax.set_theta_offset(np.pi / 2)  # Смещение для начала первого столбца (90 градусов)
    ax.set_ylim(-50, 100)
    ax.set_frame_on(False)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Добавление столбцов
    ax.bar(ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS, edgecolor="#fff0f0", linewidth=2)

    # Функция для вычисления поворота и выравнивания меток
    def get_label_rotation(angle, offset):
        rotation = np.rad2deg(angle + offset)
        alignment = "right" if angle <= np.pi else "left"
        rotation = rotation + 180 if angle <= np.pi else rotation
        return rotation, alignment

    def add_labels(angles, labels, offset, ax, radius=40):
        for angle, label in zip(angles, labels):
            rotation, alignment = get_label_rotation(angle, offset)
            ax.text(
                x=angle, y=radius, s=label, ha=alignment, va="center",
                fontsize=5.5, rotation=rotation, rotation_mode="anchor", color="#2b2a2a"
            )

    #add_labels(ANGLES[IDXS], LABELS, np.pi / 2, ax, radius=5)

    if show_legend:
        handles = [plt.Rectangle((0, 0), 1, 1, color=group_colors[cat]) for cat in group_colors]
        labels = list(group_colors.keys())
        ax.legend(handles, labels, loc="center left", bbox_to_anchor=(1.1, 0.5), fontsize=8, frameon=False)