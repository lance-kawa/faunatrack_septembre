from email.message import EmailMessage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from faunatrack.forms import ProjetForm
from faunatrack.models import Espece, Projet, Scientifique
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

import logging

logger = logging.getLogger()

def send_html_email(request):
    subject = "Salut de Django avec HTML"
    body = """
    <html>
        <body>
            <h1>Ceci est un test d'email HTML envoyé depuis Django</h1>
            <p>C'est beaucoup plus joli avec du HTML, n'est-ce pas ?</p>
        </body>
    </html>
    """

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='your-email@example.com',
        to=['recipient@example.com'],
        reply_to=['another@example.com'],
        headers={'Content-Type': 'text/html'},  # Cet en-tête n'est pas nécessaire pour les e-mails HTML
    )
    email.content_subtype = 'html'  # Indique à Django que le corps du message est du HTML
    email.send()

    return HttpResponse("Email HTML envoyé !")



# Create your views here.
def base(request: HttpRequest):
    # request.user = # None / "AnonymousUser" / User
    if request.user.is_authenticated:
        # espece = get_object_or_404(Espece, nom="ours")
        return render(request, 'base.html', {
        'especes': "espece"
    } )
        
    return redirect('login')
   


@login_required
def home(request):
    return render(request, 'home.html', {
        'price': '30',
    } )

def projet_with_2_project_displayed(request):
    projets = Projet.objects.all()
    return render(request, 'projet_list.html', {
        "object_list": projets,
        'projet_1': projets.first(),            
        'projet_2': projets.last()
    } )



class AuthorizedMixin(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin) :
    def test_func(self):
        # # GUARD CLAUSE

        # # MAUVAISE METHODE
        # if something.exist:
        #     return True
        # else:
        #     return False

        # # BONNE METHODE
        # if not something.exist:
        #     return False
        
        # return True
        
        try:
            scientifique = self.request.user.scientifique
        except Scientifique.DoesNotExist as e:        
            logger.warning(f"WARNING: {e}")
            return False
       
        if scientifique.role == Scientifique.Role.OBSERVATEUR:
            return False
        
        return True
    


class ProjetList(AuthorizedMixin, ListView): # L'ordre est important !!!!
    model = Projet
    template_name = "projet_list.html"
    queryset = Projet.objects.all()
    permission_required = "faunatrack.view_projet" # view_xxx | add_xxx | change_xxx | delete_xxxx 
    
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     return { "couleur_du_ciel": "blue-500"}

    # def get_queryset(self) -> QuerySet[Any]:
    #     return Projet.objects.filter(titre="Mon premier projet")

class ProjetCreate(AuthorizedMixin, CreateView):
    model = Projet
    template_name = "projet_create.html"
    form_class = ProjetForm
    success_url = reverse_lazy('projets_list')
    permission_required = "faunatrack.add_projet"  

class ProjetUpdate(AuthorizedMixin, UpdateView):
    model = Projet
    template_name = "projet_update.html"
    form_class = ProjetForm
    success_url = reverse_lazy('projets_list')
    permission_required = "faunatrack.change_projet"

class ProjetDetail(AuthorizedMixin, DetailView):
    model = Projet
    template_name = "projet_detail.html"
    success_url = reverse_lazy('projets_list')
    permission_required = "faunatrack.view_projet"

class ProjetDelete(AuthorizedMixin, DeleteView):
    model = Projet
    template_name = "projet_delete.html"
    success_url = reverse_lazy('projets_list')
    permission_required = "faunatrack.delete_projet"


    # espece = Espece.objects.first() # 1 er record
    # espece = Espece.objects.last() # Last record
    # espece = Espece.objects.all() # Toute la table
    # espece = Espece.objects.filter(status=Espece.StatusChoice.SAIN) # Tout les animaux hors de danger
    # try:
    #     espece = Espece.objects.get(status=Espece.StatusChoice.DANGER)
    #     return HttpResponse(espece) # "(1) Objects on Espece" / "Ours, le plus aimé des animaux"
    # except Espece.DoesNotExist as e: 
    #     print(f'Error ! {e}')
    #     return HttpResponse('Pas de espece')
    # except Espece.MultipleObjectsReturned as error: 
    #     print(f'Error ! {error}')
    #     return HttpResponse('Trop de espece')
    # espece = Espece.objects.filter(status=Espece.StatusChoice.DANGER).first() # None
    # if espece:
    #     return HttpResponse(espece)
    # return HttpResponse('Pas de espece')
    # Espece.objects.filter(nom!='ours') # ERROR
    # espece = Espece.objects.exclude(status=Espece.StatusChoice.SAIN).first() # Tout les animaux EN danger
    # observation = Observation.objects.all().order_by("-date", "quantite")
    # observation = Observation.objects.filter(projet__scientifique__user__username__contains="bast")
    # especes_id = Observation.objects.filter(date__gte=timezone.now()).values("espece__id")

    # Espece.objects.create(nom="ours")
    # espece, created = Espece.objects.get_or_create(nom="ours", default={'status': Espece.StatusChoice.DANGER}) # (espece, created)
    # Espece.objects.all().delete() # /!\ N'appel la méthode delete ou save du modèle, l'opération se fait sur le QUERYSET
    # Espece.objects.all().update() # /!\ N'appel la méthode delete ou save du modèle, l'opération se fait sur le QUERYSET

    # ours = Espece.objects.filter(nom="ours").first()
    # ours.status = Espece.StatusChoice.DANGER
    # ours.save()
    



