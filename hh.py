import csv
import string

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
    return word

def text_to_words(text):
    stopwords = {"what", "is", "the", "a", "an", "explain", "define", "tell", "me"}
    
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    words = text.split()
    filtered = [normalize(word) for word in words if word not in stopwords]
    
    return set(filtered)

def similarity(q1, q2):
    words1 = text_to_words(q1)
    words2 = text_to_words(q2)

    common = words1.intersection(words2)

    if not words1:
        return 0

    return len(common) / len(words1)

def get_best_answer(user_question, data, answer_type="short"):
    best_score = 0
    best_answer = "I’m not sure 🤔 Try asking in a different way."

    for item in data:
        # 🔥 skip if type doesn't match
        if "type" in item and item["type"] != answer_type:
            continue

        score = similarity(user_question, item["question"])

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score < 0.1:
        return "I’m not sure 🤔 Try asking in a different way."

    return best_answer
