import re
# \u064E\u064F\u0650 Damma Fatha Kasra
short_to_long_vowel_dict = {"\u064E": "و", "\u064F": "أ", "\u0650": "ي"}

arabic_consonants = "ب ت ث ج ح د ذ ر ز س ش غ ف ق ك ل م ن ه".split()
arabic_vowels = "ا أ و ي ى".split()
arabic_short_vowels = "\u064E \u064F \u0650".split()

# Use the mapping proposed in the paper
phonemes = "AO0 UH0 UW0 OY0 OW0 UW1 OY1 B P NG F V AA0 AE0 AH0 EH0 EH2 AY0 EY0 AW0 IH0 T CH G R K L M HH W N Y PH UX ZH D JH DH ER0 ER2 Z S SH IY0 IX TH".split()
arabic_equivalent = "ُو ُو ُو ُو ُو ُو وي ب ب غ ف ف َا َا َا َا َا َي َي َو ِي ت تش ق ر ك ل م ه و ن ي ف ُو ج د دج ذ ر ر ز س ش ِي ِي ث".split()
transliteration_map = {p:a for p, a in zip(phonemes, arabic_equivalent)}

def common_prefix(p1, p2):
    return sum([c1==c2 for c1, c2 in zip(p1, p2)])

def find_equivalent_character(phoneme):
    available_phonemes = sorted(transliteration_map.keys())
    matching_prefix_chars = [common_prefix(phoneme, trans_phoneme) for trans_phoneme in available_phonemes]
    max_idx = max(range(len(matching_prefix_chars)), key=lambda i: matching_prefix_chars[i])
    return transliteration_map[available_phonemes[max_idx]]

def transphonate_english_word(name):
    base_name = "".join([find_equivalent_character(p) for p in name])
    # Rule 1
    base_name = re.sub("^[\u064E\u064F]", "أ", base_name)
    base_name = re.sub("^[\u0650]", "إ", base_name)
    # Rule 2
    base_name = re.sub("[\u064E]$", "و", base_name)
    base_name = re.sub("[\u064F]$", "ا", base_name)
    base_name = re.sub("[\u0650]$", "ي", base_name)

    # Rule 3 - needs testing
    groups = re.search(f"^([{arabic_vowels}][{arabic_consonants}])([{arabic_short_vowels}])", base_name)
    if groups:
        base_name = groups(1) + short_to_long_vowel_dict[groups(2)] + base_name[3:]

    # Rule 4 - needs testing
    groups = re.search(f"^([{arabic_vowels}]?[{arabic_consonants}]+)([{arabic_short_vowels}])", base_name)
    while groups:
        base_name = groups(1) + short_to_long_vowel_dict[groups(2)] + base_name[len(groups(1)+len(groups(2))):]
        groups = re.search(f"^([{arabic_vowels}]?[{arabic_consonants}]+)([{arabic_short_vowels}])", base_name)
    # Rule 5
    groups = re.search(f"^([{arabic_vowels}]?[{arabic_consonants}]+)نق$", base_name)
    if groups:
        base_name = groups(1) + "نغ"

    # Rule 6
    groups = re.search(f"^([{arabic_vowels}]?)نق[{arabic_consonants}]", base_name)
    if groups:
        base_name = groups(1) + "ن" + base_name[len(groups(1))+2:]
    return base_name

