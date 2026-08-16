"""
Pure Python Keyword-Based Gender Classifier (step1_eda).
Evaluates 'category', 'category_name', and 'name' fields without machine learning training
to assign boolean fields: for_man, for_woman, for_unisex.
"""

def classify_gender(category_id: int | str, category_name: str, product_name: str = "") -> dict:
    """
    Classifies gender targeting for a given product based on category metadata using pure Python keywords.
    
    Returns:
        dict: {
            'for_man': bool,
            'for_woman': bool,
            'for_unisex': bool
        }
    """
    cat_str = str(category_name).lower().strip() if category_name else ""
    prod_str = str(product_name).lower().strip() if product_name else ""
    
    for_man = False
    for_woman = False
    for_unisex = False

    # Explicit Unisex indicators in category or product name
    if "unisex" in cat_str or "unisex" in prod_str:
        return {"for_man": True, "for_woman": True, "for_unisex": True}

    # Keywords for Women's fashion
    women_keywords = [
        "womens-", "women-s-", "women-", "girls-", "dresses", "bikinis", "corsets",
        "heels", "panties", "bras", "bathrobes", "hosiery", "jumpsuits", "blouses",
        "earrings", "espadrilles", "shawls", "skirts", "nightgowns", "co-ord",
        "tankinis", "kaftans", "mule", "loafers-and-moccasins", "jewelry", "pajamas"
    ]
    
    # Keywords for Men's fashion
    men_keywords = [
        "mens-", "men-s-", "men-", "boys-", "men-dress-shoes", "mens-boots",
        "mens-outdoor-shoes", "mens-sport-jackets", "mens-undergarments",
        "mens-watches", "boys-shoes", "mens-backpacks", "mens-bags",
        "mens-bath-robes", "mens-belts", "mens-bombers", "mens-bow-ties",
        "mens-cufflinks", "mens-shirts", "mens-short", "mens-ties", "mens-tracksuits"
    ]

    is_woman = any(kw in cat_str for kw in women_keywords) or any(kw in prod_str for kw in ["dámsk", "dámské", "women", "dámska"])
    is_man = any(kw in cat_str for kw in men_keywords) or any(kw in prod_str for kw in ["pánsk", "pánské", "men", "pánska"])

    if is_woman and not is_man:
        for_woman = True
        for_man = False
        for_unisex = False
    elif is_man and not is_woman:
        for_man = True
        for_woman = False
        for_unisex = False
    else:
        # Bags, watches, sunglasses, backpacks, accessories, or indeterminate categories
        for_unisex = True
        for_man = True
        for_woman = True

    return {
        "for_man": bool(for_man),
        "for_woman": bool(for_woman),
        "for_unisex": bool(for_unisex)
    }

if __name__ == "__main__":
    print(classify_gender(645, "mens-watches", "Casio Collection"))
    print(classify_gender(468, "womens-earrings", "Hot Diamonds"))
