from tools import *

class fonction():
    def __init__(self, driver):
        self.driver = driver

    def get_TOC(self):
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        # Filtre à appliquer sur les requêtes.
        def log_filter(log):
            return (
                # Il s'agit d'une réponse
                log["method"] == "Network.responseReceived"
                # Il s'agit d'une image
                and "xhtml" in log["params"]["response"]["mimeType"]
                and "https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/" in log["params"]["response"]["url"]
            )
        url  = []
        for log in filter(log_filter, logs):
            resp_url = log["params"]["response"]["url"]
            url.append(resp_url)
        return url
    
    def trouver_page_payant(self, url):
        if os.path.isfile("body.txt"):
            os.remove("body.txt")
        if os.path.isfile("body_test.txt"):
            os.remove("body_test.txt")

        driver = self.driver
        body_link_free = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
        body_link_free = body_link_free.get_attribute("innerHTML")
        body_link_free = body_link_free.split("\n")

        # récupéré le numéro d'incrémentation de la page
        numero_dessus = url.split("https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/")[1].split("/")[2]
        numero_dessous = url.split("https://biblio.nathan.fr/epubs/NATHAN/bibliomanuels/distrib_gp/")[1].split("/")[2]
        avant = url.split(numero_dessus)
        derniere_verif = "dessous"
        nb_tentative = 1
        while True:
            verif_lien = None
            print("Tentative numéro "+str(nb_tentative))
            if derniere_verif == "dessous" or numero_dessous == 0:
                numero_dessus = int(numero_dessus) + 1
                numero = str(numero_dessus)
                derniere_verif = "dessus"
            elif derniere_verif == "dessus":
                numero_dessous = int(numero_dessous) - 1
                numero = str(numero_dessous)
                derniere_verif = "dessous"
            nb_tentative += 1
            driver.get(avant[0]+numero+avant[1])
            body_link_test = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
            body_link_test = body_link_test.get_attribute("innerHTML")

            body_link_test = body_link_test.split("\n")
            for i in body_link_free:
                if re.search("[a-zA-Z]", i):
                    if i not in body_link_test:
                        verif_lien = False
                        break
            
            if verif_lien != False:
                return avant[0]+numero+avant[1]