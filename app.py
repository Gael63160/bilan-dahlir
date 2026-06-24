import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="DAHLIR - Bilan Annuel d'Activité Territorial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. STYLE CSS PERSONNALISÉ (Charte DAHLIR / Billom)
st.markdown("""
    <style>
    /* Couleurs principales */
    :root {
        --dahlir-blue: #006CA9;
        --dahlir-light: #F4F8FA;
        --dahlir-dark: #1F3E4D;
    }
    .main-title {
        color: #006CA9;
        font-family: 'Arial', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #009FE3;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        margin-top: 0px;
        margin-bottom: 25px;
    }
    .section-header {
        color: #006CA9;
        border-bottom: 2px solid #009FE3;
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .subsection-header {
        color: #1F3E4D;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
    }
    .citation-box {
        background-color: #E8F1F5;
        padding: 20px;
        border-left: 6px solid #006CA9;
        border-radius: 4px;
        font-style: italic;
        margin: 15px 0;
    }
    .visual-placeholder {
        background-color: #F4F8FA;
        border: 2px dashed #009FE3;
        padding: 20px;
        text-align: center;
        border-radius: 6px;
        color: #006CA9;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BASE DE DONNÉES GÉOGRAPHIQUE (AURA & PACA)
regions_deps = {
    "Auvergne-Rhône-Alpes (AURA)": [
        "01 - Ain", "03 - Allier", "07 - Ardèche", "15 - Cantal", 
        "26 - Drôme", "38 - Isère", "42 - Loire", "43 - Haute-Loire", 
        "63 - Puy-de-Dôme", "69 - Rhône / Métropole de Lyon", "73 - Savoie", "74 - Haute-Savoie"
    ],
    "Provence-Alpes-Côte d'Azur (PACA)": [
        "04 - Alpes-de-Haute-Provence", "05 - Hautes-Alpes", "06 - Alpes-Maritimes", 
        "13 - Bouches-du-Rhône", "83 - Var", "84 - Vaucluse"
    ]
}

# 4. BARRE LATÉRALE : CONFIGURATION DU TERRITOIRE & MODE ÉDITION
st.sidebar.image("https://dahlir.fr/wp-content/uploads/2021/04/logo-dahlir.png", width=150) # Logo indicatif
st.sidebar.title("Configuration du Bilan")

region_sel = st.sidebar.selectbox("Région", list(regions_deps.keys()))
dep_sel = st.sidebar.selectbox("Département", regions_deps[region_sel])

# Pré-remplissage intelligent si Puy-de-Dôme est sélectionné (exemple Billom)
default_territoire = "Billom Communauté" if "63" in dep_sel else "Mon Territoire"
territoire = st.sidebar.text_input("Nom du Territoire", value=default_territoire)
typologie = st.sidebar.selectbox("Typologie du Territoire", ["Mixte", "QPV", "Rural"])
referent = st.sidebar.text_input("Référent / Coordinateur", value="Gaël Le Boudouil" if "63" in dep_sel else "[Prénom Nom]")
periode = st.sidebar.text_input("Période du Bilan", value="Janvier à Décembre 2025")

st.sidebar.write("---")
mode_edition = st.sidebar.checkbox("✍️ Activer le mode édition", value=False, help="Cochez cette case pour modifier les textes et indicateurs par défaut du bilan.")

# 5. EN-TÊTE PRINCIPAL
st.markdown(f"<h1 class='main-title'>Bilan Annuel d'Activité Territorial</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 class='subtitle'>Modèle Unifié QPV & Ruralité — {territoire} ({typologie})</h2>", unsafe_allow_html=True)

# Bloc signalétique d'en-tête
st.info(f"**Région :** {region_sel} | **Département :** {dep_sel} | **Période :** {periode} | **Référent de territoire :** {referent}")

# 6. CONFIGURATION DES ONGLETS DE NAVIGATION
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏢 I. Contexte & Cadre", 
    "📊 II. Tableau de Bord (Quantitatif)", 
    "📝 III. Indicateurs Qualitatifs", 
    "⚕️ IV. Analyse Thématique Santé/Précarité", 
    "💼 V-VI. Vie Partenariale & Projections"
])

# =========================================================
# ONGLET 1 : CONTEXTE & CADRE D'ACTION
# =========================================================
with tab1:
    st.markdown("<h2 class='section-header'>I. Contexte : Cadre de l'action et enjeux locaux</h2>", unsafe_allow_html=True)
    
    st.markdown("<p class='subsection-header'>1.1 Éditorial et contexte territorial</p>", unsafe_allow_html=True)
    
    default_edito = (
        "L'année écoulée s'inscrit dans une dynamique de consolidation de nos actions de proximité. "
        "Les évolutions politiques locales et la signature des nouveaux pactes territoriaux ont renforcé la nécessité "
        "d'ajuster nos modes d'intervention sans prendre parti, en restant concentrés sur les besoins factuels des publics."
    )
    if mode_edition:
        edito_text = st.text_area("Modifier l'Éditorial / Analyse de l'année", value=default_edito, height=120)
    else:
        edito_text = default_edito
    st.write(edito_text)
    
    default_identite = (
        "Le bassin de vie se caractérise par une forte dualité entre des zones bourgs-centres en mutation "
        "et des communes rurales plus isolées qualifiées de 'zones blanches' en matière d'accès aux droits et à la santé. "
        "Le profil démographique montre un indice de vieillissement en augmentation constante, accentuant les besoins d'aller-vers."
    )
    if mode_edition:
        identite_text = st.text_area("Modifier l'Identité du territoire (Bassin de vie)", value=default_identite, height=120)
    else:
        identite_text = default_identite
    
    st.write("**Identité du territoire :**")
    st.write(identite_text)
    
    st.markdown("""
        <div class='visual-placeholder'>
            <strong>🗺️ CARTOGRAPHIE DU TERRITOIRE</strong><br>
            <em>Espace réservé à l'illustration cartographique (Zones blanches, QPV, Communes cibles).</em>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p class='subsection-header'>1.2 Missions et cadre d’intervention</p>", unsafe_allow_html=True)
    st.write(f"**Missions du poste ({referent}) :** Rappel des piliers fondamentaux du poste basés sur l'accueil, l'écoute, l'orientation et la réponse aux objectifs conventionnels (adulte-relais, médiation ou ruralité).")
    st.write("**Positionnement du DAHLIR :** Apporter une valeur ajoutée unique via la méthodologie de l'aller-vers, le travail partenarial de co-construction et le recensement fin des besoins non couverts.")

# =========================================================
# ONGLET 2 : TABLEAU DE BORD (QUANTITATIF)
# =========================================================
with tab2:
    st.markdown("<h2 class='section-header'>II. Tableau de Bord : Indicateurs Quantitatifs</h2>", unsafe_allow_html=True)
    st.write("*Les données ci-dessous proviennent des outils de suivi internes (PGI). Les lignes non réalisées peuvent être décochées ou mises à zéro.*")
    
    # Dictionnaire des valeurs par défaut
    default_quant_data = {
        "Médiation : Personnes rencontrées (Repérage social*)": [120, 100],
        "Accompagnement : Personnes en Phase 1 (Actions collectives : ATP, DI...)": [45, 40],
        "Accompagnement : Personnes en Phase 2 (Clubs / Associations)": [30, 25],
        "Accompagnement : Parcours P2 en emploi / formation / RPE": [12, 8],
        "Accompagnement : Parcours actifs en 'Phase 1'": [25, 30],
        "Accompagnement : Projets d'adhésion validés et pérennisés": [18, 15],
        "Coordination : Séances d'actions collectives réalisées": [24, 20],
        "Social : Bénéficiaires justifiant des minimas sociaux (CSS / RSA)": [55, 50],
        "Dynamique : Nouveaux projets territoriaux lancés": [4, 2]
    }
    
    final_data = {}
    
    if mode_edition:
        st.subheader("Saisie des Indicateurs")
        col_n, col_n1 = st.columns(2)
        for idx, (indicateur, valeurs) in enumerate(default_quant_data.items()):
            with col_n:
                v_n = st.number_input(f"{indicateur} (Année N)", value=valeurs[0], key=f"n_{idx}")
            with col_n1:
                v_n1 = st.number_input(f"{indicateur} (Année N-1)", value=valeurs[1], key=f"n1_{idx}")
            final_data[indicateur] = [v_n, v_n1]
    else:
        for indicateur, valeurs in default_quant_data.items():
            final_data[indicateur] = valeurs

    # Construction du DataFrame d'affichage
    df_quant = pd.DataFrame.from_dict(final_data, orient='index', columns=['Valeur N', 'Valeur N-1 (Rappel)'])
    df_quant['Évolution Absolue'] = df_quant['Valeur N'] - df_quant['Valeur N-1 (Rappel)']
    
    st.dataframe(df_quant.style.format(precision=0), use_container_width=True)
    st.caption("*Repérage social DAHLIR : démarche d’aller-vers, sensibilisation et identification du chargé d'accompagnement local.")

    # Graphique interactif N vs N-1
    st.markdown("<p class='subsection-header'>📊 Visualisation interactive pour les financeurs</p>", unsafe_allow_html=True)
    
    df_plot = df_quant.reset_index().rename(columns={'index': 'Indicateur'})
    df_melted = df_plot.melt(id_vars=['Indicateur'], value_vars=['Valeur N', 'Valeur N-1 (Rappel)'], 
                             var_name='Année', value_name='Effectif')
    
    # Raccourcir les noms des indicateurs pour le graphique
    df_melted['Indicateur_Court'] = df_melted['Indicateur'].apply(lambda x: x.split(" : ")[1] if " : " in x else x)
    df_melted['Indicateur_Court'] = df_melted['Indicateur_Court'].apply(lambda x: x[:35] + "..." if len(x) > 35 else x)
    
    fig_bar = px.bar(
        df_melted, 
        x='Effectif', 
        y='Indicateur_Court', 
        color='Année', 
        barmode='group',
        orientation='h',
        color_discrete_sequence=['#006CA9', '#009FE3'],
        title="Comparatif de l'activité du territoire (N vs N-1)"
    )
    fig_bar.update_layout(yaxis_title="", xaxis_title="Nombre de personnes / séances", legend_title="")
    st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# ONGLET 3 : ANALYSES QUALITATIVES
# =========================================================
with tab3:
    st.markdown("<h2 class='section-header'>III. Indicateurs Qualitatifs & Actions Phares</h2>", unsafe_allow_html=True)
    
    st.markdown("<p class='subsection-header'>3.1 Détail des phases d'accompagnement et transitions</p>", unsafe_allow_html=True)
    st.write("*Ce volet permet aux financeurs de comprendre finement le fonctionnement du DAHLIR et d'identifier les leviers ou les freins du public vulnérable.*")
    
    p1_def = "Les bénéficiaires arrivent majoritairement via les prescripteurs sociaux (CCAS, MDS) et la démarche proactive d'aller-vers sur les structures de première ligne (Épiceries sociales)."
    trans_def = "Le taux de concrétisation met en lumière des freins récurrents : problématiques de mobilité géographique en zone blanche rurale, coûts des licences et craintes liées à l'intégration en milieu associatif ordinaire."
    reussite_def = "Les parcours réussissent grâce à l'accompagnement physique individualisé (premières séances partagées) et à la réactivité du réseau de clubs partenaires formés à l'inclusion."
    
    if mode_edition:
        p1_txt = st.text_area("Modifier l'analyse Phase 1", value=p1_def)
        trans_txt = st.text_area("Modifier l'analyse des Freins / Transitions", value=trans_def)
        reussite_txt = st.text_area("Modifier l'analyse des Réussites", value=reussite_def)
    else:
        p1_txt, trans_txt, reussite_txt = p1_def, trans_def, reussite_def
        
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown("**Phase 1 (Diagnostic et Entrée) :**")
        st.write(p1_txt)
        st.markdown("**Transition Phase 1 vers Phase 2 (Constat sur les freins) :**")
        st.write(trans_txt)
    with col_q2:
        st.markdown("**Facteurs clés de réussite :**")
        st.write(reussite_txt)
        
        # Graphique en entonnoir de parcours (Funnel)
        fig_funnel = go.Figure(go.Funnel(
            y = ["Repérage social", "Diagnostic Phase 1", "Accompagnement Club (P2)", "Pérennisation / Adhésion"],
            x = [120, 55, 30, 18],
            textinfo = "value+percent initial",
            marker = {"color": ["#1F3E4D", "#006CA9", "#009FE3", "#E8F1F5"]}
        ))
        fig_funnel.update_layout(title_text="Visualisation du parcours d'accompagnement (Entonnoir)", margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("<p class='subsection-header'>3.2 Mise en Lumière d’un Projet Phare</p>", unsafe_allow_html=True)
    
    proj_nom = st.text_input("Nom de l'action / projet phare", value="L'Action Remobilisation - Épicerie Solidaire")
    
    p_genese = "Repérage de personnes très éloignées de la pratique régulière, isolées socialement et fréquentant l'épicerie solidaire du territoire."
    p_mep = "Mise en place d'un cycle d'ateliers passerelles (activités physiques douces, marche adaptée) directement sur le lieu de vie ou à proximité immédiate."
    p_bilan = "Forte assiduité du groupe constitué. Difficultés initiales liées à la confiance en soi, rapidement levées par la bienveillance du groupe."
    p_impact = "3 personnes ont émis le souhait d'intégrer un club de gym volontaire local à la rentrée prochaine."
    p_cit = "« Ça fait du bien pour le physique et aussi pour le moral, on rigole bien et puis ça devient le rendez-vous de la semaine. » - Une participante"
    
    if mode_edition:
        p_genese = st.text_area("Genèse du projet", value=p_genese)
        p_mep = st.text_area("Mise en œuvre", value=p_mep)
        p_bilan = st.text_area("Bilan Critique", value=p_bilan)
        p_impact = st.text_area("Impact", value=p_impact)
        p_cit = st.text_area("Témoignage", value=p_cit)

    st.markdown(f"### 🚀 {proj_nom}")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.write(f"**Genèse (Besoin identifié) :** {p_genese}")
        st.write(f"**Mise en œuvre :** {p_mep}")
        st.write(f"**Bilan Critique (+/-) :** {p_bilan}")
        st.write(f"**Impact concret :** {p_impact}")
    with col_p2:
        st.markdown(f"<div class='citation-box'>{p_cit}</div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='visual-placeholder' style='padding:40px 10px;'>
                📸 <strong>Illustration de l'action</strong><br>Reflet de la dynamique collective (avec autorisations).
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# ONGLET 4 : ANALYSE THÉMATIQUE (SANTÉ & PRÉCARITÉ)
# =========================================================
with tab4:
    st.markdown("<h2 class='section-header'>IV. Analyse Thématique : Santé, Précarité et Inclusion</h2>", unsafe_allow_html=True)
    
    st.markdown("<p class='subsection-header'>4.1 Cartographie de la Santé sur le Territoire</p>", unsafe_allow_html=True)
    st.write("*Analyse des pathologies majeures rencontrées (ALD, santé mentale, obésité) à croiser avec le coordinateur santé/insertion.*")
    
    # Données par défaut pour le camembert des pathologies
    patho_data = {
        "Pathologie / Problématique": ["Santé Mentale / Isolement", "Affections Cardiovasculaires / Métaboliques", "Obésité / Surpoids", "Maladies Chroniques / ALD Diverses"],
        "Proportion (%)": [35, 25, 20, 20]
    }
    df_patho = pd.DataFrame(patho_data)
    
    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if mode_edition:
            st.write("**Modifier la répartition des pathologies rencontrées (%) :**")
            v1 = st.number_input("Santé Mentale / Isolement", value=35)
            v2 = st.number_input("Cardiovasculaires / Métaboliques", value=25)
            v3 = st.number_input("Obésité / Surpoids", value=20)
            v4 = st.number_input("Maladies Chroniques / ALD", value=20)
            df_patho["Proportion (%)"] = [v1, v2, v3, v4]
        
        fig_pie = px.pie(
            df_patho, 
            values='Proportion (%)', 
            names='Pathologie / Problématique',
            title="Répartition des problématiques de santé constatées",
            color_discrete_sequence=['#1F3E4D', '#006CA9', '#009FE3', '#E8F1F5']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_s2:
        st.markdown("**Déterminants de santé & Isolement :**")
        st.write("L'accès à l'activité physique est fortement impacté par des facteurs environnementaux et sociaux :")
        st.write("- **Temps d'accès aux soins :** Moyenne de 25 minutes pour atteindre un spécialiste ou une structure sport-santé labellisée.")
        st.write("- **Taux de couverture CSS :** Données locales (sources Balises IdR / Observatoires) indiquant une couverture hétérogène, corrélée aux ruptures de parcours constatées en Phase 1.")

    st.markdown("<p class='subsection-header'>4.2 Indicateurs de précarité sociale par secteur</p>", unsafe_allow_html=True)
    
    # Données par défaut de précarité par secteur (Histogramme empilé)
    prec_data = {
        "Secteur / Commune": ["Centre-Bourg / QPV", "Zone Rurale Nord", "Zone Rurale Sud"],
        "Allocataires RSA": [45, 15, 20],
        "Demandeurs d'emploi": [30, 10, 15],
        "Jeunes NEETs": [15, 5, 8]
    }
    df_prec = pd.DataFrame(prec_data)
    
    if mode_edition:
        st.write("**Modifier les volumes de précarité par secteur :**")
        df_prec = st.data_editor(df_prec)
        
    fig_stack = px.bar(
        df_prec, 
        x="Secteur / Commune", 
        y=["Allocataires RSA", "Demandeurs d'emploi", "Jeunes NEETs"],
        title="Profil de vulnérabilité sociale croisé par secteur",
        color_discrete_sequence=['#006CA9', '#009FE3', '#1F3E4D'],
        barmode="stack"
    )
    fig_stack.update_layout(xaxis_title="", yaxis_title="Nombre de bénéficiaires repérés")
    st.plotly_chart(fig_stack, use_container_width=True)

# =========================================================
# ONGLET 5 : VIE PARTENARIALE & PROJECTIONS
# =========================================================
with tab5:
    st.markdown("<h2 class='section-header'>V. Vie Partenariale & VI. Projections Stratégiques</h2>", unsafe_allow_html=True)
    
    st.markdown("<p class='subsection-header'>5.1 Actions de sensibilisation partenariale (Ancrage local)</p>", unsafe_allow_html=True)
    st.write("*Participation et interventions du DAHLIR sur des événements externes non coordonnés directement (Forums emploi, dépistages CPTS, fêtes de quartier).*")
    
    radar_data = {
        "Public Cible": ["Professionnels (MDS, CCAS)", "Grand Public / Familles", "Scolaires / Collèges", "Structures de Santé (CPTS, MSP)"],
        "Nombre d'interventions": [12, 5, 8, 7]
    }
    df_radar = pd.DataFrame(radar_data)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if mode_edition:
            df_radar = st.data_editor(df_radar, key="radar_edit")
        
        fig_radar = px.line_polar(
            df_radar, 
            r="Nombre d'interventions", 
            theta="Public Cible", 
            line_close=True,
            title="Ventilation des actions de sensibilisation partenariale",
            color_discrete_sequence=['#006CA9']
        )
        fig_radar.update_traces(fill='currentColor', fillcolor='rgba(0, 108, 169, 0.2)')
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_v2:
        st.markdown("**Bilan Quali/Quanti :**")
        st.write("Les interventions auprès des professionnels (MDS, réseaux de santé) portent leurs fruits : elles représentent le premier canal d'orientation du public vers l'aller-vers du DAHLIR.")
        st.write("La présence sur les fêtes de quartier ou forums permet un repérage direct, au plus près des réalités de vie.")

    st.markdown("<h2 class='section-header'>VI. Projections et Perspectives</h2>", unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("<p class='subsection-header'>6.1 Perspectives de développement N+1</p>", unsafe_allow_html=True)
        st.write("- **Besoins non couverts :** Renforcer la présence sur les communes les plus excentrées (zones blanches de mobilité).")
        st.write("- **Collaborations potentielles :** Contractualiser des passerelles avec de nouvelles Maisons de Santé Pluriprofessionnelles (MSP) et des clubs ruraux isolés.")
    
    with col_f2:
        st.markdown("<p class='subsection-header'>6.2 Budget & Ventilation Financière</p>", unsafe_allow_html=True)
        
        fin_data = {
            "Type de Financement": ["Structurel (Conventions cadres, Adulte-relais, Socle - RDT)", "Opérationnel (Appels à projets, Actions spécifiques - Coordo)"],
            "Montant (€)": [20000, 8500]
        }
        df_fin = pd.DataFrame(fin_data)
        
        if mode_edition:
            df_fin = st.data_editor(df_fin, key="fin_edit")
            
        fig_donut = px.pie(
            df_fin, 
            values="Montant (€)", 
            names="Type de Financement", 
            hole=0.5,
            color_discrete_sequence=['#006CA9', '#009FE3'],
            title="Origine des ressources financières du territoire"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")
    st.markdown("**Annexe Technique :** Documents complémentaires disponibles au téléchargement ou à la consultation physique (Photos d'actions collectives avec autorisations, courbes détaillées de la file active PGI, extraits de presse locale, newsletters régionales).")
