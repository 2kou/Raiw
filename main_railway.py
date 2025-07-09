"""
Point d'entrée principal pour le déploiement Railway
Modifie le comportement pour Railway.app au lieu de Replit
"""

from config.env_loader import load_env
from bot.handlers import start_bot_sync
from http_server import start_server_in_background
from railway_keep_alive import RailwayKeepAliveSystem
import os
import threading
import asyncio
import logging

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def start_with_railway_integration():
    """Démarrage avec intégration Railway"""
    load_env()

    # Configuration pour Railway.app
    railway_port = int(os.environ.get('PORT', 8080))
    os.environ['PORT'] = str(railway_port)
    
    # Log deployment success message
    logger.info("🚂 Bot TeleFeed déployé avec succès sur Railway.app")

    # Start HTTP server in background
    server_thread = start_server_in_background()
    
    # Import bot client pour Railway keep alive
    from bot.handlers import client
    from config.settings import ADMIN_ID
    
    # Initialiser le système Railway keep alive
    railway_keep_alive = RailwayKeepAliveSystem(client, ADMIN_ID)
    
    # Démarrer le système de maintien d'activité Railway en arrière-plan
    asyncio.create_task(railway_keep_alive.start_railway_keep_alive())
    
    # Start the bot (main process)
    start_bot_sync()

if __name__ == "__main__":
    # Pour Railway, utiliser le main principal mais avec intégration
    load_env()

    # Configuration pour Railway.app
    railway_port = int(os.environ.get('PORT', 8080))
    os.environ['PORT'] = str(railway_port)
    
    # Log deployment success message
    print("🚂 Bot TeleFeed déployé avec succès sur Railway.app")

    # Start HTTP server in background
    server_thread = start_server_in_background()
    
    # Start the bot (main process)
    start_bot_sync()