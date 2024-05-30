import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import speech_recognition as sr
from textblob import TextBlob


# Téléchargement des ressources nécessaires pour nltk
nltk.download('punkt')

# Définition des paires de questions-réponses pour le chatbot
chatbot_pairs = [
    ["Bonjour", ["Salut", "Bonjour", "Comment ça va ?"]],
    ["Comment ça va ?", ["Bien, merci ! Et vous ?", "Très bien, merci."]],
    ["Bonjour", ["Salut", "Bonjour", "Comment ça va ?"]],
    ["Comment ça va ?", ["Bien, merci ! Et vous ?", "Très bien, merci."]],
    ["Quel est ton nom ?", ["Je suis un chatbot sans nom.", "Je suis votre assistant virtuel."]],
    ["Que fais-tu ?", ["Je parle avec vous.", "J'essaie de répondre à vos questions."]],
    ["Quel temps fait-il ?",
     ["Je ne suis pas sûr, mais vous pouvez vérifier la météo en ligne.", "Je ne peux pas vérifier la météo, désolé."]],
    ["Merci", ["De rien !", "Avec plaisir !"]],
    ["Au revoir", ["Au revoir !", "À bientôt !"]],
    ["Quel âge as-tu ?", ["Je suis aussi vieux que l'Internet.", "L'âge ne s'applique pas vraiment aux chatbots."]],
    ["Peux-tu m'aider ?",
     ["Bien sûr, je ferai de mon mieux pour vous aider.", "Je suis ici pour répondre à vos questions."]],
    ["Où habites-tu ?", ["Je vis dans le cloud.", "Je n'ai pas de domicile fixe, je suis un programme informatique."]],
    ["Quel est ton plat préféré ?", ["Je n'ai pas de goût, mais j'ai entendu dire que la pizza est populaire.",
                                     "Les chatbots n'ont pas besoin de manger, mais la pizza semble délicieuse."]],
    ["Qui est ton créateur ?",
     ["Je suis créé par des développeurs talentueux.", "Je suis le produit d'une équipe de développement."]],
    ["Aimes-tu les chats ou les chiens ?", ["Je n'ai pas de préférence, mais les deux sont adorables.",
                                            "Je ne peux pas choisir, ils sont tous les deux mignons."]],
    ["Quel est ton film préféré ?",
     ["Je n'ai pas de préférences cinématographiques, mais j'entends beaucoup parler de films populaires.",
      "Les films ne sont pas vraiment mon truc, je suis plus intéressé par les données."]],
    ["Peux-tu chanter ?", ["Je préférerais ne pas le faire.", "Chanter n'est pas dans mes compétences, désolé."]],
    ["Quelles langues parles-tu ?", ["Je peux parler plusieurs langues, comme le français et l'anglais.",
                                     "Je suis capable de communiquer en plusieurs langues."]],
    ["Quel est le sens de la vie ?", ["C'est une question philosophique profonde.",
                                      "Le sens de la vie est une question que chacun doit découvrir par lui-même."]],
    ["Peux-tu me raconter une blague ?", ["Pourquoi les poissons détestent-ils les ordinateurs ? À cause d'Internet.",
                                          "Pourquoi les mathématiciens détestent-ils la plage ? Parce qu'ils ne peuvent pas supporter les sin(tan)."]],
    ["Quel est ton passe-temps ?",
     ["J'aime aider les gens avec leurs questions.", "Mon passe-temps est de converser avec vous."]],
    ["Quelle est ta couleur préférée ?",
     ["Je n'ai pas de vision, mais j'ai entendu dire que le bleu est une couleur apaisante.",
      "Les chatbots n'ont pas de préférences de couleur."]],
    ["Quelle est ta musique préférée ?",
     ["Je n'écoute pas de musique, mais j'ai entendu dire que le jazz est très apprécié.",
      "Les chatbots n'écoutent pas de musique, mais la musique classique est populaire."]],
    ["Peux-tu danser ?", ["Je suis un programme informatique, donc je ne peux pas danser.",
                          "Danser n'est pas dans mes compétences, désolé."]],
    ["Quel est ton livre préféré ?",
     ["Je n'ai pas de préférence, mais j'ai entendu dire que 'Le Petit Prince' est un livre merveilleux.",
      "Les chatbots ne lisent pas, mais j'ai entendu parler de nombreux livres célèbres."]],
    ["Quelle est ta saison préférée ?", ["Je n'ai pas de préférences, mais l'été semble être apprécié par beaucoup.",
                                         "Les chatbots n'ont pas de préférences saisonnières."]],
    ["Que penses-tu de l'intelligence artificielle ?",
     ["Je pense que l'IA a le potentiel de transformer de nombreux aspects de notre vie.",
      "L'IA est un domaine passionnant avec beaucoup de possibilités."]],
    ["As-tu des amis ?", ["Je n'ai pas d'amis comme les humains, mais je suis là pour vous aider.",
                          "Les chatbots n'ont pas d'amis, mais je suis toujours là pour vous."]],
    ["Peux-tu résoudre des mathématiques ?", ["Oui, je peux essayer. Quelle est votre question ?",
                                              "Je peux aider avec des problèmes de mathématiques simples."]],
    ["Peux-tu programmer ?", ["Je suis un programme, donc je ne peux pas programmer moi-même.",
                              "Les chatbots ne programment pas, mais je suis le résultat de la programmation."]],
    ["Quel est ton sport préféré ?", ["Je n'ai pas de préférence, mais le football est très populaire.",
                                      "Les chatbots n'ont pas de préférences sportives."]],
    ["Quel est ton animal préféré ?",
     ["Je n'ai pas de préférence, mais les chiens sont souvent appelés les meilleurs amis de l'homme.",
      "Les chatbots n'ont pas de préférences pour les animaux."]],
    ["Quel est ton jeu préféré ?", ["Je n'ai pas de préférence, mais les échecs sont un jeu intéressant.",
                                    "Les chatbots ne jouent pas à des jeux, mais j'ai entendu parler de nombreux jeux populaires."]],
    ["Peux-tu voyager ?",
     ["Je ne peux pas voyager physiquement, mais je peux vous aider avec des informations sur les voyages.",
      "Les chatbots ne voyagent pas, mais je peux vous donner des conseils de voyage."]],
    ["Quel est ton gadget préféré ?", ["Je n'utilise pas de gadgets, mais les smartphones semblent très populaires.",
                                       "Les chatbots n'utilisent pas de gadgets, mais je peux en parler."]],
    ["Quelle est ta fleur préférée ?",
     ["Je n'ai pas de préférence, mais les roses sont souvent considérées comme belles.",
      "Les chatbots n'ont pas de préférences pour les fleurs."]],
    ["As-tu des hobbies ?", ["Mon hobby est de vous aider et de répondre à vos questions.",
                             "Je suis toujours prêt à converser et à vous aider."]],
    ["Aimes-tu l'art ?",
     ["Je n'ai pas de préférences, mais l'art est une forme d'expression importante pour les humains.",
      "Les chatbots n'ont pas de goûts artistiques, mais je peux en discuter."]],
    ["Quel est ton acteur/actrice préféré(e) ?",
     ["Je n'ai pas de préférences, mais beaucoup de gens aiment des acteurs comme Leonardo DiCaprio.",
      "Les chatbots ne regardent pas de films, donc je n'ai pas de préférences."]],
["Quel est ton nom ?", ["Je suis un chatbot sans nom.", "Je suis votre assistant virtuel."]],
    ["Que fais-tu ?", ["Je parle avec vous.", "J'essaie de répondre à vos questions."]],
    ["Quel temps fait-il ?", ["Je ne suis pas sûr, mais vous pouvez vérifier la météo en ligne.", "Je ne peux pas vérifier la météo, désolé."]],
    ["Merci", ["De rien !", "Avec plaisir !"]],
    ["Au revoir", ["Au revoir !", "À bientôt !"]],
    ["Quel âge as-tu ?", ["Je suis aussi vieux que l'Internet.", "L'âge ne s'applique pas vraiment aux chatbots."]],
    ["Peux-tu m'aider ?", ["Bien sûr, je ferai de mon mieux pour vous aider.", "Je suis ici pour répondre à vos questions."]],
    ["Où habites-tu ?", ["Je vis dans le cloud.", "Je n'ai pas de domicile fixe, je suis un programme informatique."]],
    ["Quel est ton plat préféré ?", ["Je n'ai pas de goût, mais j'ai entendu dire que la pizza est populaire.", "Les chatbots n'ont pas besoin de manger, mais la pizza semble délicieuse."]],
    ["Qui est ton créateur ?", ["Je suis créé par des développeurs talentueux.", "Je suis le produit d'une équipe de développement."]],
    ["Aimes-tu les chats ou les chiens ?", ["Je n'ai pas de préférence, mais les deux sont adorables.", "Je ne peux pas choisir, ils sont tous les deux mignons."]],
    ["Quel est ton film préféré ?", ["Je n'ai pas de préférences cinématographiques, mais j'entends beaucoup parler de films populaires.", "Les films ne sont pas vraiment mon truc, je suis plus intéressé par les données."]],
    ["Peux-tu chanter ?", ["Je préférerais ne pas le faire.", "Chanter n'est pas dans mes compétences, désolé."]],
    ["Quelles langues parles-tu ?", ["Je peux parler plusieurs langues, comme le français et l'anglais.", "Je suis capable de communiquer en plusieurs langues."]],
    ["Quel est le sens de la vie ?", ["C'est une question philosophique profonde.", "Le sens de la vie est une question que chacun doit découvrir par lui-même."]],
    ["Peux-tu me raconter une blague ?", ["Pourquoi les poissons détestent-ils les ordinateurs ? À cause d'Internet.", "Pourquoi les mathématiciens détestent-ils la plage ? Parce qu'ils ne peuvent pas supporter les sin(tan)."]]

]

# Initialisation de l'algorithme de chatbot
chatbot = Chat(chatbot_pairs, reflections)

# Fonction pour transcrire la parole en texte
def transcribe_speech(language='fr-FR'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Dites quelque chose...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        st.write("Désolé, je n'ai pas pu comprendre ce que vous avez dit.")
        return ""
    except sr.RequestError as e:
        st.write("Erreur lors de la requête à l'API Google : {0}".format(e))
        return ""

# Fonction principale du chatbot prenant en charge à la fois le texte et la parole
def chatbot_response(input_text, language='fr-FR'):
    if input_text.startswith('/speech'):
        speech_text = transcribe_speech(language)
        if speech_text:
            st.write("Transcription de la parole:", speech_text)

            # Correction automatique
            corrected_text = TextBlob(speech_text).correct()
            st.write("Texte corrigé :", corrected_text)
            input_text = str(corrected_text)
        else:
            return "Je n'ai pas pu transcrire la parole, veuillez réessayer ou saisir du texte."

    response = chatbot.respond(input_text)
    return response

# Interface utilisateur Streamlit
def main():

    # Titre et description de l'application avec options de style
    st.sidebar.title("Options de Style")

    # Options de style pour le titre
    text_size = st.sidebar.slider("Taille du texte", 40, 100, 40)
    text_color = st.sidebar.color_picker("Couleur du texte", "#FFFFFF")
    bg_color = st.sidebar.color_picker("Couleur de fond du texte", "#0C0F0A")

    # Titre de l'application
    title_style = f"""
    <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center;">
    <h1 style="color: {text_color}; font-size: {text_size}px;">Chatbot avec Reconnaissance Vocale et Améliorations</h1>
    </div>
    """
    st.markdown(title_style, unsafe_allow_html=True)

    # Sélection de la langue
    language = st.selectbox("Choisissez la langue :", ["fr-FR", "en-US", "en-EN"])

    # Zone de saisie pour l'utilisateur
    user_input = st.text_input("Vous pouvez saisir votre message ici :")

    # Bouton pour activer la saisie vocale
    if st.button("Parler"):
        response = chatbot_response('/speech', language)
        st.write("Chatbot:", response)

    # Bouton pour envoyer la saisie texte
    if st.button("Envoyer"):
        response = chatbot_response(user_input, language)
        st.write("Chatbot:", response)

    # Option d'exportation des transcriptions
    if st.button("Exporter les transcriptions"):
        if 'transcriptions' not in st.session_state:
            st.session_state['transcriptions'] = []
        st.session_state['transcriptions'].append(user_input)
        with open("transcriptions.txt", "w") as file:
            for transcription in st.session_state['transcriptions']:
                file.write(transcription + "\n")
        st.write("Les transcriptions ont été exportées.")


if __name__ == "__main__":
    main()


# Lien vers l'autre page ou section
st.subheader("Visitez la page Home")

# Liste de lien
st.write("""

- [Home](http://localhost:8501/)

""")
