import sys

import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
import squarify
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QInputDialog, QLineEdit, \
    QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Variables globales
Compo_org_1 = 2.22
Compo_org_2 = 2.22
Taux_expl_1 = 0.35
Taux_expl_2 = 0.35
Total_t = 1496
RapportSecteurs = 1.72


def plotSectors(figure, data):
    """
    Dessine le graphs des secteurs économiques
    :param figure: La figure sur laquelle le graph est crée
    :param data: Les données à afficher
    :return:
    """
    # Crée le graphique
    sectorsGraph = figure.add_subplot(211)

    # Définit la largeur des barres
    width = 0.2

    x = np.arange(len(data))

    # Définit les trois bares de secteur
    sectorsGraph.bar(x, data[:, 0], width, color='#3498db', label='Capital constant (C)')
    sectorsGraph.bar(x + width, data[:, 1], width, color='#e74c3c', label='Capital variable (V)')
    sectorsGraph.bar(x + (2 * width), data[:, 2], width, color='#f1c40f', label='Surplus (S)')

    # Définit les légendes en X
    sectorsGraph.set_xticks(x + width + width / 2)
    sectorsGraph.set_xticklabels(['Secteur 1', 'Secteur 2', 'Total'])

    # Définit la légende en y
    sectorsGraph.set_ylabel('Milliards de CHF')

    # titre
    sectorsGraph.set_title('Année X')

    # Définit la grille
    sectorsGraph.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    # Affiche les légendes des barres
    sectorsGraph.legend()


def CalcYear():
    C_1_t = (Total_t / (RapportSecteurs + 1)) * RapportSecteurs
    V_1_t = C_1_t / Compo_org_1
    S_1_t = V_1_t * Taux_expl_1
    Tot_1_t = C_1_t + V_1_t + S_1_t

    C_2_t = Total_t / (RapportSecteurs + 1)
    V_2_t = C_2_t / Compo_org_2
    S_2_t = V_2_t * Taux_expl_2
    Tot_2_t = C_2_t + V_2_t + S_2_t

    C_3_t = C_1_t + C_2_t
    V_3_t = V_1_t + V_2_t
    S_3_t = S_1_t + S_2_t
    Tot_3_t = C_3_t + V_3_t + S_3_t

    Acc_t = Tot_1_t - (C_1_t + C_2_t)
    """""
    #On convertit tout en int
    C_1_t = int(C_1_t)
    V_1_t = int(V_1_t)
    S_1_t = int(S_1_t)
    C_2_t = int(C_2_t)
    V_2_t = int(V_2_t)
    S_2_t = int(S_2_t)
    C_3_t = int(C_3_t)
    V_3_t = int(V_3_t)
    S_3_t = int(S_3_t)
    """""

    TabResultat = [[C_1_t, V_1_t, S_1_t], [C_2_t, V_2_t, S_2_t], [C_3_t, V_3_t, S_3_t]]
    return TabResultat


def gettotal(TabResultats):
    Total = 0
    for i in range(len(TabResultats)):
        Total = Total + TabResultats[i]
    return Total


# def dynemisesizeaquar(value, total):
#     AffValue = value / total
#     AffPro = (1 - AffValue) / 3
#     AffichageDynamique = [AffPro, AffValue, AffPro, AffPro]
#     return AffichageDynamique

class ParamWidget(QWidget):
    """
    Fenêtre de modification des paramètres
    """

    def __init__(self):
        """
        Constructeur de la fenêtre des paramètres
        """
        super(ParamWidget, self).__init__()
        self.initParamWidget()

    def initParamWidget(self):
        """
        Initialise la fenêtre des paramètres
        :return:
        """
        # Taille du widget
        self.setGeometry(100, 100, 800, 480)

        # Grille
        grid = QGridLayout()
        grid.setContentsMargins(150, 0, 150, 0)
        self.setLayout(grid)

        # Labels et inputs
        labExp1 = QLabel("Taux d'exploitation du secteur 1 :", self)
        ediExp1 = QLineEdit(str(Taux_expl_1))
        grid.addWidget(labExp1, 1, 1)
        grid.addWidget(ediExp1, 1, 2)

        labExp2 = QLabel("Taux d'exploitation du secteur 2 :", self)
        ediExp2 = QLineEdit(str(Taux_expl_2))
        grid.addWidget(labExp2, 2, 1)
        grid.addWidget(ediExp2, 2, 2)

        labOrga1 = QLabel("Composition organique du secteur 1 :", self)
        ediOrga1 = QLineEdit(str(Compo_org_1))
        grid.addWidget(labOrga1, 3, 1)
        grid.addWidget(ediOrga1, 3, 2)

        labOrga2 = QLabel("Composition organique du secteur 2 :", self)
        ediOrga2 = QLineEdit(str(Compo_org_2))
        grid.addWidget(labOrga2, 4, 1)
        grid.addWidget(ediOrga2, 4, 2)

        labRapports = QLabel("Rapports entre les secteurs :", self)
        ediRapports = QLineEdit(str(RapportSecteurs))
        grid.addWidget(labRapports, 5, 1)
        grid.addWidget(ediRapports, 5, 2)

        labTotal = QLabel("Total :", self)
        ediTotal = QLineEdit(str(Total_t))
        grid.addWidget(labTotal, 6, 1)
        grid.addWidget(ediTotal, 6, 2)

        # Bouton annuler
        btnCancel = QPushButton('Annuler', self)
        btnCancel.clicked.connect(self.Cancel)
        grid.addWidget(btnCancel, 7, 1)

        # Bouton enregistrer
        btnModify = QPushButton('Enregistrer', self)
        btnModify.resize(btnModify.sizeHint())
        btnModify.clicked.connect(
            lambda: self.Save(ediOrga1.text(), ediOrga2.text(), ediExp1.text(), ediExp2.text(), ediRapports.text(),
                              ediTotal.text()))
        grid.addWidget(btnModify, 7, 2)

    def Cancel(self):
        """
        Annule la modification des paramètres et ferme la fenêtre
        :return:
        """
        self.hide()

    def Save(self, orga1, orga2, expl1, expl2, sectors, total):
        """
        Enregistre les nouvelles valeurs des paramètres
        :param orga1: Nouvelle composition organique du secteur 1
        :param orga2: Nouvelle composition organique du secteur 2
        :param expl1: Nouveaux taux d'exploitation du secteur 1
        :param expl2: Nouveaux taux d'exploitation du secteur 2
        :param sectors: Nouveau rapport entre les secteurs
        :param total: Nouveau total
        :return:
        """
        # Modifie les valeurs des paramètres globaux
        global Compo_org_1
        Compo_org_1 = float(orga1)

        global Compo_org_2
        Compo_org_2 = float(orga2)

        global Taux_expl_1
        Taux_expl_1 = float(expl1)

        global Taux_expl_2
        Taux_expl_2 = float(expl2)

        global RapportSecteurs
        RapportSecteurs = float(sectors)

        global Total_t
        Total_t = float(total)

        # Réactualise les graphiques
        mainWidget.plotGraphs()

        # Ferme le widget des paramètres
        self.hide()



class MainWidget(QWidget):
    """
    Fenêtre principale de l'application
    """

    def __init__(self):
        """
        Constructeur de la fenêtre principale
        """
        super(MainWidget, self).__init__()
        self.initMainWidget()

    def initMainWidget(self):
        """
        Initialise la fenêtre principale
        :return:
        """
        self.setGeometry(100, 100, 800, 480)

        grid = QGridLayout()
        self.setLayout(grid)

        btn1 = QPushButton(self)
        btn1.resize(btn1.sizeHint())
        btn1.setIcon(QIcon("parameters.png"))
        btn1.clicked.connect(self.openParamWidget)
        grid.addWidget(btn1, 1, 0)

        btn2 = QPushButton('Plot 2 ', self)
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.plotGraphs)
        grid.addWidget(btn2, 3, 0)

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 2, 0, 1, 1)

        #Dessine les graphiques
        self.plotGraphs()

        self.show()

    def openParamWidget(self):
        """
        Instancie, puis affiche une fenêtre de modification des paramètres
        :return:
        """

        self.paramWidget = ParamWidget()
        self.paramWidget.show()
        # self.hide()

    def plotGraphs(self):
        """
        Dessine les graphiques sur la page principale
        :return:
        """

        # Remise à zéro
        self.figure.clf()

        # Données de l'année une
        DataYearOne = CalcYear()

        #Dessine le graphique des secteurs
        plotSectors(self.figure, np.array(DataYearOne))

        #Dessine le graphique des totaux
        Tot_1_t = gettotal(DataYearOne[0])
        Tot_2_t = gettotal(DataYearOne[1])
        #Tot_3_t = gettotal(DataYearOne[2])

        totalsGraph = self.figure.add_subplot(212)
        squarify.plot(sizes=[Tot_1_t, Tot_2_t], label=['Total S1', 'Total S2'], color=['#3498db', '#e74c3c'], alpha=.8,
                      ax=totalsGraph)
        totalsGraph.axis('off')

        self.canvas.draw()


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
mainWidget = MainWidget()
sys.exit(app.exec_())
