import os
import tweepy
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

def verify_twitter():
    print("--- 🕵️ VERIFICACIÓN DE CLAVES DE TWITTER ---")
    
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    # 1. Verificar que las variables existen
    print(f"1. Variables de entorno:")
    print(f"   - API_KEY: {'✅ Presente' if api_key else '❌ FALTANTE'}")
    print(f"   - API_SECRET: {'✅ Presente' if api_secret else '❌ FALTANTE'}")
    print(f"   - ACCESS_TOKEN: {'✅ Presente' if access_token else '❌ FALTANTE'}")
    print(f"   - ACCESS_SECRET: {'✅ Presente' if access_secret else '❌ FALTANTE'}")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("\n❌ DETENIDO: Faltan variables en el archivo .env")
        return

    # 2. Intentar autenticación
    print("\n2. Intentando conectar con Tweepy (API v2)...")
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        # 3. Verificar Permisos de LECTURA (Obtener usuario propio)
        print("   - Probando permisos de LECTURA (get_me)...")
        me = client.get_me()
        if me.data:
            print(f"   ✅ LECTURA OK. Usuario identificado: @{me.data.username} (ID: {me.data.id})")
        else:
            print("   ⚠️ LECTURA EXTRAÑA: No dio error pero no retornó datos.")

        # 4. Verificar Permisos de ESCRITURA (Enviar Tweet)
        print("   - Probando permisos de ESCRITURA (create_tweet)...")
        msg = "Test de conexión Datalaria Autopilot 🤖 ✅"
        response = client.create_tweet(text=msg)
        
        if response.data:
             print(f"   ✅ ESCRITURA OK. Tweet enviado con ID: {response.data['id']}")
             print("   (Puedes borrar este tweet manualmente ahora)")
        
    except tweepy.Errors.Forbidden as e:
        print("\n❌ ERROR 403 FORBIDDEN (Permisos Insuficientes)")
        print("   Esto significa que tus credenciales son válidas, pero NO TIENEN PERMISO DE ESCRITURA.")
        print("   Solución:")
        print("   1. Ve al Developer Portal.")
        print("   2. User authentication settings > App permissions.")
        print("   3. Cambia a 'Read and Write'.")
        print("   4. IMPORTANTE: Regenera el Access Token y Secret. Los viejos no se actualizan solos.")
        print(f"   Detalle técnico: {e}")
        
    except tweepy.Errors.Unauthorized as e:
        print("\n❌ ERROR 401 UNAUTHORIZED (Credenciales Inválidas)")
        print("   Esto significa que alguna de tus claves (API Key o Tokens) está mal copiada.")
        print("   Revisa espacios en blanco al inicio o final en el .env.")
        print(f"   Detalle técnico: {e}")
        
    except Exception as e:
        print(f"\n❌ ERROR DESCONOCIDO: {type(e).__name__}")
        print(f"   {e}")

if __name__ == "__main__":
    verify_twitter()
