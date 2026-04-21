import csv

def load_data():
    data = []
    with open("q.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


import string

def text_to_words(text):
    stopwords = {"what", "is", "the", "a", "an", "explain", "define", "tell", "me"}
    
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    
    words = text.split()
    filtered = [normalize(word) for word in words if word not in stopwords]
    
    return set(filtered)


ddef similarity(q1, q2):
    words1 = text_to_words(q1)
    words2 = text_to_words(q2)

    common = words1.intersection(words2)

    return len(common) / (len(words1) + len(words2) + 1)


def get_best_answer(user_question, data):
    best_score = 0
    best_answer = "I’m not sure 🤔 Try asking in a different way."

    for item in data:
        score = similarity(user_question, item["question"])

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score < 0.2:
        return "I’m not sure 🤔 Try asking in a different way."

    return best_answer

    return best_answer
def normalize(word):
    if word.startswith("gravit"):
        return "gravity"
    return word
