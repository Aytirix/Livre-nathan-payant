#comparer pour trouver le livre en plus grand
# https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/1/8/7995/online/OEBPS/TOC.xhtml (gratuit)
# https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/1/8/7725/online/OEBPS/TOC.xhtml (payant)

from itertools import filterfalse
import threading
from ast import expr_context
from re import sub
from fonction import *
from tools import *
os.system("cls")

def getbody(code1,code2):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=options)
        time.sleep(2)
        # récupéré tous les nom de fichier dans le code1/code2
        nom = os.listdir("download body/"+str(code1)+"//"+str(code2))
        code3 = 0
        for i in nom:
            if "bmp" in i:
                # parse .bmp
                bmp = str(i).split(".bmp")[0]
                code3 = int(bmp)
                break
        if code3 == 0:
            f = open("download body/"+str(code1)+"//"+str(code2)+"/"+str(code3)+".bmp","w")
            f.close()
        code3 += 1
        for i in range(code3, 100000):
            try:
                driver.get("https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/"+str(code1)+"/"+str(code2)+"/"+str(i)+"/online/OEBPS/TOC.xhtml")
                        # récupéré le body
                body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
                body = body.get_attribute("innerHTML")
                # si le fichier 0.bmp existe pas on le créer

                # renommer le fichier bmp avec le dernier code3
                os.rename("download body/"+str(code1)+"/"+str(code2)+"/"+str(i-1)+".bmp","download body/"+str(code1)+"/"+str(code2)+"/"+str(i)+".bmp")
                if "Not Found" not in body:
                    # enlever les caractères spéciaux
                    # vérifier si le dossier existe
                    body = re.sub(r'[^a-zA-Z0-9 ]', '', body)
                    # enregistrer le body dans un fichier
                    # vérifier si le fichier existe
                    if not os.path.exists("download body/"+str(code1)+"/"+str(code2)+"/"+str(code3)+".txt"):
                        with open("download body/"+str(code1)+"/"+str(code2)+"/"+str(i)+".txt", "w", encoding="utf-8") as f:
                            f.write(body)
            except Exception as e:
                print(e)
                pass
        driver.quit()
        exit()

if os.path.isfile("chromedriver.exe"):
    try:
        # lancer un thread pour chaque code1
        for code1 in range(1, 2):
            for code2 in range(1, 9):
                if not os.path.isdir("download body"):
                    os.mkdir("download body")
                if not os.path.isdir("download body/"+str(code1)):
                    os.mkdir("download body/"+str(code1))
                if not os.path.isdir("download body/"+str(code1)+"/"+str(code2)):
                    os.mkdir("download body/"+str(code1)+"/"+str(code2))
                threading.Thread(target=getbody, args=(code1,code2)).start()
        time.sleep(99999)
    except Exception as e:
        print(e)