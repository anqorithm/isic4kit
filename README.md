# ISIC4Kit

<p align="center">
  <img src="assets/logo.svg" width="400" alt="ISIC4Kit Logo">
</p>


![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-≥3.8,<4.0-blue.svg)
![PyPI](https://badge.fury.io/py/isic4kit.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/isic4kit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/isic4kit)
![PyPI - License](https://img.shields.io/pypi/l/isic4kit)
![PyPI - Status](https://img.shields.io/pypi/status/isic4kit)
![Commits](https://img.shields.io/github/last-commit/anqorithm/isic4kit)
![Contributors](https://img.shields.io/github/contributors/anqorithm/isic4kit)

A Python SDK Library for working with the International Standard Industrial Classification of All Economic Activities (ISIC), Revision 4.

## Features

- Search and navigate through the ISIC hierarchical structure
- Support for multiple languages (English, Arabic, and more coming soon)
- Pydantic-based
- Easy to use
- Well-documented
- Tested and maintained
- Lightweight and fast

## Structure

ISIC follows a hierarchical structure:

```mermaid
flowchart TD
    Section[Section] --> Division[Division]
    Division --> Group[Group]
    Group --> Class[Class]
    
    Section --> |contains| SectionDesc[Description]
    Division --> |contains| DivisionDesc[Description]
    Group --> |contains| GroupDesc[Description]
    Class --> |contains| ClassDesc[Description]
```

Each level contains:
- **Section**: Highest level (A-U), e.g., "A" for Agriculture
- **Division**: Two-digit code (01-99)
- **Group**: Three-digit code (011-999)
- **Class**: Four-digit code (0111-9999)

## Installation


### Poetry (recommended)
```bash
poetry add isic4kit
```

### pip
```bash
pip install isic4kit
```

## Dependencies

- Python >=3.8, <4.0
- pydantic ^2.10.6
- pytest ^8.3.4

## Usage

### Basic Usage

```python
from isic4kit import ISIC4Classifier

# Initialize classifier (English)
isic_en = ISIC4Classifier(language="en")

# Example 1: Get section (Agriculture)
section = isic_en.get_section("a")
# Access divisions directly
for division in section.divisions:
    print(division.code, division.description)
    # Access groups
    for group in division.groups:
        print(group.code, group.description)
        # Access classes
        for class_ in group.classes:
            print(class_.code, class_.description)
# Or use the tree visualization
section.print_tree()

# Example 2: Get division (Crop and animal production)
division = isic_en.get_division("01")
division.print_tree()

# Example 3: Get group (Growing of non-perennial crops)
group = isic_en.get_group("011")
group.print_tree()

# Example 4: Get class (Growing of cereals)
class_ = isic_en.get_class("0111")
class_.print_tree()
```

### Search Functionality

```python
# Search for activities containing "mining"
results = isic_en.search("mining")
results.print_tree()
```

### Multi-language Support

The classifier supports multiple languages. Here's an example in Arabic:

```python
# Initialize with Arabic language
isic_ar = ISIC4Classifier(language="ar")

# Example 1: Get section (الزراعة)
section_ar = isic_ar.get_section("a")
section_ar.print_tree()

# Example 2: Get division (زراعة المحاصيل والإنتاج الحيواني)
division_ar = isic_ar.get_division("01")
division_ar.print_tree()

# Example 3: Get group (زراعة المحاصيل غير الدائمة)
group_ar = isic_ar.get_group("011")
group_ar.print_tree()

# Example 4: Get class (زراعة الحبوب)
class_ar = isic_ar.get_class("0111")
class_ar.print_tree()

# Example 5: Search in Arabic
search_ar = isic_ar.search("تعدين")
search_ar.print_tree()
```

## Supported Languages

- English (en)
- Arabic (ar)
- More languages coming soon...

## Data Structure

The ISIC data is organized in a hierarchical structure:

```python
sections = [
    {
        "section": "A",
        "description": "Agriculture, forestry and fishing",
        "divisions": [
            {
                "division": "01",
                "description": "Crop and animal production",
                "groups": [
                    {
                        "group": "011",
                        "description": "Growing of non-perennial crops",
                        "classes": [
                            {
                                "class": "0111",
                                "description": "Growing of cereals"
                            },
                            # ...
                        ]
                    },
                    # ...
                ]
            },
            # ...
        ]
    },
    # ...
]
```



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contributors

- [Abdullah Alqahtani](https://github.com/anqorithm)



## License

[MIT License](LICENSE)