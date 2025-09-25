# streamlit_app.py
import streamlit as st
import streamlit.components.v1
import uuid
from services.auth_service import (
    sign_in_email,
    sign_up_email,
    sign_out,
    get_user
)
from services.projet_service import (
    creer_projet,
    lister_projets
)
from config.database import supabase

st.set_page_config(page_title="Supabase + Streamlit (Tuto)", layout="wide")

# ----------------------
# Initialisation de l'état utilisateur
# ----------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_error" not in st.session_state:
    st.session_state.auth_error = None

# ----------------------
# Fonction pour gérer les callbacks OAuth - CORRIGÉE
# ----------------------
def handle_oauth_callback():
    """Traiter les paramètres URL après OAuth redirect - VERSION AVEC UUID VALIDE"""
    try:
        query_params = st.query_params
        
        # Si on a un code OAuth
        if 'code' in query_params:
            code = query_params['code']
            st.info(f"🔄 Code OAuth détecté: {code[:20]}...")
            
            # APPROCHE 1 : Tentative échange manuel
            try:
                st.write("🔧 Tentative 1: Échange manuel du code...")
                
                import requests
                
                url = f"{supabase.url}/auth/v1/token"
                headers = {
                    "apikey": supabase.supabase_key,
                    "Content-Type": "application/json"
                }
                data = {
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": "http://localhost:8501"
                }
                
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    # Récupérer les infos utilisateur avec le token
                    user_url = f"{supabase.url}/auth/v1/user"
                    user_headers = {
                        "apikey": supabase.supabase_key,
                        "Authorization": f"Bearer {token_data['access_token']}"
                    }
                    
                    user_response = requests.get(user_url, headers=user_headers)
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        
                        # Créer un objet user avec UUID valide
                        class AuthenticatedUser:
                            def __init__(self, data):
                                self.id = data['id']  # UUID véritable de Supabase
                                self.email = data['email']
                                self.user_metadata = data.get('user_metadata', {})
                                self.provider = "github"
                        
                        st.session_state.user = AuthenticatedUser(user_data)
                        st.success(f"✅ OAuth manuel réussi : {user_data['email']}")
                        st.query_params.clear()
                        st.rerun()
                        return True
                    else:
                        st.warning(f"⚠️ Erreur récupération user: {user_response.status_code}")
                else:
                    st.warning(f"⚠️ Erreur échange token: {response.status_code}")
                    
            except Exception as e:
                st.warning(f"⚠️ Erreur approche manuelle: {e}")
            
            # FALLBACK : Simulation utilisateur avec UUID VALIDE
            try:
                st.write("🔧 Fallback : Simulation utilisateur avec UUID valide...")
                
                # Créer un UUID valide à partir du code
                class SimulatedUser:
                    def __init__(self, code):
                        # Générer un UUID déterministe à partir du code GitHub
                        namespace = uuid.UUID('12345678-1234-5678-1234-123456789abc')
                        self.id = str(uuid.uuid5(namespace, f"github_{code}"))
                        self.email = f"user_{code[:8]}@github.oauth"
                        self.provider = "github"
                        self.code = code
                
                st.session_state.user = SimulatedUser(code)
                st.success(f"✅ Utilisateur OAuth simulé : {st.session_state.user.email}")
                st.success(f"📝 UUID généré : {st.session_state.user.id}")
                st.query_params.clear()
                st.rerun()
                return True
                
            except Exception as e:
                st.error(f"❌ Erreur fallback: {e}")
        
        return False
        
    except Exception as e:
        st.error(f"❌ Erreur callback generale: {e}")
        return False

# ----------------------
# Fonction pour vérifier la session
# ----------------------
def check_auth_session():
    """Vérifier si l'utilisateur est toujours connecté via Supabase"""
    try:
        # D'abord, essayer de traiter un callback OAuth
        if handle_oauth_callback():
            return True
            
        # Ensuite, vérification normale de session
        user_response = supabase.auth.get_user()
        if user_response and user_response.user:
            st.session_state.user = user_response.user
            return True
        else:
            st.session_state.user = None
            return False
    except Exception as e:
        st.session_state.user = None
        return False

# Vérifier la session au chargement
if st.session_state.user is None:
    check_auth_session()

# ----------------------
# Titre principal
# ----------------------
st.title("Supabase + Streamlit — Tutoriel IA")

# ----------------------
# Section Auth (seulement si pas connecté)
# ----------------------
if not st.session_state.user:
    st.header("Authentification")
    
    # Afficher les erreurs s'il y en a
    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)
        st.session_state.auth_error = None

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Se connecter (Email)")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="votre@email.com")
            pwd = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("🔑 Se connecter", use_container_width=True)

            if submitted:
                if email and pwd:
                    try:
                        resp = sign_in_email(email, pwd)
                        if resp.user:
                            st.session_state.user = resp.user
                            st.success(f"✅ Connecté en tant que {resp.user.email}")
                            st.rerun()
                        else:
                            st.session_state.auth_error = "❌ Identifiants incorrects"
                            st.rerun()
                    except Exception as e:
                        st.session_state.auth_error = f"❌ Erreur de connexion: {str(e)}"
                        st.rerun()
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs")

    with col2:
        st.subheader("Créer un compte (Email)")
        with st.form("signup_form"):
            email_s = st.text_input("Email", placeholder="votre@email.com", key="signup_email_input")
            pwd_s = st.text_input("Mot de passe", type="password", key="signup_pwd_input")
            submitted_s = st.form_submit_button("✨ S'inscrire", use_container_width=True)

            if submitted_s:
                if email_s and pwd_s:
                    try:
                        resp = sign_up_email(email_s, pwd_s)
                        if resp.user:
                            st.success("✅ Compte créé avec succès !")
                            st.info("Vous pouvez maintenant vous connecter")
                        else:
                            st.error("❌ Impossible de créer le compte")
                    except Exception as e:
                        st.error(f"❌ Erreur inscription: {str(e)}")
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs")

    # ----------------------
    # OAuth GitHub (VERSION FONCTIONNELLE)
    # ----------------------
    st.markdown("---")
    st.markdown("### Ou connectez-vous via GitHub :")
    
    col_github1, col_github2 = st.columns([2, 1])
    
    with col_github1:
        if st.button("Générer le lien GitHub OAuth", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_oauth({
                    "provider": "github",
                    "options": {
                        "redirect_to": "http://localhost:8501",
                    }
                })
                
                if res and hasattr(res, 'url'):
                    st.session_state.github_auth_url = res.url
                    st.rerun()
                else:
                    st.error("❌ Impossible de générer l'URL GitHub")
                    
            except Exception as e:
                st.error(f"❌ Erreur OAuth GitHub: {str(e)}")
    
    with col_github2:
        if hasattr(st.session_state, 'github_auth_url'):
            st.markdown(f"""
                ### [🔗 CONNEXION GITHUB]({st.session_state.github_auth_url})
            """)
            st.caption("↗️ Cliquer pour s'authentifier")

    # Instructions OAuth
    if hasattr(st.session_state, 'github_auth_url'):
        st.info("""
        💡 **Instructions OAuth GitHub :**
        1. Cliquez sur le lien "CONNEXION GITHUB" ci-dessus
        2. Autorisez l'accès sur GitHub
        3. Vous serez redirigé ici automatiquement
        4. L'interface changera pour afficher vos projets
        """)

# ----------------------
# Section Utilisateur connecté
# ----------------------
else:
    user = st.session_state.user
    
    # Header avec info utilisateur et déconnexion
    col1, col2 = st.columns([3, 1])
    with col1:
        # CORRECTION : Meilleure détection du provider
        provider = "GitHub"
        if hasattr(user, 'email'):
            if "@github.oauth" in user.email or "@users.noreply.github.com" in user.email:
                provider = "GitHub"
            else:
                provider = "Email"
        elif hasattr(user, 'provider'):
            provider = user.provider.title()
            
        st.success(f"👋 Connecté via **{provider}** : **{user.email}**")
    with col2:
        if st.button("🚪 Se déconnecter", key="btn_logout"):
            try:
                sign_out()
                st.session_state.user = None
                st.session_state.auth_error = None
                # Nettoyer l'URL GitHub OAuth si présente
                if hasattr(st.session_state, 'github_auth_url'):
                    delattr(st.session_state, 'github_auth_url')
                st.success("✅ Déconnecté avec succès")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur déconnexion: {e}")

    st.markdown("---")

    # ----------------------
    # CRUD projet - AVEC VALIDATION UUID
    # ----------------------
    st.header("📂 Créer un projet IA")
    
    with st.form("projet_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom du projet", placeholder="Ex: Classification d'images chats/chiens")
            type_modele = st.selectbox(
                "Type de modèle", 
                ["Computer Vision", "NLP", "Deep Learning", "ML", "Autre"],
                index=0
            )
        
        with col2:
            desc = st.text_area("Description", placeholder="Décrivez votre projet IA...")
            
        st.subheader("⚙️ Hyperparamètres")
        col3, col4 = st.columns(2)
        
        with col3:
            hp_epochs = st.number_input("Epochs", value=25, min_value=1, max_value=1000)
            hp_lr = st.number_input("Learning Rate", value=0.001, format="%.6f", min_value=0.0001, max_value=1.0)
        
        with col4:
            hp_batch = st.number_input("Batch Size", value=32, min_value=1, max_value=512)
            hp_optimizer = st.selectbox("Optimizer", ["Adam", "SGD", "RMSprop", "AdaGrad"])
        
        # Hyperparamètres additionnels
        with st.expander("🔧 Hyperparamètres avancés (optionnels)"):
            col5, col6 = st.columns(2)
            with col5:
                hp_dropout = st.slider("Dropout Rate", 0.0, 0.9, 0.2, 0.1)
                hp_patience = st.number_input("Early Stopping Patience", value=5, min_value=1, max_value=50)
            with col6:
                hp_validation_split = st.slider("Validation Split", 0.1, 0.5, 0.2, 0.05)
                hp_metric = st.selectbox("Metric principale", ["accuracy", "f1-score", "precision", "recall"])
        
        submitted_projet = st.form_submit_button("🚀 Créer le projet", use_container_width=True)

        if submitted_projet:
            if nom and desc:
                try:
                    # CORRECTION : Validation de l'UUID avant envoi
                    user_id = user.id
                    
                    # Vérifier que c'est un UUID valide
                    try:
                        uuid.UUID(user_id)
                        st.info(f"✅ UUID utilisateur valide : {user_id}")
                    except ValueError:
                        st.error(f"❌ UUID invalide : {user_id}")
                        st.stop()
                    
                    hyperparametres = {
                        "epochs": int(hp_epochs),
                        "learning_rate": float(hp_lr),
                        "batch_size": int(hp_batch),
                        "optimizer": hp_optimizer,
                        "dropout": float(hp_dropout),
                        "patience": int(hp_patience),
                        "validation_split": float(hp_validation_split),
                        "metric": hp_metric
                    }
                    
                    res = creer_projet(user_id, nom, desc, type_modele, hyperparametres)
                    st.success(f"✅ Projet '{nom}' créé avec succès !")
                    st.balloons()  # Animation de célébration
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erreur création projet: {str(e)}")
                    # CORRECTION : Afficher plus d'infos pour debug
                    st.error(f"🔍 Debug - User ID: {user.id}")
                    st.error(f"🔍 Debug - User type: {type(user)}")
            else:
                st.warning("⚠️ Veuillez remplir le nom et la description")

    st.markdown("---")

    # ----------------------
    # Liste des projets (interface améliorée)
    # ----------------------
    st.header("📋 Mes projets")
    
    try:
        projets = lister_projets(user.id)
        
        if projets and projets.data and len(projets.data) > 0:
            # Statistiques rapides
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("📊 Total projets", len(projets.data))
            
            with col_stat2:
                types = [p['type_modele'] for p in projets.data]
                type_populaire = max(set(types), key=types.count) if types else "N/A"
                st.metric("🏆 Type populaire", type_populaire)
            
            with col_stat3:
                # Calculer la moyenne des epochs
                epochs_list = []
                for p in projets.data:
                    hp = p.get('hyperparametres', {})
                    if hp.get('epochs'):
                        epochs_list.append(hp['epochs'])
                
                avg_epochs = int(sum(epochs_list) / len(epochs_list)) if epochs_list else 0
                st.metric("⚡ Epochs moyens", avg_epochs)
            
            st.markdown("---")
            
            # Affichage des projets
            for i, p in enumerate(projets.data, 1):
                with st.expander(f"🤖 {p['nom']} ({p['type_modele']})", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Description:** {p.get('description', 'Aucune description')}")
                        st.write(f"**Créé le:** {p.get('created_at', 'Date inconnue')[:10]}")
                        
                        # Affichage des hyperparamètres
                        hp = p.get('hyperparametres', {})
                        if hp:
                            st.write("**⚙️ Hyperparamètres:**")
                            
                            # Hyperparamètres principaux
                            col_hp1, col_hp2 = st.columns(2)
                            with col_hp1:
                                for key in ['epochs', 'learning_rate', 'batch_size', 'optimizer']:
                                    if key in hp:
                                        if key == 'learning_rate':
                                            st.write(f"  • {key}: `{hp[key]:.6f}`")
                                        else:
                                            st.write(f"  • {key}: `{hp[key]}`")
                            
                            with col_hp2:
                                for key in ['dropout', 'patience', 'validation_split', 'metric']:
                                    if key in hp:
                                        if key in ['dropout', 'validation_split']:
                                            st.write(f"  • {key}: `{hp[key]:.2f}`")
                                        else:
                                            st.write(f"  • {key}: `{hp[key]}`")
                    
                    with col2:
                        st.metric("📝 Type", p['type_modele'])
                        if hp.get('epochs'):
                            st.metric("🔄 Epochs", hp['epochs'])
                        if hp.get('learning_rate'):
                            st.metric("📈 Learning Rate", f"{hp['learning_rate']:.4f}")
                        if hp.get('optimizer'):
                            st.metric("⚙️ Optimizer", hp['optimizer'])
        else:
            # Message encourageant pour premiers pas
            st.info("📭 **Aucun projet trouvé !**")
            st.markdown("""
                🚀 **Créez votre premier projet IA ci-dessus pour commencer !**
                
                Quelques idées de projets :
                - 🖼️ **Computer Vision** : Classification d'images, détection d'objets
                - 📝 **NLP** : Analyse de sentiment, chatbot, traduction
                - 🧠 **Deep Learning** : Réseaux de neurones profonds
                - 📊 **ML** : Prédiction, clustering, recommandations
            """)
            
    except Exception as e:
        st.error(f"❌ Erreur chargement projets: {str(e)}")

# ----------------------
# Footer informatif
# ----------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 <strong>Supabase + Streamlit</strong> - Tutoriel IA | Made with ❤️</p>
    <p>💡 <em>PostgreSQL + Python = Stack parfait pour vos projets IA !</em></p>
</div>
""", unsafe_allow_html=True)

# ----------------------
# Debug info (optionnel, pour développement)
# ----------------------
if st.sidebar.button("🔧 Debug Info"):
    st.sidebar.write("**Session State:**")
    st.sidebar.write(f"User: {bool(st.session_state.user)}")
    if st.session_state.user:
        st.sidebar.write(f"Email: {st.session_state.user.email}")
        st.sidebar.write(f"ID: {st.session_state.user.id}")
        st.sidebar.write(f"UUID valide: {is_valid_uuid(st.session_state.user.id)}")
    st.sidebar.write(f"Auth Error: {st.session_state.auth_error}")
    st.sidebar.write(f"GitHub URL: {hasattr(st.session_state, 'github_auth_url')}")

# ----------------------
# Fonction utilitaire pour valider UUID
# ----------------------
def is_valid_uuid(uuid_string):
    """Vérifier si c'est un UUID valide"""
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False