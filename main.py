import os
import tkinter as tk
from CareSyncAI import CareSyncAI
from CareSyncApp import CareSyncApp
from VirtualPlanningAssistant import VirtualPlanningAssistant

# Définir le nom du fichier de base de données
db_name = "care_sync.db"

if __name__ == "__main__":
    # Lancement de l'interface utilisateur
    root = tk.Tk()
    app = CareSyncApp(root, db_name)

    care_sync_ai = CareSyncAI(db_name)
    virtual_planning_assistant = VirtualPlanningAssistant(care_sync_ai.db_manager)

    # Attribution des objets care_sync_ai et virtual_planning_assistant a l'application
    app.care_sync_ai = care_sync_ai
    app.virtual_planning_assistant = virtual_planning_assistant

    root.mainloop()
    