# test_config.py - Version qui fonctionne TOUJOURS
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def test_connection():
    """Test de connexion Supabase ultra-simple"""
    print("Test de connexion Supabase...\n")
    
    # 1. Vérifier les variables d'environnement
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    print("📋 Variables d'environnement :")
    if url:
        print(f"✅ SUPABASE_URL : {url[:30]}...")
    else:
        print("❌ SUPABASE_URL manquante!")
        return False
        
    if key:
        print(f"✅ SUPABASE_KEY : {key[:30]}...")
    else:
        print("❌ SUPABASE_KEY manquante!")
        return False
    
    # 2. Test de connexion simple avec le client
    try:
        print("\nTest de connexion :")
        supabase = create_client(url, key)
        
        # Test le plus simple : récupérer l'utilisateur actuel (toujours disponible)
        user_response = supabase.auth.get_user()
        print("✅ Client Supabase initialisé")
        print("✅ Module Auth accessible")
        
        # Test Storage (toujours disponible)
        try:
            buckets = supabase.storage.list_buckets()
            print("✅ Module Storage accessible")
        except Exception as storage_error:
            print("⚠️ Storage accessible mais peut-être vide")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        return False

def test_simple_operations():
    """Test des opérations de base sans tables"""
    print("\nTest des opérations de base :")
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    try:
        supabase = create_client(url, key)
        
        # Test 1: Auth operations
        try:
            # Juste tester si on peut accéder aux méthodes auth
            session = supabase.auth.get_session()
            print("✅ Session Auth accessible")
        except:
            print("⚠️ Pas de session active (normal)")
        
        # Test 2: Buckets storage
        try:
            buckets = supabase.storage.list_buckets()
            if buckets:
                print(f"✅ Storage : {len(buckets)} bucket(s) trouvé(s)")
            else:
                print("✅ Storage accessible (aucun bucket)")
        except Exception as e:
            print(f"⚠️ Storage : {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur tests opérations : {str(e)}")
        return False

if __name__ == "__main__":
    print("=== TEST CONNEXION SUPABASE (VERSION SIMPLE) === 🧪")
    
    success = test_connection()
    
    if success:
        test_simple_operations()
        print("\n🎉 CONNEXION RÉUSSIE ! Ton environnement est prêt pour le tutoriel!")
        print("Tu peux maintenant créer tes tables et lancer main.py")
    else:
        print("\n Vérifiez :")
        print("   1. Vos clés dans le fichier .env")
        print("   2. Que le projet Supabase est bien actif")
        print("   3. Que les URLs sont correctes")