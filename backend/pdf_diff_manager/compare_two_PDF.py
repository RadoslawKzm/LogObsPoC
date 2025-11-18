from text_from_pdf_extractor import export_text_from_pdf
import difflib

file_one_path = ".\sample_pdf_file\sample-local-pdf.pdf"
file_two_path = ".\sample_pdf_file\SamplePDFPage2.pdf"



def compare_texts_first_approach(*, first_file_path : str, second_file_path : str) -> None:
    first_text = export_text_from_pdf(file_path=first_file_path)
    second_text = export_text_from_pdf(file_path=second_file_path)

    differ = difflib.Differ()
    result = list(differ.compare(first_text, second_text))
    print(''.join(result))


def compare_texts_second_approach(*, first_file_path: str, second_file_path: str) -> None:
    first_text = export_text_from_pdf(file_path=first_file_path)
    second_text = export_text_from_pdf(file_path=second_file_path)

    diff = difflib.unified_diff(
        first_text.splitlines(keepends=True),
        second_text.splitlines(keepends=True),
        fromfile=file_one_path,
        tofile=file_two_path,
        lineterm=''
    )

    print('\n'.join(diff))

compare_texts_first_approach(first_file_path=file_one_path, second_file_path=file_two_path)
compare_texts_second_approach(first_file_path=file_one_path, second_file_path=file_two_path)