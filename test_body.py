import os
import re
import sys


code1 = "1"
code2 = "1"

# verifier si le dossier existe dans "download body"/"code1"/"code2"
if os.path.isdir("download body/"+code1+"/"+code2+"/"):
    # créer un dossier trier si il n'existe pas
    if not os.path.isdir("download body/"+code1+"/"+code2+"/trier/"):
        os.mkdir("download body/"+code1+"/"+code2+"/trier/")
    # récupéré le nombre total de fichier .txt
    nb = len([name for name in os.listdir("download body/"+code1+"/"+code2+"/") if os.path.isfile(os.path.join("download body/"+code1+"/"+code2+"/", name))])
    print(nb)
    for g in range(1, nb):
        # récupéré le fichier avec le plus petit nombre et qui est un .txt
        file = min([f for f in os.listdir("download body/"+code1+"/"+code2+"/") if f.endswith(".txt")])
        # récupéré le contenu du fichier
        with open("download body/"+code1+"/"+code2+"/"+file, "r") as file_min:
            content_file_min = file_min.read()
            content_file_min = content_file_min.split("\n")
            # pour tous les fichier dans le dossier, sauf le fichier avec le plus petit nombre, on compare le contenu
            #si tous le contenu du fichier file est dans le contenu du fichier f, on déplace le fichier f dans le dossier trier
            #on prend que les fichier .txt
        for f in [f for f in os.listdir("download body/"+code1+"/"+code2+"/") if f.endswith(".txt") and f != file]:
            test = True
            with open("download body/"+code1+"/"+code2+"/"+f, "r") as file_test:
                content_file_test = file_test.read()
            for line in content_file_min:
                if re.search("[a-zA-Z]", line):
                    if line not in content_file_test:
                        test = False
            
            # si le fichier f est dans le fichier file, on déplace les deux fichier dans le dossier trier
            #on les met dans un dossier avec le nom du fichier file
            if test:
                if not os.path.isdir("download body/"+code1+"/"+code2+"/trier/"+file):
                    os.mkdir("download body/"+code1+"/"+code2+"/trier/"+file)
                os.rename("download body/"+code1+"/"+code2+"/"+f, "download body/"+code1+"/"+code2+"/trier/"+file+"/"+f)
                break
        if test:
            os.system('del /f "download body"\\'+code1+'\\'+code2+'\\'+file)
        else:
            # deplacer dans le dossier non trouver
            if not os.path.isdir("download body/"+code1+"/"+code2+"/non trouver/"):
                os.mkdir("download body/"+code1+"/"+code2+"/non trouver/")
            os.rename("download body/"+code1+"/"+code2+"/"+file, "download body/"+code1+"/"+code2+"/non trouver/"+file)
else:
    print("Le dossier n'existe pas")    