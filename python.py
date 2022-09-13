#comparer pour trouver le livre en plus grand
# https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/1/8/7995/online/OEBPS/TOC.xhtml (gratuit)
# https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/1/8/7725/online/OEBPS/TOC.xhtml (payant)

from ast import expr_context
from re import sub
from fonction import *
from tools import *
os.system("cls")

# verif insertion des paramètres
while True:
    url_depart = input("Entrez l'URL de la page du livre -> ")
    if url_depart.startswith("https://enseignants.nathan.fr/catalogue/"):
        break
    else:
        print("L'URL n'est pas valide")
while True:
    titre_livre = "livre_"+input("Entrez le titre du livre -> ")
    # caractères interdits dans les noms de fichier
    interdit = ["<", ">", ":", '"', "/", "\\", "|", "?", "*","\"","CON","PRN","AUX","NUL","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","LPT1","LPT2","LPT3","LPT4","LPT5","LPT6","LPT7","LPT8","LPT9","."," ","\t",'"',"'"]
    for i in interdit:
        titre = titre.replace(i, "")
    if titre != "":
        break
    else:
        print("Le titre n'est pas valide")
        print("Les caractères suivants sont interdits : < > : \" / \\ | ? *")
        print("Les noms de fichiers suivants sont interdits : CON PRN AUX NUL COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9 LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9 . (espace) (tabulation) \" '")

if not os.path.exists(titre_livre):
 os.makedirs(titre_livre)

if os.path.isfile("chromedriver.exe"):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=options,desired_capabilities=capabilities)
    fonction = fonction(driver)
    driver.get(url_depart)
    os.system("cls")
    print("Recherche du livre en cours...")
    time.sleep(5)
    try:
        div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ico02')))
        # récupéré l'url de la balise a qui est dans la balise div
        url_livre = WebDriverWait(div, 10).until(EC.presence_of_element_located((By.TAG_NAME,'a'))).get_attribute("href")
        driver.get(url_livre)
        time.sleep(10)
    except:
        print("Ce livre n'est pas disponible ou votre connexion est trop lente")
        driver.quit()
        exit()

    try:
        url = fonction.get_TOC()
        # si dans url il y en a un qui contient "TOC.xhtml" récupérer l'url
        for i in url:
            if "TOC.xhtml" in i:
                url_livre = i
                break
            url_livre = None

        if url_livre == None:
            for i in url:
                if "Page_" in i and ".xhtml" in i:
                    url_livre = i.split("OEBPS")
                    url_livre = url_livre[0]+"OEBPS/TOC.xhtml"
                    break
                url_livre = None
    except:
        print("Ce livre n'est pas disponible ou votre connexion est trop lente")
        driver.quit()
        exit()

    if url_livre == None:
        print("Impossible de trouver le livre, veuillez réessayer...")
        driver.quit()
        sys.exit()

    else:
        driver.get(url_livre)
        time.sleep(5)
        # récupéré le contenu de la balise body
        test = fonction.trouver_page_payant(url_livre)
        if "https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/" in test:
            # récupéré toutes les balises a de la page
            print("Livre trouvé, récupération des pages...")
            driver.get(test)
            time.sleep(5)
            a = driver.find_elements_by_tag_name("a")
            # filtre : garder seulement les balises a qui ont un attribut href qui contient "Page_"
            a = [i for i in a if "Page_" in i.get_attribute("href")]
            a = [i for i in a if ".xhtml" in i.get_attribute("href")]
            print("Nombre de pages trouvé : "+str(len(a)))
            numero_page = 1
            nb_page_telecharger = 0
            for i in a:
                if ".xhtml#Target_Page_" in i.get_attribute("href"):
                    url_page = (i.get_attribute("href")).split("/Page_")
                    img_target = url_page[1].split(".xhtml#Target_")[1]
                    url_page = url_page[0]+"/Images/"+img_target+".jpg"
                    
                    numero_page += 1
                    nb_page_telecharger += 1
                    subprocess.call("ffmpeg -i "+f'{url_page}'+" "+titre_livre+"/"+f'{str(numero_page)}'+".jpg", shell=True)
        else:
            print("Impossible de trouver la version payante")

else:
    print("Merci de télécharger le chromedriver https://chromedriver.chromium.org/downloads")
    print('Veuillez télécharger la même version que celle de votre ordinateur.')

t = input("Appuyez sur entrée pour fermé le programme")