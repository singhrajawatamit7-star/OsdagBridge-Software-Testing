"""Convert a real Pytest JUnit XML report into CSV."""
import csv
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def convert_junit_to_csv(xml_path, csv_path):
    xml_path = Path(xml_path)
    csv_path = Path(csv_path)
    if not xml_path.exists():
        raise FileNotFoundError(xml_path)
    root = ET.parse(xml_path).getroot()
    rows = []
    run_timestamp = datetime.now(timezone.utc).strftime("EXEC-%Y%m%d-%H%M%S")
    for case in root.iter("testcase"):
        classname = case.attrib.get("classname", "")
        name = case.attrib.get("name", "")
        duration = float(case.attrib.get("time", 0))
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")
        if failure is not None:
            status = "FAIL"
            remarks = failure.attrib.get("message", "Test failed")
        elif error is not None:
            status = "ERROR"
            remarks = error.attrib.get("message", "Test error")
        elif skipped is not None:
            status = "SKIPPED"
            remarks = skipped.attrib.get("message", "Test skipped")
        else:
            status = "PASS"
            remarks = "Pytest completed successfully"
        rows.append({
            "Execution_ID": run_timestamp,
            "Test_ID": f"{classname}::{name}",
            "Test_Name": name,
            "Module": classname,
            "Status": status,
            "Execution_Time_sec": round(duration, 4),
            "Remarks": remarks,
            "Execution_Date_UTC": datetime.now(timezone.utc).isoformat(),
        })
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "Execution_ID",
        "Test_ID",
        "Test_Name",
        "Module",
        "Status",
        "Execution_Time_sec",
        "Remarks",
        "Execution_Date_UTC",
    ]
    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} test records to {csv_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python scripts/export_junit_csv.py input.xml output.csv"
        )
    convert_junit_to_csv(sys.argv[1], sys.argv[2])
