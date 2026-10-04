# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    # 1. On augmente la vitesse verticale du Doodle avec la gravité
    doodle_dict["vy"] += GRAVITY

    # 2. On met à jour la position Y selon cette vitesse
    doodle_dict["y"] += doodle_dict["vy"]

    return

# ===========================================================


# ======================== PARTIE 1.2 ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    # TODO : Gérez les déplacements gauche/droite et mettez à jour
    # simultanément la direction et l'image du Doodle.

 

    # TODO : Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.



    return

# ===========================================================


# ======================== PARTIE 2.3 ========================
def move_platforms():
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    
    for plat in PLATFORMS:
        # 1. On filtre : seules les plateformes bleues bougent
        if plat["type"] == "blue":
            # 2. Mise à jour de la position horizontale
            plat["x"] += plat["vx"]
            
            # 3. Collision avec le bord gauche
            if plat["x"] <= 0:
                plat["x"] = 0
                plat["vx"] = -plat["vx"]  # Inverse la direction
                
            # 4. Collision avec le bord droit
            elif plat["x"] + plat["width"] >= SCREEN_WIDTH:
                plat["x"] = SCREEN_WIDTH - plat["width"]
                plat["vx"] = -plat["vx"]  
    return

# ===========================================================


# ======================== PARTIE 3.2 ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    # 1. Le Doodle ne peut rebondir QUE s'il descend
    if doodle_dict["vy"] <= 0:
        return

    # Dimensions du Doodle pour construire son rectangle
    doodle_rect = (
        doodle_dict["x"],
        doodle_dict["y"],
        DOODLE_WIDTH,
        DOODLE_HEIGHT
    )

    for plat in PLATFORMS:
        # Seules les plateformes actives sont prises en compte
        if not plat["active"]:
            continue

        plat_rect = (plat["x"], plat["y"], plat["width"], plat["height"])

        # Test 1 : Chevauchement des deux rectangles
        if rects_collide(doodle_rect, plat_rect):
            # Position des pieds du Doodle à l'image précédente (y_précédent = y_actuel - vy)
            previous_feet_y = (doodle_dict["y"] - doodle_dict["vy"]) + DOODLE_HEIGHT

            # Test 2 : Les pieds étaient bien au-dessus (ou au niveau) du haut de la plateforme
            if previous_feet_y <= plat["y"] + 14:
                
                # Gestion selon le type de plateforme
                if plat["type"] == "spring":
                    doodle_dict["vy"] = SPRING_JUMP_VELOCITY
                elif plat["type"] == "brown":
                    doodle_dict["vy"] = JUMP_VELOCITY
                    plat["active"] = False  # La plateforme marron se casse/s'inactive
                else:  # "green" ou "blue"
                    doodle_dict["vy"] = JUMP_VELOCITY

                # Un seul rebond doit être traité à la fois
                break 
    #
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.

    return

# ===========================================================


# ======================== PARTIE 3.3 ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    # 1. Vérifie si le Doodle a dépassé le seuil de la caméra vers le haut
    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD:
        scroll_amount = CAMERA_SCROLL_THRESHOLD - doodle_dict["y"]

        # 2. On recentre le Doodle au niveau du seuil
        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD

        # 3. On décale toutes les plateformes vers le bas
        for plat in PLATFORMS:
            plat["y"] += scroll_amount

        # 4. On augmente le score selon la distance parcourue
        doodle_dict["score"] += int(scroll_amount)

        # 5. Mise à jour du high score si nécessaire
        if doodle_dict["score"] > doodle_dict["high_score"]:
            doodle_dict["high_score"] = doodle_dict["score"]

        # 6. Suppression des plateformes sorties par le bas de l'écran
        i = 0
        while i < len(PLATFORMS):
            if PLATFORMS[i]["y"] > SCREEN_HEIGHT:
                PLATFORMS.pop(i)
            else:
                i += 1

        # 7. Génération de nouvelles plateformes en haut
        generate_new_platforms()
    return

# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    # 1. Si la liste est vide, on ne peut pas trouver la plateforme la plus haute
    if not PLATFORMS:
        return

    # 2. On trouve la plateforme la plus haute (celle qui a la plus petite valeur Y)
    highest_platform = min(PLATFORMS, key=lambda p: p["y"])

    # 3. Tant que la plateforme la plus haute est visible (en dessous du haut de l'écran)
    current_y = highest_platform["y"]
    while current_y > 0:
        # On calcule un espacement vertical aléatoire entre les limites configurées
        gap = random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
        current_y -= gap

        # Sélection du type de plateforme selon les probabilités demandées (55% verte, 20% bleue, 13% ressort)
        p_type = choose_platform_type(0.55, 0.20, 0.13)

        # Position X aléatoire pour la nouvelle plateforme
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)

        # Création et ajout de la nouvelle plateforme
        new_plat = create_platform(x, current_y, p_type)
        PLATFORMS.append(new_plat)

    return

# ===========================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
        r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
        r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )
