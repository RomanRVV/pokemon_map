import folium
from django.utils.timezone import localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_img_url(request, pokemon):
    if not pokemon.image:
        return
    img_url = request.build_absolute_uri(pokemon.image.url)
    return img_url






def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    local_time = localtime()
    active_pokemons = PokemonEntity.objects.filter(appeared_at__lte=local_time,
                                                   disappeared_at__gte=local_time)
    for pokemon_entity in active_pokemons:
        pokemon_entity_img_url = get_img_url(request, pokemon_entity)
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity_img_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemon_img_url = get_img_url(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon_img_url = get_img_url(request, requested_pokemon)
    pokemon = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": pokemon_img_url
    }

    previous_evolution = requested_pokemon.previous_evolution
    if previous_evolution:
        previous_evolution_img_url = get_img_url(request, previous_evolution)
        pokemon["previous_evolution"] = {"title_ru": previous_evolution.title,
                                         "pokemon_id": previous_evolution.id,
                                         "img_url": previous_evolution_img_url
                                         }

    next_evolutions = requested_pokemon.next_evolutions.all()
    for next_evolution in next_evolutions:
        next_evolution_img_url = get_img_url(request, next_evolution)
        pokemon["next_evolution"] = {"title_ru": next_evolution.title,
                                     "pokemon_id": next_evolution.id,
                                     "img_url": next_evolution_img_url
                                     }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    local_time = localtime()
    active_pokemons = requested_pokemon.entities.filter(appeared_at__lte=local_time,
                                                        disappeared_at__gte=local_time)
    for pokemon_entity in active_pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_img_url
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
