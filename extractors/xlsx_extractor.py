from pathlib import Path
from datetime import date, datetime, time

from openpyxl import load_workbook

from core.document import DocumentContent


def extract_xlsx(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(
            f"Excel file does not exist: {file_path}"
        )

    if file.suffix.lower() != ".xlsx":
        raise ValueError(
            f"Unsupported Excel file type: {file.suffix}"
        )

    workbook = load_workbook(
        filename=file_path,
        read_only=True,
        data_only=True,
    )

    sheet_names = workbook.sheetnames

    sections = []

    try:
        for worksheet in workbook.worksheets:

            sheet_text = _extract_worksheet(
                worksheet
            )

            if sheet_text:
                sections.append(sheet_text)

    finally:
        workbook.close()

    if not sections:
        raise ValueError(
            "No readable content was found in the Excel workbook."
        )

    return DocumentContent(
        text="\n\n".join(sections),
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type="xlsx",
        language="en",
        metadata={
            "sheet_count": len(sheet_names),
            "sheets": sheet_names,
        },
    )


def _extract_worksheet(worksheet) -> str:

    rows = []

    for row in worksheet.iter_rows(
        values_only=True
    ):
        values = [
            _format_cell(value)
            for value in row
        ]

        # Remove trailing empty cells.
        while values and not values[-1]:
            values.pop()

        # Ignore completely empty rows.
        if not values:
            continue

        rows.append(values)

    if not rows:
        return ""

    lines = [
        f"Sheet: {worksheet.title}",
        "",
    ]

    # -------------------------------------------------
    # Single-cell / free-form worksheet
    # -------------------------------------------------

    if _is_free_form(rows):

        for row_number, row in enumerate(
            rows,
            start=1,
        ):
            for column_number, value in enumerate(
                row,
                start=1,
            ):
                if not value:
                    continue

                cell_reference = (
                    f"{_column_letter(column_number)}"
                    f"{row_number}"
                )

                lines.append(
                    f"Cell {cell_reference}: {value}"
                )

        return "\n".join(lines).strip()

    # -------------------------------------------------
    # Tabular worksheet
    # -------------------------------------------------

    headers = rows[0]

    lines.append("Columns:")
    lines.append(
        " | ".join(
            header or f"Column {index + 1}"
            for index, header in enumerate(headers)
        )
    )

    lines.append("")

    for row_number, row in enumerate(
        rows[1:],
        start=2,
    ):

        if not any(row):
            continue

        lines.append(
            f"Row {row_number}:"
        )

        for column_index, value in enumerate(
            row
        ):

            if not value:
                continue

            if column_index < len(headers):
                column_name = (
                    headers[column_index]
                    or f"Column {column_index + 1}"
                )
            else:
                column_name = (
                    f"Column {column_index + 1}"
                )

            lines.append(
                f"{column_name}: {value}"
            )

        lines.append("")

    return "\n".join(lines).strip()


def _is_free_form(rows: list[list[str]]) -> bool:

    # A worksheet containing only one populated cell
    # is clearly free-form content.
    populated_cells = sum(
        1
        for row in rows
        for value in row
        if value
    )

    if populated_cells <= 3:
        return True

    # If most rows contain only one populated cell,
    # treat the worksheet as a collection of text
    # rather than as a conventional table.
    single_value_rows = sum(
        1
        for row in rows
        if sum(
            1
            for value in row
            if value
        ) == 1
    )

    return (
        len(rows) > 0
        and single_value_rows / len(rows) >= 0.8
    )


def _format_cell(value) -> str:

    if value is None:
        return ""

    if isinstance(value, datetime):
        return value.isoformat(
            sep=" ",
            timespec="seconds",
        )

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, time):
        return value.isoformat(
            timespec="seconds"
        )

    if isinstance(value, float):

        if value.is_integer():
            return str(int(value))

        return str(value)

    return str(value).strip()


def _column_letter(column_number: int) -> str:

    result = ""

    while column_number > 0:
        column_number, remainder = divmod(
            column_number - 1,
            26,
        )

        result = (
            chr(65 + remainder)
            + result
        )

    return result