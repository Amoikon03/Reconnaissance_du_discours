import streamlit as st

# Titre et description de l'application avec options de style
st.sidebar.title("Options de Style")

# Options de style pour le titre
text_size = st.sidebar.slider("Taille du texte", 40, 100, 40)
text_color = st.sidebar.color_picker("Couleur du texte", "#FFFFFF")
bg_color = st.sidebar.color_picker("Couleur de fond du texte", "#0C0F0A")

# Titre de l'application
title_style = f"""
<div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center;">
<h1 style="color: {text_color}; font-size: {text_size}px;">Améliorer l'application de reconnaissance du discours</h1>
</div>
"""
st.markdown(title_style, unsafe_allow_html=True)

# Description
st.subheader("Description : ")

# Variables pour le style du titre
bg_color = '#f0f0f0'
text_color = '#333333'
text_size = 24

# Utilisation des colonnes de Streamlit pour organiser le texte et l'image côte à côte
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="text-align: justify;">
   Il s'agit d'améliorer une application de reconnaissance de la parole en ajoutant de nouvelles fonctionnalités pour augmenter sa fonctionnalité. Cela signifie probablement que l'application de base existe déjà et qu'elle est capable de convertir la parole en texte, mais qu'il y a des opportunités pour la rendre plus robuste, utile et conviviale.  
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("Reconnaissance du discours/A.jpg", caption="Reconnaissance automatique de la parole", use_column_width=True)

# Lien vers l'autre page ou section
st.subheader("Visitez la page Discours")
# Liste de lien
st.write("""

- [Discours](http://localhost:8501/Discours)

""")
