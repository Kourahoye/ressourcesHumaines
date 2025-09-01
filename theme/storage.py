from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
import os

# Liste des fichiers/dirs à garder
WHITELIST = [
    "css/",       # CSS FA et ton CSS perso
    "js/",        # JS FA et ton JS perso
    "webfonts/",  # Polices FA
]

class MinimalFontAwesomeStorage(ManifestStaticFilesStorage):
    def should_copy_file(self, path, source_storage):
        # On garde le fichier si son chemin commence par un des éléments de la whitelist
        for item in WHITELIST:
            if path.startswith(item):
                return True
        return False
