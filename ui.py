from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QTextEdit, QHBoxLayout, QMessageBox,
    QTableWidgetItem, QStackedWidget, QComboBox, QLabel,
    QHeaderView, QDoubleSpinBox
)
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtGui import QColor
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from data_handler import DataHandler
from visualization import Visualization


class CSVViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Viewer")
        self.setGeometry(100, 100, 900, 500)
        self.showMaximized()

        # Инициализация модулей
        self.data_handler = DataHandler()
        self.visualization = Visualization()

        # Основной контейнер с переключаемыми страницами
        self.stack = QStackedWidget(self)

        # Страница загрузки данных
        self.data_page = self.create_data_page()
        self.stack.addWidget(self.data_page)

        # Страница визуализации
        self.visualization_page = self.create_visualization_page()
        self.stack.addWidget(self.visualization_page)

        # Основной layout
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def create_data_page(self):
        """Создает страницу загрузки данных"""
        page = QWidget()
        layout = QHBoxLayout()

        vbox = QVBoxLayout()

        self.btn_load = QPushButton("Загрузить CSV")
        self.btn_load.clicked.connect(self.load_csv)
        vbox.addWidget(self.btn_load)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Вставьте CSV-данные")
        vbox.addWidget(self.text_edit)

        self.btn_process = QPushButton("Обработать данные")
        self.btn_process.clicked.connect(self.process_manual_input)
        vbox.addWidget(self.btn_process)

        self.btn_clear = QPushButton("Очистить данные")
        self.btn_clear.clicked.connect(self.clear_data)
        vbox.addWidget(self.btn_clear)

        self.btn_visualize = QPushButton("Перейти к визуализации")
        self.btn_visualize.clicked.connect(self.show_visualization_page)
        self.btn_visualize.setEnabled(False)
        vbox.addWidget(self.btn_visualize)

        layout.addLayout(vbox, 1)

        self.table = QTableWidget()
        layout.addWidget(self.table, 3)

        page.setLayout(layout)
        return page

    def create_visualization_page(self):
        """Создает страницу визуализации"""
        page = QWidget()
        layout = QHBoxLayout()

        # Левая панель с выпадающими списками для параметров
        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_back = QPushButton("Назад к данным")
        self.btn_back.clicked.connect(self.show_data_page)
        left_panel.addWidget(self.btn_back)

        # Параметры функции для визуализации
        self.param_widgets = {}

        params = [
            ('items', "Выберите столбец для 'items'"),
            ('values', "Выберите столбец для 'values'"),
            ('groups', "Выберите столбец для 'groups'")
        ]

        for param, label_text in params:
            param_layout = QVBoxLayout()
            param_layout.setSpacing(5)

            label = QLabel(label_text)
            self.param_widgets[param] = QComboBox()

            param_layout.addWidget(label)
            param_layout.addWidget(self.param_widgets[param])

            left_panel.addLayout(param_layout)
            left_panel.addSpacing(10)

        # Добавляем выпадающий список для выбора шаблона
        template_layout = QVBoxLayout()
        template_layout.setSpacing(5)
        template_label = QLabel("Выберите шаблон")
        self.template_selector = QComboBox()
        self.template_selector.addItems(self.visualization.load_templates())
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_selector)
        left_panel.addLayout(template_layout)
        left_panel.addSpacing(10)

        # Кнопка для выбора цветов
        self.btn_choose_colors = QPushButton("Выбрать цвета")
        self.btn_choose_colors.clicked.connect(self.choose_colors)
        left_panel.addWidget(self.btn_choose_colors)

        # Контейнер для отображения кружков с цветами
        self.color_widgets_container = QVBoxLayout()
        left_panel.addLayout(self.color_widgets_container)

        # Элементы управления для ax.set_ylim
        ylim_layout = QHBoxLayout()
        ylim_label = QLabel("Границы оси Y:")
        self.ylim_min = QDoubleSpinBox()
        self.ylim_min.setRange(-100.0, 100.0)
        self.ylim_min.setValue(-50.0)
        self.ylim_max = QDoubleSpinBox()
        self.ylim_max.setRange(-100.0, 100.0)
        self.ylim_max.setValue(90.0)
        self.btn_apply_ylim = QPushButton("Применить")
        self.btn_apply_ylim.clicked.connect(self.plot_graph)

        ylim_layout.addWidget(ylim_label)
        ylim_layout.addWidget(self.ylim_min)
        ylim_layout.addWidget(self.ylim_max)
        ylim_layout.addWidget(self.btn_apply_ylim)

        left_panel.addLayout(ylim_layout)

        # Кнопки
        self.btn_plot = QPushButton("Построить график")
        self.btn_plot.clicked.connect(self.plot_graph)
        left_panel.addWidget(self.btn_plot)

        self.legend_visible = True
        self.btn_toggle_legend = QPushButton("Скрыть легенду")
        self.btn_toggle_legend.clicked.connect(self.toggle_legend)
        left_panel.addWidget(self.btn_toggle_legend)

        layout.addLayout(left_panel, 1)

        # Правая панель (предпросмотр графика)
        self.visualization.canvas = FigureCanvas(self.visualization.figure)
        self.visualization.toolbar = NavigationToolbar(self.visualization.canvas, self)

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.visualization.toolbar)
        right_panel.addWidget(self.visualization.canvas)

        layout.addLayout(right_panel, 3)

        page.setLayout(layout)
        return page

    def choose_colors(self):
        """Открывает диалог выбора цветов для каждой группы"""
        if self.data_handler.df is None:
            return

        groups_column = self.param_widgets['groups'].currentText()
        unique_groups = self.data_handler.df[groups_column].unique()

        default_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]

        self.visualization.group_colors = {}
        for i, group in enumerate(unique_groups):
            self.visualization.group_colors[group] = default_colors[i % len(default_colors)]

        self.update_color_widgets()

    def update_color_widgets(self):
        """Обновляет цвет кружочков в соответствии с текущими цветами групп"""
        # Очищаем контейнер перед добавлением новых виджетов
        while self.color_widgets_container.count():
            item = self.color_widgets_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        color_circles_layout = QHBoxLayout()
        color_circles_layout.setSpacing(10)

        for group, color in self.visualization.group_colors.items():
            color_circle = QLabel()
            color_circle.setFixedSize(30, 30)
            color_circle.setStyleSheet(
                f"background-color: {color};"
                "border-radius: 15px;"
                "border: 1px solid black;"
            )
            color_circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            color_circle.setToolTip(group)
            color_circle.mousePressEvent = lambda event, g=group: self.change_group_color(g)

            color_circles_layout.addWidget(color_circle)

        self.color_widgets_container.addLayout(color_circles_layout)

    def change_group_color(self, group):
        """Изменяет цвет для конкретной группы"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.visualization.group_colors[group] = color.name()
            self.update_color_widgets()  # Обновляем виджеты с цветами
            self.plot_graph()  # Обновляем график

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV", "", "CSV (*.csv)")
        if file_path and self.data_handler.load_csv(file_path):
            self.show_data(self.data_handler.df)
            self.btn_visualize.setEnabled(True)
            self.update_column_list()

    def process_manual_input(self):
        text = self.text_edit.toPlainText()
        if self.data_handler.process_text_input(text):
            self.show_data(self.data_handler.df)
            self.btn_visualize.setEnabled(True)
            self.update_column_list()

    def clear_data(self):
        self.data_handler.clear_data()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.text_edit.clear()
        self.param_widgets['items'].clear()
        self.param_widgets['values'].clear()
        self.param_widgets['groups'].clear()
        self.template_selector.clear()
        self.btn_visualize.setEnabled(False)

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def show_data(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

    def show_visualization_page(self):
        """Переключает на страницу визуализации"""
        self.update_column_list()
        self.stack.setCurrentWidget(self.visualization_page)

    def show_data_page(self):
        """Переключает на страницу загрузки данных"""
        self.stack.setCurrentWidget(self.data_page)

    def update_column_list(self):
        """Обновляет список переменных, отображая их фактический тип данных"""
        if self.data_handler.df is not None:
            for param in self.param_widgets.values():
                param.clear()
                param.addItems(self.data_handler.get_columns())

    def plot_graph(self):
        """Вызывает выбранный шаблон визуализации"""
        try:
            items_column = self.param_widgets['items'].currentText()
            values_column = self.param_widgets['values'].currentText()
            groups_column = self.param_widgets['groups'].currentText()

            items = self.data_handler.df[items_column].astype(str).tolist()
            values = self.data_handler.df[values_column].astype(float).tolist()
            groups = self.data_handler.df[groups_column].astype(str).tolist()

            self.visualization.plot_graph(
                items, values, groups,
                self.template_selector.currentText(),
                show_legend=self.legend_visible,
                y_min=self.ylim_min.value(),
                y_max=self.ylim_max.value()
            )

        except Exception as e:
            self.show_error(f"Ошибка построения графика:\n{e}")

    def toggle_legend(self):
        """Переключает отображение легенды на графике"""
        self.legend_visible = not self.legend_visible
        self.plot_graph()