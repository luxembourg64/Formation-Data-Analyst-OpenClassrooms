import streamlit as st
import pandas as pd
import joblib

# --- Config ---
st.set_page_config(page_title="ONCFM – Détection de faux billets", layout="wide")

# ✅ CSS : harmonisation du slider (or du logo)
# À placer juste après set_page_config (avant tout widget)
st.markdown(
    """
    <style>
    /* Slider rail (inactif) */
    div[data-baseweb="slider"] > div > div {
        background-color: #444444 !important;
    }

    /* Slider rail actif */
    div[data-baseweb="slider"] > div > div > div {
        background-color: #D4AF37 !important;
    }

    /* Slider thumb (le bouton rond) */
    div[data-baseweb="slider"] span {
        background-color: #D4AF37 !important;
        border: 2px solid #E6C75A !important;
    }

    /* Slider value label */
    div[data-baseweb="slider"] div[role="slider"] {
        color: #D4AF37 !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

MODEL_PATH = "pipeline_detection_faux_billets.pkl"
FEATURES = ["diagonal", "height_left", "height_right", "margin_up", "margin_low", "length"]

# --- Header : texte à gauche, logo à droite ---
col_text, col_logo = st.columns([6, 2])

with col_text:
    st.markdown(
        """
        <h1 style="margin-bottom: 2px; letter-spacing: 0.5px;">
            Détection automatique de faux billets
        </h1>
        <p style="color:#bbbbbb; margin-top: 0; font-size: 15px;">
            Organisation nationale de lutte contre le faux-monnayage (ONCFM)
        </p>
        """,
        unsafe_allow_html=True
    )

with col_logo:
    st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
    st.image("oncfm_logo.png", width=170)

st.write(
    "Charge un fichier CSV (ex: `billets_production.csv`). "
    "L’application affiche la prédiction (**VRAI/FAUX**), les probabilités associées "
    "et un **degré de confiance**."
)

# --- Sidebar (Paramètres) ---
st.sidebar.header("Paramètres")
threshold_vrai = st.sidebar.slider(
    "Seuil d’acceptation (proba_vrai ≥ seuil → VRAI)",
    min_value=0.50,
    max_value=0.99,
    value=0.95,
    step=0.01,
)

st.sidebar.caption(
    "Ce seuil correspond au niveau de confiance minimal requis pour accepter un billet "
    "comme authentique. Plus le seuil est élevé, plus le contrôle est strict."
)

show_only_faux = st.sidebar.checkbox("Afficher uniquement les FAUX", value=False)

@st.cache_resource
def load_model(path: str):
    return joblib.load(path)

# --- Chargement modèle ---
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    st.error(f"Impossible de charger le modèle '{MODEL_PATH}'. Détail : {e}")
    st.stop()

# --- Upload CSV ---
uploaded = st.file_uploader("📄 Uploader un fichier CSV", type=["csv"])

if uploaded is None:
    st.info("⬆️ Uploade un CSV pour lancer la prédiction.")
    st.stop()

# --- Lecture CSV ---
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"Impossible de lire le CSV. Détail : {e}")
    st.stop()

st.subheader("Aperçu du fichier importé")
st.dataframe(df.head(), use_container_width=True)

# --- Vérification colonnes attendues ---
missing = [c for c in FEATURES if c not in df.columns]
if missing:
    st.error(
        "Colonnes manquantes dans le fichier : "
        f"{missing}. Colonnes attendues : {FEATURES} (+ une colonne 'id' optionnelle)."
    )
    st.stop()

# --- Message métier (seuil d’acceptation) ---
st.info(
    "**Aide à la décision :** le curseur définit un **seuil d’acceptation**. "
    f"Un billet est classé **VRAI** si `proba_vrai ≥ {threshold_vrai:.2f}` ; "
    "sinon il est classé **FAUX** et doit être priorisé pour un contrôle manuel."
)

# --- Préparation X ---
X = df[FEATURES].copy()

# --- Prédictions ---
try:
    proba = model.predict_proba(X)
    proba_vrai = proba[:, 1]
    proba_faux = proba[:, 0]
except Exception as e:
    st.error(f"Erreur lors du predict_proba. Détail : {e}")
    st.stop()

pred_label = ["VRAI" if p >= threshold_vrai else "FAUX" for p in proba_vrai]
confidence = [max(pf, pv) for pf, pv in zip(proba_faux, proba_vrai)]

out = df.copy()
out["prediction_label"] = pred_label
out["proba_faux"] = proba_faux
out["proba_vrai"] = proba_vrai
out["confiance"] = confidence

# Tri par risque décroissant
out_sorted = out.sort_values("proba_faux", ascending=False)

# Compteurs globaux
nb_total = len(out_sorted)
nb_faux_total = int((out_sorted["prediction_label"] == "FAUX").sum())
nb_vrai_total = int((out_sorted["prediction_label"] == "VRAI").sum())

# Message "à contrôler"
if nb_faux_total > 0:
    st.warning(f"⚠️ **{nb_faux_total} billet(s) à contrôler en priorité** (classés FAUX).")
else:
    st.success("✅ Aucun billet classé FAUX : aucun contrôle prioritaire requis.")

# --- Couleur texte VRAI / FAUX ---
def color_pred(val):
    if val == "FAUX":
        return "color: #ff4b4b; font-weight: 700;"
    return "color: #2ecc71; font-weight: 700;"

# Application du filtre d’affichage
display_df = out_sorted.copy()
if show_only_faux:
    display_df = display_df[display_df["prediction_label"] == "FAUX"]

st.subheader("Résultats (triés par probabilité d’être FAUX)")
st.dataframe(
    display_df.style.applymap(color_pred, subset=["prediction_label"]),
    use_container_width=True
)

# --- KPIs colorés ---
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div style="text-align:center">
            <div style="font-size:16px; color:#cccccc;">Nombre de billets</div>
            <div style="font-size:36px; font-weight:700;">{nb_total}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div style="text-align:center">
            <div style="font-size:16px; color:#ff4b4b;">Prédits FAUX</div>
            <div style="font-size:36px; font-weight:700; color:#ff4b4b;">{nb_faux_total}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style="text-align:center">
            <div style="font-size:16px; color:#2ecc71;">Prédits VRAI</div>
            <div style="font-size:36px; font-weight:700; color:#2ecc71;">{nb_vrai_total}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Exports CSV ---
st.subheader("Exports")

# Export complet
csv_all = out_sorted.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Télécharger les prédictions (CSV complet)",
    data=csv_all,
    file_name="predictions_billets_complet.csv",
    mime="text/csv",
)

# Export "FAUX uniquement"
df_faux = out_sorted[out_sorted["prediction_label"] == "FAUX"].copy()

if df_faux.empty:
    st.download_button(
        "⬇️ Télécharger les billets FAUX uniquement (CSV)",
        data="".encode("utf-8"),
        file_name="predictions_billets_FAUX.csv",
        mime="text/csv",
        disabled=True,
    )
else:
    csv_faux = df_faux.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Télécharger les billets FAUX uniquement (CSV)",
        data=csv_faux,
        file_name="predictions_billets_FAUX.csv",
        mime="text/csv",
    )
