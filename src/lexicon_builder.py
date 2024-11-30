class LexiconBuilder:
    def __init__(self):
        self.lexicon = {}
        self.word_id = 1  # Starting word ID

    def build_lexicon(self, words):
        """Build the lexicon and return updated lexicon with word IDs"""
        for word in words:
            if word not in self.lexicon:
                self.lexicon[word] = self.word_id
                self.word_id += 1
        return self.lexicon
