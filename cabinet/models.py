from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_administrateur = models.BooleanField('administrateur', default=False)
    is_personnel = models.BooleanField('personnel', default=False)
    is_client = models.BooleanField('client', default=False)
    is_avocat = models.BooleanField('avocat', default=False)
    genre = models.CharField(max_length=200,default='pas de genre')
    photo = models.FileField(upload_to='images',blank=True,default='aucune image')
    phone = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    adresse = models.CharField(max_length = 150,default='aucune adresse')
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
         
class Personnel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    service = models.CharField(max_length=50,default='pas de service')
    class Meta:
        verbose_name = 'Personnel' 
        verbose_name_plural = 'Personnels'
    def __str__(self): 
        return self.service

class Service(models.Model): 
    NomServ = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'Service' 
        verbose_name_plural = 'Services'
    def __str__(self):
        return self.NomServ

class Avocat(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=False)
    class Meta:
        verbose_name = 'Avocat' 
        verbose_name_plural = 'Avocats'
    def __str__(self): 
        return self.service
 
class Client(models.Model): 
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    nationalite = models.CharField(max_length=200,default='pas de nationalite')
    profession=models.CharField(max_length=200,default='aucune profession')
    class Meta:  
        verbose_name = 'Client'  
        verbose_name_plural = 'Clients'
    def __str__(self): 
        return self.user.username

class Dossier(models.Model):
    numDossier=models.CharField(max_length=200,default='pas de num')
    titreDossier=models.CharField(max_length=20,default='pas de titre')
    objDossier=models.CharField(max_length=20,default='pas d object') 
    username=models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    dateTimeOuverture=models.DateTimeField(auto_now_add=True) 
    dateTimeFermeture=models.CharField(max_length=100,default='En cours')
    class Meta:
        verbose_name = 'Dossier' 
        verbose_name_plural = 'Dossiers'
    def __str__(self):
        return self.numDossier

class Acte(models.Model):
    numDossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, default=False)
    titreAct = models.CharField(max_length=20,default='pas de titre')
    DescrpAct = models.TextField(default='pas des actes')
    fichierActe = models.FileField(upload_to='media')
    dateActe = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Acte' 
        verbose_name_plural = 'Actes'
    def __str__(self):
        return self.numAct

class Archive(models.Model): 
    numDossier=models.CharField(max_length=200,default='pas de num')
    titreDossier=models.CharField(max_length=20,default='pas de titre')
    objDossier=models.CharField(max_length=20,default='pas d object')
    dateTimeOuverture=models.CharField(max_length=15,default='pas de date')
    dateTimeFermeture=models.CharField(max_length=15,default='pas de date')
    def __str__(self):
        return self.numDossier

class Fichier(models.Model):
    titre = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    name_client = models.CharField(max_length=20,default='pas de nom')
    fichier = models.FileField(upload_to='media')
    date_send = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre