from pathlib import Path
import kagglehub


def download_olist() -> Path:
    path = kagglehub.dataset_download(
        "olistbr/brazilian-ecommerce"
    )

    dataset_path = Path(path)

    print("[1/4] Download concluído.")
    print(f"Dataset: {dataset_path}")

    return dataset_path


if __name__ == "__main__":
    download_olist()