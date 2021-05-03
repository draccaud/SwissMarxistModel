import random
import sys

import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
import squarify
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PrettyWidget(QWidget):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        grid = QGridLayout()
        self.setLayout(grid)

        btn1 = QPushButton('Plot 1 ', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(self.plot1)
        grid.addWidget(btn1, 5, 0)

        btn2 = QPushButton('Plot 2 ', self)
        btn2.resize(btn2.sizeHint())
        # btn2.clicked.connect(self.plot2)
        grid.addWidget(btn2, 5, 1)

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 3, 0, 1, 2)

        self.show()

    def plot1(self):
        self.figure.clf()

        ax1 = self.figure.add_subplot(211)

        # Values of each group
        bars1 = [12, 28, 1, 8, 22]
        bars2 = [28, 7, 16, 4, 10]
        bars3 = [25, 3, 23, 25, 17]

        # Heights of bars1 + bars2
        bars = np.add(bars1, bars2).tolist()

        # The position of the bars on the x-axis
        r = [0, 1, 2, 3, 4]

        bar_width = 1

        # Create brown bars
        ax1.axes.bar(r, bars1, color='#7f6d5f', edgecolor='white', width=bar_width)
        # Create green bars (middle), on top of the first ones
        ax1.axes.bar(r, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=bar_width)
        # Create green bars (top)
        ax1.axes.bar(r, bars3, bottom=bars, color='#2d7f5e', edgecolor='white', width=bar_width)

        ax1.plot()

        ax2 = self.figure.add_subplot(234)
        df = pd.DataFrame({'nb_people': [random.randint(1, 10) for _ in range(4)],
                           'group': ["group A", "group B", "group C", "group D"]})

        squarify.plot(sizes=df['nb_people'], label=df['group'], alpha=.8, ax=ax2)
        ax2.axis('off')

        ax3 = self.figure.add_subplot(235)
        df = pd.DataFrame({'nb_people': [random.randint(1, 10) for _ in range(4)],
                           'group': ["group A", "group B", "group C", "group D"]})

        squarify.plot(sizes=df['nb_people'], label=df['group'], alpha=.8, ax=ax3)
        ax3.axis('off')

        ax4 = self.figure.add_subplot(236)
        df = pd.DataFrame({'nb_people': [random.randint(1, 10) for _ in range(4)],
                           'group': ["group A", "group B", "group C", "group D"]})

        squarify.plot(sizes=df['nb_people'], label=df['group'], alpha=.8, ax=ax4)
        ax4.axis('off')

        self.canvas.draw()

        self.canvas.draw_idle()

    def plot2(self):
        return


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
GUI = PrettyWidget()
sys.exit(app.exec_())
