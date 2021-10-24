from tkinter import Entry, Widget

chiffres = [str(x) for x in range(1,10)]

class Cellule:

  def __init__(self, entry):
    self.entry: Entry = entry
    self.possibilites: list = []
    self.ligne: Ligne
    self.colonne: Colonne
    self.region: Region
    self.numero_de_ligne: int
    self.numero_de_colonne: int

  def est_vide(self) -> bool:
    return self.entry.get() == ""
  def est_pas_vide(self) -> bool:
    return self.est_vide() == False
  def contient(self, valeur) -> bool:
    return self.entry.get() == valeur
  def clear(self):
    self.entry.delete(0)
  def set(self, valeur):
    self.possibilites.clear()
    valeur = str(valeur)
    self.ligne.chiffres_manquants.remove(valeur)
    self.colonne.chiffres_manquants.remove(valeur)
    self.region.chiffres_manquants.remove(valeur)
    self.entry.delete(0)
    self.entry.insert(0, valeur)

  ##### Méthode de résolution

  def identifyPossibilities(self):
    if (self.est_vide()):
      for chiffre in chiffres:
        if (self.ligne.contient(chiffre) == False
          and self.colonne.contient(chiffre) == False
          and self.region.contient(chiffre) == False):
          if (chiffre not in self.possibilites):
            self.possibilites.append(chiffre)
        else:
          if (chiffre in self.possibilites):
            self.possibilites.remove(chiffre)
      # print("Possibilités:", cell.possibilites)
      if (len(self.possibilites) == 1):
        chiffre = self.possibilites[0]
        print("Inscription de", chiffre, "en ", self.numero_de_ligne, self.numero_de_colonne,": seule valeur possible")
        self.set(chiffre)
        self.ligne.updatePossibilites()
        self.colonne.updatePossibilites()
        self.region.updatePossibilites()
        return True
    return False


  def __str__(self):
    val = self.entry.get()
    if (val == ""):
      val = " "
    return val

class Zone:
  def __init__(self):
    self.list: list = []
    self.chiffres_manquants = chiffres.copy()

  def getCellule(self, index) -> Cellule:
    return self.list[index]

  def contient(self, val) -> bool:
    for cell in self.list:
      if (cell.contient(val)):
        return True
    return False

  def nbVal(self) -> int:
    nb = 0
    for cell in self.list:
      if (cell.est_pas_vide()):
        nb += 1
    return nb

  def setChiffresManquants(self):
    cell: Cellule
    for cell in self.list:
      self.chiffres_manquants += cell.possibilites
    self.chiffres_manquants = list(set(self.chiffres_manquants))

  def updatePossibilites(self):
    cell: Cellule
    for cell in self.list:
      cell.identifyPossibilities()

  # def __str__(self):
  #   return str([cell.__str__() for cell in self.zone])

class Ligne(Zone):
  def __str__(self):
    return "|".join([cell.__str__() for cell in self.list])
class Colonne(Zone):
  pass
class Region(Zone):
  pass

class Sudoku:
  def __init__(self):
    self.grilleL = [Ligne() for x in range(9)]
    self.grilleC = [Colonne() for x in range(9)]
    self.grilleR = [Region() for x in range(9)]
    self.blocage = False
    self.blocageTKWidget: Widget

  def __str__(self):
    return str("\n".join([ligne.__str__() for ligne in self.grilleL]))

  def fill(self, valeurs):
    for indexDeLigne, table in enumerate(valeurs):
      for indexDeColonne, val in enumerate(table):
        if (val != None):
          self.getCellule(indexDeLigne, indexDeColonne).set(val)
        else:
          self.getCellule(indexDeLigne, indexDeColonne).clear()

  def ajouteCelluleDansColonne(self, cellule: Cellule, indexDeColonne):
    cellule.colonne = self.grilleC[indexDeColonne]
    cellule.numero_de_colonne = indexDeColonne+1
    self.grilleC[indexDeColonne].list.append(cellule)

  def ajouteCelluleDansLigne(self, cellule: Cellule, indexDeLigne):
    cellule.ligne = self.grilleL[indexDeLigne]
    cellule.numero_de_ligne = indexDeLigne+1
    self.grilleL[indexDeLigne].list.append(cellule)

  def ajouteCelluleDansRegion(self, cellule: Cellule, indexDeRegion):
    cellule.region = self.grilleR[indexDeRegion]
    self.grilleR[indexDeRegion].list.append(cellule)

  def est_fini(self) -> bool:
    ligne = 0
    while ligne < len(self.grilleL):
      col = 0
      while col < len(self.getLigne(ligne).list):
        cell: Cellule = self.getLigne(ligne).getCellule(col)
        if (cell.est_vide()):
          return False
        col += 1
      ligne += 1
    return True

  def est_bloque(self) -> bool:
    return self.blocage
    self.compteur += 1
    if (self.compteur > 10):
      return True
    else:
      return False

  def getCellule(self, ligne, colonne) -> Cellule:
    return self.grilleL[ligne].list[colonne]

  def getLigne(self, ligne) -> Ligne:
    return self.grilleL[ligne]

  def getColonne(self, colonne) -> Colonne:
    return self.grilleC[colonne]

  def getRegion(self, index) -> Region:
    return self.grilleR[index]

  def getRegionDeCellule(self, ligne, colonne) -> Region:
    return self.grilleR[int(colonne/3)+int(ligne/3)*3]

  def resolve(self):
    self.verrouillageGraphique()

    while self.est_fini() == False and self.est_bloque() == False:
      print("Sudoku à finir")
      while self.est_fini() == False and self.est_bloque() == False:
        self.blocage = True
        self.identifyAllPossibilities()

      self.blocage = False
      while self.est_fini() == False and self.est_bloque() == False:
        self.blocage = True
        for ligne in self.grilleL:
          for chiffre in ligne.chiffres_manquants:
            self.fillUniquePossibleCellForNumber(chiffre, ligne)
        for colonne in self.grilleC:
          for chiffre in colonne.chiffres_manquants:
            self.fillUniquePossibleCellForNumber(chiffre, colonne)
        for region in self.grilleR:
          for chiffre in region.chiffres_manquants:
            self.fillUniquePossibleCellForNumber(chiffre, region)
      print()

    if self.est_bloque():
      print("Sudoku bloqué")
      self.afficheBlocageMessage()
    else:
      print("Sudoku fini !")

  def verrouillageGraphique(self):
    for ligne in self.grilleL:
      for cell in ligne.list:
        cell: Cellule
        if cell.est_pas_vide():
          cell.entry.config(background="#edf2f7")

  def afficheBlocageMessage(self):
    self.blocageTKWidget.grid(column=1, row=2, pady=10)

  ##########################
  # Fonctions de résolution

  def identifyAllPossibilities(self):
    cell: Cellule
    effet: bool = False
    for ligne in self.grilleL:
      for cell in ligne.list:
        effet ^= cell.identifyPossibilities()
    if effet:
      self.blocage = False
    print()

  def fillUniquePossibleCellForNumber(self, number, zone: Zone):
    solution: Cellule = None
    cell: Cellule
    for cell in zone.list:
      if (number in cell.possibilites):
        if solution is None:
          solution = cell
        else:
          return
    if solution is not None:
      print("Inscription de", number, "en", solution.numero_de_ligne, solution.numero_de_colonne, ": seule cellule possible")
      solution.set(number)
      solution.ligne.updatePossibilites()
      solution.colonne.updatePossibilites()
      solution.region.updatePossibilites()
      self.blocage = False
