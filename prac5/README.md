# Practice 5 – Python Regular Expressions (RegEx)

## Objective
The goal of this practice is to learn how to use Regular Expressions (RegEx) in Python using the `re` module.  
Students practice searching, matching, extracting, and replacing text patterns and apply these skills to parse receipt data.

---

## Tasks

### 1. Study Python RegEx

Complete the Python RegEx tutorial from W3Schools:

https://www.w3schools.com/python/python_regex.asp

Topics covered:
- RegEx Introduction
- RegEx Syntax and Metacharacters
- Special Sequences
- Character Classes
- Quantifiers
- `re.search()`
- `re.findall()`
- `re.split()`
- `re.sub()`
- `re.match()`
- Flags (`re.IGNORECASE`, `re.MULTILINE`)

---

### 2. Practical Exercise – Receipt Parsing

Using the provided `raw.txt` file, create a Python program that parses receipt data.

Tasks completed by the program:

1. Extract all prices from the receipt
2. Find all product names
3. Calculate the total amount
4. Extract date and time information
5. Find payment method
6. Create structured output (JSON or formatted text)

---

## Project Structure

Practice5/
│
├── receipt_parser.py
├── raw.txt
└── README.md

- `receipt_parser.py` – Python script that parses receipt data using regex
- `raw.txt` – receipt text used as input
- `README.md` – documentation of the practice

---

## How to Run

1. Install Python.
2. Place the receipt text in `raw.txt`.
3. Run the script:

python receipt_parser.py

The script will parse the receipt and print the extracted information.

---

## Online Problem Set

Additional programming tasks were completed at:

http://ejudge.kz/new-client?contest_id=705

Topics include:
- iterators
- dates
- math
- JSON

---

## Resources

- https://www.w3schools.com/python/python_regex.asp
- https://regex101.com/
- https://docs.python.org/3/library/re.html
- https://regexr.com/

---

## Author

Practice 5 – Python Regular Expressions