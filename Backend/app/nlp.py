import re
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "Dataset" / "goal_dataset.csv"


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv(DATA_PATH)

df = df.dropna(
    subset=["text", "goal", "category"]
)

df["text"] = df["text"].astype(str)
df["goal"] = df["goal"].astype(str)
df["category"] = df["category"].astype(str)


# =========================================================
# TF-IDF VECTORIZER
# =========================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X = vectorizer.fit_transform(df["text"])


# =========================================================
# GOAL MODEL
# =========================================================

goal_model = LogisticRegression(
    max_iter=2000
)

goal_model.fit(
    X,
    df["goal"]
)


# =========================================================
# CATEGORY MODEL
# =========================================================

category_model = LogisticRegression(
    max_iter=2000
)

category_model.fit(
    X,
    df["category"]
)


# =========================================================
# GOAL KEYWORDS
# =========================================================

GOAL_KEYWORDS = {

    # Electronics
    "laptop": ("Laptop", "Electronics"),
    "computer": ("Laptop", "Electronics"),
    "phone": ("Mobile Phone", "Electronics"),
    "mobile": ("Mobile Phone", "Electronics"),
    "smartphone": ("Mobile Phone", "Electronics"),

    # Housing
    "house": ("House Purchase", "Housing"),
    "home": ("House Purchase", "Housing"),
    "renovation": ("House Renovation", "Housing"),
    "renovate": ("House Renovation", "Housing"),
    "furniture": ("Furniture", "Housing"),

    # Vehicle
    "car": ("Car", "Vehicle"),
    "bike": ("Bike", "Vehicle"),
    "scooter": ("Bike", "Vehicle"),
    "vehicle": ("Vehicle", "Vehicle"),

    # Education
    "education": ("Higher Education", "Education"),
    "college": ("Higher Education", "Education"),
    "studies": ("Higher Education", "Education"),
    "study": ("Higher Education", "Education"),
    "school": ("School Fees", "Education"),
    "course": ("Education Course", "Education"),

    # Medical
    "medical": ("Medical Fund", "Medical"),
    "hospital": ("Medical Fund", "Medical"),
    "health": ("Medical Fund", "Medical"),
    "treatment": ("Medical Fund", "Medical"),

    # Travel
    "travel": ("Family Travel", "Travel"),
    "trip": ("Family Travel", "Travel"),
    "vacation": ("Family Travel", "Travel"),
    "holiday": ("Family Travel", "Travel"),

    # Marriage
    "marriage": ("Marriage", "Marriage"),
    "wedding": ("Marriage", "Marriage"),

    # Emergency
    "emergency": ("Emergency Fund", "Emergency"),

    # Business
    "business": ("Business", "Business"),
    "startup": ("Business", "Business"),
    "shop": ("Business", "Business")
}


# =========================================================
# NUMBER WORDS
# =========================================================

NUMBER_WORDS = {

    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,

    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20
}


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    text = str(text).strip().lower()

    text = text.replace(",", "")

    return text


# =========================================================
# EXTRACT AMOUNT
# =========================================================

def extract_amount(text):

    text = str(text).lower().strip()

    # Remove commas for easier matching
    text = text.replace(",", "")

    # -----------------------------------------
    # ₹80000 / 80000 / ₹ 80000
    # -----------------------------------------

    match = re.search(
        r"₹\s*(\d+(?:\.\d+)?)",
        text
    )

    if match:
        return int(float(match.group(1)))

    # -----------------------------------------
    # 80000 rupees
    # -----------------------------------------

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:rupees|rs)",
        text
    )

    if match:
        return int(float(match.group(1)))

    # -----------------------------------------
    # 3 lakh / 3 lakhs
    # -----------------------------------------

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)",
        text
    )

    if match:
        return int(float(match.group(1)) * 100000)

    # -----------------------------------------
    # 2 crore / 2 crores
    # -----------------------------------------

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:crore|crores)",
        text
    )

    if match:
        return int(float(match.group(1)) * 10000000)

    # -----------------------------------------
    # Plain large number
    # -----------------------------------------

    numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        text
    )

    for value in numbers:

        number = float(value)

        if number >= 1000:
            return int(number)

    # -----------------------------------------
    # Word-based lakh
    # -----------------------------------------

    for word, number in NUMBER_WORDS.items():

        if re.search(
            rf"\b{word}\s+(?:lakh|lakhs|lac|lacs)\b",
            text
        ):
            return number * 100000

    return None

# =========================================================
# EXTRACT DURATION
# =========================================================

def extract_duration(text):

    text = str(text).lower().strip()

    # -----------------------------------------
    # 1 year / 2 years
    # -----------------------------------------

    match = re.search(
        r"\b(\d+)\s*(?:year|years|yr|yrs)\b",
        text
    )

    if match:
        return int(match.group(1)) * 12

    # -----------------------------------------
    # 12 months / 24 months
    # -----------------------------------------

    match = re.search(
        r"\b(\d+)\s*(?:month|months|mo|mos)\b",
        text
    )

    if match:
        return int(match.group(1))

    # -----------------------------------------
    # Word-based years
    # -----------------------------------------

    for word, number in NUMBER_WORDS.items():

        if re.search(
            rf"\b{word}\s+(?:year|years)\b",
            text
        ):
            return number * 12

    # -----------------------------------------
    # Word-based months
    # -----------------------------------------

    for word, number in NUMBER_WORDS.items():

        if re.search(
            rf"\b{word}\s+(?:month|months)\b",
            text
        ):
            return number

    # -----------------------------------------
    # Common phrases
    # -----------------------------------------

    if "next year" in text:
        return 12

    if "within a year" in text:
        return 12

    if "in a year" in text:
        return 12

    if "one year" in text:
        return 12

    if "two years" in text:
        return 24

    if "three years" in text:
        return 36

    return None

# =========================================================
# KEYWORD GOAL DETECTION
# =========================================================

def detect_goal_by_keyword(text):

    text = normalize_text(text)

    # Longer keywords first
    keywords = sorted(
        GOAL_KEYWORDS.keys(),
        key=len,
        reverse=True
    )


    for keyword in keywords:

        if re.search(
            rf"\b{re.escape(keyword)}\b",
            text
        ):

            goal, category = (
                GOAL_KEYWORDS[keyword]
            )

            return (
                goal,
                category,
                0.99
            )


    return (
        None,
        None,
        0.0
    )


# =========================================================
# CUSTOM GOAL
# =========================================================

def extract_custom_goal(text):

    text = str(text).strip()


    # Example:
    # save money for photography course

    match = re.search(
        r"\bfor\s+(.+?)(?:\s+in\s+|\s+within\s+|\s+next\s+|$)",
        text,
        re.IGNORECASE
    )


    if match:

        goal = match.group(1).strip()

        if goal:

            return goal


    return None


# =========================================================
# MAIN NLP FUNCTION
# =========================================================

def understand_goal(text):

    if not text or not text.strip():

        return {

            "success": False,

            "message":
                "Please enter your future goal."

        }


    original_text = text.strip()


    # =====================================================
    # KEYWORD DETECTION
    # =====================================================

    keyword_goal, keyword_category, keyword_confidence = (
        detect_goal_by_keyword(
            original_text
        )
    )


    # =====================================================
    # ML PREDICTION
    # =====================================================

    text_vector = vectorizer.transform(
        [original_text]
    )


    goal_probabilities = (
        goal_model.predict_proba(
            text_vector
        )[0]
    )


    best_goal_index = (
        goal_probabilities.argmax()
    )


    ml_goal = (
        goal_model.classes_[
            best_goal_index
        ]
    )


    ml_confidence = float(
        goal_probabilities[
            best_goal_index
        ]
    )


    category_probabilities = (
        category_model.predict_proba(
            text_vector
        )[0]
    )


    best_category_index = (
        category_probabilities.argmax()
    )


    ml_category = (
        category_model.classes_[
            best_category_index
        ]
    )


    # =====================================================
    # FINAL GOAL + CATEGORY
    # =====================================================

    if keyword_goal:

        final_goal = keyword_goal

        final_category = keyword_category

        confidence = keyword_confidence


    elif ml_confidence >= 0.45:

        final_goal = ml_goal

        final_category = ml_category

        confidence = ml_confidence


    else:

        custom_goal = (
            extract_custom_goal(
                original_text
            )
        )


        if custom_goal:

            final_goal = (
                custom_goal.title()
            )

        else:

            final_goal = "Custom Goal"


        final_category = "Custom"

        confidence = ml_confidence


    # =====================================================
    # AMOUNT
    # =====================================================

    target_amount = extract_amount(
        original_text
    )


    # =====================================================
    # DURATION
    # =====================================================

    duration_months = extract_duration(
        original_text
    )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {

        "success": True,

        "original_text":
            original_text,

        "goal":
            final_goal,

        "category":
            final_category,

        "target_amount":
            target_amount,

        "duration_months":
            duration_months,

        "confidence":
            round(
                confidence * 100,
                2
            )

    }


# =========================================================
# COMPATIBILITY
# =========================================================

def predict_intent(text):

    return understand_goal(text)