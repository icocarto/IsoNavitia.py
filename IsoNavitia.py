import requests, csv, json, key
from tkinter import *
from tkinter.filedialog import *


class Navitia:
    """Classe regroupant les fonctions de Navitia.io"""

    def __init__(self):
        toto="toto"

        

    def coverage(self):
        """ recupération du coverage en fonction
            des coordonnées en entrée"""
        self.nlat = olat
        self.nlng = olng
        self.ndest = str(self.nlng+';'+self.nlat)
        self.url1 = 'https://api.navitia.io/v1/coord/'
        self.urlq = self.url1+self.ndest
        self.reponse = requests.get(self.urlq, headers={'Authorization':navkey})
        self.cov_output = self.reponse.json()
        try:
            self.coverage = str(self.cov_output['message']).strip('""')
            self.coverage = "No coverage"
        except:
            self.coverage = str(self.cov_output['regions']).strip("[]")
            self.coverage = self.coverage.strip("'")
        return self.coverage

    def journey(self):
        """ Récupération des temps de trajet
        pour chaque points du réseau"""
        self.urla = 'https://api.navitia.io/v1/coverage/'
        self.urlb = '/coords/'
        self.urlc = '/journeys'
        self.coverage = iso.coverage()
        self.urlq = self.urla+self.coverage+self.urlb+self.ndest+self.urlc
        self.resp = requests.get(self.urlq, headers={'Authorization':navkey})
        self.json = self.resp.json()
        self.resultjourney = self.json['journeys']
        return self.resultjourney
        
    def radius (self, isoval):
        """Calcul du rayon accessible à pied avec une vitesse de 1.12 km/h"""
        radius = ((isoval*60)-self.duration)*1.12
        if radius>0:
            radius="{:.2f}".format(radius)
        else :
            radius=""
        return radius
        
    def isochron (self, olng, olat,navkey):
        """ecriture du resultat pour des isochrones pre determinés
           TODO ajouter une boite de texte dans l'interface pour laisser
           l'utilisateur definir la valeur de l'isochrone"""
        self.journey = iso.journey()
        #print (self.journey)
        with open('MONFICHIER2.csv', 'w') as sortie:
            csv_out=csv.writer(sortie, delimiter=';', lineterminator='\n')
            csv_out.writerow(['lon',
                              'lat',
                              'duration',
                              'radius5',
                              'radius10',
                              'radius15',
                              'radius20',
                              'radius30',
                              'radius45',
                              'radius60',
                              'radius90'])
            r=0
            self.result = []
            
            for r in range(len(self.journey)):
                self.pt = self.journey[r]['to']['stop_point']['coord']
                self.ptlon = self.pt['lon']
                self.ptlat = self.pt['lat']
                self.duration = self.journey[r]['duration']
                self.radius5 = iso.radius(5)
                self.radius10 = iso.radius(10)
                self.radius15 = iso.radius(15)
                self.radius20 = iso.radius(20)
                self.radius30 = iso.radius(30)
                self.radius45 = iso.radius(45)
                self.radius60 = iso.radius(60)
                self.radius90 = iso.radius(90)
                self.result1 = self.ptlon,self.ptlat,self.duration,self.radius5,self.radius10,self.radius15,self.radius20,self.radius30,self.radius45,self.radius60,self.radius90
                csv_out.writerow([self.ptlon,self.ptlat,self.duration,self.radius5,self.radius10,self.radius15,self.radius20,self.radius30,self.radius45,self.radius60,self.radius90])
                self.result.append(self.result1)
                r=+1
        sortie.close()
        return self.result

        



navkey = key.navkey
olng = "-1.675104"
olat = "48.093708"
iso = Navitia()
result = iso.isochron(olng,olat,navkey)


print(result)


