import csv
import string
import difflib

# ================== WORD CORRECTION ==================
def correct_word(word, vocab):
    matches = difflib.get_close_matches(word, vocab, n=1, cutoff=0.8)
    return matches[0] if matches else word


def load_data():
    data = []
    try:
        with open("q.csv", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("Error: q.csv file not found!")
    return data


# ================== NORMALIZATION & AUTO-CORRECT ==================
def normalize(word):
    word = word.lower().strip()
    synonyms = {
        "gravitation": "gravity",
        "gravitational": "gravity",
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
        "loss": "loss",
        "photosynthesis": "photosynthesis",
        "mass": "mass",
        "weight": "weight",
    }
    return synonyms.get(word, word)


def auto_correct(sentence, vocab):
    words = sentence.lower().split()
    corrected = [correct_word(w, vocab) for w in words]
    return " ".join(corrected)


def text_to_words(text):
    stopwords = {"what", "is", "the", "a", "an", "explain", "define", "tell", "me", "about"}
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    filtered = [normalize(word) for word in words if word not in stopwords]
    return set(filtered)


def build_vocab(data):
    vocab = set()
    for item in data:
        if "question" in item:
            words = item["question"].lower().split()
            for w in words:
                vocab.add(w)
    return vocab


# ================== SIMILARITY ==================
def similarity(q1, q2):
    words1 = text_to_words(q1)
    words2 = text_to_words(q2)
    
    common = words1.intersection(words2)
    score = len(common) * 2  # Give more weight to common words
    
    # Fuzzy matching for similar words
    for w1 in words1:
        for w2 in words2:
            if len(w1) > 3 and len(w2) > 3:
                ratio = difflib.SequenceMatcher(None, w1, w2).ratio()
                if ratio > 0.8:
                    score += 1.5
    
    # Exact phrase bonus
    if q1.lower() in q2.lower() or q2.lower() in q1.lower():
        score += 3
    
    return score


# ================== GET BEST ANSWER ==================
def get_best_answer(user_question, data, answer_type="short", subject="science"):
    best_score = 0
    best_item = None
    best_question = ""

    for item in data:
        # Subject filter
        if "subject" in item and item["subject"].strip().lower() != subject:
            continue
            
        score = similarity(user_question, item["question"])
        
        if score > best_score:
            best_score = score
            best_item = item
            best_question = item["question"]

    if best_item is None:
        return "I couldn’t find any relevant answer in the database 😅", ""

    # Select answer based on type
    if answer_type == "short":
        raw_short = best_item.get("short", best_item.get("answer", ""))
        
        # Improve very short answers by using part of long answer
        if len(raw_short.split()) < 8 and "long" in best_item:
            long_text = best_item["long"]
            sentences = [s.strip() for s in long_text.split('.') if s.strip()]
            if sentences:
                best_answer = '. '.join(sentences[:2]) + '.'
            else:
                best_answer = raw_short
        else:
            best_answer = raw_short
    else:
        best_answer = best_item.get("long", best_item.get("answer", "No detailed answer available."))

    # Low confidence message
    if best_score < 2:
        return f"Closest match found:\n\n{best_answer}", best_question

    return best_answer, best_question
