def analiz_text(text):

    text=text.lower()

    positive_words = ["mutlu", "iyi", "harika"]
    negative_words = ["üzgün", "kötü", "stresli"]

    pos = 0
    neg = 0

    for word in positive_words:
        if word in text:
            pos += 1

    for word in positive_words:
        if word in text:
            pos += 1

   
    total = pos + neg
    
    if total == 0:
        return  {
            "positive": 0,
            "negative": 0,
            "neutral": 100
        }
    
    pozitif_yuzde=int((pos/total)*100)
    negatif_yuzde=int((neg/total)*100)
    notr_yuzde = 100 - pozitif_yuzde - negatif_yuzde

    return {
        "positive":pozitif_yuzde,
        "negative":negatif_yuzde,
        "neatural":notr_yuzde
    }

def generate_advice(result):

    if result["negative"] > 60:
        return "Bugün biraz zorlanmış görünüyorsun."

    elif result["positive"] > 70:
        return "Harika bir gün geçirmişsin!"

    else:
        return "Dengeli bir gün gibi görünüyor."


result = analiz_text("Seni cok seviyorum")
advice = generate_advice(result)

print(result)
print("Tavsiye:", advice)
       
   