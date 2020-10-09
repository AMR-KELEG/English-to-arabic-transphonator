import re


class Transphonator:
    def __init__(self):
        # \u064E\u064F\u0650 Damma Fatha Kasra
        self.short_to_long_vowel_dict = {"\u064E": "و", "\u064F": "أ", "\u0650": "ي"}

        self.arabic_consonants = "ب ت ث ج ح د ذ ر ز س ش غ ف ق ك ل م ن ه".split()
        self.arabic_vowels = "ا أ و ي ى".split()
        self.arabic_short_vowels = "\u064E \u064F \u0650".split()

        # Use the mapping proposed in the paper
        self.phonemes = "AO0 UH0 UW0 OY0 OW0 UW1 OY1 B P NG F V AA0 AE0 AH0 EH0 EH2 AY0 EY0 AW0 IH0 T CH G R K L M HH W N Y PH UX ZH D JH DH ER0 ER2 Z S SH IY0 IX TH".split()
        self.arabic_equivalent = "ُو ُو ُو ُو ُو ُو وي ب ب غ ف ف َا َا َا َا َا َي َي َو ِي ت تش ق ر ك ل م ه و ن ي ف ُو ج د دج ذ ر ر ز س ش ِي ِي ث".split()
        self.transliteration_map = {
            p: a for p, a in zip(self.phonemes, self.arabic_equivalent)
        }

        # TODO: Make sure the file is there before loading it
        with open("data/cmudict", "r", encoding="ISO-8859-1") as f:
            lines = [l.strip() for l in f.readlines()]
            words = [l.split()[0] for l in lines]
            phonemes = [l.split()[1:] for l in lines]
        self.english_word_to_phoneme = {w.lower():p for w, p in zip(words, phonemes)}

    def _common_prefix(self, p1, p2):
        return sum([c1 == c2 for c1, c2 in zip(p1, p2)])

    def _find_equivalent_character(self, phoneme):
        available_phonemes = sorted(self.transliteration_map.keys())
        matching_prefix_chars = [
            self._common_prefix(phoneme, trans_phoneme)
            for trans_phoneme in available_phonemes
        ]
        max_idx = max(
            range(len(matching_prefix_chars)), key=lambda i: matching_prefix_chars[i]
        )
        return self.transliteration_map[available_phonemes[max_idx]]

    def transphonate_english_word(self, english_word):
        english_word = english_word.lower()
        if english_word in self.english_word_to_phoneme:
            english_word_phonemes = self.english_word_to_phoneme[english_word]
            return self.transphonate_english_phonemes(english_word_phonemes)
        else:
            # TODO: Use logging messages
            print('Not found')

    def transphonate_english_phonemes(self, english_word_phonemes):
        arabic_translphonated_word = "".join(
            [self._find_equivalent_character(p) for p in english_word_phonemes]
        )

        # Rule 1
        arabic_translphonated_word = re.sub(
            "^[\u064E\u064F]", "أ", arabic_translphonated_word
        )
        arabic_translphonated_word = re.sub(
            "^[\u0650]", "إ", arabic_translphonated_word
        )
        # Rule 2
        arabic_translphonated_word = re.sub(
            "[\u064E]$", "و", arabic_translphonated_word
        )
        arabic_translphonated_word = re.sub(
            "[\u064F]$", "ا", arabic_translphonated_word
        )
        arabic_translphonated_word = re.sub(
            "[\u0650]$", "ي", arabic_translphonated_word
        )

        # Rule 3 - needs testing
        groups = re.search(
            f"^([{self.arabic_vowels}][{self.arabic_consonants}])([{self.arabic_short_vowels}])",
            arabic_translphonated_word,
        )
        if groups:
            arabic_translphonated_word = (
                groups(1)
                + self.short_to_long_vowel_dict[groups(2)]
                + arabic_translphonated_word[3:]
            )

        # Rule 4 - needs testing
        groups = re.search(
            f"^([{self.arabic_vowels}]?[{self.arabic_consonants}]+)([{self.arabic_short_vowels}])",
            arabic_translphonated_word,
        )
        while groups:
            arabic_translphonated_word = (
                groups(1)
                + self.short_to_long_vowel_dict[groups(2)]
                + arabic_translphonated_word[len(groups(1) + len(groups(2))) :]
            )
            groups = re.search(
                f"^([{self.arabic_vowels}]?[{self.arabic_consonants}]+)([{self.arabic_short_vowels}])",
                arabic_translphonated_word,
            )

        # Rule 5
        groups = re.search(
            f"^([{self.arabic_vowels}]?[{self.arabic_consonants}]+)نق$",
            arabic_translphonated_word,
        )
        if groups:
            arabic_translphonated_word = groups(1) + "نغ"

        # Rule 6
        groups = re.search(
            f"^([{self.arabic_vowels}]?)نق[{self.arabic_consonants}]",
            arabic_translphonated_word,
        )
        if groups:
            arabic_translphonated_word = (
                groups(1) + "ن" + arabic_translphonated_word[len(groups(1)) + 2 :]
            )

        return arabic_translphonated_word

if __name__ == "__main__":
    words = input().split()
    trans = Transphonator()
    for word in words:
        print(word, trans.transphonate_english_word(word))