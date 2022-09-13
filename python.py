#comparer pour trouver le livre en plus grand
# https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/3/12001/online/OEBPS/TOC.xhtml (gratuit)
# https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/2/3/12000/online/OEBPS/TOC.xhtml (payant)

from fonction import *
from tools import *

os.system("cls")


if not os.path.exists("téléchargement"):
 os.makedirs("téléchargement")

# verif insertion des paramètres
while True:
    # url_depart = input("Entrez l'URL de la page du livre -> ")
    url_depart = "https://enseignants.nathan.fr/catalogue/culture-economique-juridique-et-manageriale-2e-annee-bts-gpme-sam-ndrc-mco-et-cg-livre-licence-numerique-i-manuel-20-9782091652986.html"
    if url_depart.startswith("https://enseignants.nathan.fr/catalogue/"):
        break
    else:
        print("L'URL n'est pas valide")

while True:
    try:
        # nombres_pages_livre = int(input("Entrez le nombre de page à télécharger -> "))+1
        nombres_pages_livre = 1
        # le numéro doit être inférieur à 9999
        if nombres_pages_livre < 9999:
            break
        else:
            print("Le numéro de page est trop grand")
    except:
        print("Le numéro de page n'est pas valide")

# afficher_le_driver = input('Afficher le driver ? (y/n) (par défaut : y) -> ')
afficher_le_driver = "y"
if afficher_le_driver != "y" or afficher_le_driver != "n":
    afficher_le_driver == "y"





if os.path.isfile("chromedriver.exe"):
    options = webdriver.ChromeOptions()
    if afficher_le_driver == "n":
        options.add_argument("--headless")

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=options,desired_capabilities=capabilities)
    fonction = fonction(driver)
    driver.get(url_depart)
    time.sleep(5)
    div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ico02')))
    # récupéré l'url de la balise a qui est dans la balise div
    url_livre = WebDriverWait(div, 10).until(EC.presence_of_element_located((By.TAG_NAME,'a'))).get_attribute("href")
    driver.get(url_livre)
    time.sleep(10)
    url = fonction.lien_jpg("lien_départ")
    print(url)
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
    if url_livre == None:
        print("Impossible de trouver le livre, veuillez réessayer...")
        driver.quit()
        sys.exit()
    else:
        driver.get(url_livre)
    for i in range(1,nombres_pages_livre):
        if i <= 9:
            #ouvrir une nouvelle page chrome
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1])
            #aller sur la page xhtml
            driver.get(url+"/Page_0000"+str(i)+".xhtml")
            #récupéré le lien de la photo (.jpg)
            link_jpg = fonction.lien_jpg(".jpg")
            name_jpg = "page"+str(i)
            #téléchargement de la photo
            subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
            #fermer la page en cour de chrome
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        elif i >= 10 and i <= 99:   
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url+"/Page_000"+str(i)+".xhtml")
            link_jpg = fonction.lien_jpg(".jpg")
            name_jpg = "page"+str(i)
            subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        elif i >= 100 and i <= 999:
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url+"/Page_00"+str(i)+".xhtml")
            link_jpg = fonction.lien_jpg(".jpg")
            name_jpg = "page"+str(i)
            subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        elif i >= 1000:
            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url+"/Page_0"+str(i)+".xhtml")
            link_jpg = fonction.lien_jpg(".jpg")
            name_jpg = "page"+str(i)
            subprocess.call("ffmpeg -i "+f'{link_jpg}'+" téléchargement/"+f'{name_jpg}'+".jpg", shell=True)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    driver.quit()
else:
    print("Merci de télécharger le chromedriver https://chromedriver.chromium.org/downloads")
    print('Veuillez télécharger la même version que celle de votre ordinateur.')

t = input("Appuyez sur entrée pour fermé le programme")