import discord
from discord.ext import commands
from datetime import datetime
import cv2
from urllib.request import urlopen, Request
import numpy as np
from io import BytesIO
import json, random

class Interact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.regionals = {"z": "🇿", "y": "🇾", "x": "🇽", "w": "🇼", "v": "🇻", "u": "🇺", "t": "🇹", "s": "🇸", "r": "🇷", "q": "🇶", "p": "🇵", "o": "🇴", "n": "🇳", "m": "🇲", "l": "🇱", "k": "🇰", "j": "🇯", "i": "🇮", "h": "🇭", "g": "🇬", "f": "🇫", "e": "🇪", "d": "🇩", "c": "🇨", "b": "🇧", "a": "🇦"}
        self.emojis = {"soccer": "⚽", "basketball": "🏀", "football": "🏈", "baseball": "⚾", "tennis": "🎾", "volleyball": "🏐", "rugby_football": "🏉", "8ball": "🎱", "golf": "⛳", "golfer": "🏌", "ping_pong": "🏓", "badminton": "🏸", "hockey": "🏒", "field_hockey": "🏑", "cricket": "🏏", "ski": "🎿", "skier": "⛷", "snowboarder": "🏂", "ice_skate": "⛸", "bow_and_arrow": "🏹", "fishing_pole_and_fish": "🎣", "rowboat": "🚣", "swimmer": "🏊", "surfer": "🏄", "bath": "🛀", "basketball_player": "⛹", "lifter": "🏋", "bicyclist": "🚴", "mountain_bicyclist": "🚵", "horse_racing": "🏇", "levitate": "🕴", "trophy": "🏆", "running_shirt_with_sash": "🎽", "medal": "🏅", "military_medal": "🎖", "reminder_ribbon": "🎗", "rosette": "🏵", "ticket": "🎫", "tickets": "🎟", "performing_arts": "🎭", "art": "🎨", "circus_tent": "🎪", "microphone": "🎤", "headphones": "🎧", "musical_score": "🎼", "musical_keyboard": "🎹", "saxophone": "🎷", "trumpet": "🎺", "guitar": "🎸", "violin": "🎻", "clapper": "🎬", "video_game": "🎮", "space_invader": "👾", "dart": "🎯", "game_die": "🎲", "slot_machine": "🎰", "bowling": "🎳", "♡": "heart", "green_apple": "🍏", "apple": "🍎", "pear": "🍐", "tangerine": "🍊", "lemon": "🍋", "banana": "🍌", "watermelon": "🍉", "grapes": "🍇", "strawberry": "🍓", "melon": "🍈", "cherries": "🍒", "peach": "🍑", "pineapple": "🍍", "tomato": "🍅", "eggplant": "🍆", "hot_pepper": "🌶", "corn": "🌽", "sweet_potato": "🍠", "honey_pot": "🍯", "bread": "🍞", "cheese": "🧀", "poultry_leg": "🍗", "meat_on_bone": "🍖", "fried_shrimp": "🍤", "egg": "🍳", "cooking": "🍳", "hamburger": "🍔", "fries": "🍟", "hotdog": "🌭", "pizza": "🍕", "spaghetti": "🍝", "taco": "🌮", "burrito": "🌯", "ramen": "🍜", "stew": "🍲", "fish_cake": "🍥", "sushi": "🍣", "bento": "🍱", "curry": "🍛", "rice_ball": "🍙", "rice": "🍚", "rice_cracker": "🍘", "oden": "🍢", "dango": "🍡", "shaved_ice": "🍧", "ice_cream": "🍨", "icecream": "🍦", "cake": "🍰", "birthday": "🎂", "custard": "🍮", "candy": "🍬", "lollipop": "🍭", "chocolate_bar": "🍫", "popcorn": "🍿", "doughnut": "🍩", "cookie": "🍪", "beer": "🍺", "beers": "🍻", "wine_glass": "🍷", "cocktail": "🍸", "tropical_drink": "🍹", "champagne": "🍾", "sake": "🍶", "tea": "🍵", "coffee": "☕", "baby_bottle": "🍼", "fork_and_knife": "🍴", "fork_knife_plate": "🍽", "dog": "🐶", "cat": "🐱", "mouse": "🐭", "hamster": "🐹", "rabbit": "🐰", "bear": "🐻", "panda_face": "🐼", "koala": "🐨", "tiger": "🐯", "lion_face": "🦁", "cow": "🐮", "pig": "🐷", "pig_nose": "🐽", "frog": "🐸", "octopus": "🐙", "monkey_face": "🐵", "see_no_evil": "🙈", "hear_no_evil": "🙉", "speak_no_evil": "🙊", "monkey": "🐒", "chicken": "🐔", "penguin": "🐧", "bird": "🐦", "baby_chick": "🐤", "hatching_chick": "🐣", "hatched_chick": "🐥", "wolf": "🐺", "boar": "🐗", "horse": "🐴", "unicorn": "🦄", "bee": "🐝", "honeybee": "🐝", "bug": "🐛", "snail": "🐌", "beetle": "🐞", "ant": "🐜", "spider": "🕷", "scorpion": "🦂", "crab": "🦀", "snake": "🐍", "turtle": "🐢", "tropical_fish": "🐠", "fish": "🐟", "blowfish": "🐡", "dolphin": "🐬", "flipper": "🐬", "whale": "🐳", "whale2": "🐋", "crocodile": "🐊", "leopard": "🐆", "tiger2": "🐅", "water_buffalo": "🐃", "ox": "🐂", "cow2": "🐄", "dromedary_camel": "🐪", "camel": "🐫", "elephant": "🐘", "goat": "🐐", "ram": "🐏", "sheep": "🐑", "racehorse": "🐎", "pig2": "🐖", "rat": "🐀", "mouse2": "🐁", "rooster": "🐓", "turkey": "🦃", "dove": "🕊", "dog2": "🐕", "poodle": "🐩", "cat2": "🐈", "rabbit2": "🐇", "chipmunk": "🐿", "feet": "🐾", "paw_prints": "🐾", "dragon": "🐉", "dragon_face": "🐲", "cactus": "🌵", "christmas_tree": "🎄", "evergreen_tree": "🌲", "deciduous_tree": "🌳", "palm_tree": "🌴", "seedling": "🌱", "herb": "🌿", "shamrock": "☘", "four_leaf_clover": "🍀", "bamboo": "🎍", "tanabata_tree": "🎋", "leaves": "🍃", "fallen_leaf": "🍂", "maple_leaf": "🍁", "ear_of_rice": "🌾", "hibiscus": "🌺", "sunflower": "🌻", "rose": "🌹", "tulip": "🌷", "blossom": "🌼", "cherry_blossom": "🌸", "bouquet": "💐", "mushroom": "🍄", "chestnut": "🌰", "jack_o_lantern": "🎃", "shell": "🐚", "spider_web": "🕸", "earth_americas": "🌎", "earth_africa": "🌍", "earth_asia": "🌏", "full_moon": "🌕", "waning_gibbous_moon": "🌖", "last_quarter_moon": "🌗", "waning_crescent_moon": "🌘", "new_moon": "🌑", "waxing_crescent_moon": "🌒", "first_quarter_moon": "🌓", "waxing_gibbous_moon": "🌔", "moon": "🌔", "new_moon_with_face": "🌚", "full_moon_with_face": "🌝", "first_quarter_moon_with_face": "🌛", "last_quarter_moon_with_face": "🌜", "sun_with_face": "🌞", "crescent_moon": "🌙", "star": "⭐", "star2": "🌟", "dizzy": "💫", "sparkles": "✨", "comet": "☄", "sunny": "☀", "white_sun_small_cloud": "🌤", "partly_sunny": "⛅", "white_sun_cloud": "🌥", "white_sun_rain_cloud": "🌦", "cloud": "☁", "cloud_rain": "🌧", "thunder_cloud_rain": "⛈", "cloud_lightning": "🌩", "zap": "⚡", "fire": "🔥", "boom": "💥", "collision": "💥", "snowflake": "❄", "cloud_snow": "🌨", "snowman2": "☃", "snowman": "⛄", "wind_blowing_face": "🌬", "dash": "💨", "cloud_tornado": "🌪", "fog": "🌫", "umbrella2": "☂", "umbrella": "☔", "droplet": "💧", "sweat_drops": "💦", "ocean": "🌊", "watch": "⌚", "iphone": "📱", "calling": "📲", "computer": "💻", "keyboard": "⌨", "desktop": "🖥", "printer": "🖨", "mouse_three_button": "🖱", "trackball": "🖲", "joystick": "🕹", "compression": "🗜", "minidisc": "💽", "floppy_disk": "💾", "cd": "💿", "dvd": "📀", "vhs": "📼", "camera": "📷", "camera_with_flash": "📸", "video_camera": "📹", "movie_camera": "🎥", "projector": "📽", "film_frames": "🎞", "telephone_receiver": "📞", "telephone": "☎", "phone": "☎", "pager": "📟", "fax": "📠", "tv": "📺", "radio": "📻", "microphone2": "🎙", "level_slider": "🎚", "control_knobs": "🎛", "stopwatch": "⏱", "timer": "⏲", "alarm_clock": "⏰", "clock": "🕰", "hourglass_flowing_sand": "⏳", "hourglass": "⌛", "satellite": "📡", "battery": "🔋", "electric_plug": "🔌", "bulb": "💡", "flashlight": "🔦", "candle": "🕯", "wastebasket": "🗑", "oil": "🛢", "money_with_wings": "💸", "dollar": "💵", "yen": "💴", "euro": "💶", "pound": "💷", "moneybag": "💰", "credit_card": "💳", "gem": "💎", "scales": "⚖", "wrench": "🔧", "hammer": "🔨", "hammer_pick": "⚒", "tools": "🛠", "pick": "⛏", "nut_and_bolt": "🔩", "gear": "⚙", "chains": "⛓", "gun": "🔫", "bomb": "💣", "knife": "🔪", "hocho": "🔪", "dagger": "🗡", "crossed_swords": "⚔", "shield": "🛡", "smoking": "🚬", "skull_crossbones": "☠", "coffin": "⚰", "urn": "⚱", "amphora": "🏺", "crystal_ball": "🔮", "prayer_beads": "📿", "barber": "💈", "alembic": "⚗", "telescope": "🔭", "microscope": "🔬", "hole": "🕳", "pill": "💊", "syringe": "💉", "thermometer": "🌡", "label": "🏷", "bookmark": "🔖", "toilet": "🚽", "shower": "🚿", "bathtub": "🛁", "key": "🔑", "key2": "🗝", "couch": "🛋", "sleeping_accommodation": "🛌", "bed": "🛏", "door": "🚪", "bellhop": "🛎", "frame_photo": "🖼", "map": "🗺", "beach_umbrella": "⛱", "moyai": "🗿", "shopping_bags": "🛍", "balloon": "🎈", "flags": "🎏", "ribbon": "🎀", "gift": "🎁", "confetti_ball": "🎊", "tada": "🎉", "dolls": "🎎", "wind_chime": "🎐", "crossed_flags": "🎌", "izakaya_lantern": "🏮", "lantern": "🏮", "envelope": "✉", "email": "📧", "envelope_with_arrow": "📩", "incoming_envelope": "📨", "love_letter": "💌", "postbox": "📮", "mailbox_closed": "📪", "mailbox": "📫", "mailbox_with_mail": "📬", "mailbox_with_no_mail": "📭", "package": "📦", "postal_horn": "📯", "inbox_tray": "📥", "outbox_tray": "📤", "scroll": "📜", "page_with_curl": "📃", "bookmark_tabs": "📑", "bar_chart": "📊", "chart_with_upwards_trend": "📈", "chart_with_downwards_trend": "📉", "page_facing_up": "📄", "date": "📅", "calendar": "📆", "calendar_spiral": "🗓", "card_index": "📇", "card_box": "🗃", "ballot_box": "🗳", "file_cabinet": "🗄", "clipboard": "📋", "notepad_spiral": "🗒", "file_folder": "📁", "open_file_folder": "📂", "dividers": "🗂", "newspaper2": "🗞", "newspaper": "📰", "notebook": "📓", "closed_book": "📕", "green_book": "📗", "blue_book": "📘", "orange_book": "📙", "notebook_with_decorative_cover": "📔", "ledger": "📒", "books": "📚", "book": "📖", "open_book": "📖", "link": "🔗", "paperclip": "📎", "paperclips": "🖇", "scissors": "✂", "triangular_ruler": "📐", "straight_ruler": "📏", "pushpin": "📌", "round_pushpin": "📍", "triangular_flag_on_post": "🚩", "flag_white": "🏳", "flag_black": "🏴", "closed_lock_with_key": "🔐", "lock": "🔒", "unlock": "🔓", "lock_with_ink_pen": "🔏", "pen_ballpoint": "🖊", "pen_fountain": "🖋", "black_nib": "✒", "pencil": "📝", "memo": "📝", "pencil2": "✏", "crayon": "🖍", "paintbrush": "🖌", "mag": "🔍", "mag_right": "🔎", "grinning": "😀", "grimacing": "😬", "grin": "😁", "joy": "😂", "smiley": "😃", "smile": "😄", "sweat_smile": "😅", "laughing": "😆", "satisfied": "😆", "innocent": "😇", "wink": "😉", "blush": "😊", "slight_smile": "🙂", "upside_down": "🙃", "relaxed": "☺", "yum": "😋", "relieved": "😌", "heart_eyes": "😍", "kissing_heart": "😘", "kissing": "😗", "kissing_smiling_eyes": "😙", "kissing_closed_eyes": "😚", "stuck_out_tongue_winking_eye": "😜", "stuck_out_tongue_closed_eyes": "😝", "stuck_out_tongue": "😛", "money_mouth": "🤑", "nerd": "🤓", "sunglasses": "😎", "hugging": "🤗", "smirk": "😏", "no_mouth": "😶", "neutral_face": "😐", "expressionless": "😑", "unamused": "😒", "rolling_eyes": "🙄", "thinking": "🤔", "flushed": "😳", "disappointed": "😞", "worried": "😟", "angry": "😠", "rage": "😡", "pensive": "😔", "confused": "😕", "slight_frown": "🙁", "frowning2": "☹", "persevere": "😣", "confounded": "😖", "tired_face": "😫", "weary": "😩", "triumph": "😤", "open_mouth": "😮", "scream": "😱", "fearful": "😨", "cold_sweat": "😰", "hushed": "😯", "frowning": "😦", "anguished": "😧", "cry": "😢", "disappointed_relieved": "😥", "sleepy": "😪", "sweat": "😓", "sob": "😭", "dizzy_face": "😵", "astonished": "😲", "zipper_mouth": "🤐", "mask": "😷", "thermometer_face": "🤒", "head_bandage": "🤕", "sleeping": "😴", "zzz": "💤", "poop": "💩", "shit": "💩", "smiling_imp": "😈", "imp": "👿", "japanese_ogre": "👹", "japanese_goblin": "👺", "skull": "💀", "ghost": "👻", "alien": "👽", "robot": "🤖", "smiley_cat": "😺", "smile_cat": "😸", "joy_cat": "😹", "heart_eyes_cat": "😻", "smirk_cat": "😼", "kissing_cat": "😽", "scream_cat": "🙀", "crying_cat_face": "😿", "pouting_cat": "😾", "raised_hands": "🙌", "clap": "👏", "wave": "👋", "thumbsup": "👍", "+1": "👍", "thumbsdown": "👎", "-1": "👎", "punch": "👊", "facepunch": "👊", "fist": "✊", "v": "✌", "ok_hand": "👌", "raised_hand": "✋", "hand": "✋", "open_hands": "👐", "muscle": "💪", "pray": "🙏", "point_up": "☝", "point_up_2": "👆", "point_down": "👇", "point_left": "👈", "point_right": "👉", "middle_finger": "🖕", "hand_splayed": "🖐", "metal": "🤘", "vulcan": "🖖", "writing_hand": "✍", "nail_care": "💅", "lips": "👄", "tongue": "👅", "ear": "👂", "nose": "👃", "eye": "👁", "eyes": "👀", "bust_in_silhouette": "👤", "busts_in_silhouette": "👥", "speaking_head": "🗣", "baby": "👶", "boy": "👦", "girl": "👧", "man": "👨", "woman": "👩", "person_with_blond_hair": "👱", "older_man": "👴", "older_woman": "👵", "man_with_gua_pi_mao": "👲", "man_with_turban": "👳", "cop": "👮", "construction_worker": "👷", "guardsman": "💂", "spy": "🕵", "santa": "🎅", "angel": "👼", "princess": "👸", "bride_with_veil": "👰", "walking": "🚶", "runner": "🏃", "running": "🏃", "dancer": "💃", "dancers": "👯", "couple": "👫", "two_men_holding_hands": "👬", "two_women_holding_hands": "👭", "bow": "🙇", "information_desk_person": "💁", "no_good": "🙅", "ok_woman": "🙆", "raising_hand": "🙋", "person_with_pouting_face": "🙎", "person_frowning": "🙍", "haircut": "💇", "massage": "💆", "couple_with_heart": "💑", "couple_ww": "👩‍❤️‍👩", "couple_mm": "👨‍❤️‍👨", "couplekiss": "💏", "kiss_ww": "👩‍❤️‍💋‍👩", "kiss_mm": "👨‍❤️‍💋‍👨", "family": "👪", "family_mwg": "👨‍👩‍👧", "family_mwgb": "👨‍👩‍👧‍👦", "family_mwbb": "👨‍👩‍👦‍👦", "family_mwgg": "👨‍👩‍👧‍👧", "family_wwb": "👩‍👩‍👦", "family_wwg": "👩‍👩‍👧", "family_wwgb": "👩‍👩‍👧‍👦", "family_wwbb": "👩‍👩‍👦‍👦", "family_wwgg": "👩‍👩‍👧‍👧", "family_mmb": "👨‍👨‍👦", "family_mmg": "👨‍👨‍👧", "family_mmgb": "👨‍👨‍👧‍👦", "family_mmbb": "👨‍👨‍👦‍👦", "family_mmgg": "👨‍👨‍👧‍👧", "womans_clothes": "👚", "shirt": "👕", "tshirt": "👕", "jeans": "👖", "necktie": "👔", "dress": "👗", "bikini": "👙", "kimono": "👘", "lipstick": "💄", "kiss": "💋", "footprints": "👣", "high_heel": "👠", "sandal": "👡", "boot": "👢", "mans_shoe": "👞", "shoe": "👞", "athletic_shoe": "👟", "womans_hat": "👒", "tophat": "🎩", "helmet_with_cross": "⛑", "mortar_board": "🎓", "crown": "👑", "school_satchel": "🎒", "pouch": "👝", "purse": "👛", "handbag": "👜", "briefcase": "💼", "eyeglasses": "👓", "dark_sunglasses": "🕶", "ring": "💍", "closed_umbrella": "🌂", "100": "💯", "1234": "🔢", "heart": "❤", "yellow_heart": "💛", "green_heart": "💚", "blue_heart": "💙", "purple_heart": "💜", "broken_heart": "💔", "heart_exclamation": "❣", "two_hearts": "💕", "revolving_hearts": "💞", "heartbeat": "💓", "heartpulse": "💗", "sparkling_heart": "💖", "cupid": "💘", "gift_heart": "💝", "heart_decoration": "💟", "peace": "☮", "cross": "✝", "star_and_crescent": "☪", "om_symbol": "🕉", "wheel_of_dharma": "☸", "star_of_david": "✡", "six_pointed_star": "🔯", "menorah": "🕎", "yin_yang": "☯", "orthodox_cross": "☦", "place_of_worship": "🛐", "ophiuchus": "⛎", "aries": "♈", "taurus": "♉", "gemini": "♊", "cancer": "♋", "leo": "♌", "virgo": "♍", "libra": "♎", "scorpius": "♏", "sagittarius": "♐", "capricorn": "♑", "aquarius": "♒", "pisces": "♓", "id": "🆔", "atom": "⚛", "u7a7a": "🈳", "u5272": "🈹", "radioactive": "☢", "biohazard": "☣", "mobile_phone_off": "📴", "vibration_mode": "📳", "u6709": "🈶", "u7121": "🈚", "u7533": "🈸", "u55b6": "🈺", "u6708": "🈷", "eight_pointed_black_star": "✴", "vs": "🆚", "accept": "🉑", "white_flower": "💮", "ideograph_advantage": "🉐", "secret": "㊙", "congratulations": "㊗", "u5408": "🈴", "u6e80": "🈵", "u7981": "🈲", "a": "🅰", "b": "🅱", "ab": "🆎", "cl": "🆑", "o2": "🅾", "sos": "🆘", "no_entry": "⛔", "name_badge": "📛", "no_entry_sign": "🚫", "x": "❌", "o": "⭕", "anger": "💢", "hotsprings": "♨", "no_pedestrians": "🚷", "do_not_litter": "🚯", "no_bicycles": "🚳", "non_potable_water": "🚱", "underage": "🔞", "no_mobile_phones": "📵", "exclamation": "❗", "heavy_exclamation_mark": "❗", "grey_exclamation": "❕", "question": "❓", "grey_question": "❔", "bangbang": "‼", "interrobang": "⁉", "low_brightness": "🔅", "high_brightness": "🔆", "trident": "🔱", "fleur_de_lis": "⚜", "part_alternation_mark": "〽", "warning": "⚠", "children_crossing": "🚸", "beginner": "🔰", "recycle": "♻", "u6307": "🈯", "chart": "💹", "sparkle": "❇", "eight_spoked_asterisk": "✳", "negative_squared_cross_mark": "❎", "white_check_mark": "✅", "diamond_shape_with_a_dot_inside": "💠", "cyclone": "🌀", "loop": "➿", "globe_with_meridians": "🌐", "m": "Ⓜ", "atm": "🏧", "sa": "🈂", "passport_control": "🛂", "customs": "🛃", "baggage_claim": "🛄", "left_luggage": "🛅", "wheelchair": "♿", "no_smoking": "🚭", "wc": "🚾", "parking": "🅿", "potable_water": "🚰", "mens": "🚹", "womens": "🚺", "baby_symbol": "🚼", "restroom": "🚻", "put_litter_in_its_place": "🚮", "cinema": "🎦", "signal_strength": "📶", "koko": "🈁", "ng": "🆖", "ok": "🆗", "up": "🆙", "cool": "🆒", "new": "🆕", "free": "🆓", "zero": "0⃣", "one": "1⃣", "two": "2⃣", "three": "3⃣", "four": "4⃣", "five": "5⃣", "six": "6⃣", "seven": "7⃣", "eight": "8⃣", "nine": "9⃣", "ten": "🔟","0": "0⃣", "1": "1⃣", "2": "2⃣", "3": "3⃣", "4": "4⃣", "5": "5⃣", "6": "6⃣", "7": "7⃣", "8": "8⃣", "9": "9⃣", "10": "🔟", "keycap_ten": "🔟", "arrow_forward": "▶", "pause_button": "⏸", "play_pause": "⏯", "stop_button": "⏹", "record_button": "⏺", "track_next": "⏭", "track_previous": "⏮", "fast_forward": "⏩", "rewind": "⏪", "twisted_rightwards_arrows": "🔀", "repeat": "🔁", "repeat_one": "🔂", "arrow_backward": "◀", "arrow_up_small": "🔼", "arrow_down_small": "🔽", "arrow_double_up": "⏫", "arrow_double_down": "⏬", "arrow_right": "➡", "arrow_left": "⬅", "arrow_up": "⬆", "arrow_down": "⬇", "arrow_upper_right": "↗", "arrow_lower_right": "↘", "arrow_lower_left": "↙", "arrow_upper_left": "↖", "arrow_up_down": "↕", "left_right_arrow": "↔", "arrows_counterclockwise": "🔄", "arrow_right_hook": "↪", "leftwards_arrow_with_hook": "↩", "arrow_heading_up": "⤴", "arrow_heading_down": "⤵", "hash": "#⃣", "asterisk": "*⃣", "information_source": "ℹ", "abc": "🔤", "abcd": "🔡", "capital_abcd": "🔠", "symbols": "🔣", "musical_note": "🎵", "notes": "🎶", "wavy_dash": "〰", "curly_loop": "➰", "heavy_check_mark": "✔", "arrows_clockwise": "🔃", "heavy_plus_sign": "➕", "heavy_minus_sign": "➖", "heavy_division_sign": "➗", "heavy_multiplication_x": "✖", "heavy_dollar_sign": "💲", "currency_exchange": "💱", "copyright": "©", "registered": "®", "tm": "™", "end": "🔚", "back": "🔙", "on": "🔛", "top": "🔝", "soon": "🔜", "ballot_box_with_check": "☑", "radio_button": "🔘", "white_circle": "⚪", "black_circle": "⚫", "red_circle": "🔴", "large_blue_circle": "🔵", "small_orange_diamond": "🔸", "small_blue_diamond": "🔹", "large_orange_diamond": "🔶", "large_blue_diamond": "🔷", "small_red_triangle": "🔺", "black_small_square": "▪", "white_small_square": "▫", "black_large_square": "⬛", "white_large_square": "⬜", "small_red_triangle_down": "🔻", "black_medium_square": "◼", "white_medium_square": "◻", "black_medium_small_square": "◾", "white_medium_small_square": "◽", "black_square_button": "🔲", "white_square_button": "🔳", "speaker": "🔈", "sound": "🔉", "loud_sound": "🔊", "mute": "🔇", "mega": "📣", "loudspeaker": "📢", "bell": "🔔", "no_bell": "🔕", "black_joker": "🃏", "mahjong": "🀄", "spades": "♠", "clubs": "♣", "hearts": "♥", "diamonds": "♦", "flower_playing_cards": "🎴", "thought_balloon": "💭", "anger_right": "🗯", "speech_balloon": "💬", "clock1": "🕐", "clock2": "🕑", "clock3": "🕒", "clock4": "🕓", "clock5": "🕔", "clock6": "🕕", "clock7": "🕖", "clock8": "🕗", "clock9": "🕘", "clock10": "🕙", "clock11": "🕚", "clock12": "🕛", "clock130": "🕜", "clock230": "🕝", "clock330": "🕞", "clock430": "🕟", "clock530": "🕠", "clock630": "🕡", "clock730": "🕢", "clock830": "🕣", "clock930": "🕤", "clock1030": "🕥", "clock1130": "🕦", "clock1230": "🕧", "eye_in_speech_bubble": "👁‍🗨", "speech_left": "🗨", "eject": "⏏", "red_car": "🚗", "car": "🚗", "taxi": "🚕", "blue_car": "🚙", "bus": "🚌", "trolleybus": "🚎", "race_car": "🏎", "police_car": "🚓", "ambulance": "🚑", "fire_engine": "🚒", "minibus": "🚐", "truck": "🚚", "articulated_lorry": "🚛", "tractor": "🚜", "motorcycle": "🏍", "bike": "🚲", "rotating_light": "🚨", "oncoming_police_car": "🚔", "oncoming_bus": "🚍", "oncoming_automobile": "🚘", "oncoming_taxi": "🚖", "aerial_tramway": "🚡", "mountain_cableway": "🚠", "suspension_railway": "🚟", "railway_car": "🚃", "train": "🚋", "monorail": "🚝", "bullettrain_side": "🚄", "bullettrain_front": "🚅", "light_rail": "🚈", "mountain_railway": "🚞", "steam_locomotive": "🚂", "train2": "🚆", "metro": "🚇", "tram": "🚊", "station": "🚉", "helicopter": "🚁", "airplane_small": "🛩", "airplane": "✈", "airplane_departure": "🛫", "airplane_arriving": "🛬", "sailboat": "⛵", "boat": "⛵", "motorboat": "🛥", "speedboat": "🚤", "ferry": "⛴", "cruise_ship": "🛳", "rocket": "🚀", "satellite_orbital": "🛰", "seat": "💺", "anchor": "⚓", "construction": "🚧", "fuelpump": "⛽", "busstop": "🚏", "vertical_traffic_light": "🚦", "traffic_light": "🚥", "checkered_flag": "🏁", "ship": "🚢", "ferris_wheel": "🎡", "roller_coaster": "🎢", "carousel_horse": "🎠", "construction_site": "🏗", "foggy": "🌁", "tokyo_tower": "🗼", "factory": "🏭", "fountain": "⛲", "rice_scene": "🎑", "mountain": "⛰", "mountain_snow": "🏔", "mount_fuji": "🗻", "volcano": "🌋", "japan": "🗾", "camping": "🏕", "tent": "⛺", "park": "🏞", "motorway": "🛣", "railway_track": "🛤", "sunrise": "🌅", "sunrise_over_mountains": "🌄", "desert": "🏜", "beach": "🏖", "island": "🏝", "city_sunset": "🌇", "city_sunrise": "🌇", "city_dusk": "🌆", "cityscape": "🏙", "night_with_stars": "🌃", "bridge_at_night": "🌉", "milky_way": "🌌", "stars": "🌠", "sparkler": "🎇", "fireworks": "🎆", "rainbow": "🌈", "homes": "🏘", "european_castle": "🏰", "japanese_castle": "🏯", "stadium": "🏟", "statue_of_liberty": "🗽", "house": "🏠", "house_with_garden": "🏡", "house_abandoned": "🏚", "office": "🏢", "department_store": "🏬", "post_office": "🏣", "european_post_office": "🏤", "hospital": "🏥", "bank": "🏦", "hotel": "🏨", "convenience_store": "🏪", "school": "🏫", "love_hotel": "🏩", "wedding": "💒", "classical_building": "🏛", "church": "⛪", "mosque": "🕌", "synagogue": "🕍", "kaaba": "🕋", "shinto_shrine": "⛩"}
        self.answers = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
 

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(content=f"pong {[emoji for emoji in self.bot.emojis if emoji.name == 'floshed'][0]}")

    @commands.command(name='love',hidden=True,
                    brief='Show your love!',
                    help='Use this command to give someone your love! <3',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def love(self, ctx):
        actions = {
            'self': "Love yourself in private, {}... ಠ_ಠ",
            'bot': "I love you too, {} ( ＾◡＾)っ ♡",
            'default': "Hey {1}, {0} loves you! ( ＾◡＾)っ ♡",
            'none': "{} is feeling love!"
        }
        await interaction(ctx, self.bot, actions)
    
    @commands.command(name='hug',hidden=True,
                    brief='Hug someone!',
                    help='Use this command to give someone a hug! 🤗',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def hug(self, ctx):
        actions = {
            'self': "You can't hug yourself, {}, so I'll hug you instead! (づ ◕‿◕ )づ",
            'bot': "Aww, thanks {}! 🥰",
            'default': "{1} just got a BIG hug from {0}! (づ ◕‿◕ )づ",
            'none': "\*{} hugs the air\*"
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='kiss',hidden=True,
                    brief='Kiss someone!',
                    help='Use this command to give someone a juicy kiss! 😘',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def kiss(self, ctx):
        actions = {
            'self': "You can't kiss yourself, {}, so I'll kiss you instead! (*¯ ³¯*)♡",
            'bot': "Uh, thanks {} 😳",
            'default': "{1} just received a juicy kiss from {0}! (*¯ ³¯*)♡",
            'none': "\*{} sends kisses into the air\*"
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='lick',hidden=True,
                    brief='Lick someone!',
                    help='Use this command to lick someone, but make sure you and they are vaccinated first! 👅💦',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def lick(self, ctx):
        actions = {
            'self': "{} just licked themself, like a cat... 🐈",
            'bot': "I hope you have your tetanus shot in order {} 😳",
            'default': "{1} got licked all over by {0}! (っˆڡˆς)",
            'none': "https://tenor.com/bHk1o.gif"
        }
        await interaction(ctx, self.bot, actions)


    @commands.command(name='hide',hidden=True,
                    brief='Hide from someone!',
                    help='Use this command to hide from someone else!',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def hide(self, ctx):
        actions = {
            'self': "I know it's scary, but you have to face your inner demons, {} 😔",
            'bot': "I'll find you eventually {}... 😈",
            'default': "{0} is trying to hide from {1} ┬┴┬┴┤(･_├┬┴┬┴",
            'none': "{} hides from nothing, like an idiot."
        }
        await interaction(ctx, self.bot, actions)

# 630134121469050897 Bea in [x.id for x in ctx.message.mentions]:

    @commands.command(name='fuck',hidden=True,
                    brief='Fuck someone! (make sure you get their consent first)',
                    help='Use this command to have sex with someone else, but only after they consent, of course 😌!',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def fuck(self, ctx, *s):
        if ctx.author.id == 142944000138018816 and ctx.guild.id == 904530074236256256: 
            await ctx.send(file=discord.File(self.bot.imagesMap['no']))
            return
        actions = {
            'self': "Ok, masturbator {}... 😳",
            'bot': "I'm flattered, {}, but I'm already in a relationship!",
            'default': "Hey {1}, {0} wants to **FUCK**! ( ͡° ͜ʖ ͡°)",
            'none': "{} yells \"***FUCK " + ' '.join(s).upper() + "***\" out loud!"
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='slap',hidden=True,
                    brief='Slap someone!',
                    help='Use this command to slap someone else!',
                    usage='[user1|role1[, user2|role2[, ...]]]')
    async def slap(self, ctx):
        actions = {
            'self': "Please stop slapping yourself, {}, it's making everyone else unconfortable...",
            'bot': "You know I'm made of metal, right {}? You hurt yourself more than you hurt me.",
            'default': "{1} got the absolute shit slapped out of them by {0}! ( ‘д‘ ⊂ 彡☆))Д´)",
            'none': "\*SLAP\* TOP O' THE MORNIN TO YA LADDIES!"
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='snipe',hidden=True,
                brief='Snipe someone!',
                help='Use this command to kill your enemies!',
                usage='[user1|role1[, user2|role2[, ...]]]')
    async def snipe(self, ctx):
        actions = {
            'self': "Nooooooooooo, don't kill yourself {} you're so sexy " + str(discord.utils.find(lambda e: e.name.lower() == "sexy", self.bot.emojis)) or '🥺',
            'bot': "Nice try, bitch {}, but you'll have to do better than that! 😎",
            'default': "{1} got sniped by {0}! ξ(✿ ❛‿❛)ξ▄︻┻┳═一",
            'none': "Stop wasting bullets, {}."
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='dab',hidden=True,
                brief='Dab on them haters!',
                help='Use this command to dab on someone!',
                usage='[user1|role1[, user2|role2[, ...]]]')
    async def dab(self, ctx):
        actions = {
            'self': "You're dabbing on yourself, {}?! Bruh that's kinda cringe ngl",
            'bot': "Nice dab, {}! \*dabs back\* ㄥ(⸝ ، ⸍ )‾‾‾‾‾",
            'default': "Hey {1}, you just got dabbed on by {0}! ㄥ(⸝ ، ⸍ )‾‾‾‾‾",
            'none': "ㄥ(⸝ ، ⸍ )‾‾‾‾‾"
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='cry',hidden=True,
                brief='Someone made you cry?',
                help='Use this command when someone makes you cry, or if you just feel like crying!',
                usage='[user1|role1[, user2|role2[, ...]]]')
    async def cry(self, ctx):
        actions = {
            'self': "Don't beat yourself up {}, you're perfect just the way you are! ( ＾◡＾)っ ♡",
            'bot': "I'm so sorry {}... 😢",
            'default': "{1} just made {0} cry! .·´¯\`(>▂<)´¯\`·.",
            'none': ".·´¯\`(>▂<)´¯\`·."
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='spank',hidden=True,
                brief='Spank someone 😳',
                help='Use this command to punish someone who\'s been very naughty!',
                usage='[user1|role1[, user2|role2[, ...]]]')
    async def spank(self, ctx):
        actions = {
            'self': "You should get someone else to spank you {}, this is kinda sad...",
            'bot': "Harder {} UwU " + str(discord.utils.find(lambda e: e.name.lower() == "ahegao", self.bot.emojis)) or '🥵',
            'default': "{1} got spanked by {0}! (=ﾟ ωﾟ)つ (‿ˠ‿)",
            'none': "You have to spank someone!"
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='whip',hidden=True,
                brief='Whip someone 😉',
                help='Use this command if you wanna be *very* kinky!',
                usage='[user1|role1[, user2|role2[, ...]]]')
    async def whip(self, ctx):
        actions = {
            'self': "If you wanna hurt yourself there are easier ways to do it {}...",
            'bot': "Harder {} UwU " + str(discord.utils.find(lambda e: e.name.lower() == "ahegao", self.bot.emojis)) or '🥵',
            'default': "{1} was whipped by {0}! (˵ ͡~ ͜ʖ ͡°˵)ﾉ⌒",
            'none': "{} whips the air."
        }
        await interaction(ctx, self.bot, actions)

    @commands.command(name='interactions', brief='Interact with someone else.')
    async def interactions(self, ctx):
        embed = discord.Embed(title="Interactions", description="Here's all the interactions you can perform:")
        embed.add_field(name="Friendly", value="love\nhug\nkiss")
        embed.add_field(name="Sexual", value="fuck\nspank")
        embed.add_field(name="Neutral", value="hide\ndab")
        embed.add_field(name="Weird", value="lick")
        embed.add_field(name="Negative", value="cry")
        embed.add_field(name="Aggressive", value="cough\nslap\nsnipe")
        await ctx.send(embed=embed)

    @commands.command(name='cough',
                    brief='Give someone COVID-19.',
                    help='Use this command to help spread COVID-19 to innocent victims.',
                    usage='[user1[, user2[, ...]]]')
    async def cough(self, ctx : commands.Context, *member_ids):
        try:
            members = [ctx.guild.get_member(int(x)) for x in member_ids if x.isdigit()]
            mentions = set(ctx.message.mentions).union(set([member for member in members if member is not None]))
        except:
            await ctx.send(content=f'Error - Invalid ID(s)')
            return
        if len(mentions) > 0:
            for mention in mentions:
                if mention.id == ctx.author.id:
                    await ctx.send(content=f"Please cough outward, not inward, you'll ruin your lungs {ctx.author.mention}.")
                else:
                    await ctx.send(content=f"{mention.mention} got COVID-19 from {ctx.author.mention}.")
                    roles = [x for x in ctx.guild.roles if x.name.lower() == 'corona']
                    if len(roles) == 0:
                        role = await ctx.guild.create_role(name="corona",colour=discord.Colour.from_rgb(68,145,44),hoist=True)
                        for i in range(len(ctx.guild.roles)-1,0,-1):
                            try:
                                await role.edit(position=i)
                                break
                            except:
                                continue
                    else:
                        role = roles[0]
                    await mention.add_roles(role)
        else:
            await ctx.send(content=f"{ctx.author.mention}, please wear a mask!")

    @commands.command(name='cure',
                    brief='A CURE FOR COVID-19 HAS BEEN FOUND!',
                    help='Give someone (or yourself, you selfish bitch) the cure for COVID-19!',
                    usage='[user1[, user2[, ...]]] (no arguments to cure everyone who is sick)')
    async def cure(self, ctx, *member_ids):
        members = [ctx.guild.get_member(int(x)) for x in member_ids if x.isdigit()]
        mentions = set(ctx.message.mentions).union(set(members))
        roles = [x for x in ctx.guild.roles if x.name.lower() == 'corona']
        if len(roles) == 0:
            await ctx.send("Error - no corona found")
        else:
            role = roles[0]
            # await role.delete()
            if len(mentions) == 0:
                if ctx.author.id == self.bot.owner_id or ctx.channel.permissions_for(ctx.author).administrator == True:
                    for user in ctx.guild.members:
                        if role in user.roles:
                            await user.remove_roles(role)
                    await ctx.send(content=f"It's a miracle! Everyone who was sick has been cured!")
                else:
                    await ctx.send(content="You didn't tell me who to cure.")
            else:
                for mention in mentions:
                    if not mention:
                        await ctx.send(content="Error - Invalid ID")
                        continue
                    if role in mention.roles:
                        if mention.id != ctx.author.id or ctx.author.id == self.bot.owner_id:
                            await mention.remove_roles(role)
                            await ctx.send(content=f"It's a miracle! {mention.mention} has been cured!")
                        else:
                            await ctx.send(content=f"Bitch you ain't a god, you can't cure yourself.")
                    elif mention.id == ctx.author.id:
                        await ctx.send(content=f"Don't worry {mention.mention}, you're not sick... yet.")
                    else:
                        await ctx.send(content=f"{mention.mention} doesn't have COVID-19, and you can't cure their stupidity.")

















    @commands.command(name='water',brief='Drink water!')
    async def water(self, ctx):
        await ctx.send(content='Beep bop\nThis is your new favorite bot\nDrink water')

    @commands.command(name='pills',brief='Take your pills!')
    async def pills(self, ctx):
        await ctx.send(content='Beep bop\nThis is your new favorite bot\nTake your pills')
    
    @commands.command(name='enfim',brief='Enfim...')
    async def enfim(self, ctx):
        await ctx.message.reply(content='a hipocrisia',mention_author=False)

    @commands.command(name='spoiler',brief='Shh, it\'s a spoiler!',
                    usage='[string]')
    async def spoiler(self, ctx, *message):
        await ctx.message.delete()
        if message[0].lower() == "copy":
            await ctx.send(content="`{}`".format(''.join(f"||{x}||" for x in ' '.join(message[1:]))))
        else:
            await ctx.send(content=''.join(f"||{x}||" for x in ' '.join(message)))

    @commands.command(name='say')
    async def say(self, ctx, *content):
        await ctx.message.delete()
        s = ' '.join(content).replace("\\n","\n")
        if "<@" in s:
            message_sent = await ctx.send(content=discord.utils.escape_mentions(s))
            await message_sent.edit(content=s)
        else:
            await ctx.send(content=s)

    @commands.command(name='reply')
    async def reply(self, ctx, *content):
        reply_text = list(content)
        await ctx.message.delete()
        if ref := ctx.message.reference:
            message_id = ref.message_id
        else:
            message_id = reply_text.pop(0)
        s = ' '.join(reply_text).replace("\\n","\n")
        msg = await ctx.fetch_message(message_id)
        await msg.reply(content=s)

    @commands.command(name="neopronouns",hidden=True,aliases=['np','neop'])
    async def neopronouns(self, ctx):
        with open("db/words_dictionary.json") as f:
            words = json.load(f)
        word = random.choice(list(words.keys()))
        await ctx.send(content=f"{word}/{word}s/{word}self")

    @commands.command(name='uwu',
                    brief='UwUifies a message or text.',
                    help='Use this command to UwUify a given message or text.',
                    usage='[messageID1|string1[, messageID2|string2[, ...]]] (use with no arguments to UwUify the previously sent message)')
    async def uwu(self, ctx : commands.Context, *args):
        msg : discord.MessageReference = ctx.message.reference
        if msg:
            message = msg.resolved
            uwuified = uwuify(message.content)
            await send_without_mentions(ctx, uwuified)
            return
        if not args:
            messages = await ctx.channel.history(limit=3).flatten()
            uwuified = uwuify(messages[1].content)
            await send_without_mentions(ctx, uwuified)
        else:
            # await ctx.message.delete()
            for arg in args:
                try:
                    message = await ctx.fetch_message(arg)
                    uwuified = uwuify(message.content)
                    await send_without_mentions(ctx, uwuified)
                except:
                    if arg.isdigit():
                        await ctx.send(content="Invalid message ID")
                    else:
                        uwuified = uwuify(' '.join(args))
                        await send_without_mentions(ctx, uwuified)
                        break

    @commands.command(name='react',
                    brief='React to a message.',
                    help='This command can be used to react to the previously sent message using any emoji.',
                    usage='emoji_name1[, emoji_name2[, ...]]')
    async def react(self, ctx, *reactions):
        await ctx.message.delete()
        messages = await ctx.channel.history(limit=2).flatten()
        message = messages[0]
        for reaction in reactions:
            if reaction in self.emojis:
                await message.add_reaction(self.emojis[reaction])
                continue
            if reaction in self.regionals:
                await message.add_reaction(self.regionals[reaction])
                continue
            try:
                await message.add_reaction([emoji for emoji in self.bot.emojis if reaction in emoji.name][0])
            except IndexError:
                await ctx.send(content=f"Error - emoji {reaction} not found")

    @commands.command(name='regional',
                    brief='Send a WIDE message',
                    help='Use this command to send a message using only letter emojis.',
                    usage='text')
    async def regional(self, ctx, *words):
        sentence = ""
        for word in words:
            for letter in word:
                sentence += self.regionals.get(letter.lower(),letter) + ' '
            sentence += '   '
        await ctx.send(content=sentence)

    @commands.command(name='overlay')
    async def overlay(self, ctx, overlayimg=None, url=None):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,}
        if not overlayimg:
            overlay_img = cv2.imread(f"images/floshed.png",cv2.IMREAD_UNCHANGED)
        elif ":" in overlayimg:
            _, emoji_name, emoji_id = overlayimg.strip("<>").split(":",2)
            emoji_obj = self.bot.get_emoji(int(emoji_id))
            if emoji_obj:
                try:
                    #emj = await emoji_obj.url.read()
                    req = Request(emoji_obj.url, None, headers)
                    arr = np.asarray(bytearray(urlopen(req).read()), dtype='uint8')
                    #overlay_img = cv2.imdecode(np.fromstring(emj, np.uint8), cv2.IMREAD_UNCHANGED)
                    overlay_img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                except Exception as e:
                    await ctx.send(content=e)
                    return
            else:
                await ctx.send(content=f"Error - emoji {emoji_name} is not in any of my servers, so I can't use it :(")
                return
        elif overlayimg.isalpha():
            try:
                overlay_img = cv2.imread(f"images/{overlayimg}.png",cv2.IMREAD_UNCHANGED)
            except FileNotFoundError:
                await ctx.send(content=f"Error - image {overlayimg} not found")
                return
        else:
            await ctx.send(content=f"Sorry, I don't support default emojis... yet")
            return
        if url is None:
            attch = ctx.message.attachments
            if len(attch) > 0:
                url = attch[0].url
            else:
                messages = await ctx.channel.history(limit=3).flatten()
                attchx = messages[-2].attachments
                if len(attchx) > 0:
                    url = attchx[0].url
                else:
                    await ctx.send(content="Error - no input image found.")
                    return
        try:
            request = Request(url, None, headers)
            response = urlopen(request)
            img = np.asarray(bytearray(response.read()), dtype='uint8')
            if ".pfdsafdsng" in url:
                img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
            else:
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                b_channel, g_channel, r_channel = cv2.split(img)
                alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.
                img = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                resized = cv2.resize(overlay_img, (w,h))
                alpha_overlay = resized[:,:,3] / 255.0
                alpha_img = 1.0 - alpha_overlay
                for c in range(0,4):
                    img[y:y+h, x:x+w, c] = (alpha_overlay * resized[:,:,c] +
                                            alpha_img * img[y:y+h, x:x+w, c])
            success, buffered = cv2.imencode(".png", img)
            await ctx.send(file=discord.File(BytesIO(buffered),filename="image.png"))
        except Exception as e:
            await ctx.send(content=e)
            return

    @commands.command(name='magicball',
                    brief='Ask the magic 8-ball a question.',
                    help='The magic 8-ball will answer all of your yes-or-no questions, just ask! Use it for seeking advice or for predicting the future!',
                    usage='question')
    async def magicball(self, ctx):
        await ctx.message.reply(content=random.choice(self.answers),mention_author=False)

    @commands.command(name='judge',
                    brief='Judge someone\'s taste in music.',
                    help='Wanna be an asshole? This is the perfect command for you. Just mention someone who is listening to something on Spotify to judge them for it.',
                    usage='@user')
    async def judge(self, ctx : commands.Context, member : discord.Member = None):
        judge_self = False
        if not member:
            member = ctx.author
            judge_self = True
        try:
            spotify = [ x for x in member.activities if type(x) == discord.Spotify][0]
        except IndexError:
            if judge_self:
                await ctx.send("You didn't mention anyone for me to judge.")
            else:
                await ctx.send("That user is not listening to anything on Spotify right now. Try again later.")
            return
        song_name = spotify.title
        song_artists = spotify.artists
        if judge_self:
            await ctx.send("You didn't mention anyone for me to judge, so I'll judge you. 👀")
        await ctx.send(f"Wow {member.mention}, you're *really* listening to **{song_name}** by **{' & '.join(song_artists)}**?! Like, unironically?! 😂")
        
        

async def send_without_mentions(ctx : commands.Context, message : str):
    if "<@" in message:
        message_sent = await ctx.send(content=discord.utils.escape_mentions(message))
        await message_sent.edit(content=message)
    else:
        await ctx.send(content=message)

def uwuify(message : str):
    converter = {'r': 'w', 'l': 'w', 'R': 'W', 'L': 'W', 't': 'd', 'T': 'D'}
    uwuified = ""
    th = False
    for i, char in enumerate(message):
        if th: 
            th = False
            continue
        if char in "rlRL":
            uwuified += converter[char]
        elif char in "tT" and i + 1 < len(message) and message[i+1] in "hH":
            th = True
            uwuified += converter[char]
        else:
            uwuified += char
    return uwuified + " UwU"

async def interaction(ctx, bot, actions):
    mentions = set(ctx.message.mentions).union(set(ctx.message.role_mentions))
    if(len(mentions) > 0):
        if ctx.author in mentions:
            await ctx.send(content=actions["self"].format(ctx.author.mention))
        else:
            for mention in mentions:
                if bot.user.id == mention.id:
                    await ctx.send(content=actions["bot"].format(ctx.author.mention))
                else:
                    await ctx.send(content=actions["default"].format(ctx.author.mention,mention.mention))
    else:
        await ctx.send(content=actions["none"].format(ctx.author.mention))

def setup(bot):
    bot.add_cog(Interact(bot))
