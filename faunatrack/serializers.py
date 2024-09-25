from rest_framework import serializers

from faunatrack.models import Projet, Scientifique


class ScientifiqueSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() # get_xxx

    def get_user(self, object):
        return object.user.username
    
    class Meta:
        model = Scientifique
        fields = '__all__'

    

class ProjetSerializer(serializers.ModelSerializer):

    scientifique = ScientifiqueSerializer(read_only=True)
    extra_message = serializers.SerializerMethodField(read_only=True) # get_xxx

    def get_extra_message(self, object):
        if "pabo" in object.titre:
            return "Votre titre est moche"
        return "Maginifique titre !" 

    class Meta:
        model = Projet
        exclude = [ 'updated_at']
        read_only_fields = ["created_at", ]