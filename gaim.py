import os
import random
import shutil

from PIL import Image
from settings import *

SPACEDITS_OBJECT_DICT = {
    "Player": ["Ship"],
    "player": ["Ship"],
    "Enemy": ["Alien"],
    "Ally": ["Ship"],
    "Obstacle": ["Asteroid"],
    "Goal": ["Goal"],
    "Collectible": ["Medallion"],
    "Portal": ["Portal"]
}


THURBO_OBJECT_DICT = {
    "Player": ["Tribloc"],
    "player": ["Tribloc"],
    "Enemy": ["Sword"],
    "Ally": ["RTJ"],
    "Obstacle": ["Platform"],
    "Goal": ["Goal"],
    "Collectible": ["Medallion"],
    "Portal": ["Portal"]
}

ABF_OBJECT_DICT = {
    "Player": ["Ball"],
    "player": ["Ball"],
    "Enemy": ["Ball"],
    "Ally": ["Ball"],
    "Obstacle": ["Platform"],
    "Goal": ["Goal"],
    "Collectible": ["Medallion"],
    "Portal": ["Portal"]
}
BOOTYRACE_OBJECT_DICT = {
    "Player": ["Boat"],
    "player": ["Boat"],
    "Enemy": ["Boat"],
    "Ally": ["Boat"],
    "Obstacle": ["Platform"],
    "Goal": ["Goal"],
    "Collectible": ["Medallion"],
    "Portal": ["Portal"]
}
OTHAIDO_OBJECT_DICT = {
    "Player": ["Ball"],
    "player": ["Ball"],
    "Enemy": ["Ball"],
    "Ally": ["Ball"],
    "Obstacle": ["Platform"],
    "Goal": ["Goal"],
    "Collectible": ["Medallion"],
    "Portal": ["Portal"]
}

GAYM_OBJECT_DICT = {
    "ABF": ABF_OBJECT_DICT,
    "ThurBo": THURBO_OBJECT_DICT,
    "Othaido": OTHAIDO_OBJECT_DICT,
    "BootyDefence": BOOTYRACE_OBJECT_DICT,
    "SpaceDits": SPACEDITS_OBJECT_DICT
}

PLAYER_FACTOR_OPTIONS_DICT = {
    "Movement": {
        "2-direction": ["Can move up and down or left and right.", True],
        "4-direction": ["Can move up or down or left or right.", True],
        "8-direction": ["Can move up or down and left or right.", True]
    },
    "Projectiles": {
        "Can Shoot": ["If player can shoot projectiles.", True],
        "Follow Enemy": ["If the projectiles will follow enemies", False]
    },
    "Camera": {
        "Can Move": ["If the camera moves.", False],
        "Follow Player": ["If the camera follows the player.", False]
    },
    "Statistics": {
        "Health": ["Starting health of the player.", random.randint(0, 99)],
        "Offence": ["Offensive power of the player.", random.randint(0, 99)],
        "Defence": ["Defensive ability of the player.", random.randint(0, 99)]
    },
    "spirite": ["What will the player look like?", Image.new("RGBA", (128, 128), BLUE)]
}

ENEMY_FACTOR_OPTIONS_DICT = {
    "Movement": {
        "2-direction": ["Can move up and down or left and right.", True],
        "4-direction": ["Can move up or down or left or right.", False],
        "8-direction": ["Can move up or down and left or right.", False]
    },
    "Projectiles": {
        "Can Shoot": ["If enemy can shoot projectiles.", True]
    },
    "Statistics": {
        "Health": ["Starting health of the enemy.", random.randint(0, 99)],
        "Offence": ["Offensive power of the enemy.", random.randint(0, 99)],
        "Defence": ["Defensive ability of the enemy.", random.randint(0, 99)]
    }
}

GOAL_FACTOR_OPTIONS_DICT = {
    "Kill enemies": ["Kill a specific number of enemies.", random.randint(0, 99)],
    "Survive minutes": ["Survive an amount of minutes.", random.randint(0, 9)],
    "Arrive destination": ["Arrive at the destination.", True],
    "Collect things": ["Collect a number of things and stuff.", random.randint(0, 99)]
}

ENVIRONMENT_FACTOR_OPTIONS_DICT = {
    "Safe": ["Does the environment have spikes and lava or flowers and bunnies?", True],
    "Difficulty": ["How many obstacles are in the way?", 0],
    "Theme": ["Is it set in space or on a farm or in the city?", ["Space", "Farm", "City"]],
    "Engine": ["Which engine will power the gaim?", ["ABF", "ThurBo", "SpaceDits", "Booty Defence", "Othaido"]]
}


def generate_player_factors(img: Image, kre8dict: dict) -> (Image, dict):
    kre8dict["gaim"]["Player"] = {
        "Movement": random.choice(list(PLAYER_FACTOR_OPTIONS_DICT["Movement"].keys())),
        "Projectiles": {
            "Can Shoot": PLAYER_FACTOR_OPTIONS_DICT["Projectiles"]["Can Shoot"][1],
            "Follow Enemy": PLAYER_FACTOR_OPTIONS_DICT["Projectiles"]["Follow Enemy"][1]
        },
        "Camera": {
            "Can Move": PLAYER_FACTOR_OPTIONS_DICT["Camera"]["Can Move"][1],
            "Follow Player": PLAYER_FACTOR_OPTIONS_DICT["Camera"]["Follow Player"][1]
        },
        "Statistics": {
            "Health": PLAYER_FACTOR_OPTIONS_DICT["Health"][1],
            "Offence": PLAYER_FACTOR_OPTIONS_DICT["Offence"][1],
            "Defence": PLAYER_FACTOR_OPTIONS_DICT["Defence"][1]
        },
        "spirite": PLAYER_FACTOR_OPTIONS_DICT["spirite"][1]
    }
    return img, kre8dict


def generate_enemy_factors(img: Image, kre8dict: dict) -> (Image, dict):
    kre8dict["gaim"]["Enemy"] = {
        "Movement": random.choice(list(ENEMY_FACTOR_OPTIONS_DICT["Movement"].keys())),
        "Projectiles": {
            "Can Shoot": ENEMY_FACTOR_OPTIONS_DICT["Projectiles"]["Can Shoot"][1]
        },
        "Statistics": {
            "Health": ENEMY_FACTOR_OPTIONS_DICT["Health"][1],
            "Offence": ENEMY_FACTOR_OPTIONS_DICT["Offence"][1],
            "Defence": ENEMY_FACTOR_OPTIONS_DICT["Defence"][1]
        },
    }
    return img, kre8dict


def generate_goal_factors(img: Image, kre8dict: dict) -> (Image, dict):
    kre8dict["gaim"]["Goal"] = {
        "Goal One": random.choice(list(GOAL_FACTOR_OPTIONS_DICT.keys())),
        "Goal Two": random.choice(list(GOAL_FACTOR_OPTIONS_DICT.keys())),
        "Goal Three": random.choice(list(GOAL_FACTOR_OPTIONS_DICT.keys())),
        "Goal Four": random.choice(list(GOAL_FACTOR_OPTIONS_DICT.keys()))
    }
    return img, kre8dict


def generate_environment_factors(img: Image, kre8dict: dict) -> (Image, dict):
    """
    Generate environment factors such as theme and which engine to use.
    :param img:
    :param kre8dict:
    :return:
    """
    kre8dict["gaim"]["Environment"] = {
        "Safe": ENVIRONMENT_FACTOR_OPTIONS_DICT["Safe"][1],
        "Difficulty": ENVIRONMENT_FACTOR_OPTIONS_DICT["Difficulty"][1],
        "Theme": random.choice(ENVIRONMENT_FACTOR_OPTIONS_DICT["Theme"][1]),
        "Engine": random.choice(ENVIRONMENT_FACTOR_OPTIONS_DICT["Engine"][1])
    }
    return img, kre8dict


def add_gaim(img: Image, kre8dict: dict) -> Image:
    return img


def create_directory(img: Image, kre8dict: dict, gaim_str="") -> Image:
    directory = kre8dict['use_id']
    parent_directory = f"{kre8dict['artributes'][3]}"
    path = os.path.join(parent_directory, directory)
    if not os.path.isdir(path):
        print(path)
        os.mkdir(path)
    else:
        print(path)
    print("made  " + path)
    return img
