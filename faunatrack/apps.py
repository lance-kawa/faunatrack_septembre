from django.apps import AppConfig


class FaunatrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faunatrack'

    def ready(self):
        from faunatrack import signals # noqa

    

        # class PayloadRequestWeather(BaseModel):
        #     nom: str
        #     prenom: str


        # def get_weather(self):
        #     response = requests.post("url", json={
        #         "param1": "a"
        #     }, 
        #     headers = {
        #         "ContentType": "application/json"
        #     })
        #     if response.status_code == 200:
        #         "success"
        #     else:
        #         raise KeyError()
        #     # Toujours vérifier le status_code avant d'appeler json()
        #     payload = response.json()
        #     data = PayloadRequestWeather(**payload) # On peut utiliser pydantic pour valider les données reçues
        #     data.nom 

        #     requests.get()
        #     requests.delete()
        #     requests.put()