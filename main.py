import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
import os
from tkinter import messagebox
import numpy as np
import cv2
from PIL import Image, ImageTk

largeur = 400
hauteur = 450

largeurImage = 398
hauteurImage = 448

# Créer la fenêtre principale
window = tk.Tk()
window.title("Etiquetage Image")
window.geometry("1280x670")
window.minsize(600, 350)

# Changer la couleur de fond
window.configure(bg='lightblue')

# Ajouter le grand titre
title_label = tk.Label(window, text="APPLICATION ETIQUETAGE IMAGE - M1 Images et Interactions",
                       font=("Berlin sans FB", 24, "bold"), fg='blue', bg='lightblue')
title_label.grid(row=0, column=0, columnspan=3, pady=5, padx=5)

# Variables globales
imageOriginale = None
imageBinaireGris = None


# Fonction pour ouvrir l'image
def open_image(label):
    global imageOriginale
    file_path = askopenfilename()
    if file_path:
        imageOriginale = cv2.imread(file_path)  # Lire l'image avec OpenCV
        image_pil = Image.open(file_path)
        image_pil = image_pil.resize((largeurImage, hauteurImage), Image.LANCZOS)  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image_pil)
        label.config(image=photo)
        label.image = photo


# Fonction pour quitter l'application
def quit_app():
    if askyesno('Message', 'Êtes-vous sûr de vouloir quitter le programme?'):
        window.destroy()


# Fonction pour convertir l'image en niveaux de gris et l'afficher
def imageBinaire():
    global imageOriginale, imageBinaireGris
    if imageOriginale is None:
        messagebox.showerror("Erreur", "Aucune image n'a été chargé!")
        return
    else:
        # Conversion en niveaux de gris
        imageBinaireGris = cv2.cvtColor(imageOriginale, cv2.COLOR_BGR2GRAY)

        # Affichage dans image_label2
        image_pil = Image.fromarray(imageBinaireGris)
        image_pil = image_pil.resize((largeurImage, hauteurImage), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image_pil)
        image_label2.config(image=photo)
        image_label2.image = photo


# Fonction pour l'étiquetage des composants connexes
def etiqueter_image():
    global imageBinaireGris
    if imageBinaireGris is None:
        messagebox.showerror("Erreur", "Aucune image binaire n'a été convertie!")
        return

    # Seuillage binaire pour s'assurer que l'image est bien binaire
    _, binary_image = cv2.threshold(imageBinaireGris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Inverser les couleurs pour avoir le fond noir et les composants blancs
    binary_image = cv2.bitwise_not(binary_image)

    # Etiquetage des composants connexes
    num_labels, labels_im = cv2.connectedComponents(binary_image)

    # Normalisation des étiquettes pour une meilleure visualisation
    labels_im = (labels_im * 255 / (num_labels - 1)).astype(np.uint8)

    # Affichage dans image_label3
    image_pil = Image.fromarray(labels_im)
    image_pil = image_pil.resize((largeurImage, hauteurImage), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image_pil)
    image_label3.config(image=photo)
    image_label3.image = photo


# Fonction pour l'étiquetage des composants connexes
"""def etiqueter_image():
    global imageBinaireGris
    if imageBinaireGris is None:
        messagebox.showerror("Erreur", "Aucune image binaire n'a été convertie!")
        return

    # Seuillage binaire pour s'assurer que l'image est bien binaire
    _, binary_image = cv2.threshold(imageBinaireGris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Inverser les couleurs pour avoir le fond noir et les composants blancs
    binary_image = cv2.bitwise_not(binary_image)

    # Etiquetage des composants connexes avec statistiques
    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

    # Filtrage des petits composants (optionnel)
    min_size = 50  # Taille minimale des composants à garder
    for label in range(1, num_labels):  # Commencer à 1 pour ignorer l'arrière-plan
        if stats[label, cv2.CC_STAT_AREA] < min_size:
            labels_im[labels_im == label] = 0

    # Re-normalisation des étiquettes après filtrage
    labels_im = (labels_im * 255 / (num_labels - 1)).astype(np.uint8)

    # Affichage dans image_label3
    image_pil = Image.fromarray(labels_im)
    image_pil = image_pil.resize((largeurImage, hauteurImage), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image_pil)
    image_label3.config(image=photo)
    image_label3.image = photo"""


# Fonction pour vider les cases
def viderCases():
    global image_label1, image_label2, image_label3

    # Vider les images dans les labels
    image_label1.config(image='')
    image_label2.config(image='')
    image_label3.config(image='')

    # Réinitialiser les références d'image pour éviter les fuites de mémoire
    image_label1.image = None
    image_label2.image = None
    image_label3.image = None


# Fonction pour enregistrer les images
def enregistrer_images():
    global image_label1, image_label2, image_label3

    # Demander à l'utilisateur de choisir un dossier pour sauvegarder les images
    save_directory = tk.filedialog.askdirectory()
    if not save_directory:
        return

    if image_label1.image is None:
        messagebox.showerror("Erreur", "Aucun image n'est ajouté.")
    else:
        # Sauvegarder image_label1
        if image_label1.image:
            image_pil1 = ImageTk.getimage(image_label1.image)
            image_path1 = os.path.join(save_directory, "image1.png")
            image_pil1.save(image_path1)
            print(f"Image 1 enregistrée à {image_path1}")

        # Sauvegarder image_label2
        if image_label2.image:
            image_pil2 = ImageTk.getimage(image_label2.image)
            image_path2 = os.path.join(save_directory, "image2.png")
            image_pil2.save(image_path2)
            print(f"Image 2 enregistrée à {image_path2}")

        # Sauvegarder image_label3
        if image_label3.image:
            image_pil3 = ImageTk.getimage(image_label3.image)
            image_path3 = os.path.join(save_directory, "image3.png")
            image_pil3.save(image_path3)
            print(f"Image 3 enregistrée à {image_path3}")

        # Confirmation
        messagebox.showinfo("Enregistrement", "Les images ont été enregistrées avec succès.")
        viderCases()


# Boucle pour les frames
for ligne in range(1):
    for colonne in range(3):
        image_frame1 = tk.Frame(window, bg='white', bd=2, relief='sunken', width=largeur, height=hauteur)
        image_frame1.grid(row=1, column=0, padx=10, pady=10)
        image_frame1.grid_propagate(False)  # Empêcher le cadre de se redimensionner

        image_frame2 = tk.Frame(window, bg='white', bd=2, relief='sunken', width=largeur, height=hauteur)
        image_frame2.grid(row=1, column=1, padx=10, pady=10)
        image_frame2.grid_propagate(False)

        image_frame3 = tk.Frame(window, bg='white', bd=2, relief='sunken', width=largeur, height=hauteur)
        image_frame3.grid(row=1, column=2, padx=10, pady=10)
        image_frame3.grid_propagate(False)

# Créer des labels pour afficher les images dans les cadres de chaque frames
image_label1 = tk.Label(image_frame1, bg='white', bd=2, relief='solid')
image_label1.pack(expand=True, fill='both')

image_label2 = tk.Label(image_frame2, bg='white', bd=2, relief='solid')
image_label2.pack(expand=True, fill='both')

image_label3 = tk.Label(image_frame3, bg='white', bd=2, relief='solid')
image_label3.pack(expand=True, fill='both')

# Créer des boutons
button1 = tk.Button(window, text="Ajouter image", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    command=lambda: open_image(image_label1), width=30, height=1)
button1.grid(row=2, column=0, padx=20, pady=10)

button2 = tk.Button(window, text="Conversion binaire", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    command=imageBinaire, width=30, height=1)
button2.grid(row=2, column=1, padx=20, pady=10)

button3 = tk.Button(window, text="Etiqueter image", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    command=etiqueter_image, width=30, height=1)
button3.grid(row=2, column=2, padx=20, pady=10)

button4 = tk.Button(window, text="Enregistrer image", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    command=enregistrer_images, width=30, height=1)
button4.grid(row=3, column=0, padx=40, pady=0)

button4 = tk.Button(window, text="Vider les cases", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    command=viderCases, width=30, height=1)
button4.grid(row=3, column=1, padx=40, pady=0)

button4 = tk.Button(window, text="Quitter le programme", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    command=quit_app, width=30, height=1)
button4.grid(row=3, column=2, padx=40, pady=0)

# Créer un menu
menu = tk.Menu(window, bg="lightblue", fg="black", font=("Berlin sans FB", 14))
window.config(menu=menu)

# Ajouter des éléments au menu
file_menu = tk.Menu(menu, tearoff=0, bg="lightblue", fg="black", font=("Berlin sans FB", 14))
menu.add_cascade(label="Fichier", menu=file_menu, font=("Berlin sans FB", 14))
file_menu.add_command(label="Ajouter image", command=lambda: open_image(image_label1))
file_menu.add_command(label="Conversion binaire", command=imageBinaire)
file_menu.add_command(label="Etiqueter l'image", command=etiqueter_image)
file_menu.add_command(label="Vider les cases", command=viderCases)
file_menu.add_command(label="Quitter", command=quit_app)

# Lancer la boucle principale de l'interface graphique
window.mainloop()
