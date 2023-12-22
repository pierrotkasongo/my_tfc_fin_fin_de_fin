from django.shortcuts import render,redirect,get_object_or_404 
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import *
from django.contrib import messages
from my_tfc_fin import settings
import secrets
import string
# Create your views here.
def home(request):
    return render(request,'index.html')

# administrateur
def connexion(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_administrateur:
            login(request, user)
            return redirect('enreg_personnel')
        elif user is not None and user.is_personnel:
            login(request, user)
            return redirect('personnel_enregis_avocat')
        elif user is not None and user.is_avocat:
            login(request, user)
            return redirect('avocat_enregis_client')
        elif user is not None and user.is_client:
            login(request, user)
            return redirect('client')
        else:
            messages.error(request, "Erreur sur l'dentification")
            return render(request, 'login.html')
    return render(request,'login.html')

@login_required
def enreg_personnel(request):
    if request.user.is_authenticated:
        personnels = Personnel.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            service =request.POST['service'].lower()
            photo= request.FILES['photo']
            adresse = request.POST['adresse'].lower()
            
            letters = string.ascii_letters
            digits = string.digits
            alphabet = letters + digits
            pwd_length = 6
            password=''
            for i in range(pwd_length):
                password += ''.join(secrets.choice(alphabet))
            
            is_personnel = True
            if User.objects.filter(email=email):
                messages.error(request, "L'adresse email existe déjà !")
            else:                
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, genre=genre,email=email, phone=phone, 
                    photo=photo, adresse=adresse, password=password, is_personnel=is_personnel)
                personnel=Personnel.objects.create(user=user, service=service)
                if user is not None:
                    messages.success(request, "personnel ajouté avec succès !")
                    sujet = "Bienvenu(e) " + user.username + " " + user.first_name + " Vous êtes membre du cabinet *MUBENESHA* étant que Personnel!"
                    message = "Votre mot de passe pour accéder au système est : " + password
                    expediteur = settings.EMAIL_HOST_USER
                    destinateur = [email]
                    send_mail(sujet, message, expediteur,destinateur, fail_silently=True)
                    print("Mode passe générer est: "+ password)
                else:
                    messages.error(request, "L'enregistrement échoué !")
                
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                personnels = Personnel.objects.filter(user__username__icontains=username) | Personnel.objects.filter(user__first_name__icontains=username)
        
    return render(request,'administrateur/enreg_personnel.html',{'personnels': personnels})

@login_required
def update_personnel(request, id):
    if request.user.is_authenticated:
        personnels = get_object_or_404(Personnel, user__id=id)
        page = 'update_personnel'
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            service = request.POST['service'].lower()
            photo= request.FILES['photo']
            created_at=request.POST['created_at']
            adresse = request.POST['adresse'].lower()
            
            objet = User.objects.get(id=id)
            objet.first_name=first_name
            objet.last_name=last_name
            objet.username=username
            objet.genre=genre
            objet.email=email
            objet.phone=phone
            objet.photo=photo
            objet.created_at=created_at
            objet.adresse=adresse
            objet.save()
            
            objet1 = Personnel.objects.get(user__id=id)
            objet1.service=service
            objet1.save()
            messages.success(request, "personnel a été modifier avec succès !")
            return redirect('enreg_personnel')
            
        return render(request, "administrateur/update_personnel.html" , {'page':page,'personnels': personnels})
    else:
        return redirect('connexion')

@login_required
def delete_personnel(request, id):
    if request.user.is_authenticated:
        personnel= get_object_or_404(User, id=id)
        personnel.delete()
        return redirect('enreg_personnel')
    else:
        return redirect('connexion')

@login_required
def enreg_avocat(request):
    if request.user.is_authenticated:
        services = Service.objects.all()
        avocats = Avocat.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            email = request.POST['email']
            genre = request.POST['genre'].lower()
            phone = request.POST['phone']
            service =int(request.POST['service'])
            id_service=Service.objects.get(id=service)
            photo= request.FILES['photo']
            adresse = request.POST['adresse'].lower()
            
            letters = string.ascii_letters
            digits = string.digits
            alphabet = letters + digits
            pwd_length = 6
            password=''
            for i in range(pwd_length):
                password += ''.join(secrets.choice(alphabet))
                
            is_avocat = True
            if User.objects.filter(email=email):
                messages.error(request, "L'adresse email existe déjà !")
            else:
                user = User.objects.create_user(first_name=first_name, username=username ,last_name=last_name,email=email, phone=phone, 
                    genre=genre, photo=photo, adresse=adresse, password=password, is_avocat=is_avocat)
                avocat=Avocat.objects.create(user=user, service=id_service)
                print("Mode passe générer est: "+ password)
                
                if user is not None:
                    messages.success(request, "avocat ajouté avec succès !")
                    sujet = "Bienvenu(e) " + user.username + " " + user.first_name + " Vous êtes membre du cabinet *MUBENESHA* étant que avocat!"
                    message = "Votre mot de passe pour accéder au système est : " + password
                    expediteur = settings.EMAIL_HOST_USER
                    destinateur = [email]
                    send_mail(sujet, message, expediteur,destinateur, fail_silently=True)
                else:
                    messages.error(request, "L'enregistrement échoué !")
                
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                avocats= Avocat.objects.filter(user__username__icontains=username) | Avocat.objects.filter(user__first_name__icontains=username)
    return render(request, "administrateur/enreg_avocat.html" , {'avocats': avocats,'services':services})

@login_required
def service_avocat(request):
    if request.user.is_authenticated:
        services = Service.objects.all().order_by('id')
        if request.method == 'POST':
            NomServ = request.POST['NomServ'].lower()
            service = Service.objects.create(NomServ=NomServ)
 
        if request.method == "GET":
            NomServ = request.GET.get('recherche')
            if NomServ is not None:
                services= Service.objects.filter(NomServ__icontains=NomServ)
    return render(request, "administrateur/service.html" , {'services':services})

@login_required
def delete_service(request, id):
    if request.user.is_authenticated:
        service = get_object_or_404(Service, id=id)
        service.delete()
        return redirect('service_avocat')
    else:
        return redirect('connexion')


@login_required
def update_avocat(request, id):
    if request.user.is_authenticated:
        services = Service.objects.all()
        avocats = get_object_or_404(Avocat, user__id=id)
        page = 'update_avocat'
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            service =int(request.POST['service'])
            id_service=Service.objects.get(id=service)
            photo= request.FILES['photo']
            created_at=request.POST['created_at']
            adresse = request.POST['adresse'].lower()
           
            objet = User.objects.get(id=id)
            objet.first_name=first_name
            objet.last_name=last_name
            objet.username=username
            objet.genre=genre
            objet.email=email
            objet.phone=phone
            objet.photo=photo
            objet.created_at=created_at
            objet.adresse=adresse
            objet.save()
            
            objet1 = Avocat.objects.get(user__id=id)
            objet1.service=id_service
            objet1.save()
            messages.success(request, "avocat a été modifier avec succès !")
            return redirect('enreg_avocat')
            
        return render(request, "administrateur/update_avocat.html" , {'page':page,'avocats': avocats,'services':services})
    else:
        return redirect('connexion')


@login_required
def delete_avocat(request, id):
    if request.user.is_authenticated:
        avocat= get_object_or_404(User, id=id)
        avocat.delete()
        return redirect('enreg_avocat')
    else:
        return redirect('connexion')

@login_required
def enreg_client(request):
    if request.user.is_authenticated:
        clients = Client.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            nationalite = request.POST['nationalite'].lower()
            photo = request.FILES['photo']
            profession = request.POST['profession'].lower()
            adresse = request.POST['adresse'].lower()
            
            letters = string.ascii_letters
            digits = string.digits
            alphabet = letters + digits
            pwd_length = 6
            password=''
            for i in range(pwd_length):
                password += ''.join(secrets.choice(alphabet))
            
            is_client = True
            if User.objects.filter(email=email):
                messages.error(request, "L'adresse email existe déjà !")
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, genre=genre, email=email,phone=phone, photo=photo, adresse=adresse, password=password, is_client=is_client)
                client=Client.objects.create(user=user, profession=profession,nationalite=nationalite)
                print("Mode passe générer est: "+ password)
                
                if user is not None:
                    messages.success(request, "client enregistre avec succès !")
                    sujet = "Bienvenu(e) " + user.username + " " + user.first_name + " Vous êtes membre du cabinet *MUBENESHA* étant que client!"
                    message = "Votre mot de passe pour accéder au système est : " + password
                    expediteur = settings.EMAIL_HOST_USER
                    destinateur = [email]
                    send_mail(sujet, message, expediteur,destinateur, fail_silently=True)
                else:
                    messages.error(request, "L'enregistrement échoué !")
                
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                clients = Client.objects.filter(user__username__icontains=username) | Client.objects.filter(user__first_name__icontains=username)
    return render(request, "administrateur/enreg_client.html", {'clients': clients})


@login_required
def update_client(request, id):
    if request.user.is_authenticated:
        clients = get_object_or_404(Client, user__id=id)
        page = 'update_client'
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            nationalite = request.POST['nationalite'].lower()
            photo = request.FILES['photo']
            created_at = request.POST['created_at']
            profession = request.POST['profession'].lower()
            
            objet = User.objects.get(id=id)
            objet.first_name=first_name
            objet.last_name=last_name
            objet.username=username
            objet.genre=genre
            objet.email=email
            objet.phone=phone
            objet.photo=photo
            objet.created_at=created_at
            objet.save()
            
            objet1 = Client.objects.get(user__id=id)
            objet1.profession=profession
            objet1.nationalite=nationalite
            objet1.save()
            messages.success(request, "client a été modifier avec succès !")
            return redirect('enreg_client')
    return render(request, "administrateur/update_client.html", {'page':page,'clients': clients})

@login_required
def delete_client(request, id):
    if request.user.is_authenticated:
        client= get_object_or_404(User, id=id)
        client.delete()
        return redirect('enreg_client')
    else:
        return redirect('connexion')
    
@login_required
def liste_dossier(request):
    dossier= Dossier.objects.all()
    if request.method == "GET":
        numDossier = request.GET.get('recherche')
        if numDossier is not None:
            dossier= Dossier.objects.filter(numDossier=numDossier) | Dossier.objects.filter(titreDossier__icontains=numDossier)
    context = {
        'dossiers':dossier,
        }
    return render(request, "administrateur/liste_dossier.html",context)

@login_required
def admin_update_dossier_client(request, id):
    if request.user.is_authenticated:
        dossiers = get_object_or_404(Dossier, id=id)
        page = 'admin_update_dossier_client'
        administrateurs = User.objects.filter(is_administrateur=True).order_by('username')
        if request.method == 'POST':
            numDossier=request.POST['numDossier']
            titreDossier=request.POST['titreDossier']
            objDossier=request.POST['objDossier']
            dateTimeFermeture=request.POST['dateTimeFermeture']
            
            objet = Dossier.objects.get(id=id)
            objet.numDossier=numDossier
            objet.titreDossier=titreDossier
            objet.objDossier=objDossier
            objet.dateTimeFermeture=dateTimeFermeture
            objet.save()
            messages.success(request, "dossier a été clôture avec succès !")
            return redirect('liste_dossier')
    return render(request, "administrateur/update_dossier.html", {'page':page,'dossiers': dossiers,'administrateurs': administrateurs})

@login_required
def admin_delete_dossier_client(request, id):
    if request.user.is_authenticated:
        dossier= get_object_or_404(Dossier, id=id)
        dossier.delete()
        return redirect('liste_dossier')
    else:
        return redirect('connexion')

@login_required
def liste_acte(request):
    actes = Acte.objects.all().order_by('id')
    if request.method == "GET":
        titreAct = request.GET.get('recherche')
        if titreAct is not None:
            actes= Acte.objects.filter(numAct=titreAct) | Acte.objects.filter(titreAct__icontains=titreAct)
    return render(request, "administrateur/liste_acte.html",{'actes':actes})

@login_required
def admin_update_acte(request, id):
    if request.user.is_authenticated:
        actes = get_object_or_404(Acte, id=id)
        page = 'admin_update_acte'
        administrateurs = User.objects.filter(is_administrateur=True).order_by('username')
        if request.method == 'POST':
            titreAct=request.POST['titreAct']
            DescrpAct=request.POST['DescrpAct']
            objet = Acte.objects.get(id=id)
            objet.titreAct=titreAct
            objet.DescrpAct=DescrpAct
            objet.save()
            messages.success(request, "l'acte a été modifier avec succès !")
            return redirect('liste_acte')
    return render(request, "administrateur/update_acte.html",{'page':page,'actes':actes})

@login_required
def liste_send_file(request):
    if request.user.is_authenticated:
        fichiers = Fichier.objects.all().order_by('id')
        fichier_number = fichiers.count() 
    
    if request.method == "GET":
        titre = request.GET.get('recherche')
        if titre is not None:
            fichiers = Fichier.objects.filter(titre__icontains=titre) |Fichier.objects.filter(fichier__icontains=titre)
        
    return render(request, "administrateur/liste_send_file.html",{'fichiers':fichiers,'fichier_number':fichier_number})

@login_required
def admin_delete_send_file(request, id):
    if request.user.is_authenticated:
        fichiers = get_object_or_404(Fichier, id=id)
        fichiers.delete()
        return redirect('liste_send_file')
    else:
        return redirect('connexion')
    
@login_required
def liste_archive(request):
    archives = Archive.objects.all().order_by('id')
    archive_number = archives.count()
    if request.method == "GET":
        numDossier = request.GET.get('recherche')
        if numDossier is not None:
            archives= Archive.objects.filter(numDossier=numDossier) | Archive.objects.filter(titreDossier__icontains=numDossier)
    return render(request, "administrateur/liste_archive.html",{'archives':archives,'archive_number':archive_number})

@login_required
def admin_delete_dossier_arch(request, id):
    if request.user.is_authenticated:
        archives = get_object_or_404(Archive, id=id)
        archives.delete()
        return redirect('liste_archive')
    else:
        return redirect('connexion')


# les methodes pour les actions du personnel
@login_required
def personnel_enregis_avocat(request):
    if request.user.is_authenticated:
        services = Service.objects.all()
        avocats = Avocat.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            email = request.POST['email']
            genre = request.POST['genre'].lower()
            phone = request.POST['phone']
            service =int(request.POST['service'])
            id_service=Service.objects.get(id=service)
            photo= request.FILES['photo']
            adresse = request.POST['adresse'].lower()
            
            letters = string.ascii_letters
            digits = string.digits
            alphabet = digits + letters
            pwd_length = 6
            password=''
            for i in range(pwd_length):
                password += ''.join(secrets.choice(alphabet))
                
            is_avocat = True
            if User.objects.filter(email=email):
                messages.error(request, "L'adresse email existe déjà !")
            else:
                user = User.objects.create_user(first_name=first_name, username=username ,last_name=last_name,email=email, phone=phone, 
                    genre=genre, photo=photo, adresse=adresse, password=password, is_avocat=is_avocat)
                avocat=Avocat.objects.create(user=user, service=id_service)
               
                print("Mode passe générer est: "+ password)
                
                if user is not None:
                    messages.success(request, "avocat ajouté avec succès !")
                    sujet = "Bienvenu(e) " + user.username + " " + user.first_name + " Vous êtes membre du cabinet *MUBENESHA* étant que avocat!"
                    message = "Votre mot de passe pour accéder au système est : " + password
                    expediteur = settings.EMAIL_HOST_USER
                    destinateur = [email]
                    send_mail(sujet, message, expediteur,destinateur, fail_silently=True)
                else:
                    messages.error(request, "L'enregistrement échoué !")
                
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                avocats = Avocat.objects.filter(user__username__icontains=username) | Avocat.objects.filter(user__first_name__icontains=username)
    return render(request, "personnel/enreg_avocat.html" , {'avocats': avocats,'services':services})

@login_required
def personnel_update_avocat(request, id):
    if request.user.is_authenticated:
        services = Service.objects.all()
        avocats = get_object_or_404(Avocat, user__id=id)
        page = 'update_avocat'
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            service =int(request.POST['service'])
            id_service=Service.objects.get(id=service)
            photo= request.FILES['photo']
            created_at=request.POST['created_at']
            adresse = request.POST['adresse'].lower()
            
            objet = User.objects.get(id=id)
            objet.first_name=first_name
            objet.last_name=last_name
            objet.username=username
            objet.genre=genre
            objet.email=email
            objet.phone=phone
            objet.photo=photo
            objet.created_at=created_at
            objet.adresse=adresse
            objet.save()
            
            objet1 = Avocat.objects.get(user__id=id)
            objet1.service=id_service
            objet1.save()
            messages.success(request, "Avocat a été modifier avec succès !")
            return redirect('personnel_enregis_avocat')
            
        return render(request, "personnel/update_avocat.html" , {'page':page,'avocats': avocats,'services':services})
    else:
        return redirect('connexion')

def personnel_delete_avocat(request, id):
    if request.user.is_authenticated:
        avocat= get_object_or_404(User, id=id)
        avocat.delete()
        return redirect('personnel_enregis_avocat')
    else:
        return redirect('connexion')

@login_required
def personnel_enreg_client(request):
    if request.user.is_authenticated:
        page = 'personnel_enreg_client'
        clients = Client.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            nationalite = request.POST['nationalite'].lower()
            photo= request.FILES['photo']
            profession = request.POST['profession'].lower()
            adresse = request.POST['adresse'].lower()
            
            letters = string.ascii_letters
            digits = string.digits
            alphabet = digits + letters
            pwd_length = 6
            password=''
            for i in range(pwd_length):
                password += ''.join(secrets.choice(alphabet))
            
            is_client = True
            if User.objects.filter(email=email):
                messages.error(request, "L'adresse email existe déjà!")
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, genre=genre, email=email,phone=phone, photo=photo, adresse=adresse, password=password, is_client=is_client)
                client=Client.objects.create(user=user, profession=profession,nationalite=nationalite)
                
                print("Mode passe générer est: "+ password)
                
                if user is not None:
                    messages.success(request, "client enregistre avec succès !")
                    sujet = "Bienvenu(e) " + user.username + " " + user.first_name + " Vous êtes membre du cabinet *MUBENESHA* étant que client!"
                    message = "Votre mot de passe pour accéder au système est : " + password
                    expediteur = settings.EMAIL_HOST_USER
                    destinateur = [email]
                    send_mail(sujet, message, expediteur,destinateur, fail_silently=True)
                else:
                    messages.error(request, "L'enregistrement échoué !")
                
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                clients = Client.objects.filter(user__username__icontains=username) | Client.objects.filter(user__first_name__icontains=username)
    return render(request, "personnel/enreg_client.html",{'clients': clients})

@login_required
def personnel_update_client(request, id):
    if request.user.is_authenticated:
        clients = get_object_or_404(Client, user__id=id)
        page = 'personnel_update_client'
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            nationalite = request.POST['nationalite'].lower()
            photo = request.FILES['photo']
            created_at = request.POST['created_at']
            profession = request.POST['profession'].lower()
            
            objet = User.objects.get(id=id)
            objet.first_name=first_name
            objet.last_name=last_name
            objet.username=username
            objet.genre=genre
            objet.email=email
            objet.phone=phone
            objet.photo=photo
            objet.created_at=created_at
            objet.save()
            
            objet1 = Client.objects.get(user__id=id)
            objet1.profession=profession
            objet1.nationalite=nationalite
            objet1.save()
            messages.success(request, "client a été modifier avec succès !")
            return redirect('personnel_enreg_client')
    return render(request, "personnel/update_client.html", {'page':page,'clients': clients})

def personnel_delete_client(request, id):
    if request.user.is_authenticated:
        client= get_object_or_404(User, id=id)
        client.delete()
        return redirect('personnel_enreg_client')
    else:
        return redirect('connexion')

    
@login_required
def liste_dossier_person(request):
    dossier= Dossier.objects.all()
    if request.method == "GET":
        numDossier = request.GET.get('recherche')
        if numDossier is not None:
            dossier= Dossier.objects.filter(numDossier=numDossier) | Dossier.objects.filter(titreDossier__icontains=numDossier)
    context = {
        'dossiers':dossier,
        }
    return render(request, "personnel/liste_dossier.html",context)

@login_required
def person_delete_dossier_client(request, id):
    if request.user.is_authenticated:
        dossier= get_object_or_404(Dossier, id=id)
        dossier.delete()
        return redirect('liste_dossier_person')
    else:
        return redirect('connexion')

@login_required
def person_update_dossier_client(request, id):
    if request.user.is_authenticated:
        dossiers = get_object_or_404(Dossier, id=id)
        page = 'person_update_dossier_client'
        personnels = User.objects.filter(is_personnel=True).order_by('username')
        if request.method == 'POST':
            numDossier=request.POST['numDossier']
            titreDossier=request.POST['titreDossier']
            objDossier=request.POST['objDossier']
            dateTimeFermeture=request.POST['dateTimeFermeture']
           
            objet = Dossier.objects.get(id=id)
            objet.numDossier=numDossier
            objet.titreDossier=titreDossier
            objet.objDossier=objDossier
            objet.dateTimeFermeture=dateTimeFermeture
            objet.save()
            messages.success(request, "dossier a été modifier avec succès !")
            return redirect('liste_dossier_person')
    return render(request, "personnel/update_dossier.html", {'page':page,'dossiers': dossiers,'personnels': personnels})

@login_required
def liste_acte_person(request):
    actes = Acte.objects.all().order_by('id')
    if request.method == "GET":
        titreAct = request.GET.get('recherche')
        if titreAct is not None:
            actes= Acte.objects.filter(numAct=titreAct) | Acte.objects.filter(titreAct__icontains=titreAct)
    return render(request, "personnel/liste_acte.html",{'actes':actes})

@login_required
def person_update_acte(request, id):
    if request.user.is_authenticated:
        actes = get_object_or_404(Acte, id=id)
        page = 'person_update_acte'
        administrateurs = User.objects.filter(is_personnel=True).order_by('username')
        if request.method == 'POST':
            titreAct=request.POST['titreAct']
            DescrpAct=request.POST['DescrpAct']
            objet = Acte.objects.get(id=id)
            objet.titreAct=titreAct
            objet.DescrpAct=DescrpAct
            objet.save()
            return redirect('liste_acte_person')
    return render(request, "personnel/update_acte.html",{'page':page,'actes':actes})

@login_required
def liste_archive_person(request):
    archives = Archive.objects.all().order_by('-id')
    archive_number = archives.count()
    if request.method == "GET":
        numDossier = request.GET.get('recherche')
        if numDossier is not None:
            archives= Archive.objects.filter(numDossier=numDossier) | Archive.objects.filter(titreDossier__icontains=numDossier)
    return render(request, "personnel/liste_archive.html",{'archives':archives,'archive_number':archive_number})

@login_required
def person_delete_dossier_archive(request, id):
    if request.user.is_authenticated:
        archive = get_object_or_404(Archive, id=id)
        archive.delete()
        return redirect('liste_archive_person')
    else:
        return redirect('connexion')
    
    
#Avocat
@login_required
def avocat_enregis_client(request):
    if request.user.is_authenticated:
        page = 'avocat_enregis_client'
        clients = Client.objects.all()
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username =  request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            nationalite = request.POST['nationalite'].lower()
            photo= request.FILES['photo']
            profession = request.POST['profession'].lower()
            adresse = request.POST['adresse'].lower()
            
            letters = string.ascii_letters
            digits = string.digits
            alphabet = digits + letters
            pwd_length = 6
            password=''
            for i in range(pwd_length):
                password += ''.join(secrets.choice(alphabet))
                
            is_client = True
            if User.objects.filter(email=email):
                messages.error(request, "L'adresse email existe déjà !")
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, genre=genre, email=email,phone=phone, photo=photo, adresse=adresse, password=password, is_client=is_client)
                client=Client.objects.create(user=user, profession=profession,nationalite=nationalite)
               
                print("Mode passe générer est: "+ password)
                
                if user is not None:
                    messages.success(request, "client enregistre avec succès !")
                    sujet = "Bienvenu(e) " + user.username + " " + user.first_name + " Vous êtes membre du cabinet *MUBENESHA* étant que client!"
                    message = "Votre mot de passe pour accéder au système est : " + password
                    expediteur = settings.EMAIL_HOST_USER
                    destinateur = [email]
                    send_mail(sujet, message, expediteur,destinateur, fail_silently=True)
                else:
                    messages.error(request, "L'enregistrement échoué !")
                
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                clients= Client.objects.filter(user__username__icontains=username) | Client.objects.filter(user__first_name__icontains=username)
    return render(request, "avocat/avocat_enregis_client.html",{'clients': clients})

@login_required
def avocat_update_client(request, id):
    if request.user.is_authenticated:
        clients = get_object_or_404(Client, user__id=id)
        page = 'avocat_update_client'
        if request.method == 'POST':
            first_name = request.POST['first_name'].lower()
            last_name = request.POST['last_name'].lower()
            username = request.POST['username'].lower()
            genre = request.POST['genre'].lower()
            email = request.POST['email']
            phone = request.POST['phone']
            nationalite = request.POST['nationalite'].lower()
            photo = request.FILES['photo']
            created_at = request.POST['created_at']
            profession = request.POST['profession'].lower()
            
            objet = User.objects.get(id=id)
            objet.first_name=first_name
            objet.last_name=last_name
            objet.username=username
            objet.genre=genre
            objet.email=email
            objet.phone=phone
            objet.photo=photo
            objet.created_at=created_at
            objet.save()
            
            objet1 = Client.objects.get(user__id=id)
            objet1.profession=profession
            objet1.nationalite=nationalite
            objet1.save()
            
            messages.success(request, "client a été modifier avec succès !")
            return redirect('avocat_enregis_client')
    return render(request, "avocat/update_client.html", {'page':page,'clients': clients})

def avocat_delete_client(request, id):
    if request.user.is_authenticated:
        client= get_object_or_404(User, id=id)
        client.delete()
        return redirect('avocat_enregis_client')
    else:
        return redirect('connexion')

@login_required
def avocat_ajout_dossier(request):
    if request.user.is_authenticated:
        page = 'avocat_ajout_dossier'
        avocats = User.objects.filter(is_avocat=True).order_by('username')
        dossiers = Dossier.objects.all().order_by('-id')
        clients = User.objects.filter(is_client=True).order_by('username')
        if request.method == 'POST':
            
            digits = string.digits
            nombre = digits
            pwd_length = 4
            numDossier =''
            for i in range(pwd_length):
                numDossier += ''.join(secrets.choice(nombre))
            
            titreDossier=request.POST['titreDossier']
            objDossier=request.POST['objDossier']
            username=int(request.POST['username'])
            id_username = User.objects.get(id=username)
            dateTimeOuverture=request.POST['dateTimeOuverture']
           
            if Dossier.objects.filter(numDossier=numDossier):
                messages.error(request, 'Le numero du dossier existe déjà !')
            else:
                new_dossier = Dossier.objects.create(numDossier=numDossier, titreDossier=titreDossier,objDossier=objDossier,username=id_username,
                                                     dateTimeOuverture=dateTimeOuverture)
                if new_dossier is not None:
                    messages.success(request, "dossier ajouté avec succès !")
                    print("Numéro du dossier est: "+ numDossier)
                else:
                    messages.error(request, "L'enregistrement échoué !")
        if request.method == "GET":
            titreDossier = request.GET.get('recherche')
            if titreDossier is not None:
                dossiers = Dossier.objects.filter(titreDossier__icontains=titreDossier)| Dossier.objects.filter(numDossier=titreDossier) 
    return render(request, 'avocat/avocat_ajout_dossier.html',{'page': page,'clients': clients,'avocats': avocats,'dossiers': dossiers})

@login_required
def avocat_update_dossier(request, id):
    if request.user.is_authenticated:
        dossiers = get_object_or_404(Dossier, id=id)
        page = 'avocat_update_dossier'
        avocats = User.objects.filter(is_avocat=True).order_by('username')
        if request.method == 'POST':
            numDossier=request.POST['numDossier']
            titreDossier=request.POST['titreDossier']
            objDossier=request.POST['objDossier']
            dateTimeFermeture=request.POST['dateTimeFermeture']
            
            objet = Dossier.objects.get(id=id)
            objet.numDossier=numDossier
            objet.titreDossier=titreDossier
            objet.objDossier=objDossier
            objet.dateTimeFermeture=dateTimeFermeture
            objet.save()
            messages.success(request, "dossier a été clôturer avec succès !")
            return redirect('avocat_ajout_dossier')
    return render(request, "avocat/avocat_update_dossier.html", {'page':page,'dossiers': dossiers,'avocats': avocats})

@login_required
def avocat_liste_send_file(request):
    if request.user.is_authenticated:
        fichiers = Fichier.objects.all().order_by('id')
        fichier_number = fichiers.count()
        
    if request.method == "GET":
            titre = request.GET.get('recherche')
            if titre is not None:
                fichiers = Fichier.objects.filter(titre__icontains=titre) |Fichier.objects.filter(fichier__icontains=titre)
    return render(request, "avocat/liste_send_file.html",{'fichiers':fichiers,'fichier_number':fichier_number})

@login_required
def avocat__delete_send_file(request, id):
    if request.user.is_authenticated:
        fichiers = get_object_or_404(Fichier, id=id)
        fichiers.delete()
        return redirect('avocat_liste_send_file')
    else:
        return redirect('connexion')

@login_required
def avocat_update_ach_dossier(request, id):
    if request.user.is_authenticated:
        dossiers = get_object_or_404(Dossier, id=id)
        postarchive = Dossier.objects.all()
        page = 'avocat_update_ach_dossier'
        
        if request.method == 'POST':
            numDossier=request.POST['numDossier']
            titreDossier=request.POST['titreDossier']
            objDossier=request.POST['objDossier']
            
            
            dateTimeOuverture=request.POST["dateTimeOuverture"]
            dateTimeFermeture=request.POST["dateTimeFermeture"]
            arc_dossier = Archive.objects.create(numDossier=numDossier, titreDossier=titreDossier, objDossier=objDossier,
                                                 dateTimeOuverture=dateTimeOuverture,dateTimeFermeture=dateTimeFermeture)
            
            arc_dossier = get_object_or_404(Dossier, id=id) 
            arc_dossier.delete()
            messages.success(request, "dossier a été archiver avec succès !") 
            return redirect('avocat_ajout_dossier')
    return render(request, "avocat/avocat_update_ach_dossier.html", {'dossiers': dossiers,'postarchive':postarchive})

@login_required
def avocat_delete_dossier_archive(request, id):
    if request.user.is_authenticated:
        archive = get_object_or_404(Archive, id=id)
        archive.delete()
        return redirect('avocat_archive_post_dossier_view')
    else:
        return redirect('connexion')
@login_required  
def avocat_archive_post_dossier_view(request):
    archives = Archive.objects.all().order_by('id')
    archive_number = archives.count()
    if request.method == "GET":
        titreDossier = request.GET.get('recherche')
        if titreDossier is not None:
            archives= Archive.objects.filter(titreDossier__icontains=titreDossier) | Archive.objects.filter(numDossier__icontains=titreDossier)
    return render(request,'avocat/archive.html',{'archives':archives,'archive_number':archive_number})

@login_required
def avocat_delete_dossier(request, id):
    if request.user.is_authenticated:
        dossier = get_object_or_404(Dossier, id=id)
        dossier.delete()
        return redirect('avocat_ajout_dossier')
    else:
        return redirect('connexion')

@login_required
def avocat_recherche_dossier(request):
    dossier = Dossier.objects.all()
    if request.method == "GET":
        numDossier = request.GET.get('recherche') 
        if numDossier is not None:
            dossier= Dossier.objects.filter(numDossier=numDossier)
    context = {
        'dossiers':dossier,
    }
    return render(request,'avocat_ajout_dossier',context)


@login_required
def avocat_redige_acte(request):
    if request.user.is_authenticated:
        page = 'avocat_redige_acte'
        avocats = User.objects.filter(is_avocat=True).order_by('username')
        actes = Acte.objects.all()
        dossiers = Dossier.objects.all().order_by('-id')
        if request.method == 'POST':
            numDossier=int(request.POST['numDossier'])
            id_numDossier = Dossier.objects.get(id=numDossier)
            titreAct=request.POST['titreAct']
            DescrpAct=request.POST['DescrpAct']
            fichierActe=request.FILES['fichierActe']
            if Acte.objects.filter(numDossier=numDossier):
                messages.error(request, "Le numero de l'acte existe déjà !")
            else:
                new_acte= Acte.objects.create(numDossier=id_numDossier, titreAct=titreAct, DescrpAct=DescrpAct, fichierActe=fichierActe)
                messages.success(request, "Acte rédiger et enregitre avec succès !")
                
        if request.method == "GET":
            titreAct = request.GET.get('recherche')
            if titreAct is not None:
                actes= Acte.objects.filter(titreAct__icontains=titreAct) | Acte.objects.filter(fichierActe__icontains=titreAct)
    return render(request, 'avocat/avocat_redige_acte.html',{'page': page,'avocats': avocats,'actes': actes,'dossiers': dossiers})

@login_required
def avocat_update_acte(request, id):
    if request.user.is_authenticated:
        actes = get_object_or_404(Acte, id=id)
        page = 'avocat_update_acte'
        avocats = User.objects.filter(is_avocat=True).order_by('username')
        if request.method == 'POST':
            titreAct=request.POST['titreAct']
            DescrpAct=request.POST['DescrpAct']
            fichierActe=request.FILES['fichierActe']
            objet = Acte.objects.get(id=id)
            objet.titreAct=titreAct
            objet.DescrpAct=DescrpAct
            objet.fichierActe=fichierActe
            objet.save()
            messages.success(request, "l'acte a été modifier avec succès !")
            return redirect('avocat_redige_acte')
    return render(request, "avocat/avocat_update_acte.html", {'page':page,'actes': actes,'avocats': avocats})

def avocat_delete_acte(request, id):
    if request.user.is_authenticated:
        acte = get_object_or_404(Acte, id=id)
        acte.delete()
        return redirect('avocat_redige_acte')
    else:
        return redirect('connexion')


#Client
def client(request):
    if request.user.is_authenticated:
        id_username = request.user.id
        dossiers = Dossier.objects.filter(username=id_username)
        
        if request.method == "GET":
            username = request.GET.get('recherche')
            if username is not None:
                dossiers = Dossier.objects.filter(titreDossier=username) | Dossier.objects.filter(objDossier__icontains=username)
    return render(request, "client/client.html",{'dossiers':dossiers})

def mon_espace_client(request):
    return render(request, "client/mon_espace.html")

def send_file_avocat(request):
    if request.user.is_authenticated:
        id_username = request.user.id
        avocats = User.objects.filter(is_avocat=True).order_by('username')
        
        if request.method == 'POST':
            titre = request.POST['titre'].lower()
            username = int(request.POST['username'])
            id_av_username = User.objects.get(id=username)
            name_client = request.POST['name_client'].lower()
            fichier = request.FILES['fichier']
            date_send=request.POST['date_send']
            objet = Fichier.objects.create(titre = titre, username = id_av_username, name_client=name_client, fichier = fichier, date_send = date_send)
            objet.save()
            if objet is not None:
                messages.success(request, "Fichier envoyé avec succès !")
            else:
                messages.error(request, "Fichier non envoyé !")
        
    return render(request, "client/send_file_avocat.html",{'avocats': avocats})


def not_found(request, exception):
    return render(request,'erreur.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('connexion')
