import math
import random

LOADING_TERMS = ["Downloading", "Updating", "Executing", "Finding", "Searching for", "Deleting",
                 "Creating", "Mixing", "Baking", "Loading", "Uploading", "Rolling", "Planting",
                 "Growing", "Typing", "Brewing", "Shopping for", "Fishing for", "Stashing", "Formatting",
                 "Coiling", "Breaking", "Toasting", "Meowing", "Pouring"]
MID_TERMS = ["a", "all the", "some", "the most", "that", "this", "many", "the entire", "the empty"]
LOADED_TERMS = ["cookie", "cache", "chip", "lock", "keyboard", "logic", "code", "math", "cereal",
                "vape", "water", "juice", "rug", "cord", "port", "puppy", "kitten", "gaim", "key",
                "phone", "table", "mouse", "coffee", "tea", "python", "java", "screen", "virus",
                "bread", "toast", "ball", "cloud", "recycling bin", "mug", "desk"]
LOADING_BRACKETS = ["{}", "[]", "()", "<>", "‹›", "«»", "↻↺"]


def random_loading_phrase() -> str:
    loading_word = random.choice(LOADING_TERMS)
    mid_term = random.choice(MID_TERMS)
    loaded_word = random.choice(LOADED_TERMS)
    phrase = loading_word + " " + mid_term + " "
    if mid_term in ["some", "all the", "the most", "many"]:
        phrase += loaded_word + "'s"
    else:
        phrase += loaded_word
    if loading_word == "Baking" and loaded_word in ["puppy", "kitten", "mouse"]:
        return phrase + ("." * random.randint(2, 5)) + "some cookies" + ("." * random.randint(2, 5))
    else:
        return phrase + ("." * random.randint(2, 5))
    # return phrase


def polypointlist(sides: int, offset: int, cx: int, cy: int, radius: int) -> list:
    step = 2 * math.pi / sides
    offset = math.radians(offset)
    pointlist = [(radius * math.cos(step * n + offset) + cx, radius * math.sin(step * n + offset) + cy) for n in
                 range(0, int(sides) + 1)]
    return pointlist


def clamp(n, minn, maxn, wrap_around=False):
    if wrap_around:
        if n > maxn:
            return minn
        elif n < minn:
            return maxn
        else:
            return n
    else:
        return max(min(maxn, n), minn)

def set_masterpiece_size(image_size: str) -> tuple[int, int]:
    """
    Set the size of the masterpiece.

    Args:
        image_size: String identifier for the desired image size

    Returns:
        tuple[int, int]: Width and height in pixels
    """
    SIZE_MAPPING = {
        "chicken": (320, 320),
        "dog": (640, 640),
        "camel": (960, 960),
        "avatar": (500, 500),
        "tile": (500, 700),
        "banner": (1500, 500),
        "sleeves": (400, 560),
        "playmat": (1920, 1120),
        "sticker": (420, 420),
        "pen": (64, 64)
    }

    return SIZE_MAPPING.get(image_size.lower(), (0, 0))


def angle_between_points(point1, point2):
    """
    Calculate the angle in degrees from point1 to point2.

    Args:
        point1: tuple (x1, y1) - starting point
        point2: tuple (x2, y2) - ending point

    Returns:
        float: angle in degrees (0-360)
    """
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the difference
    dx = x2 - x1
    dy = y2 - y1

    # Calculate an angle in radians, then convert to degrees
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    # Convert to 0-360 range if needed
    if angle_deg < 0:
        angle_deg += 360

    return -angle_deg
