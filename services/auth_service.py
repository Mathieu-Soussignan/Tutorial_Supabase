from config.database import supabase
from typing import Optional, Dict

class AuthService:
    
    @staticmethod
    def inscrire_utilisateur(email: str, password: str) -> Dict:
        """Inscription d'un nouvel utilisateur"""
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                return {
                    "success": True,
                    "user": response.user,
                    "message": "Inscription réussie. Vérifiez vos emails."
                }
            else:
                return {
                    "success": False,
                    "message": "Erreur lors de l'inscription"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur: {str(e)}"
            }
    
    @staticmethod
    def connecter_utilisateur(email: str, password: str) -> Dict:
        """Connexion utilisateur"""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                return {
                    "success": True,
                    "user": response.user,
                    "access_token": response.session.access_token
                }
            else:
                return {
                    "success": False,
                    "message": "Identifiants incorrects"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur connexion: {str(e)}"
            }

    @staticmethod
    def connexion_anonyme() -> Dict:
        """Connexion anonyme pour les démos"""
        try:
            response = supabase.auth.sign_in_anonymously()
            
            if response.user:
                return {
                    "success": True,
                    "user": response.user,
                    "message": "Connexion anonyme réussie"
                }
            else:
                return {
                    "success": False,
                    "message": "Erreur connexion anonyme"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur auth anonyme: {str(e)}"
            }
    
    @staticmethod
    def deconnecter_utilisateur() -> bool:
        """Déconnexion"""
        try:
            supabase.auth.sign_out()
            return True
        except Exception:
            return False
    
    @staticmethod
    def utilisateur_actuel() -> Optional[Dict]:
        """Récupérer l'utilisateur connecté"""
        try:
            user = supabase.auth.get_user()
            return user.user if user else None
        except Exception:
            return None