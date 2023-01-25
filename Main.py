import os
import sys

from PySide2.QtCore import QDir
from PySide2.QtWidgets import QApplication, QTabWidget

from components.Analytics import Analytics
from components.ImageGallery import ImageGallery

from pymongo import MongoClient

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabs = QTabWidget()

    root = os.path.dirname(os.path.abspath(__file__))
    QDir.addSearchPath('images', os.path.join(root, 'images'))

    # Connecting MongoDb and fetching database
    client = MongoClient("mongodb://localhost:27017/")
    my_database = client['bottle_classifier_db']
    my_collection = my_database['bottles']

    # Creating Tabs [ Analytics , Image Gallery ]
    tabs.addTab(Analytics(my_collection), "Analytics")
    tabs.addTab(ImageGallery(my_collection), "Image Gallery")
    tabs.setWindowTitle("Bottle Classifier")
    tabs.setStyleSheet(
        "QTabWidget::pane { border: 2px solid lightgray;  top:-1px;   background: rgb(245, 245, 245); }"
        "QTabBar::tab { background: rgb(230, 230, 230); border: 2px solid lightgray; padding: 12px; width:120px }"
        "QTabBar::tab:selected { background: rgb(245, 245, 245);  margin-bottom: -1px;  }"
        "QTabBar::tab { margin-left:2px; margin-right:2px; font-size:15px; font-weight:bold}")

    tabs.show()
    sys.exit(app.exec_())
