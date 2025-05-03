import os
from flask import current_app

def get_precedente_suivante_recette(recette):
    plat = recette.plat_name
    for lsn in plat.recettes:
        if lsn.title == recette.title:
            index = plat.recettes.index(lsn)
            precedente_recette = plat.recettes[index - 1] if index > 0 else None
            suivante_recette = (
                plat.recettes[index + 1] if index < len(plat.recettes) - 1 else None
            )
            break
    return precedente_recette, suivante_recette

def delete_picture(picture_name, path):
    picture_path = os.path.join(current_app.root_path, path, picture_name)
    try:
        os.remove(picture_path)
    except:
        pass
