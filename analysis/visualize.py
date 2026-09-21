import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import config

class CatalogVisualizer:
    @staticmethod
    def generate_all_plots(df: pd.DataFrame):
        if df.empty:
            return ""

        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 1. Price Distribution
        sns.histplot(df["price"], kde=True, ax=axes[0, 0], color="#2563eb", bins=15)
        axes[0, 0].set_title("1. Product Price Distribution")
        axes[0, 0].set_xlabel("Price (INR)")

        # 2. Rating Distribution (Cleaned Seaborn syntax)
        sns.countplot(data=df, x="rating", hue="rating", ax=axes[0, 1], palette="Blues_d", legend=False)
        axes[0, 1].set_title("2. Rating Distribution")
        axes[0, 1].set_xlabel("Rating (Stars)")

        # 3. Price vs. Rating
        sns.scatterplot(data=df, x="rating", y="price", ax=axes[1, 0], color="#e11d48", s=80)
        axes[1, 0].set_title("3. Price vs. Rating")
        axes[1, 0].set_xlabel("Rating")
        axes[1, 0].set_ylabel("Price (INR)")

        # 4. Products by Category (Cleaned Seaborn syntax)
        top_cats = df["category"].value_counts().head(5).reset_index()
        top_cats.columns = ["category", "count"]
        sns.barplot(data=top_cats, x="count", y="category", hue="category", ax=axes[1, 1], palette="viridis", legend=False)
        axes[1, 1].set_title("4. Products by Top Categories")
        axes[1, 1].set_xlabel("Count")

        plt.tight_layout()
        save_path = config.OUTPUT_DIR / "analysis_charts.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        return str(save_path)