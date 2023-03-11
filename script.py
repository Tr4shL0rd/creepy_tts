"""DOC STRING"""
import requests
from playsound import playsound

voices = {
        "adult female #1": "Adult Female #1",
        "adult female #2": "Adult Female #2",
        "adult male #1": "Adult Male #1",
        "adult male #2": "Adult Male #2",
        "adult male #3": "Adult Male #3",
        "adult male #4": "Adult Male #4",
        "adult male #5": "Adult Male #5",
        "adult male #6": "Adult Male #6",
        "adult male #7": "Adult Male #7",
        "adult male #8": "Adult Male #8",
        "robosoft #1": "RoboSoft One",
        "robosoft #2": "RoboSoft Two",
        "robosoft #3": "RoboSoft Three",
        "robosoft #4": "RoboSoft Four",
        "robosoft #5": "RoboSoft Five",
        "robosoft #6": "RoboSoft Six",
        "female whisper": "Female Whisper",
        "male whisper": "Male Whisper",
        "mary": "Mary",
        "mary (for telephone)": "Mary (for Telephone)",
        "mary in hall": "Mary in Hall",
        "mary in space": "Mary in Space",
        "mary in stadium": "Mary in Stadium",
        "mike": "Mike",
        "mike (for telephone)": "Mike (for Telephone)",
        "mike in hall": "Mike in Hall",
        "mike in space": "Mike in Space",
        "mike in stadium": "Mike in Stadium",
        "sam": "Sam",
    }
def list_voices() -> None:
    """
    Lists all available voices
    """

    for voice in voices:
        print(voice)


def get_sound_bite(string:str, voice:str) -> str:
    """
    returns tts sound
    """

    if len(STRING) > 4088:
        print("Text too long")
    voice_limit = f"https://www.tetyys.com/SAPI4/VoiceLimitations?voice={voice}"
    print("getting voice data")
    voice_conf_dict = requests.get(voice_limit, timeout=1).json()

    print("receiving tts sound clip")
    url = f"https://www.tetyys.com/SAPI4/SAPI4?text={string}&voice={voice}&pitch={voice_conf_dict['defPitch']}&speed={voice_conf_dict['defSpeed']}"
    r = requests.get(url, timeout=2)

    cont = r.content
    with open("data.wav", "wb") as f:
        print("Saving data")
        f.write(cont)
    return f.name

VOICE = voices.get("sam", None)
STRING = "never gonna give you up"
tts_sound_path = get_sound_bite(STRING,VOICE)
playsound(tts_sound_path)
