# ml_sentiment_tf.py

from transformers import pipeline


try:
    classifier = pipeline(
        "sentiment-analysis",
        model="savasy/bert-base-turkish-sentiment-cased",
        framework="tf"   
    )
    ML_AVAILABLE = True
except Exception as e:
    print("ML modeli yüklenemedi, sadece rule-based çalışacak:", e)
    ML_AVAILABLE = False

# 🔹 Rule-based fallback (her zaman çalışır)
positive_words = ["mutlu", "iyi", "harika", "rahatladım", "güzel", "keyifli"]
negative_words = ["üzgün", "kötü", "stresli", "yorgun", "sinirli"]

contrast_words = [
    "ama", "fakat", "ancak", "sonra", "daha sonra",
    "başta", "ilk başta", "önce", "sonunda"
]

def analyze_rule_based(text: str):
    text = text.lower()
    words = text.split()
    
    # "ama" veya benzeri bağlaçlardan sonra ağırlık ver
    for cw in contrast_words:
        if cw in words:
            index = words.index(cw)
            words = words[index+1:]
            break
    
    mid = len(words) // 2
    first_half = words[:mid]
    second_half = words[mid:]
    
    pos = 0
    neg = 0
    
    # İlk yarı normal
    for w in first_half:
        if w in positive_words:
            pos += 1
        if w in negative_words:
            neg += 1
            
    # İkinci yarı 1.5x ağırlık
    for w in second_half:
        if w in positive_words:
            pos += 1.5
        if w in negative_words:
            neg += 1.5
            
    total = pos + neg
    if total == 0:
        return {"positive": 0, "negative": 0, "neutral": 100}
    
    positive_percent = int((pos / total) * 100)
    negative_percent = int((neg / total) * 100)
    neutral_percent = 100 - positive_percent - negative_percent
    
    return {"positive": positive_percent, "negative": negative_percent, "neutral": neutral_percent}

# 🔹 Tavsiye Fonksiyonu
def generate_advice(result: dict):
    if result["negative"] > 60:
        return "Bugun biraz zorlanmiş görünüyorsun. Kendine zaman ayirmak iyi olabilir."
    elif result["positive"] > 70:
        return "Harika bir ruh halindesin! Bu enerjini korumaya çaliş."
    else:
        return "Dengeli bir gün geçirmiş gibisin."

# 🔹 Tek Fonksiyon: ML veya Rule-based otomatik seçer
def analyze_and_advise(text: str):
    if ML_AVAILABLE:
        ml_result = classifier(text)[0]  # [{'label': 'POSITIVE', 'score': 0.95}]
        label = ml_result['label']
        score = ml_result['score']
        if label.upper() == "POSITIVE":
            sentiment = {"positive": int(score*100), "negative": int((1-score)*100), "neutral": 0}
        elif label.upper() == "NEGATIVE":
            sentiment = {"positive": int((1-score)*100), "negative": int(score*100), "neutral": 0}
        else:
            sentiment = {"positive": 0, "negative": 0, "neutral": 100}
    else:
        sentiment = analyze_rule_based(text)
        
    advice = generate_advice(sentiment)
    return {"sentiment": sentiment, "advice": advice}

# 🔹 Test
if __name__ == "__main__":
    text =text =text = """Bugun sabah erken saatlerde uyandim ve pencerenin onunde biraz zaman gectirdim.
Gunes yeni yeni doguyor, hafif bir serinlik ve kus civiltilari esliginde odama doluyordu.
Kahvaltimi yaparken kahvemin kokusu butun evi sardi ve o an kucuk seylerin ne kadar huzur verdigini fark ettim.
Ardindan bilgisayarimi actim ve gunun planini goze kaydettim; biraz calismam, biraz kitap okumam ve kisa bir yuruyus yapmam gerektigini not ettim."""
    result = analyze_and_advise(text)
    print(result)