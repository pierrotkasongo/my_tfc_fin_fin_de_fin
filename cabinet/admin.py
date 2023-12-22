from django.contrib import admin
from .models import *
# Register your models here.

"""
class AdminUser(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username","is_administrateur","is_personnel","is_avocat","is_client","genre","photo","phone","created_at","adresse") 
    
    """
admin.site.register(User)

class AdminPersonnel(admin.ModelAdmin):
    list_display = ("user", "service") 
admin.site.register(Personnel, AdminPersonnel)

class AdminService(admin.ModelAdmin):
    list_display = ("id", "NomServ") 
admin.site.register(Service, AdminService)

class AdminAvocat(admin.ModelAdmin):
    list_display = ("user", "service") 
admin.site.register(Avocat, AdminAvocat)

class AdminClient(admin.ModelAdmin):
    list_display = ("user","nationalite", "profession")
admin.site.register(Client, AdminClient)

class AdminDossier(admin.ModelAdmin):
    list_display = ("id","numDossier", "titreDossier","objDossier","dateTimeOuverture","dateTimeFermeture")
admin.site.register(Dossier, AdminDossier) 

class AdminActe(admin.ModelAdmin):
    list_display = ("id","titreAct","DescrpAct","fichierActe")
admin.site.register(Acte, AdminActe)

class AdminArchive(admin.ModelAdmin):
    list_display = ("id","numDossier", "titreDossier","objDossier","dateTimeOuverture","dateTimeFermeture")
admin.site.register(Archive, AdminArchive) 

class AdminFichier(admin.ModelAdmin):
    list_display = ("id","titre", "username","name_client","fichier","date_send")
admin.site.register(Fichier,AdminFichier) 





