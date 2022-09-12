#URL de https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/2/11338/online/OEBPS/Chapter_001/Page_00001.xhtml
#URL à https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/2/11338/online/OEBPS/Chapter_001/Page_00244.xhtml
#https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/3/12000/online/OEBPS/Chapter_002/Page_00
#décalage de 2 pages (si on veut aller à la page 100, on doit aller à la page 102)

import subprocess,configparser, os, time, selenium,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
os.system("cls")

def lien_jpg():
    #Si connexion lente, on peut mettre un sleep
    # time.sleep(1)
    r = driver.execute_script("return window.performance.getEntries();")
    network = []
    for res in r:
        #ajouter le lien dans la liste
        network.append(res['name'])
    try:
        for i in network:
            if i.endswith('.jpg'):
                link_jpg = i
                print("\nLe lien de la photo est  est : " + link_jpg +"\n")
        return link_jpg
    except:
        print("\nErreur de récupération du lien de la photo "+str(i)+"\n")

if not os.path.exists("téléchargement"):
 os.makedirs("téléchargement")
if not os.path.isfile("config.txt"):
    f = open("config.txt", "w+")
    f.write("[LIEN]\n")
    f.write("\n")
    f.write("; exemple : https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/2/11338/online/OEBPS/Chapter_001/Page_00001.xhtml\n")
    f.write("url = none\n")
    f.write("\n")
    f.write(";Le nombre de page du livre que vous souaithez télécharger\n")
    f.write("nombre de page au total du livre = 0\n")
    f.write("\n")
    f.write("; soit y pour l'afficher ou n pour le cacher\n")
    f.write("afficher le driver = y\n")
    f.close()

config = configparser.ConfigParser()
config.read('config.txt')

url_config = config.get('LIEN', 'url').split("/Page")[0]
nombres_pages_livre = int(config.get('LIEN', 'nombre de page au total du livre'))+1
afficher_le_driver = config.get('LIEN', 'afficher le driver')

if os.path.isfile("chromedriver.exe"):
    if "https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/" not in url_config:
        print("Merci de mettre une URL valide")
    else:
            options = webdriver.ChromeOptions()
            if afficher_le_driver == "n":
                options.add_argument("--headless")

            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)
            driver.get('https://google.fr/')
            time.sleep(3)


            for i in range(1,nombres_pages_livre):
                if i < 10:
                    #ouvrir une nouvelle page chrome
                    driver.execute_script("window.open('');") 
                    driver.switch_to.window(driver.window_handles[1])
                    #aller sur la page xhtml
                    driver.get(url_config+"/Page_0000"+str(i)+".xhtml")
                    #récupéré le lien de la photo (.jpg)
                    link_jpg = lien_jpg()
                    name_jpg = "page"+str(i)
                    #téléchargement de la photo
                    subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
                    #fermer la page en cour de chrome
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                elif i >= 10 and i < 100:   
                    driver.execute_script("window.open('');") 
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(url_config+"/Page_000"+str(i)+".xhtml")
                    link_jpg = lien_jpg()
                    name_jpg = "page"+str(i)
                    subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                elif i > 100:
                    driver.execute_script("window.open('');") 
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(url_config+"/Page_00"+str(i)+".xhtml")
                    link_jpg = lien_jpg()
                    name_jpg = "page"+str(i)
                    subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            driver.quit()
else:
    print("Merci de télécharger le chromedriver https://chromedriver.chromium.org/downloads")
    print('Veuillez télécharger la même version que celle de votre ordinateur.')

t = input("Appuyez sur entrée pour fermé le programme")