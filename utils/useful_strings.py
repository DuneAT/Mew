class UsefulStrings:

    modelfile_text = """FROM {model_path}

    PARAMETER num_ctx {num_ctx}

    TEMPLATE {modelfile_template}

    PARAMETER stop <|im_end|>
    PARAMETER stop <|im_start|>user
    PARAMETER stop <|end|>"""

    modelfile_embedding_text = """FROM {model_path}"""

class UsefulStrings_fr:

    welcome = "Bienvenue sur Mew !"
    prompt = "Entrez votre texte ici..."
    ask = "Envoyer"
    upload = "Télécharger un document"
    delete = "Supprimer"
    file = "Fichier"
    close_preview = "Fermer l'aperçu"

class UsefulStrings_en:

    welcome = "Welcome on Mew!"
    prompt = "Enter your text here..."
    ask = "Ask"
    upload = "Upload a file"
    delete = "Delete"
    file = "File"
    close_preview = "Close preview"