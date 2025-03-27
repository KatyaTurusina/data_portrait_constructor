import os
import importlib.util
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        self.templates_dir = "templates"  # Папка с шаблонами графиков
        self.figure, self.ax = plt.subplots(subplot_kw=dict(polar=True))
        self.canvas = None
        self.toolbar = None
        self.group_colors = {}

    def load_templates(self):
        """Загружает список доступных шаблонов визуализации"""
        templates = []
        if os.path.exists(self.templates_dir):
            templates = [f.replace(".py", "") for f in os.listdir(self.templates_dir) if f.endswith(".py")]
        return templates

    def plot_graph(self, items, values, groups, template_name, show_legend=True, y_min=-0.1, y_max=0.7):
        """Вызывает выбранный шаблон визуализации"""
        try:
            # Очищаем текущий график
            self.ax.clear()

            # Импортируем шаблон как модуль
            template_path = os.path.join(self.templates_dir, f"{template_name}.py")
            spec = importlib.util.spec_from_file_location(template_name, template_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Список возможных имен функций для построения графиков
            plot_functions = [
                "circular_scatter_plot_subjects",  # Для scatter шаблона
                "plot_circular_barchart",  # Для нового barchart шаблона
            ]

            # Поиск и вызов функции из шаблона
            plot_function = None
            for func_name in plot_functions:
                if hasattr(module, func_name):
                    plot_function = getattr(module, func_name)
                    break

            if plot_function is None:
                raise ValueError(f"В шаблоне {template_name} нет подходящей функции для построения графика.")

            # Вызов функции построения графика
            plot_function(
                items, values, groups, self.ax,
                show_legend=show_legend,
                group_colors=self.group_colors
            )

            # Устанавливаем границы оси Y
            self.ax.set_ylim(y_min, y_max)

            # Обновляем канвас
            if self.canvas:
                self.canvas.draw()

        except Exception as e:
            print(f"Ошибка при построении графика: {e}")
            raise e