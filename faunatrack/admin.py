from django.contrib import admin

from faunatrack.models import Coordonnee, Espece, Observation, Projet, Scientifique

# Register your models here.
@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ["nom", "status"]
    list_filter = ["status"]
    search_fields = ["nom", "status"]
    ordering = ["-nom"]
    list_editable = ["status"]


class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 1

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ["date", "espece"]
    
@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ["titre", "scientifique"]
    exclude = ("slug",)
    inlines = [ObservationInline] 

@admin.register(Scientifique)
class ScientifiqueAdmin(admin.ModelAdmin):
    list_display = ["user__username", "role"] #user.username



@admin.register(Coordonnee)
class CoordonneeAdmin(admin.ModelAdmin):
    list_display = ["lattitude", "longitude"]
    exclude = ['url_google_maps']