import csv
import os
import difflib

def save_log(question, corrected, answer, feedback=""):
    with open("user_logs.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([question, corrected, answer, feedback])

def build_vocab(data):
    vocab = set()
    for item in data:
        words = item["question"].lower().split()
        vocab.update(words)
    return vocab

def correct_word(word, vocab):
    matches = difflib.get_close_matches(word, vocab, n=1, cutoff=0.8)
    return matches[0] if matches else word

def auto_correct(sentence, vocab):
    words = sentence.lower().split()
    return " ".join(correct_word(w, vocab) for w in words)
