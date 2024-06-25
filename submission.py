import argparse
import json
from pathlib import Path

from src.data_cleanup import DataCleanup
from src.pdf import DocumentAI


def main(path_to_case_pdf: str):
    """Write the entrypoint to your submission here"""
    document_ai = DocumentAI()
    documents = document_ai(Path(path_to_case_pdf))
    parsed_pages = []
    for page in documents.pages:
        page_layout = page.layout
        parsed_pages.append(
            {
                "text": document_ai.layout_to_text(page_layout, documents.text),
                "page": page.page_number,
            }
        )
    data_cleanup = DataCleanup()
    cleaned_data = data_cleanup.cleanup_data(parsed_pages)
    with open('cleaned_data.json', 'w') as f:
        json.dump(cleaned_data, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path-to-case-pdf',
                        metavar='path',
                        type=str,
                        help='Path to local test case with which to run your code')
    args = parser.parse_args()
    main(args.path_to_case_pdf)
