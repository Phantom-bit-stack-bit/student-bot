import csv
import string
import difflib
def correct_word(word, vocab):
    matches = difflib.get_close_matches(word, vocab, n=1, cutoff=0.8)
    return matches[0] if matches else word
def load_data():
    data = []
    with open("q.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def normalize(word):
    if word.startswith("gravit"):
        return "gravity"
    if word.startswith("weigh"):
        return "weight"
    if word.startswith("dens"):
        return "density"
    if word.startswith("mass"):
        return "mass"
    if word.startswith("grav"):
        return "gravity"
    if word.startswith("ener"):
        return "energy"
    if word.startswith("velo"):
        return "velocity"
    return word
def auto_correct(sentence, vocab):
    words = sentence.lower().split()
    corrected = [correct_word(w, vocab) for w in words]
    return " ".join(corrected)
def normalize(word):
    word = word.lower()

    synonyms = {
        "gravitation": "gravity",
        "force": "force",
        "push": "force",
        "pull": "force",
        "purchase": "buy",
        "buying": "buy",
        "sale": "sell",
        "selling": "sell",
        "income": "revenue",
        "earning": "revenue",
        "profit": "profit",
        "gain": "profit",
        "loss": "loss"
    }

    return synonyms.get(word, word)
def text_to_words(text):
    stopwords = {"what", "is", "the", "a", "an", "explain", "define", "tell", "me"}

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    words = text.split()
    filtered = [normalize(word) for word in words if word not in stopwords]
    
    return set(filtered)
def build_vocab(data):
    vocab = set()

    for item in data:
        words = item["question"].lower().split()
        for w in words:
            vocab.add(w)

    return vocab
def similarity(q1, q2):
    words1 = text_to_words(q1)
    words2 = text_to_words(q2)

    common = words1.intersection(words2)
    score = len(common)

    # 🔥 NEW: fuzzy matching for typos
    for w1 in words1:
        for w2 in words2:
            if len(w1) > 3 and len(w2) > 3:
                ratio = difflib.SequenceMatcher(None, w1, w2).ratio()
                if ratio > 0.8:   # similar words
                    score += 0.5

    # existing boosts
    if any(word in q2.lower() for word in words1):
        score += 1

    if q1.lower() in q2.lower():
        score += 2

    return score
def get_best_answer(user_question, data, answer_type="short", subject="science"):
    best_score = 0
    best_answer = None
    best_question = ""

    for item in data:
        if "subject" in item and item["subject"].strip().lower() != subject:
            continue

        if "type" in item and item["type"] != answer_type:
            continue

        score = similarity(user_question, item["question"])

        if score > best_score:
            best_score = score
            best_answer = item["answer"]
            best_question = item["question"]

    if best_answer is None:
        return "I couldn’t find any relevant answer 😅", ""

    if best_score < 0.1:
        return f"I couldn't find exact match, but here's closest answer:\n\n{best_answer}", best_question

    return best_answer, best_question
