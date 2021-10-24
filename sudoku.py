import tkinter as tk
from tkinter import font as tkfont
from tkinter.constants import CENTER, FLAT
from classes import Sudoku, Cellule

sudoku = Sudoku()

def ouverture():
  window = tk.Tk()
  window.rowconfigure(0, weight=1)
  window.columnconfigure(0, weight=1)
  window.rowconfigure(2, weight=1)
  window.columnconfigure(2, weight=1)

  window.title("Sudoku")
  window.geometry("500x400")

  innerWindow = tk.Frame(window)
  innerWindow.grid(column=1, row=1)

  titre = tk.Label(innerWindow, text="Résolution de Sudoku", font=tkfont.Font(family="Helvetica", size="15", weight='bold'));
  titre.grid(column=1, row=0, pady=10)

  blocageMessage = tk.Label(innerWindow, text="Résolution du Sudoku bloquée", foreground="red");
  sudoku.blocageTKWidget = blocageMessage

  startButton = tk.Button(innerWindow, text = "Lancer", command=lambda:[sudoku.resolve(), startButton.destroy(), fillForDemoButton.destroy()])
  startButton.grid(column=1, row=2, pady=10)

  fillForDemoButton = tk.Button(innerWindow, text = "Sudoku de démo", command=lambda:[remplirAvecDonneesDeTest(), fillForDemoButton.destroy()])
  fillForDemoButton.grid(column=1, row=3, pady=10)

  cadre = tk.Frame(innerWindow)
  cadre.grid(column=1, row=1)

  # colonnes de région
  for i in range(3):
    # lignes de région
    for j in range(3):
      # région de 3 x 3
      region = tk.Frame(cadre, borderwidth=2)
      region.grid(column=i, row=j)
      for k in range(3):
        for l in range(3):
          cell = Cellule(tk.Entry(region, width=2, relief=FLAT, justify=CENTER, font=tkfont.Font(family="Helvetica", size="10")))
          cell.entry.grid(column=k, row=l)
          sudoku.ajouteCelluleDansColonne(cell, i*3+k)
          sudoku.ajouteCelluleDansLigne(cell, j*3+l)
          sudoku.ajouteCelluleDansRegion(cell, j*3+i)
  window.mainloop()

def remplirAvecDonneesDeTest():
  # remplissage d'un sudoku de test
  test = [
    [None, 5, None, 1, None, None, None, None, None],
    [2, None, 4, None, None, None, None, 9, 3],
    [None, None, None, None, None, 3, 4, 5, None],
    [7, 2, 1, None, 3, 8, 6, 4, None],
    [4, 3, None, None, 5, 7, 9, 8, 1],
    [None, None, None, None, 6, 1, None, None, 2],
    [None, None, None, None, None, 4, None, None, 9],
    [1, None, 5, 3, None, None, 8, None, None],
    [6, 4, None, 8, None, 2, None, None, None],
  ]
  sudoku.fill(test)

ouverture()