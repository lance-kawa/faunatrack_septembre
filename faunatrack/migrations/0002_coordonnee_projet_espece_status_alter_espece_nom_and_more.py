# Generated by Django 5.1.1 on 2024-09-23 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faunatrack', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordonnee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lattitude', models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=13, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=10, default=None, max_digits=13, null=True)),
                ('url_google_maps', models.URLField(blank=True, default=None, null=True, verbose_name='google url')),
            ],
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='espece',
            name='status',
            field=models.CharField(choices=[('HDD', 'Hors de danger'), ("En voie d'extinction", 'En Voie De Disparition'), ('En Danger', 'Danger')], default='HDD', max_length=255, verbose_name="status de l'espèce"),
        ),
        migrations.AlterField(
            model_name='espece',
            name='nom',
            field=models.CharField(max_length=255, unique=True, verbose_name='nom'),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=0)),
                ('date', models.DateTimeField()),
                ('notes', models.TextField()),
                ('coordonnee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='observations', to='faunatrack.coordonnee')),
                ('espece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='faunatrack.espece')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='faunatrack.projet')),
            ],
        ),
        migrations.CreateModel(
            name='Scientifique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Admin', 'Administateur'), ('Createur', 'Propriétaire'), ('Contributeur', 'contributeur'), ('Observateur', 'Observateur')], default='Observateur', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='scientifique', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='projet',
            name='scientifique',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='faunatrack.scientifique'),
        ),
    ]
