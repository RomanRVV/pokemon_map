from .models import Pokemon, PokemonEntity


def show_previous_evolution(requested_pokemon):
    if requested_pokemon.previous_evolution:
        if requested_pokemon.previous_evolution.image:
            previous_evolution_img_url = request.build_absolute_uri(requested_pokemon.previous_evolution.image.url)
        else:
            previous_evolution_img_url = None
    pokemon["previous_evolution"] = {"title_ru": requested_pokemon.previous_evolution.title,
                                     "pokemon_id": requested_pokemon.previous_evolution.id,
                                     "img_url": previous_evolution_img_url
                                     }
