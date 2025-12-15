import os
import re
import yaml
import pandas as pd
from pathlib import Path

# config
base_path = r"D:\Sathish\Guvi_HCL\Project_2\data"
out_dir = r"D:\Sathish\Guvi_HCL\Project_2\output_by_ticker"
max_ticker_files = 50   # save up to 50 tickers (as you requested)

Path(out_dir).mkdir(parents=True, exist_ok=True)

def sanitize_filename(name: str) -> str:
    if not isinstance(name, str) or name.strip() == "":
        return "UNKNOWN_TICKER"
    s = name.strip()
    s = re.sub(r"[^\w\-\_\.]", "_", s)
    return s

def find_ticker_in_value(val):
    """
    Recursively search value for a key or string that looks like a ticker.
    If val is dict -> check keys named 'ticker' (ci) or recurse into values.
    If val is list -> search items.
    If scalar -> return None.
    """
    if val is None:
        return None
    # dict: direct key match
    if isinstance(val, dict):
        for k, v in val.items():
            if isinstance(k, str) and k.lower() == "ticker":
                return v
        # recurse deeper
        for v in val.values():
            res = find_ticker_in_value(v)
            if res is not None:
                return res
        return None
    # list: check each element
    if isinstance(val, list):
        for item in val:
            res = find_ticker_in_value(item)
            if res is not None:
                return res
        return None
    # scalar: nothing to inspect
    return None

def get_ticker_from_row(row: pd.Series):
    """
    1) Look for columns whose name is exactly 'ticker' (case-insensitive)
    2) Look for columns containing 'ticker' in the name
    3) Inspect each cell for nested dict/list containing a 'ticker' key
    """
    # 1 & 2 - column name based
    for col in row.index:
        if isinstance(col, str) and col.lower() == "ticker":
            val = row[col]
            if pd.notna(val) and str(val).strip() != "":
                return val
    for col in row.index:
        if isinstance(col, str) and "ticker" in col.lower():
            val = row[col]
            if pd.notna(val) and str(val).strip() != "":
                return val

    # 3 - inspect cell values
    for col in row.index:
        cell = row[col]
        # try recursive search in cell if it's dict/list
        try:
            res = find_ticker_in_value(cell)
        except Exception:
            res = None
        if res is not None and str(res).strip() != "":
            return res

    return None

# --- read all YAML files into one combined DataFrame (like your original) ---
rows = []
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.lower().endswith((".yaml", ".yml")):
            fp = os.path.join(root, file)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    # handle multi-doc yaml
                    docs = list(yaml.safe_load_all(f))
            except Exception as e:
                print(f"Skipping {fp} (read error): {e}")
                continue

            for doc_idx, doc in enumerate(docs):
                if doc is None:
                    continue

                # Attempt to flatten top-level dict/list into DataFrame rows
                try:
                    part_df = pd.json_normalize(doc)
                except Exception:
                    # fallback handling
                    if isinstance(doc, dict):
                        part_df = pd.DataFrame([doc])
                    elif isinstance(doc, list):
                        # list of scalars -> single column 'value'
                        if all(not isinstance(x, dict) for x in doc):
                            part_df = pd.DataFrame({"value": doc})
                        else:
                            part_df = pd.DataFrame(doc)
                    else:
                        part_df = pd.DataFrame({"value": [doc]})

                # add provenance columns
                # part_df["__source_file"] = file
                # part_df["__source_folder"] = root
                # part_df["__doc_index"] = doc_idx

                rows.append(part_df)

if not rows:
    print("No YAML rows found. Exiting.")
    raise SystemExit(0)

final_df = pd.concat(rows, ignore_index=True, sort=False)

# --- group rows by ticker and write CSV files ---
# We'll collect rows per ticker into dict of DataFrames (efficient) then save
grouped = {}
unknown_rows = []

for idx, row in final_df.iterrows():
    ticker = get_ticker_from_row(row)
    if ticker is None:
        # store index to unknown bucket
        unknown_rows.append(row)
        continue
    ticker_str = str(ticker).strip()
    if ticker_str == "":
        unknown_rows.append(row)
        continue
    fname = sanitize_filename(ticker_str)
    if fname not in grouped:
        grouped[fname] = []
    grouped[fname].append(row)

# Save up to max_ticker_files tickers
ticker_names = list(grouped.keys())
if len(ticker_names) == 0:
    print("No tickers found in data. Writing all rows to UNKNOWN_TICKER.csv")
    pd.DataFrame(unknown_rows).to_csv(os.path.join(out_dir, "UNKNOWN_TICKER.csv"), index=False, encoding="utf-8")
else:
    saved = 0
    skipped_tickers = []
    for tname in ticker_names:
        if saved >= max_ticker_files:
            skipped_tickers.append(tname)
            continue
        rows_list = grouped[tname]
        df_t = pd.DataFrame(rows_list)
        out_path = os.path.join(out_dir, f"{tname}.csv")
        df_t.to_csv(out_path, index=False, encoding="utf-8")
        saved += 1

    # Save unknowns if any
    if unknown_rows:
        pd.DataFrame(unknown_rows).to_csv(os.path.join(out_dir, "UNKNOWN_TICKER.csv"), index=False, encoding="utf-8")

    print(f"Saved {saved} ticker CSV files to: {out_dir}")
    if skipped_tickers:
        print(f"Skipped {len(skipped_tickers)} additional tickers (limit={max_ticker_files}).")
        print("First skipped tickers:", skipped_tickers[:10])
