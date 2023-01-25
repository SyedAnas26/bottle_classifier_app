from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QFrame, QPushButton, QLayout
from PySide2 import QtCore, QtGui, QtWidgets


# Thumbnail Image Widget class
class ThumbWidget(QtWidgets.QFrame):

    def __init__(self, bottle_quality, pixmap, parent=None):
        super().__init__(parent)

        # Setting up the Frame and size for each Image
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setFixedSize(192, 192)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Setting the image in a QLabel
        pixmap_label = QtWidgets.QLabel(pixmap=pixmap, scaledContents=True)

        # Color Codes for Bottom Line
        line_color_codes = {"Bad": "#ff0f0f", "Good": "#51ff47"}

        bottom_line = QFrame()
        bottom_line.setStyleSheet(f"background:{line_color_codes[bottle_quality]};min-height:8px;")

        # Adding the image and line widgets
        layout.addWidget(pixmap_label)
        layout.addWidget(bottom_line)


class ImageGallery(QtWidgets.QMainWindow):

    def __init__(self, bottle_collection, parent=None):
        super().__init__(parent)

        # Fetching Bottles data using the MongoDB collection
        self.bottle_list = list(bottle_collection.find())

        # Creating a List Widget to show the list of Images
        self.product_list_widget = QtWidgets.QListWidget(
            viewMode=QtWidgets.QListWidget.IconMode,
            iconSize=QtCore.QSize(192, 192),
            resizeMode=QtWidgets.QListWidget.Adjust,
            movement=QtWidgets.QListWidget.Static,
        )

        # Creating Button Filters
        self.all_button = QPushButton("ALL")
        self.good_button = QPushButton("GOOD")
        self.bad_button = QPushButton("BAD")

        # Initializing the UI
        self.init_UI()

    def init_UI(self):

        self.product_list_widget.setGridSize(QtCore.QSize(192 + 12, 192 + 12))
        self.product_list_widget.setFrameStyle(QFrame.NoFrame)

        # Adding the items to List Widget
        self.populateListItems(self.bottle_list)

        self.all_button.setFixedSize(70, 30)
        self.good_button.setFixedSize(90, 30)
        self.bad_button.setFixedSize(80, 30)

        self.all_button.clicked.connect(self.onButtonClick)
        self.good_button.clicked.connect(self.onButtonClick)
        self.bad_button.clicked.connect(self.onButtonClick)

        self.all_button.setCheckable(True)
        self.good_button.setCheckable(True)
        self.bad_button.setCheckable(True)

        self.setStyleSheet(
            "QPushButton { background-color: lightgray;color: black;padding: 2px;font: bold 14px;border-radius: 4px; } "
            "QPushButton:hover { background-color: #75b7f0 }"
            "QPushButton:checked { background-color: #75b7f0 }")

        # Horizontal Layout for Button Filters
        button_layout = QHBoxLayout()
        button_layout.setSizeConstraint(QLayout.SetMaximumSize)
        button_layout.addStretch(0)
        button_layout.setContentsMargins(0, 0, 20, 0)
        button_layout.setSpacing(10)

        button_layout.addWidget(self.all_button, 0, Qt.AlignRight)
        button_layout.addWidget(self.good_button, 0, Qt.AlignRight)
        button_layout.addWidget(self.bad_button, 0, Qt.AlignRight)

        # Creating Vertical layout and adding filters and List Widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        layout.addLayout(button_layout)
        layout.addWidget(self.product_list_widget)

        layout.setSpacing(30)
        layout.setContentsMargins(10, 30, 10, 20)

    def populateListItems(self, bottle_data):

        # Clearing the list items before adding
        self.product_list_widget.clear()

        # Creating List Item for each Bottle Document (BSON)
        for bottle in bottle_data:
            # Widget Creation
            item = QtWidgets.QListWidgetItem()
            item_widget = ThumbWidget(bottle['status'], QtGui.QPixmap(f"images:{bottle['unit_id']}.jpg"))
            item.setSizeHint(QtCore.QSize(192, 192))

            self.product_list_widget.addItem(item)
            self.product_list_widget.setItemWidget(item, item_widget)

    def onButtonClick(self):
        # Unchecking previously checked buttons
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            if button is not self.sender():
                button.setChecked(False)

        # Filtering the list according to the Filter Button selection ("All,"Good","Bad")
        filtered_list = []
        if self.sender().text() == "ALL" or self.sender().isChecked() is False:
            filtered_list = self.bottle_list
        elif self.sender().text() == "GOOD":
            filtered_list = list(filter(lambda d: d['status'] == "Good", self.bottle_list))
        elif self.sender().text() == "BAD":
            filtered_list = list(filter(lambda d: d['status'] == "Bad", self.bottle_list))

        self.populateListItems(filtered_list)
