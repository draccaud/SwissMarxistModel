import sys
import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
from enum import Enum
import squarify
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QFormLayout, QMessageBox, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Variables globales
current_year = 1
production_records = []
# Composition organique des secteurs 1 et 2
organic_composition_1 = 2.22
organic_composition_2 = 2.22
# Taux d'exploitation des secteurs 1 et 2
rate_of_exploitation_1 = 0.35
rate_of_exploitation_2 = 0.35
sectors_ratio = 1.72
production_total = 1496


# Modes d'accumulation
class AccumulationMode(Enum):
    BALANCED = 0
    CONSTANT_CAPITAL_MAXIMISATION = 1
    VARIABLE_CAPITAL_MAXIMISATION = 2


# Mode d'accumulation actuelle
accumulation_mode = AccumulationMode.BALANCED


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
    sectorsGraph.set_title('Année ' + str(current_year))

    # Définit la grille
    sectorsGraph.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    # Affiche les légendes des barres
    # sectorsGraph.legend()


def CalcFirstYear():
    """
    Calcul les données de la première année
    :return:
    """
    # Total du secteur 1
    total1 = production_total / (sectors_ratio + 1) * sectors_ratio
    # Capital constant du secteur 1
    constantCapital1 = organic_composition_1 / (organic_composition_1 + rate_of_exploitation_1 + 1) * total1
    # Capital variable du secteur 1
    variableCapital1 = constantCapital1 / organic_composition_1
    # Surplus du secteur 1
    surplus1 = variableCapital1 * rate_of_exploitation_1

    # Total du secteur 2
    total2 = production_total / (sectors_ratio + 1)
    # Capital constant du secteur 2
    constantCapital2 = organic_composition_2 / (organic_composition_2 + rate_of_exploitation_2 + 1) * total2
    # Capital variable du secteur 2
    variableCapital2 = constantCapital2 / organic_composition_2
    # Surplus du secteur 2
    surplus2 = variableCapital2 * rate_of_exploitation_2

    # Total de capital constant
    constantCapitalTotal = constantCapital1 + constantCapital2
    # Total de capital variable
    variableCapitalTotal = variableCapital1 + variableCapital2
    # Surplus total
    surplusTotal = surplus1 + surplus2

    # Accumulation
    accumulation = total1 - (constantCapital1 + constantCapital2)

    global production_records
    production_records = [[constantCapital1, variableCapital1, surplus1, total1, constantCapital2, variableCapital2,
                           surplus2, total2, constantCapitalTotal, variableCapitalTotal, surplusTotal, production_total,
                           accumulation]]


def CalcNextYear():
    """
    Calcul les données de l'année suivante
    :return:
    """
    # Récupère la variable globale
    global current_year

    # Récupère l'accumulation de l'année précédente
    latsYearAccumulation = production_records[current_year - 2][12]

    # Capital constant du secteur 1
    constantCapital1 = production_records[current_year - 2][0] + (latsYearAccumulation * (organic_composition_1 /
                                                                                          (organic_composition_1 + 1)))
    # Capital variable du secteur 2
    variableCapital1 = constantCapital1 / organic_composition_1
    # Surplus du secteur 1
    surplus1 = variableCapital1 * rate_of_exploitation_1
    # Total du secteur 1
    sector1Total = constantCapital1 + variableCapital1 + surplus1

    # Capital constant du secteur 1
    constantCapital2 = production_records[(current_year - 2)][4] + latsYearAccumulation - \
                       (constantCapital1 - production_records[current_year - 2][0])
    # Capital variable du secteur 2
    variableCapital2 = constantCapital2 / organic_composition_2
    # Surplus du secteur 2
    surplus2 = variableCapital2 * rate_of_exploitation_2
    # Total du secteur 2
    sector2Total = constantCapital2 + variableCapital2 + surplus2

    # Total du capital constant
    constantCapitalTotal = constantCapital1 + constantCapital2
    # Total du capital variable
    variableCapitalTotal = variableCapital1 + variableCapital2
    # Surplus total
    surplusTotal = surplus1 + surplus2
    # Total de la production
    productionTotal = constantCapitalTotal + variableCapitalTotal + surplusTotal

    # Accumulation
    accumulation = sector1Total - constantCapitalTotal

    production_records.append([constantCapital1, variableCapital1, surplus1, sector1Total, constantCapital2,
                               variableCapital2, surplus2, sector2Total, constantCapitalTotal, variableCapitalTotal,
                               surplusTotal, productionTotal, accumulation])


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
        Instancie la fenêtre des paramètres
        :return:
        """
        # Définit la taille de la fenêtre
        self.setGeometry(100, 100, 800, 480)

        # Layout principal
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Layout des paramètres
        paramLayout = QFormLayout()
        mainLayout.addLayout(paramLayout)
        # mainLayout.setContentsMargins(150, 100, 150, 100)

        # Taux d'exploitation du secteur 1
        editRateOfExploitation1 = QLineEdit(str(rate_of_exploitation_1))
        paramLayout.addRow(QLabel("Taux d'exploitation du secteur 1 :"), editRateOfExploitation1)

        # Taux d'exploitation du secteur 2
        editRateOfExploitation2 = QLineEdit(str(rate_of_exploitation_2))
        paramLayout.addRow(QLabel("Taux d'exploitation du secteur 2 :"), editRateOfExploitation2)

        # Composition organique du secteur 1
        editOrganicComposition1 = QLineEdit(str(organic_composition_1))
        paramLayout.addRow(QLabel("Composition organique du secteur 1 :"), editOrganicComposition1)

        # Composition organique du secteur 2
        editOrganicComposition2 = QLineEdit(str(organic_composition_2))
        paramLayout.addRow(QLabel("Composition organique du secteur 2 :"), editOrganicComposition2)

        # Rapport entre les secteurs
        editSectorsRatio = QLineEdit(str(sectors_ratio))
        paramLayout.addRow(QLabel("Rapports entre les secteurs :"), editSectorsRatio)

        # Total de la production
        editProductionTotal = QLineEdit(str(production_total))
        paramLayout.addRow(QLabel("Total :"), editProductionTotal)

        # Mode d'accumulation
        cbAccumulationMode = QComboBox()
        cbAccumulationMode.addItem("Équilibré", AccumulationMode.BALANCED.value)
        cbAccumulationMode.addItem("Maximisation du capital constant",
                                   AccumulationMode.CONSTANT_CAPITAL_MAXIMISATION.value)
        cbAccumulationMode.addItem("Maximisation du capital variable",
                                   AccumulationMode.VARIABLE_CAPITAL_MAXIMISATION.value)
        # Affiche de base le mode d'accumulation actuelle
        cbAccumulationMode.setCurrentIndex(accumulation_mode.value)
        paramLayout.addRow(QLabel("Mode d'accumulation :"), cbAccumulationMode)

        # Ligne des boutons
        buttonsLayout = QHBoxLayout()
        mainLayout.addLayout(buttonsLayout)

        # Bouton annuler
        btnCancel = QPushButton()
        btnCancel.setIcon(QIcon("cancel.png"))
        btnCancel.clicked.connect(self.Cancel)
        buttonsLayout.addWidget(btnCancel)

        # Bouton enregistrer
        btnSave = QPushButton()
        btnSave.setIcon(QIcon("save.png"))
        buttonsLayout.addWidget(btnSave)
        btnSave.clicked.connect(lambda: self.Save(editOrganicComposition1.text(), editOrganicComposition2.text(),
                                                  editRateOfExploitation1.text(), editRateOfExploitation2.text(),
                                                  editSectorsRatio.text(), editProductionTotal.text(),
                                                  cbAccumulationMode.currentData()))

    def Cancel(self):
        """
        Annule la modification des paramètres et ferme la fenêtre
        :return:
        """
        self.hide()

    def Save(self, organicComposition1, organicComposition2, rateExploitation1, rateOfExploitation2, sectorsRatio,
             productionTotal, accumulationMode):
        """
        Enregistre les nouvelles valeurs des paramètres
        :param organicComposition1: Nouvelle composition organique du secteur 1
        :param organicComposition2: Nouvelle composition organique du secteur 2
        :param rateExploitation1: Nouveaux taux d'exploitation du secteur 1
        :param rateOfExploitation2: Nouveaux taux d'exploitation du secteur 2
        :param sectorsRatio: Nouveau rapport entre les secteurs
        :param productionTotal: Nouveau total de production
        :param accumulationMode: Nouveau mode de production
        :return:
        """
        # Récupère les variables globales
        global organic_composition_1
        global organic_composition_2
        global rate_of_exploitation_1
        global rate_of_exploitation_2
        global sectors_ratio
        global production_total
        global accumulation_mode

        try:
            # Tente de convertir en float les inputs
            organicComposition1 = float(organicComposition1)
            organicComposition2 = float(organicComposition2)
            rateExploitation1 = float(rateExploitation1)
            rateOfExploitation2 = float(rateOfExploitation2)
            sectorsRatio = float(sectorsRatio)
            productionTotal = float(productionTotal)
            accumulation_mode = AccumulationMode(accumulationMode)
        except ValueError:
            # Si une exception est soulevée, affiche une erreur
            QMessageBox.about(self, "Erreur", "Saisie invalide")
        else:
            # Si les inputs sont supérieurs à zéro
            if organicComposition1 > 0 and organicComposition2 > 0 and rateExploitation1 > 0 \
                    and rateOfExploitation2 > 0 and sectorsRatio > 0 and productionTotal > 0:
                # Actualise les variables globales
                organic_composition_1 = organicComposition1
                organic_composition_2 = organicComposition2
                rate_of_exploitation_1 = rateExploitation1
                rate_of_exploitation_2 = rateOfExploitation2
                sectors_ratio = sectorsRatio
                production_total = productionTotal

                # Réactualise les graphiques
                mainWidget.plotGraphs()
                # Ferme le widget des paramètres
                self.hide()
            else:
                # Sinon affiche une erreur
                QMessageBox.about(self, "Erreur", "Saisie inférieur à zéro")


class MainWidget(QWidget):
    """
    Fenêtre principale de l'application
    """

    def __init__(self):
        """
        Constructeur de la fenêtre principale
        """
        super(MainWidget, self).__init__()
        # Instancie le bouton previous ici afin de pouvoir le rendre (in)actif depuis une méthode
        self.btnPrevious = QPushButton()
        # Instancie la figure et le canevas ici afin de pouvoir les atteindre depuis une méthode
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)

        self.initMainWidget()

    def initMainWidget(self):
        """
        Instancie la fenêtre principale
        :return:
        """
        # Définit la taille de la fenêtre
        self.setGeometry(100, 100, 800, 480)

        # Layout principal
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Haut de la fenêtre
        topLayout = QHBoxLayout()
        mainLayout.addLayout(topLayout)

        # Bouton info
        btnInfo = QPushButton()
        btnInfo.setIcon(QIcon("info.png"))
        btnInfo.clicked.connect(self.openParamWidget)
        topLayout.addWidget(btnInfo)

        # Bouton reset
        btnReset = QPushButton()
        btnReset.setIcon(QIcon("reset.png"))
        btnReset.clicked.connect(self.reset)
        topLayout.addWidget(btnReset)

        # Bouton paramètres
        btnParam = QPushButton()
        btnParam.setIcon(QIcon("param.png"))
        btnParam.clicked.connect(self.openParamWidget)
        topLayout.addWidget(btnParam)

        # Ajoute le canevas au layout principal
        mainLayout.addWidget(self.canvas)

        # Layout du bas
        bottomLayout = QHBoxLayout()
        mainLayout.addLayout(bottomLayout)

        # Bouton précédent
        self.btnPrevious.setIcon(QIcon("previous.png"))
        self.btnPrevious.clicked.connect(self.previous)
        bottomLayout.addWidget(self.btnPrevious)
        # Désactive, de base, le bouton
        self.btnPrevious.setEnabled(False)

        # Bouton étape par étape
        btnStepByStep = QPushButton()
        btnStepByStep.setIcon(QIcon("stepByStep.png"))
        btnStepByStep.clicked.connect(self.plot_clustered_stacked)
        bottomLayout.addWidget(btnStepByStep)

        # Bouton suivant
        btnNext = QPushButton()
        btnNext.setIcon(QIcon("next.png"))
        btnNext.clicked.connect(self.next)
        bottomLayout.addWidget(btnNext)

        # Dessine les graphiques
        self.plotGraphs()
        self.show()

    @staticmethod
    def openParamWidget():
        """
        Instancie, puis affiche une fenêtre de modification des paramètres
        :return:
        """
        paramWidget = ParamWidget()
        paramWidget.show()

    def reset(self):
        """
        Remet à zéro les paramètres et affiche le graphique initial
        :return:
        """
        # Remet à zéro les paramètres
        global production_records
        production_records = []
        global organic_composition_1
        organic_composition_1 = 2.22
        global organic_composition_2
        organic_composition_2 = 2.22
        global rate_of_exploitation_1
        rate_of_exploitation_1 = 0.35
        global rate_of_exploitation_2
        rate_of_exploitation_2 = 0.35
        global production_total
        production_total = 1496
        global sectors_ratio
        sectors_ratio = 1.72
        global current_year
        current_year = 1

        # Désactive le bouton previous
        mainWidget.btnPrevious.setEnabled(False)

        # Dessine le graphique
        self.plotGraphs()

    def openInfoWidget(self):
        return

    def plotGraphs(self):
        """
        Dessine les graphiques sur la page principale
        :return:
        """
        global production_records

        # Remise à zéro
        self.figure.clf()

        # Si année, calcule les données de la première année
        if current_year == 1:
            CalcFirstYear()

        # Récupère les données à afficher
        GraphData = np.array([[production_records[current_year - 1][0], production_records[current_year - 1][1],
                               production_records[current_year - 1][2]], [production_records[current_year - 1][4],
                                                                          production_records[current_year - 1][5],
                                                                          production_records[current_year - 1][6]],
                              [production_records[current_year - 1][8], production_records[current_year - 1][9],
                               production_records[current_year - 1][10]]])

        # Appelle la fonction qui dessine le grphique des secteurs
        plotSectors(self.figure, GraphData)

        # Dessine le graph des totaux
        totalsGraph = self.figure.add_subplot(212)
        squarify.plot(sizes=[production_records[current_year - 1][3], production_records[current_year - 1][7]],
                      label=['Total S1', 'Total S2'], color=['#3498db', '#e74c3c'], alpha=.8, ax=totalsGraph)
        # Enlève les axes du graphique
        totalsGraph.axis('off')

        #Mets à jour le canevas
        self.canvas.draw()

    def next(self):
        """
        Passe à l'année suivante
        :return:
        """
        # Récupère la variable globale
        global current_year
        # Avance d'une année
        current_year = current_year + 1

        global production_records

        # Si pas année une
        if production_records[current_year - 2]:
            CalcNextYear()

        # Active le bouton permettant de revenir en arrière
        mainWidget.btnPrevious.setEnabled(True)
        self.plotGraphs()

    def previous(self):
        """
        Passe à l'année précédente
        :return:
        """
        # Récupère la variable global
        global current_year

        # Si l'année actuelle n'est pas la première
        if current_year > 1:
            # Recule d'une année
            current_year = current_year - 1

            # Si on retourne à la première année, désactive le bouton de retour en arrière
            if current_year == 1:
                mainWidget.btnPrevious.setEnabled(False)

            self.plotGraphs()

    def plot_clustered_stacked(self, dfall=[], **kwargs):

        # create fake dataframes
        # Les c
        df1 = pd.DataFrame(np.array([[588, 0], [342, 80], [930, 0]]))

        # Les v
        df2 = pd.DataFrame(np.array([[265, 0], [154, 0], [419, 0]]))

        # Les s
        df3 = pd.DataFrame(np.array([[93, 0], [54, 0], [147, 0]]))

        dfall = [df1, df2, df3]

        self.figure.clf()

        axe = self.figure.add_subplot(211)

        for df in dfall:  # for each data frame
            axe = df.plot(kind="bar",
                          linewidth=0,
                          stacked=True,
                          ax=axe,
                          legend=False,
                          grid=False,
                          **kwargs)  # make bar plots

        count = 0

        h, l = axe.get_legend_handles_labels()  # get the handles we want to modify
        for i in range(0, 6, 2):  # len(h) = n_col * n_df
            for j, pa in enumerate(h[i:i + 2]):
                for rect in pa.patches:  # for each index
                    rect.set_x(rect.get_x() + 1 / 4 * i / 2)
                    rect.set_width(1 / 4)

                    if count <= 2:
                        rect.set_color("#3498db")
                    elif count == 6 or count == 7 or count == 8:
                        rect.set_color("#e74c3c")
                    elif count == 12 or count == 13 or count == 14:
                        rect.set_color("#f1c40f")

                    count = count + 1

        axe.set_xticks((np.arange(0, 6, 2) + 1 / 4) / 2)
        axe.set_xticklabels(["Secteur 1", "Secteur 2", "Total"], rotation=0)

        # Définit la grille
        axe.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        # l1 = axe.legend(h[:2], ["base", "ajout"], loc=[1.01, 0.5])
        # axe.add_artist(l1)

        totalsGraph = self.figure.add_subplot(212)
        squarify.plot(sizes=[946, 550], label=['Total S1', 'Total S2'], color=['#3498db', '#e74c3c'], alpha=.8,
                      ax=totalsGraph)
        totalsGraph.axis('off')

        self.canvas.draw()


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
mainWidget = MainWidget()
sys.exit(app.exec_())
