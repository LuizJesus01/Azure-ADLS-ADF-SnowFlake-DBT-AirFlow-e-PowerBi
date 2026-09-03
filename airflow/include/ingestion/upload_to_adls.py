from pathlib import Path
import os

from azure.storage.blob import BlobServiceClient


ACCOUNT_URL = (
    "https://projetosengdados."
    "blob.core.windows.net"
)

CONTAINER_NAME = "projetos"

REMOTE_ROOT = "ProjetoSnowFlake/Raw"


def upload_to_adls(local_root: Path) -> None:

    sas_token = os.getenv(
        "AZURE_STORAGE_SAS_TOKEN"
    )

    if not sas_token:
        raise ValueError(
            "AZURE_STORAGE_SAS_TOKEN não encontrada."
        )

    blob_service_client = BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=sas_token
    )

    container_client = (
        blob_service_client
        .get_container_client(CONTAINER_NAME)
    )

    folders = {
        "CSV": local_root / "CSV",
        "json": local_root / "json",
        "parquet": local_root / "parquet",
    }

    expected_blobs = []

    # ========================================================
    # UPLOAD
    # ========================================================

    for remote_folder, local_folder in folders.items():

        for local_file in local_folder.iterdir():

            if not local_file.is_file():
                continue

            blob_name = (
                f"{REMOTE_ROOT}/"
                f"{remote_folder}/"
                f"{local_file.name}"
            )

            expected_blobs.append(blob_name)

            print(
                f"Upload: {local_file.name}"
            )

            blob_client = (
                container_client
                .get_blob_client(blob_name)
            )

            with open(local_file, "rb") as data:

                blob_client.upload_blob(
                    data,
                    overwrite=True
                )

    print("[3/4] Upload ADLS concluído.")

    # ========================================================
    # VALIDAÇÃO PÓS-UPLOAD
    # ========================================================

    print("\nValidando arquivos no ADLS...")

    found_blobs = {
        blob.name
        for blob in container_client.list_blobs(
            name_starts_with=REMOTE_ROOT
        )
    }

    missing_blobs = [
        blob_name
        for blob_name in expected_blobs
        if blob_name not in found_blobs
    ]

    print(
        f"Arquivos esperados: {len(expected_blobs)}"
    )

    print(
        f"Arquivos encontrados: "
        f"{len(expected_blobs) - len(missing_blobs)}"
    )

    print(
        f"Arquivos ausentes: {len(missing_blobs)}"
    )

    if missing_blobs:

        print("\nArquivos não encontrados:")

        for blob_name in missing_blobs:
            print(f"- {blob_name}")

        raise RuntimeError(
            "Falha na validação pós-upload."
        )

    print("[4/4] Validação ADLS concluída.")