"""DOC STRING"""
import argparse
import time
import hashlib
import requests
from playsound import playsound
from bs4 import BeautifulSoup as bs
from rich import print
from persistent_cache import PersistentCache

s_time = time.time()
cache = PersistentCache(cache_dir="cache")
DEFAULT_TIMEOUT = 5

parser = argparse.ArgumentParser(epilog="Made by Tr4shL0rd")
parser.add_argument(
                    dest="tts_string",
                    help="text for tts",
                    default="Never Gonna Give You Up!"
                    )
parser.add_argument(
                    "--voice",
                    dest="tts_voice",
                    help="voice for tts",
                    action="store",
                    default="Sam",
                    )
parser.add_argument(
                    "--no-voice",
                    dest="tts_no_voice",
                    help="silences tts voice",
                    action="store_true",
                    default=False,
                    )
args = parser.parse_args()


def number_name_to_number(string:str) -> str:
    """dsa"""
    numbers = {
        "one": "1",
        "two":"2",
        "three":"3",
        "four":"4",
        "five":"5",
        "six":"6",
    }
    return f"RoboSoft {numbers[string.split(' ')[-1].lower()]}"

def get_voices() -> dict:
    """dwas"""
    cache_key = "voices"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    else:

        _voices = {}
        nl_char = "\n"
        url = "https://www.tetyys.com/SAPI4/"
        page = requests.get(url, timeout=DEFAULT_TIMEOUT)
        soup = bs(page.content, "html.parser")
        voice_options = soup.select_one("html body div.content div.generator div.options div.voice select#voice")
        for names in voice_options.children:
            name = names.text.replace(nl_char, '')
            if len(name) != 0:
                #print(name)
                if "RoboSoft" in name:
                    name = number_name_to_number(name)
                _voices[name.lower().split(",")[0]] = name
        cache.set(cache_key,_voices)
        return _voices

def list_voices() -> None:
    """
    Lists all available voices
    """
    all_voices = get_voices()
    for _v in all_voices:
        print(_v)

def get_voice_conf(voice:str) -> dict:
    """returns voice configs"""
    cache_key = f"voice_conf_{voice}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    else:
        voice_limit = f"https://www.tetyys.com/SAPI4/VoiceLimitations?voice={voice}"
        data = requests.get(voice_limit, timeout=DEFAULT_TIMEOUT).json()
        cache.set(cache_key,data)
        return data

def get_sound_bite(string:str, voice:str, pitch:int, speed:int):
    """
    DWAS
    """
    hashed_string = hashlib.md5(string.encode()).hexdigest()
    cache_key = f"tts_{hashed_string}_{voice}_{pitch}_{speed}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    else:
        url = f"https://www.tetyys.com/SAPI4/SAPI4?text={string}&voice={voice}&pitch={pitch}&speed={speed}"
        data = requests.get(url, timeout=DEFAULT_TIMEOUT)
        cache.set(cache_key, data.content)
        return data.content



def main(string:str, voice:str) -> str:
    """
    returns tts sound
    """
    #exit()
    if len(string) > 4088:
        print("Text too long")
    print("getting voice data")

    voice_conf = get_voice_conf(voice)
    print("receiving tts sound clip")
    cont = get_sound_bite(string, voice, voice_conf['defPitch'],voice_conf['defSpeed'])

    with open("data.wav", "wb") as f:
        print("Saving data")
        f.write(cont)
    return f.name

if __name__ == "__main__":
    voices = get_voices()
    selected_voice = args.tts_voice
    if args.tts_voice not in voices:
        print("voice not found")
    else:
        selected_voice = voices[args.tts_voice]

    tts_sound_path = main(string=args.tts_string, voice=selected_voice)
    print(time.time() - s_time)
    if not args.tts_no_voice:
        playsound(tts_sound_path)
    cache.clean_up()
