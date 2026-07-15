import csv
import string
import difflib

def load_data():
    data = []
    try:
        with open("q.csv", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except Exception as e:
        print("Error loading q.csv:", e)
    return data

def build_vocab(data):
    vocab = set()
    for item in data:
        if "question" in item:
            for word in item["question"].lower().split():
                vocab.add(word)
    return vocab

def auto_correct(sentence, vocab):
    words = sentence.lower().split()
    corrected = []
    for w in words:
        matches = difflib.get_close_matches(w, vocab, n=1, cutoff=0.7)
        corrected.append(matches[0] if matches else w)
    return " ".join(corrected)

def get_best_answer(user_question, data, answer_type="short", subject="science"):
    best_score = -1
    best_item = None
    best_matched = ""

    user_q_clean = user_question.lower().strip()

    for item in data:
        if "subject" in item and item["subject"].strip().lower() != subject:
            continue
            
        q_text = item.get("question", "").lower()
        score = 0
        
        # Better similarity
        if user_q_clean in q_text or q_text in user_q_clean:
            score += 10
        score += len(set(user_q_clean.split()) & set(q_text.split())) * 2
        
        if score > best_score:
            best_score = score
            best_item = item
            best_matched = item.get("question", "")

    if best_item is None or best_score < 1:
        return "Sorry, I couldn't find a matching answer. Try rephrasing your question.", "No match"

    # Get answer
    if answer_type == "short":
        answer = best_item.get("short", best_item.get("answer", "No answer available"))
    else:
        answer = best_item.get("long", best_item.get("answer", "No detailed answer available"))

    return answer, best_matched
