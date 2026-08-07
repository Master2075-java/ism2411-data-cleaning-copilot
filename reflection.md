# Copilot Development Reflection

### What Copilot Generated
GitHub Copilot was used to scaffold the main cleaning functions in `src/data_cleaning.py`. By writing clear function docstrings and prompt comments, Copilot auto-generated initial structures for `load_data`, `clean_column_names`, `handle_missing_values`, and `remove_invalid_rows`. It quickly filled in standard `pandas` syntax such as `.read_csv()`, `.fillna()`, and filtering conditions.

### What I Modified
I made several modifications to Copilot's initial code suggestions to improve reliability:
1. **Dynamic Path Resolution:** Copilot used hardcoded relative paths that failed when running the script from different working directories in Thonny. I modified the execution block to use `os.path.abspath(__file__)` to dynamically locate the `data/` folder relative to the script's directory.
2. **Column Name Cleaning:** Copilot originally suggested a basic string replacement `.replace(' ', '_')`. I improved this by using regex (`r'\s+'`) combined with `.str.strip()` to handle leading/trailing spaces and multiple continuous spaces in headers.
3. **Explicit Type Casting:** I added `pd.to_numeric(..., errors='coerce')` before imputing missing values to ensure any improper text entries inside numeric columns were cleanly converted to NaNs first.

### What I Learned
Through this project, I learned that while AI coding assistants like GitHub Copilot significantly speed up writing repetitive code and pandas operations, human oversight is essential. Copilot provides syntax based on common patterns, but it cannot anticipate specific runtime environments (like working directories) or exact business logic rules without critical evaluation and testing.