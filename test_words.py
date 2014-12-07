""" 
Unit tests for words
"""

import unittest
from words import *

class WordTest(unittest.TestCase):
    # Unit tests for words
    def test_get_words(self):
        s = "a, b, c"
        w = get_words(s)
        self.assertEqual(len(w), 3)
        self.assertTrue("a" in w)
        self.assertTrue("b" in w)
        self.assertTrue("c" in w)

    def test_random_pick(self):
        s = set(["a", "b", "c", "d"])
        c = random_pick(s, 2)
        
        self.assertEqual(len(c), 2)
        for a in c:
            self.assertTrue(a in s)

    def test_save_load(self):
        w = Words()
        w.words = "a b c d"
        c = w.save()
        l = Words.load(c)
        self.assertEqual(l.words, "a b c d")
        
    def test_save_load_with_notes(self):
        w = Words()
        w.words = "a b c d"
        w.notes = "notes"
        c = w.save()
        l = Words.load(c)
        self.assertEqual(l.words, "a b c d")
        self.assertEqual(l.notes, "notes")

if __name__ == "__main__":
    unittest.main()
