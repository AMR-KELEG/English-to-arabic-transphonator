# Transphonate English words to Arabic
- This repository implements the set of rules mentioned in [Translating English Names to Arabic Using Phonotactic Rules by F Alshuwaier et al., 2011](https://www.aclweb.org/anthology/Y11-1051.pdf) 

## Main idea
- It's not easy to transliterate English words to Arabic using handwritten rules since most of the words aren't pronunced in a specific way and thus having a set of 1-1 rules for transliterating is really hard.
- The Carnegie Mellon University is maintaining a dictionary mapping English words to the way they are pronunced (Using the [`ARPAbet`](https://en.wikipedia.org/wiki/ARPABET) symbol set which is somehow related to [`IPA`](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet).
	- "The Carnegie Mellon University Pronouncing Dictionary is an open-source machine-readable pronunciation dictionary for North American English that contains over 134,000 words and their pronunciations. CMUdict is being actively maintained and expanded. We are open to suggestions, corrections and other input."
	- For more details, check the [dictionary's webpage](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)

## Usage
- Download the CMU dictionary by using:
`pip install english_to_arabic_transphonator`

- Use a `Transphonator` object
```
from english_to_arabic_transphonator.transphonator import Transphonator

words = "This is awesome".split()
trans = Transphonator()
for word in words:
    print(word, trans.transphonate_english_word(word))
```

The output for the sentence `This is awesome` is:
```
this ذِيس
is إيز
awesome أوسَام
```

