import os
import logging

logger = logging.getLogger(__name__)


def clean_gutenberg_file(input_file, output_file):
    if os.path.exists(output_file):
        logger.debug("Cleaned file already exists. Skipping cleaning.")
        return

    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    start_idx = None
    end_idx = None

    # Find the start and end markers
    for i, line in enumerate(lines):
        if line.startswith("*** START OF THE PROJECT GUTENBERG EBOOK"):
            start_idx = i
        if line.startswith("*** END OF THE PROJECT GUTENBERG EBOOK"):
            end_idx = i
            break

    # If both markers are found, extract the content
    if start_idx is not None and end_idx is not None:
        cleaned_content = lines[start_idx + 1 : end_idx]
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.writelines(cleaned_content)
    else:
        logger.warning(f"Markers not found in {input_file}. File not cleaned.")
