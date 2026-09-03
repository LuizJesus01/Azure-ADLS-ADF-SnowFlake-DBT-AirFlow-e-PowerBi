from download_olist import download_olist
from prepare_olist_files import prepare_olist_files
from upload_to_adls import upload_to_adls


def main():

    print("=" * 50)
    print("OLIST INGESTION PIPELINE")
    print("=" * 50)

    dataset_path = download_olist()

    landing_path = prepare_olist_files(
        dataset_path
    )

    upload_to_adls(
        landing_path
    )

    print("=" * 50)
    print("PIPELINE FINALIZADO COM SUCESSO")
    print("=" * 50)


if __name__ == "__main__":
    main()