import sqlite3
import csv
import pandas as pd

class Recepten:
    def __init__(self, database="recepten_database.db"):
        self.dbconnection = sqlite3.connect(database)
        self.cursor = self.dbconnection.cursor()

    def voeg_recept_toe(self, naam, beschrijving):
        self.cursor.execute("INSERT INTO recepten (naam, beschrijving) VALUES (?, ?)", (naam, beschrijving))
        self.dbconnection.commit()
        return self.cursor.lastrowid

    def voeg_ingredient_toe(self, recept_id, naam, hoeveelheid):
        self.cursor.execute("INSERT INTO ingredienten (recept_id, naam, hoeveelheid) VALUES (?, ?, ?)", (recept_id, naam, hoeveelheid))
        self.dbconnection.commit()

    def toon_recepten(self):
        self.cursor.execute("SELECT * FROM recepten")
        recepten = self.cursor.fetchall()
        for recept in recepten:
            print(f"Recept ID: {recept[0]}, Naam: {recept[1]}, Beschrijving: {recept[2]}")
            self.cursor.execute("SELECT naam, hoeveelheid FROM ingredienten WHERE recept_id = ?", (recept[0],))
            ingredienten = self.cursor.fetchall()
            for ingredient in ingredienten:
                print(f"  - {ingredient[0]}: {ingredient[1]}")

    def toon_recept(self, naam):
        self.cursor.execute("SELECT * FROM recepten WHERE naam = ?", (naam,))
        recepten = self.cursor.fetchall()
        if recepten:
            for recept in recepten:
                print(f"Recept ID: {recept[0]}, Naam: {recept[1]}, Beschrijving: {recept[2]}")
                self.cursor.execute("SELECT naam, hoeveelheid FROM ingredienten WHERE recept_id = ?", (recept[0],))
                ingredienten = self.cursor.fetchall()
                print("Ingrediënten:")
                for ingredient in ingredienten:
                    print(f"  - {ingredient[0]}: {ingredient[1]}")
        else:
            print("Geen recept gevonden met de naam:", naam)

    def genereer_csv(self):
        self.cursor.execute("SELECT * FROM recepten")
        recepten = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM ingredienten")
        ingredienten = self.cursor.fetchall()

        with open("recepten_report.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Naam", "Beschrijving"])
            writer.writerows(recepten)

        with open("ingredienten_report.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Recept ID", "Naam", "Hoeveelheid"])
            writer.writerows(ingredienten)

        print("Csv bestand is succesvol gegenereerd")

if __name__ == "__main__":
    db = Recepten()
    
    while True:
        print("\n")
        print("Wat wil je doen?")
        print("1 - Voeg een nieuw recept toe")
        print("2 - Voeg ingrediënten toe aan een recept")
        print("3 - Toon alle recepten")
        print("4 - Zoek een recept")
        print("5 - Zet om naar csv")
        print("6 - Stoppen")
        
        keuze = input("Maak je keuze (1-6): ")
        
        if keuze == "1":
            naam = input("Recept: ")
            beschrijving = input("Beschrijving: ")
            recept_id = db.voeg_recept_toe(naam, beschrijving)
            print(f"Recept '{naam}' toegevoegd met ID {recept_id}.")

        elif keuze == "2":
            recept_id = input("Voer het recept ID in: ")
            naam = input("Ingrediënt: ")
            hoeveelheid = input("Hoeveelheid: ")
            db.voeg_ingredient_toe(recept_id, naam, hoeveelheid)
            print(f"Ingrediënt '{naam}' toegevoegd aan recept ID {recept_id}.")

        elif keuze == "3":
            db.toon_recepten()

        elif keuze == "4":
            naam = input("Recept: ")
            db.toon_recept(naam)
        
        elif keuze == "5":
            db.genereer_csv()

        elif keuze == "6":
            print("Eet smakelijk!")
            break

        else:
            print("Ongeldig, geef een getal in van 1 tot en met 6")
