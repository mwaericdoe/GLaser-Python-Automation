# GLaser Python Automation

A Python-based automation tool for modifying text, barcode, and QR code objects in **GLaser**, the laser marking software used with Gweike G3 laser systems.

## Overview

This project allows you to automatically update the content of existing objects in an open GLaser project using Python.

The following object types are supported:

- Text objects
- Barcode objects
- QR code objects

Objects are selected by their position in the GLaser object list. Their content is then updated directly through the Windows UI Automation interface.

This can be useful for automating serial numbers, product labels, identification codes, and individual QR codes.

## Features

- Connects to an already running GLaser instance.
- Automatically brings the GLaser window to the foreground.
- Selects objects by their index in the object list.
- Updates text, barcode, and QR code content.
- Uses Windows UI Automation instead of simulated mouse or keyboard input.
- Provides a simple function call with three parameters.

**Important:** The script only modifies object content. It does not start a preview, marking, or engraving process.

## Requirements

- Windows
- Gweike laser system with GLaser installed
- Python 3
- An open GLaser project

Install the required Python packages:

```bash
pip install pywinauto pywin32
```

## Usage

The main function accepts three parameters:

```python
update_glaser_object(object_type, object_index, new_content)
```

| Parameter | Description |
|---|---|
| `object_type` | `"Text"`, `"Barcode"`, or `"QR-Code"` |
| `object_index` | Object position in the GLaser list, starting at `0` |
| `new_content` | The new content to write into the object |

### Examples

**Update a text object:**

```python
update_glaser_object("Text", 4, "12345")
```

**Update a barcode:**

```python
update_glaser_object("Barcode", 1, "123456789")
```

**Update a QR code:**

```python
update_glaser_object("QR-Code", 2, "https://example.com")
```

## Importing the function

If the Python code is saved as `glaser.py`, you can import it into another Python script:

```python
from glaser import update_glaser_object

update_glaser_object("Text", 4, "12345")
```

## How it works

The script uses:

- **pywinauto (UIA backend):** Accesses GLaser interface elements.
- **pywin32:** Activates the GLaser application window through the Windows API.
- **Windows UI Automation:** Selects objects and updates their associated input fields.

The automation follows these steps:

1. Connects to the running GLaser application.
2. Brings the GLaser window to the foreground.
3. Selects the requested object.
4. Locates the corresponding content input field.
5. Writes the new content.
6. Moves focus to another property field to commit the change.
7. Deselects the object.

## Compatibility and limitations

- GLaser must already be running.
- A project must already be open.
- Object indexes refer to the current order in the GLaser object list.
- The automation IDs are based on GLaser version `GLaser_v2.0.65_2026.04.24`.
- Changes to the GLaser interface may require adjustments to the automation IDs.
- The QR code workflow should be tested with the specific GLaser installation.
- The script does not start a laser marking or engraving operation.

## Safety recommendation

Always create a backup of your GLaser project before running automated modifications.

## License

This project can be published under the MIT License. Add a `LICENSE` file to the repository if you choose this license.
