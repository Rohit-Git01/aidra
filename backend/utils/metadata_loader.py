from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMA_DIR = BASE_DIR / "metadata" / "schema"
RELATIONSHIP_DIR = BASE_DIR / "metadata" / "relationships"
GLOSSARY_DIR = BASE_DIR / "metadata" / "business_glossary"


def load_json_metadata(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {file_path}")
    if file_path.stat().st_size == 0:
        raise ValueError(f"Empty metadata file: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata_directory(directory_path):
    directory_path = Path(directory_path)
    if not directory_path.exists():
        raise FileNotFoundError(f"Metadata directory not found: {directory_path}")

    metadata = {}
    for json_file in sorted(directory_path.glob("*.json")):
        try:
            metadata[json_file.stem] = load_json_metadata(json_file)
        except (json.JSONDecodeError, ValueError, FileNotFoundError) as exc:
            print(f"Skipping invalid metadata file '{json_file.name}': {exc}")
    return metadata


def load_schema_metadata():
    return load_metadata_directory(SCHEMA_DIR)


def load_relationship_metadata():
    return load_metadata_directory(RELATIONSHIP_DIR)


def load_glossary_metadata():
    return load_metadata_directory(GLOSSARY_DIR)


if __name__ == "__main__":
    print("schema metadata:\n", load_schema_metadata())
    print("relationship metadata:\n", load_relationship_metadata())
    print("glossary metadata:\n", load_glossary_metadata())