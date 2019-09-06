import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.url = 'https://habr.com/ru/news/'
        self.window = QWidget()

        self.table = QTableWidget(self.window)
        self.create_window()
        self.window.show()

    def create_window(self):
        self.window.setMinimumSize(QSize(600, 500))
        self.window.setWindowTitle(self.url)
        grid_layout = QGridLayout()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(["Title", "Author", "Reference", "Comments", "Rating"])

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)

        grid_layout.addWidget(self.table, 0, 0)
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        menu = mainMenu.addMenu('Laba')

        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.about)
        helpAction = QAction('Help', self)
        helpAction.triggered.connect(self.help)

        menu.addAction(aboutAction)
        menu.addAction(helpAction)

        grid_layout.setMenuBar(mainMenu)
        self.window.setLayout(grid_layout)

    def about(self):
        QMessageBox.about(self, "About", "Palochkin Ilya\n8-T3O-301B-16")

    def help(self):
        QMessageBox.about(self, "Help", "List of news from Habr")

    def parse(self):
        try:
            r = requests.get(self.url)
            soup = BeautifulSoup(r.content, 'html.parser')

            data = soup.find_all("article", {"class": "post post_preview"})
            self.table.setRowCount(len(data))
            i = 0
            for item in data:
                titles = item.find_all("a", {"class": "post__title_link"})
                for title in titles:
                    self.table.setItem(i, 0, QTableWidgetItem(title.text))

                authors = item.find_all("span", {"class": "user-info__nickname user-info__nickname_small"})
                for author in authors:
                    self.table.setItem(i, 1, QTableWidgetItem(author.text))

                urls = item.find_all("h2", {"class": "post__title"})
                for url in urls:
                    a = url.find('a')
                    self.table.setItem(i, 2, QTableWidgetItem(a.get('href')))

                ratings = item.find_all("span", {"class": "voting-wjt__counter"})
                for rating in ratings:
                    self.table.setItem(i, 4, QTableWidgetItem(rating.text))

                comments = item.find_all("span", {"class": "post-stats__comments-count"})
                if comments:
                    for comment in comments:
                        self.table.setItem(i, 3, QTableWidgetItem(comment.text))
                else:
                    self.table.setItem(i, 3, QTableWidgetItem("0"))
                i += 1

            self.table.resizeColumnsToContents()
            return True
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Access denied")
            msg.setWindowTitle("Error!")
            msg.setDetailedText("Can't get info from:\n" + self.url)
            msg.exec_()
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    result = mw.parse()
    if result:
        sys.exc_info()
        app.exec_()
