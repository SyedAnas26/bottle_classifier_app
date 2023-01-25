import math

from PySide2.QtCore import QAbstractProxyModel, QModelIndex, QItemSelection
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide2.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QComboBox, QListView, QLabel

from typing import Any
from datetime import datetime, timedelta
from collections import defaultdict

from components.BarChart import create_chart


class Analytics(QWidget):
    def __init__(self, bottle_collection):
        super().__init__()

        # Fetching Bottles data using the MongoDB collection
        self.bottle_list = list(bottle_collection.find())

        # Combo Box for Selecting SKU ID
        self.combo = QComboBox(self)

        # Selected SKU : Default is the First index Value
        self.selected_sku = 1

        # Possible SKU ID list
        self.sku_id_list = list(set(bottle['sku_id'] for bottle in self.bottle_list))

        # Bottle Data as {"SKUID":{"TIME":{"Good":"GOOD COUNT", "Bad": "BAD COUNT"}}}
        # eg - {1:{"9.30":{"Good":9,"Bad":1}, .. }
        self.bottle_data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        # Layout for Chart
        self.chart_layout = QHBoxLayout()

        # Initializing the UI
        self.initUI()

    def initUI(self):

        # Creating the list for Combo Select box ( SKU selection )
        model = QStandardItemModel()

        for sku_id in self.sku_id_list:
            model.appendRow(QStandardItem(f"SKU {sku_id}"))

        # Populating the bottle_data_dict with the data from DB
        for item in self.bottle_list:
            sku_id = item["sku_id"]
            status = item["status"]
            timestamp = datetime.strptime(item["time_stamp"], "%d-%m-%Y %H:%M")
            rounded_minutes = math.floor(timestamp.minute / 30) * 30
            interval_start = timestamp.replace(minute=rounded_minutes, second=0, microsecond=0)
            interval_end = interval_start + timedelta(minutes=30)
            interval_str = "" + interval_end.strftime("%H:%M")
            self.bottle_data_dict[sku_id][interval_str][status] += 1

        # Creating Chart using the populated data
        self.chart_layout.addWidget(create_chart(self.selected_sku, self.bottle_data_dict))

        # Setting Up and Formatting Combo Box
        self.combo.setStyleSheet(
            "QComboBox { border: 1px solid #c4c4c4; border-radius: 10px; min-width: 10em;min-height:2em;"
            "background: #c4c4c4; font-size:15px;padding: 5px;}"
            "QComboBox QAbstractItemView { margin-top:4px;border-radius: 10px; background: #c4c4c4;}"
            "QComboBox::drop-down { border-color: transparent; } "
            "QComboBox QAbstractItemView::item { "
            "padding: 4px 4px 4px 4px; min-height: 30px; min-width: 40px;border-radius: 10px; }"
            "QComboBox::down-arrow{ image: url(images:arrow.png);width: 16px;height: 16px; margin-right:15px; }"
            "QComboBox::down-arrow:pressed{ image : url(images:down.png);width: 16px;height: 16px; margin-right:15px; }"
            "QListView::item:selected {  color: black; background-color: #969595;}")

        self.combo.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.combo.view().window().setAttribute(Qt.WA_TranslucentBackground)

        self.combo.setModel(ProxyModel(model, 'Select a SKU'))
        self.combo.setCurrentIndex(0)

        self.combo.setView(QListView())
        self.combo.currentIndexChanged.connect(self.onSelectionChange)

        # Horizontal Layout for Combo Label and Combo Box
        h_layout = QHBoxLayout()
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(0, 0, 0, 0)

        label_for_combo = QLabel("SKU Selection:", self)
        label_for_combo.setStyleSheet("font-weight: bold;margin-left:30px;font-size:15px")

        h_layout.addWidget(label_for_combo)
        h_layout.addWidget(self.combo)

        h_layout.addStretch(0)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(10)

        # Vertical Layout for Combo Horizontal layout and the Bar Chart
        v_layout = QVBoxLayout()

        v_layout.addLayout(h_layout)
        v_layout.addLayout(self.chart_layout)

        self.setLayout(v_layout)

    def onSelectionChange(self, index):
        # Index 0 is the placeholder so avoiding 0
        if index != 0:
            # Getting the selected SKU ID
            self.selected_sku = self.sku_id_list[index - 1]

            # Deleting the previous chart
            chart_widget = self.chart_layout.itemAt(0).widget()
            chart_widget.deleteLater()

            # Creating a new chart with the selected SKU ID
            self.chart_layout.addWidget(create_chart(self.selected_sku, self.bottle_data_dict))


###

# Creating a ProxyModel only for showing the Placeholder text in QComboBox ( "Select a SKU" )

###
class ProxyModel(QAbstractProxyModel):
    def __init__(self, model, placeholderText='---', parent=None):
        super().__init__(parent)
        self._placeholderText = placeholderText
        self.setSourceModel(model)

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return self.createIndex(row, column)

    def parent(self, index: QModelIndex = ...) -> QModelIndex:
        return QModelIndex()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().rowCount() + 1 if self.sourceModel() else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.sourceModel().columnCount() if self.sourceModel() else 0

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.row() == 0 and role == Qt.DisplayRole:
            return self._placeholderText
        elif index.row() == 0 and role == Qt.EditRole:
            return None
        else:
            return super().data(index, role)

    def mapFromSource(self, sourceIndex: QModelIndex):
        return self.index(sourceIndex.row() + 1, sourceIndex.column())

    def mapToSource(self, proxyIndex: QModelIndex):
        return self.sourceModel().index(proxyIndex.row() - 1, proxyIndex.column())

    def mapSelectionFromSource(self, sourceSelection: QItemSelection):
        return super().mapSelection(sourceSelection)

    def mapSelectionToSource(self, proxySelection: QItemSelection):
        return super().mapSelectionToSource(proxySelection)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if not self.sourceModel():
            return None
        if orientation == Qt.Vertical:
            return self.sourceModel().headerData(section - 1, orientation, role)
        else:
            return self.sourceModel().headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        return self.sourceModel().removeRows(row, count - 1)
