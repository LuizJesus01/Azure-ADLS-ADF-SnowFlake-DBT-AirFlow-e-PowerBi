from pathlib import Path
import pandas as pd


OUTPUT_DIR = (
    Path.home()
    / "ProjetoSnowFlake"
    / "data"
    / "landing"
)


def prepare_olist_files(source_dir: Path) -> Path:

    csv_dir = OUTPUT_DIR / "CSV"
    json_dir = OUTPUT_DIR / "json"
    parquet_dir = OUTPUT_DIR / "parquet"

    for directory in (
        csv_dir,
        json_dir,
        parquet_dir,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # JSON
    json_files = {
        "olist_customers_dataset.csv": "customers.json",
        "olist_order_payments_dataset.csv": "payments.json",
        "olist_order_reviews_dataset.csv": "reviews.json",
    }

    for source_name, target_name in json_files.items():

        df = pd.read_csv(
            source_dir / source_name
        )

        df.to_json(
            json_dir / target_name,
            orient="records",
            lines=True,
            force_ascii=False
        )

        print(f"JSON criado: {target_name}")

    # PARQUET
    parquet_files = {
        "olist_geolocation_dataset.csv": "geolocation.parquet",
        "olist_order_items_dataset.csv": "order_items.parquet",
        "olist_orders_dataset.csv": "orders.parquet",
    }

    for source_name, target_name in parquet_files.items():

        df = pd.read_csv(
            source_dir / source_name
        )

        df.to_parquet(
            parquet_dir / target_name,
            index=False
        )

        print(f"Parquet criado: {target_name}")

    # CSV
    csv_files = {
        "olist_products_dataset.csv": "products.csv",
        "olist_sellers_dataset.csv": "sellers.csv",
        "product_category_name_translation.csv":
            "category_translation.csv",
    }

    for source_name, target_name in csv_files.items():

        df = pd.read_csv(
            source_dir / source_name
        )

        df.to_csv(
            csv_dir / target_name,
            index=False
        )

        print(f"CSV criado: {target_name}")

    print("[2/4] Preparação concluída.")

    return OUTPUT_DIR


if __name__ == "__main__":

    source = Path(
        "/home/luiz/.cache/kagglehub/"
        "datasets/olistbr/"
        "brazilian-ecommerce/versions/2"
    )

    prepare_olist_files(source)