import csv
from bs4 import BeautifulSoup

# Page HTML à parser
html = """
...
"""

# Analyse le contenu HTML de la page à l'aide de BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Trouve tous les éléments HTML qui contiennent les informations des avocats
avocat_elements = soup.find_all("div", class_="avocat-content")

# Ouvre un fichier CSV à l'emplacement spécifié en mode écriture
with open("/home/yvanoide/iadev-python/djan/scrap/avocats.csv", "w", newline="") as csvfile:
    # Crée un objet writer pour écrire dans le fichier CSV
    writer = csv.writer(csvfile)

    # Écrit l'en-tête du fichier CSV
    writer.writerow(["Nom", "Prestation de serment", "Adresse", "Téléphone", "Fax", "N° de Case", "Spécialités", "Email", "Site web"])

    # Parcourt tous les éléments HTML qui contiennent les informations des avocats
    for avocat_element in avocat_elements:
        # Récupère le nom de l'avocat à partir de l'élément HTML
        avocat_name = avocat_element.find("h3", class_="avocat-title").text.strip()

        # Récupère la date de prestation de serment de l'avocat à partir de l'élément HTML
        avocat_serment = avocat_element.find("strong", string="Prestation de serment :").find_next_sibling("br").next_sibling.text.strip()

        # Récupère l'adresse de l'avocat à partir de l'élément HTML
        avocat_adresse = avocat_element.find("p", class_="adresse").text.strip()

        # Récupère le numéro de téléphone de l'avocat à partir de l'élément HTML
        avocat_telephone = avocat_element.find("p", class_="telephone").text.strip()

        # Récupère le numéro de fax de l'avocat à partir de l'élément HTML
        avocat_fax = avocat_element.find("p", class_="fax").text.strip()

        # Récupère le numéro de case de l'avocat à partir de l'élément HTML
        avocat_case = avocat_element.find("p", class_="case").text.strip()

        # Trouve l'élément HTML qui contient la ou les spécialités de l'avocat
        specialite_element = avocat_element.find("p", class_="specialite")

        # Vérifie si l'élément HTML qui contient la ou les spécialités de l'avocat a été trouvé
        if specialite_element is not None:
            # Récupère la ou les spécialités de l'avocat à partir de l'élément HTML
            avocat_specialites = specialite_element.text.strip().split(", ")
        else:
            # Définit une liste vide pour les spécialités de l'avocat
            avocat_specialites = []

        # Trouve l'élément HTML qui contient l'adresse email de l'avocat
        email_element = avocat_element.find("a", class_="email")

        # Vérifie si l'élément HTML qui contient l'adresse email de l'avocat a été trouvé
        if email_element is not None:
            # Récupère l'adresse email de l'avocat à partir de l'élément HTML
            avocat_email = email_element["href"].split(":")[1]
        else:
            # Définit une chaîne vide pour l'adresse email de l'avocat
            avocat_email = ""

        # Trouve l'élément HTML qui contient le site web de l'avocat
        site_element = avocat_element.find("a", class_="site-web")

        # Vérifie si l'élément HTML qui contient le site web de l'avocat a été trouvé
        if site_element is not None:
            # Récupère le site web de l'avocat à partir de l'élément HTML
            avocat_site_web = site_element["href"]
        else:
            # Définit une chaîne vide pour le site web de l'avocat
            avocat_site_web = ""

        # Écrit les informations de l'avocat dans le fichier CSV
        writer.writerow([avocat_name, avocat_serment, avocat_adresse, avocat_telephone, avocat_fax, avocat_case, ", ".join(avocat_specialites), avocat_email, avocat_site_web])

# Affiche un message de succès
print("Les données ont été enregistrées avec succès dans le fichier avocats.csv.")
