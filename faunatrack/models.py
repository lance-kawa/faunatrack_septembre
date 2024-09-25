from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.models import User
from django.core.mail import send_mail    
from django.utils.text import slugify  
import uuid
import logging

logger = logging.getLogger()

class BaseModel(models.Model):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, blank=True) # /!\ Les méthodes des modules doivent être référecé et non pas appelés (pas de parenthèse)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # name = models.CharField(unique=True)
    # slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
        

class Scientifique(models.Model):
    class Role(models.TextChoices):
        ADMIN = ("Admin", "Administateur")
        CREATEUR = ("Createur", "Propriétaire")
        CONTRIBUTEUR = ("Contributeur", "contributeur")
        OBSERVATEUR = ("Observateur", "Observateur")
    
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="scientifique") #user.scientifique
    role = models.CharField(choices=Role.choices, default=Role.OBSERVATEUR, max_length=255)
    # roles = models.JSONField(default=[])
    
    def __str__(self) -> str:
        return self.user.username 
    
    class Meta:
        verbose_name = "Utilisateur Faunatrack"   
        verbose_name_plural = "Utilisateurs Faunatrack"

# DECONSEILLE   
# class FaunatrackUser(AbstractUser):
#     universite = ...

class Espece(models.Model):

    class StatusChoice(models.TextChoices):
        SAIN = ("HDD", "Hors de danger")
        EN_VOIE_DE_DISPARITION = "En voie d'extinction"
        DANGER = "En Danger"

    nom = models.CharField(max_length=255, verbose_name=_("nom"), unique=True)
    status = models.CharField(max_length=255, choices=StatusChoice.choices, default=StatusChoice.SAIN, verbose_name="status de l'espèce")

    def __str__(self):
        """ Override __str__ method from django to have a nice name on UX """
        return f"{self.nom}, le plus aimé de tout les animaux"
        
    def destroy(self):
        print('bonjour')



    

class Projet(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scientifique = models.ForeignKey(Scientifique, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(blank=True)
    # uuid = models.UUIDField(primary_key=True, unique=True) # 1 2 3 => "az14-aze25-aze6-dsf57"

    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titre) # Mon premier titre => mon-premier-titre // mon_premier_titre => mon-premier-titre
        logger.info("Projet à bien été sauvegardé", titre=self.titre)
        super().save( *args, **kwargs)

class Observation(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="observations")
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, related_name="observations") # espece.observations  -> [ obs1, obs2 ]
    coordonnee = models.ForeignKey("faunatrack.Coordonnee", related_name="observations", on_delete=models.PROTECT) 
    quantite = models.IntegerField(default=0) # On considère qu'une observation peut être échouée et avoir observé 0 especes
    date = models.DateTimeField()    
    notes = models.TextField()
    images = models.ImageField(upload_to="obs_especes/", default=None, null=True)

    def __str__(self):
        return f"{self.espece} observé le {self.date} à {self.coordonnee}"
    
    class Meta:
        unique_together = ["espece", "coordonnee"]

##### 
# VALIDATORS FOR COORDONNE
#####
def validate_lattitude(value):  # BDD et Serveur Web
    if value < -90 or value > 90:
        raise ValidationError("La latitude doit être comprise entre -90 et 90 degree")                  
    
def validate_lattidue_not_a_string(value):
    # try:
    #     CoordonnePydantic(lattitude=value)
    # a = {
    #     "nom": "bastien",
    #     "prénom": "jean"
    # 
    # }
    # class NameDict(BaseModel):
    #     nom: str
    #     prenom: str
    
    # data = NameDict(**a)
    # if data.nom == "bastien":
    #     pass
    # except pydantic.ValueError as e :

    if isinstance(value, str):
        raise ValidationError("La latitude doit être comprise entre -90 et 90 degree")
    
def validate_longitude(value):  
    if value < -180 or value > 180:
        raise ValidationError("La longitude doit être comprise entre -180 et 180 degree")



class Coordonnee(models.Model):
    lattitude = models.DecimalField(max_digits=13, decimal_places=10, default=None, null=True, blank=True, validators=[validate_lattitude, validate_lattidue_not_a_string])
    longitude =  models.DecimalField(max_digits=13, decimal_places=10, default=None, null=True, blank=True, validators=[validate_longitude])
    url_google_maps = models.URLField(verbose_name="google url", null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"LAT: {self.lattitude}, LONG: {self.longitude}"  

    def gps_to_google_maps_url(self):
        """ Method for Faunatrack logic """
        return f"http://maps.google.com/maps?q={self.lattitude},{self.longitude}"
 
    def save(self, *args, **kwargs):
        """ Override the save method for alter attributes when saving the model """
        # rajouter des actions AVANT la modification en bdd
        self.url_google_maps = self.gps_to_google_maps_url()
        super().save(*args, **kwargs)
        subject = 'Salut de Django'
        message = 'Ceci est un message test envoyé par Django.'
        email_from = 'your-email@example.com'
        recipient_list = ['recipient1@example.com', 'recipient2@example.com']
        send_mail(subject, message, email_from, recipient_list)
        # rajouter des actions APRES la modification en bdd
