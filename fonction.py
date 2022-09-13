from tools import *

class fonction():
    def __init__(self, driver):
        self.driver = driver

    def lien_jpg(self,type):
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
            print(f"Caught {resp_url}")
            url.append(resp_url)
        return url