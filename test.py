from time import sleep
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json
import base64

# Requêtes Chrome
capabilities = DesiredCapabilities.CHROME

# capabilities["loggingPrefs"] = {"performance": "ALL"}  # Pour chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # Pour chromedriver 75+

driver = webdriver.Chrome(
    desired_capabilities=capabilities, executable_path="chromedriver.exe" # Mettre ici le bon driver
)

# On va à l'adresse qui nous intéresse.
driver.get("https://biblio.nathan.fr/extrait/9782091652986/?openBook=9782091652986_extrait%3fdXNlck5hbWU9bWM3NUpBYjloblZ1VDJlV1IwOG4wcHJBYWJNeXZqTVhWdzRpTi9sdk9CZz0mdXNlclBhc3N3b3JkPWw2dzFhamd3emRhNDBaUjBrTGRQd1R4dXhBbnlhNkVmU1owM1FhM3RSYms9JmRlbW89dHJ1ZSZ3YXRlcm1hcms9ZmFsc2U=")
sleep(10)  # On attend que la page ait le temps de se charger.

# On extrait toutes les requêtes.
logs_raw = driver.get_log("performance")
logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

# Filtre à appliquer sur les requêtes.
def log_filter(log):
    return (
        # Il s'agit d'une réponse
        log["method"] == "Network.responseReceived"
        # Il s'agit d'une image
        and "xhtml" in log["params"]["response"]["mimeType"]
    )

for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    mime = log["params"]["response"]["mimeType"]
    print(f"Caught {resp_url}")
    print(f"Mime: {mime}")
    
    # On récupère le contenu.
    content = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
    if content['base64Encoded']:
        content = base64.b64decode(content['body'])
    else:
        content = content['body']
    # print(content)