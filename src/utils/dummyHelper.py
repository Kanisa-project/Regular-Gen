import random
from config import settings as s

all_card_template = {"card_name": [],
                     "card_set": [],
                     "card_id": [],
                     "card_rarity": [],
                     "card_type": []}

digimon_card_template = {"card_name": [],
                         "card_attribute": [],
                         "card_digi_type": [],
                         "card_play_cost": [],
                         "card_dp": []}

yugioh_card_template = {"card_name": [],
                        "card_attribute": [],
                        "card_digi_type": [],
                        "card_play_cost": [],
                        "card_dp": []}

pokemon_card_template = {"card_name": [],
                         "card_types": [],
                         "card_hp": [],
                         "card_": [],
                         "card_dp": []}

lorcana_card_template = {"card_name": [],
                         "card_": [],
                         "card__type": [],
                         "card_cost": [],
                         "card_dp": []}

mtg_card_template = {"card_name": [],
                     "card_set": [],
                     "card_cmc": [],
                     "card_layout": [],
                     "card_type": [],
                     "card_colors": [],
                     "card_mana_cost": []}

all_gaim_template = {"player_name": [],
                     "high_score": [],
                     "prev_score": [],
                     "average_score": [],
                     "total_score": []}

candy_slinger_template = {"player_name": [],
                          "money": [],
                          "gumdrop": [],
                          "gummy_bear": [],
                          "gummy_worm": [],
                          "candy_cane": [],
                          "jelly_bean": [],
                          "fruit_chew": [],
                          "rock_candy": [],
                          "candy_corn": [],
                          "sour_gummy ring": [],
                          "butterscotch disc": []}

k_paint_template = {"player_name": [],
                    "high_score": [],
                    "prev_score": [],
                    "color_palette": []}

othaido_template = {"player_name": [],
                    "high_score": [],
                    "prev_score": [],
                    "num_of_aett": []}

pylanes_template = {"player_name": [],
                    "player_wizard": [],
                    "high_score": [],
                    "prev_score": []}

ALPHANUMERIC_WORD_LISTS = {
    ",": ["comma", "coma", "kona", "players", "right", "turtle", "look", "please", "feel", "less"],
    "'": ["apostrophe", "trophy", "post", "apostle", "hustle", "bussin", "combine", "pretty", "if", "you"],
    " ": ["space", "blank", "empty", "nope", "paris", "almost", "copper", "whole", "world", "ice"],
    ":": ["colon", "dots", "top", "heart", "frankfurt", "star", "silver", "try", "too", "hard"],
    "-": ["dash", "lined", "middle", "zip", "greenville", "half", "fake", "get", "my", "hair"],
    "_": ["under", "line", "bottom", "score", "moscow", "over", "gold", "why", "do", "I"],
    "0": ["zero", "none", "hero", "villain", "beijing", "eye", "platinum", "yeah", "baby", "ever"],
    "1": ["one", "lonely", "win", "juan", "tokyo", "hand", "sapphire", "run", "the", "jewels"],
    "2": ["two", "too", "lose", "to", "madagascar", "foot", "emerald", "render", "final", "fantasy"],
    "3": ["three", "tree", "charm", "triangle", "chicago", "knee", "ruby", "crash", "hit", "wall"],
    "4": ["four", "fore", "core", "square", "seattle", "ear", "diamond", "in", "right", "now"],
    "5": ["five", "high", "hive", "pentagon", "miami", "hair", "opal", "need", "miracle", "stranded"],
    "6": ["six", "sticks", "chicks", "angle", "detroit", "finger", "jade", "let", "down", "around"],
    "7": ["seven", "heaven", "Kevin", "shovel", "mesa", "toe", "topaz", "head", "died", "hole"],
    "8": ["eight", "straight", "infinite", "ate", "youngstown", "bones", "quartz", "call", "name", "side"],
    "9": ["nine", "no", "max", "final", "akron", "teeth", "onyx", "headphone", "window", "door"],
    "a": ["alpha", "after", "aloha", "all", "atlanta", "aisle", "amber", "ape", "apple", "acura"],
    "b": ["bravo", "being", "bang", "bunny", "buffalo", "banquet", "blue", "bat", "broccoli", "bently"],
    "c": ["charlie", "cold", "climb", "cow", "cleveland", "concert", "cerulean", "cat", "cauliflower", "car"],
    "d": ["delta", "dinner", "drink", "dead", "denver", "diner", "dandelion", "dog", "dragonfruit", "dodge"],
    "e": ["echo", "evening", "east", "eat", "ellensburg", "elegant", "ecru", "elephant", "eggplant", "elantra"],
    "f": ["foxtrot", "fire", "flint", "flower", "flynt", "ferocious", "firebrick", "fox", "fennel", "ford"],
    "g": ["golf", "grass", "golden", "game", "georgia", "giant", "green", "gorilla", "grape", "golfcart"],
    "h": ["hotel", "hurried", "hungry", "humble", "houston", "hurling", "hotpink", "hippopotamus", "honeydew", "honda"],
    "i": ["india", "in", "ice", "into", "idaho", "icicle", "indigo", "iguana", "iceberg", "illicit"],
    "j": ["juliette", "just", "jump", "Jessica", "jamestown", "jungle", "jade", "jaguar", "jalapenos", "jetplane"],
    "k": ["kilo", "killed", "knight", "kindle", "kentucky", "kingly", "khaki", "kangaroo", "kale", "kudi"],
    "l": ["lima", "last", "long", "list", "london", "lost", "lavender", "llama", "legumes", "lincoln"],
    "m": ["mike", "month", "mass", "moon", "massachusetts", "more", "magenta", "monkey", "mushroom", "minivan"],
    "n": ["november", "near", "noble", "noon", "nashville", "never", "navyblue", "newt", "napa", "nas"],
    "o": ["oscar", "open", "opera", "out", "oakland", "optic", "orchid", "orangutan", "orange", "october"],
    "p": ["papa", "punch", "prince", "penelope", "philadelphia", "pan", "periwinkle", "platypus", "potato", "poptart"],
    "q": ["quebec", "queen", "quest", "quilt", "queens", "question", "quicksilver", "quail", "quinoa", "quack"],
    "r": ["romeo", "really", "random", "rake", "reno", "ranch", "red", "rhinoceros", "radish", "reel"],
    "s": ["sierra", "sold", "simple", "sake", "scranton", "sacred", "saffron", "snake", "spinach", "soil"],
    "t": ["tango", "time", "topple", "take", "tuscaloosa", "ton", "tawny", "turkey", "taro", "taser"],
    "u": ["uniform", "until", "under", "utility", "ukraine", "ultra", "ube", "unicorn", "ugli", "up"],
    "v": ["victor", "very", "vixen", "vampire", "vienna", "violence", "violet", "vulture", "vanilla", "voss"],
    "w": ["whiskey", "wise", "west", "well", "wuhan", "well", "white", "whale", "watermelon", "wet"],
    "x": ["x-ray", "x-men", "Xena", "xylophone", "xi'an", "xacto", "xanadu", "xenops", "ximenia", "xoom"],
    "y": ["yankee", "yelled", "yip", "yuck", "yakima", "yarn", "yellow", "yak", "yam", "yup"],
    "z": ["zulu", "zebra", "zoinks", "zealand", "zhengzhou", "zombie", "zaffre", "zebra", "zucchini", "zoom"]
}


def new_dummy_subclient() -> list:
    """Return a list of possible subclients, between 0 and 4 long."""
    subclient_list = ", ".join(random.sample(s.sub_clients, random.randint(0, 3)))
    return subclient_list


def new_dummy_accountid() -> str:
    """Return a random accountID without the unique identifier number."""
    return f"{random.choice(['RED', 'BLU', 'GRN', 'BLK', 'WHT', 'PRPL', 'ORNG'])}"


def new_dummy_tech_username_password() -> (str, str):
    """Return a dummy username for a technician."""
    first_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    second_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    return f"{first_word.title()}{second_word.title()}", f"{first_word}123"


def new_dummy_business() -> str:
    """Return a random fake business name."""
    first_word = random.choice(s.animal_sounds)
    second_word = random.choice(s.animal_sounds)
    busi = random.choice(s.business_abbreviations)
    return f"{first_word} {second_word} {busi}"


def new_dummy_email() -> str:
    """Return a fake random email address."""
    first_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    second_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    email_provider = random.choice(s.email_domains)
    return f"{first_word}.{second_word}@{email_provider}"


def new_dummy_pool_address() -> str:
    """Generate a fake random pool address."""
    first_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    second_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    third_word = random.choice(s.ALPHANUMERIC_DICT[random.choice(s.ALPHANUMERIC)])
    gibberish = "".join(random.choice(first_word + second_word + third_word + "3769420425") for _ in range(16))
    return f"https://{first_word}.{second_word}.pool/{third_word}/{gibberish}"


def new_dummy_pool_username():
    pass


def new_dummy_pool_nickname():
    pass


def new_dummy_full_name() -> str:
    """Generate a random first and last name."""
    return f"{random.choice(s.first_names)} {random.choice(s.last_names)}"


def new_dummy_phone_number() -> str:
    """Generate a new random phone number."""
    area_code = random.randint(0, 999)
    first_part = random.randint(0, 999)
    second_part = random.randint(0, 9999)
    return "({:03d}){:03d}-{:04d}".format(area_code, first_part, second_part)


def generate_dummy_technician() -> dict:
    """Generate enough dummy info for a technician."""
    username, password = new_dummy_tech_username_password()
    fullname = new_dummy_full_name().split()
    dummy_technician_data_card = {
        "Username": username,
        "Password": password,
        "First_Name": fullname[0],
        "Last_Name": fullname[1],
        "Clearance_Level": random.choice(["Admin", "Technician"]),
        "Email": new_dummy_email(),
        "Phone_number": new_dummy_phone_number(),
    }
    return dummy_technician_data_card


def generate_dummy_pool() -> dict:
    """
    Returns a dictionary of dummy/placeholder values.
    :return: Dictionary of pool address and pool nickname
    """
    dummy_pool = new_dummy_pool_address()
    dummy_nickname = dummy_pool.split(".")[1]
    dummy_username = "BLU3"
    dummy_pool_data_card = {
        "Address": dummy_pool,
        "Username": dummy_username,
        "Nickname": dummy_nickname
    }
    return dummy_pool_data_card


def generate_dummy_owner() -> dict:
    dummy_owner_data_card = {
        "accountID": new_dummy_accountid(),
        "Business_Name": new_dummy_business(),
        "Primary_Contact": new_dummy_full_name(),
        "Sub_clients": new_dummy_subclient(),
        "Email": new_dummy_email(),
        "Phone_Number": new_dummy_phone_number(),
        "Service_Level": random.choice(["Level 1", "Level 2", "Level 3"]),
        "Number_Workers": random.choice(["5", "1", "16", "8", f"{random.randint(3, 6)}"]),
        "Primary_Pool": generate_dummy_pool()
    }
    return dummy_owner_data_card
