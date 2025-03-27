import numpy as np
import matplotlib.pyplot as plt

def circular_scatter_plot_subjects(items, values, groups, ax, show_legend=True, group_colors=None):
    """
    Рисует scatter plot с точками, расположенными в секторах.

    Параметры:
    - items: Список названий (предметов).
    - values: Список числовых значений.
    - groups: Список категорий.
    - ax: Ось для рисования графика.
    - show_legend: Если True, отображает легенду, иначе скрывает.
    - group_colors: Словарь с цветами для каждой группы.
    """
    # Если цвета не переданы, используем стандартные
    if group_colors is None:
        group_colors = {group: f"C{i}" for i, group in enumerate(set(groups))}

    # Уникальные категории для цвета
    unique_groups = list(set(groups))
    num_groups = len(unique_groups)

    # Углы для каждого элемента (сектора)
    num_items = len(items)
    angles = np.linspace(0, 2 * np.pi, num_items, endpoint=False)

    # Радиусы для точек (10 кружков по Y)
    # Новый диапазон: от -50 до 100
    radii = np.linspace(-20, 90, 10)  # 10 кружков по радиусу (от -50 до 100)

    # Отслеживание уже добавленных категорий в легенду
    added_groups = set()

    # Рисуем точки
    for i, (item, value, group) in enumerate(zip(items, values, groups)):
        angle = angles[i]
        color = group_colors[group]

        # Нормализуем значение (максимум 10 кружков по Y)
        # Новый диапазон: от -50 до 100
        normalized_score = min(int((value + 50) / 15), 10)  # Нормализация для диапазона (-50, 100)

        # Добавляем категорию в легенду, если еще нет
        label = group if group not in added_groups else ""
        added_groups.add(group)

        # Закрашенные точки (по радиусу)
        ax.scatter(
            np.full(normalized_score, angle), radii[:normalized_score],
            c=[color], s=100, alpha=1, edgecolors='lightgray', linewidths=0.5, label=label
        )

        # Пустые точки (если не весь ряд заполнен)
        if normalized_score < 10:
            ax.scatter(
                np.full(10 - normalized_score, angle), radii[normalized_score:],
                c='white', s=100, alpha=1, edgecolors='lightgray', linewidths=0.5
            )

    # Настройки осей
    ax.set_ylim(-50, 100)  # Новый диапазон оси Y
    ax.set_frame_on(False)  # Убираем рамку
    ax.xaxis.grid(False)  # Отключаем сетку по X
    ax.yaxis.grid(False)  # Отключаем сетку по Y
    ax.set_xticks([])  # Убираем подписи по X
    ax.set_yticks([])  # Убираем подписи по Y

    # Добавляем легенду, если show_legend True
    if show_legend:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8, frameon=False)