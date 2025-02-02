from django.db import models  # noqa F401
from datetime import datetime


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Имя покемона")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Имя покемона на английском")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Имя покемона на японском")
    image = models.ImageField(upload_to='images', verbose_name="Изображение покемона")
    description = models.TextField(blank=True, verbose_name="Описание покемона")
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name="next_evolutions",
                                           verbose_name="Предыдущая эволюция покемона")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name="entities",
                                verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появится в:")
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет в:")
    level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
    strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")

    def __str__(self):
        return self.pokemon.title
