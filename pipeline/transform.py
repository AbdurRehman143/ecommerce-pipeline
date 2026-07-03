import json
import pandas as pd
import os

def transform_products():
    with open("data/products_raw.json", "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Keep only business-relevant fields
    df = df[["id", "title", "category", "price", "rating"]]
    
    # Flatten the rating column (it's a dict with 'rate' and 'count')
    df["rating_score"] = df["rating"].apply(lambda x: x["rate"])
    df["rating_count"] = df["rating"].apply(lambda x: x["count"])
    df = df.drop(columns=["rating"])
    
    # Clean category names
    df["category"] = df["category"].str.strip().str.title()
    
    # Add revenue potential column
    df["revenue_potential"] = df["price"] * df["rating_count"]
    
    # Summary metrics by category
    summary = df.groupby("category").agg(
        total_products=("id", "count"),
        avg_price=("price", "mean"),
        avg_rating=("rating_score", "mean"),
        total_revenue_potential=("revenue_potential", "sum")
    ).round(2).reset_index()
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/products_clean.csv", index=False)
    summary.to_csv("data/category_summary.csv", index=False)
    
    print("Transformation complete.")
    print("\nCategory Summary:")
    print(summary.to_string(index=False))
    
    return df, summary

if __name__ == "__main__":
    transform_products()