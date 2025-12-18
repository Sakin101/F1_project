
import re
_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
from config import KEYWORD_MAP, MOTORSPORT_CLASSIFICATION_PROMPT
from utils.llm_call import call_llm
#TODO: Understand N-grams and how to generate them.
def classify_with_llm(title):
    prompt=MOTORSPORT_CLASSIFICATION_PROMPT.format(title=title)
    classification=call_llm(prompt=prompt)
    breakpoint()
    return classification
def tokenize(text):
    return _TOKEN_PATTERN.findall(text.lower())
def generate_ngrams(tokens,n):
    #breakpoint()
    return {
        " ".join(tokens[i:i+n])
        for i in range(len(tokens)-n+1)
    }
def compare(title,phrase):
    title_tokens=tokenize(title)
    phrase_tokens=tokenize(phrase)
    return " ".join(phrase_tokens) in " ".join(title_tokens)

def rule_based_motorsports_classification(
    title:str,
    min_score:int=1,
    dominance_ratio:float=1.5
):
    category_score={}
    for key,value in KEYWORD_MAP.items():
        score=0
        for phrase in value:
            if compare(title,phrase):
                score+=1
        category_score[key]=score
    best_category, best_score=max(category_score.items(),key=lambda x:x[1])
    sorted_score=sorted(category_score.values(),reverse=True)
    if len(sorted_score)>1 and sorted_score[0]<sorted_score[1]*dominance_ratio:
        return None
    return best_category
    
def classify_motorsport(title:str)->str:
    category=rule_based_motorsports_classification(title)
    if category is not None:
        return category
    else:
        return classify_with_llm(title)
if __name__=="__main__":
    titles = [
        "Ben Sulayem wins second term as FIA president formula e",
        "Every 2025 F1 driver ranked from worst to best",
        "Aprilia's aero supremacy survived a key test",
        "Why Porsche and its first Formula E customer are splitting up",
        "What we know as Alpine's 2026 Hypercar breaks cover",
        "F1 Esports championship announces new format",
    ]

    for t in titles:
        print(f"{t}  -->  {classify_motorsport(t)}")