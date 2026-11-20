from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.shopping import ShoppingRequest


def recommend_products(db: Session, preferences: ShoppingRequest) -> list[tuple[int, Product]]:
    products = db.query(Product).filter(Product.in_stock.is_(True)).all()
    ranked = []
    wanted_colors = {value.casefold() for value in preferences.colors}
    for product in products:
        if preferences.category and product.category.casefold() != preferences.category.casefold():
            continue
        if preferences.occasion and product.occasion.casefold() != preferences.occasion.casefold():
            continue
        if preferences.min_budget is not None and product.price < preferences.min_budget:
            continue
        if preferences.max_budget is not None and product.price > preferences.max_budget:
            continue
        available_sizes = {value.strip().casefold() for value in product.sizes.split(",")}
        if preferences.size and preferences.size.casefold() not in available_sizes:
            continue
        product_colors = {value.strip().casefold() for value in product.color.split(",")}
        if wanted_colors and not wanted_colors.intersection(product_colors):
            continue
        score = 0
        if preferences.category and product.category.casefold() == preferences.category.casefold():
            score += 3
        if preferences.occasion and product.occasion.casefold() == preferences.occasion.casefold():
            score += 3
        if wanted_colors.intersection(product_colors):
            score += 2
        if preferences.size:
            score += 2
        if preferences.style_preferences:
            searchable = f"{product.name} {product.description} {product.category}".casefold()
            score += sum(1 for style in preferences.style_preferences if style.casefold() in searchable)
        ranked.append((score, product))
    ranked.sort(key=lambda item: (-item[0], item[1].price, item[1].name))
    return ranked[:preferences.limit]


def explain_recommendation(product: Product, preferences: ShoppingRequest, score: int) -> str:
    reasons = []
    if preferences.category and product.category.casefold() == preferences.category.casefold():
        reasons.append(f"matches your {product.category.lower()} category")
    if preferences.occasion and product.occasion.casefold() == preferences.occasion.casefold():
        reasons.append(f"suits a {preferences.occasion.lower()} occasion")
    if preferences.colors and any(c.casefold() in {p.strip().casefold() for p in product.color.split(",")} for c in preferences.colors):
        reasons.append("matches your color choice")
    if preferences.size:
        reasons.append(f"is available in size {preferences.size}")
    return "Recommended because it " + (", ".join(reasons) if reasons else "fits your budget and is in stock") + "."
