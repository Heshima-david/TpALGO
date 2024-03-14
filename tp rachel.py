from datetime import datetime

class Client:
    def __init__(self, nom_client, date_de_naissance, numeros_telephone):
        self.nom_client = nom_client
        self.date_de_naissance = date_de_naissance
        self.numeros_telephone = numeros_telephone
        self.facture = 0.0

    def afficher_informations_client(self):
        print('Informations sur le client:')
        print()
        return {
            'nom' : self.nom_client,
            'date de naissance' : self.date_de_naissance,
            'abonnés': self.numeros_telephone,
            'montant_facture': self.facture
        }

class ImporterCDR:
    def __init__(self):
        self.clients = []
        self.cdr_stack = []

    def fichier_cdr(self, path):
        with open(path, 'r') as file:
            for l in file:
                info = l.split('|')
                dict_entry = {
                    'identifiant_appel': info[0],
                    'type_call': int(info[1]),
                    'date_heure': str(info[2]),
                    'appelant': info[3],
                    'appele': info[4] if info[4] != "" else None,
                    'duree': int(info[5]) if info[5] != "" else None,
                    'taxe': int(info[6]),
                    'total_volume': int(info[7])
                }
                self.cdr_stack.append(dict_entry)
                
    def calculer_facture(self, client: Client):
        client.facture = Facturation.calculer_montant_facture(client, self.cdr_stack)
    
    def statistiques(self, client: Client, periode):
        return Statistiques.afficher_statistiques_client(client, self.cdr_stack, periode)

class Facturation:
    
    @staticmethod
    def _calculer_montant_sms(cdr, taxed=False):
        base_price = 0.001 if not taxed else 0.002
        tax_rate = 0.1 if cdr['taxe'] == 1 else 0.16 if cdr['taxe'] == 2 else 0
        return base_price + (base_price * tax_rate)

    @staticmethod
    def _calculer_montant_appel(cdr, taxed=False):
        base_price = cdr['duree'] * (0.025 if not taxed else 0.05) / 60
        tax_rate = 0.1 if cdr['taxe'] == 1 else 0.16 if cdr['taxe'] == 2 else 0
        return base_price + (base_price * tax_rate)

    @staticmethod
    def _calculer_montant_internet(cdr):
        base_price = cdr['total_volume'] * 0.03
        tax_rate = 0.1 if cdr['taxe'] == 1 else 0.16 if cdr['taxe'] == 2 else 0
        return base_price + (base_price * tax_rate)
    
    @staticmethod
    def _calculer_montant_cdr(cdr):
        if cdr['type_call'] == 1:  
            if cdr['appele'] and cdr['appele'].startswith(('24381', '24382', '24383')):
                return Facturation._calculer_montant_sms(cdr)
            else:
                return Facturation._calculer_montant_sms(cdr, taxed=True)
        elif cdr['type_call'] == 0:  
            if cdr['appele'] and cdr['appele'].startswith(('24381', '24382', '24383')):
                return Facturation._calculer_montant_appel(cdr)
            else:
                return Facturation._calculer_montant_appel(cdr, taxed=True)
        elif cdr['type_call'] == 2:  
            return Facturation._calculer_montant_internet(cdr)
    
    @staticmethod
    def calculer_montant_facture(client: Client, cdr_stack):
        total_montant = 0.0
        for cdr in cdr_stack:
            if cdr['appelant'] in client.numeros_telephone:
                montant = Facturation._calculer_montant_cdr(cdr)
                total_montant += montant
        return total_montant

class Statistiques:
    @staticmethod
    def afficher_statistiques_client(client: Client, cdr_stack, periode):
        n_appels = 0
        duree_appels = 0
        n_sms = 0
        n_giga_utilises = 0.0
        
        for cdr in cdr_stack:
            date_heure = cdr['date_heure'][:8]
            if cdr['appelant'] in client.numeros_telephone and date_heure == periode:
                if cdr['type_call'] == 0:
                    n_appels += 1
                    duree_appels += cdr['duree']
                elif cdr['type_call'] == 1:
                    n_sms += 1
                elif cdr['type_call'] == 2:
                    n_giga_utilises += cdr['total_volume'] / 1024
                    
        return {
            'n_appels': n_appels,
            'duree_appels (secondes)': duree_appels,
            'n_sms': n_sms,
            'giga_utilises': n_giga_utilises
        }

# Exemple d'utilisation du code modifié :
client_polytechnique = Client("POLYTECHNIQUE", "28-10-1955", ["243818140560", "243818140120"])
print(client_polytechnique.afficher_informations_client())
print()

CDR = ImporterCDR()
CDR.fichier_cdr("cdr.txt")
CDR.fichier_cdr("tp_algo.txt")
print("Voici la pile des dictionnaires:")
print()
print(CDR.cdr_stack)
print() 

CDR.calculer_facture(client_polytechnique)
print(f"La facture du client POLYTECHNIQUE est de {client_polytechnique.facture} $.")
print()

periodes = ["20230114", "20230214", "20230111"]  
for periode in periodes:
    statistiques = CDR.statistiques(client_polytechnique, periode)
    print(f"Statistiques pour la période {periode}:")
    print(f"Nombre d'appels: {statistiques['n_appels']}")
    print(f"Durée totale des appels (en secondes): {statistiques['duree_appels (secondes)']}")
    print(f"Nombre de SMS: {statistiques['n_sms']}")
    print(f"Volume de données utilisé (en giga-octets): {statistiques['giga_utilises']:.2f} Go")
    