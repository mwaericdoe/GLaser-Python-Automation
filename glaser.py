
import time

import win32gui
from pywinauto import Application


def update_glaser_object(object_type, object_index, new_content):
    """
    Update the content of an existing object in GLaser.

    Args:
        object_type (str):
            "Text", "Barcode", or "QR-Code".

        object_index (int):
            Position of the object in the GLaser object list.
            The index starts at 0.

        new_content (str):
            New content to write into the object.
    """

    # Base path for the object property controls
    base_path = (
        "MainWindow.centralWidget.widget_ViewArea.widget_docView."
        "widget_docDock_background.ObjPropertyWidget.widget_obj_background."
        "widget_prop."
    )

    # Input field and focus field for each supported object type
    object_fields = {
        "text": (
            base_path
            + "TextWidget_GWK.widget_variant.widget_3.edit_content",
            base_path
            + "TextWidget_GWK.le_wordSpacing",
            "Edit"
        ),
        "barcode": (
            base_path
            + "BarWidget.widget_variant.widget_3.edit_content",
            base_path
            + "BarWidget.wg_FontSetting.cb_FontSize",
            "ComboBox"
        ),
        "qr-code": (
            base_path
            + "QrCodeWidget.widget_variant.widget_3.edit_content",
            base_path
            + "QrCodeWidget.widget_2.combo_barType",
            "ComboBox"
        )
    }

    # Normalize the object type
    normalized_type = object_type.strip().lower()

    if normalized_type not in object_fields:
        raise ValueError(
            "Invalid object type. Use 'Text', 'Barcode', or 'QR-Code'."
        )

    content_field_id, focus_field_id, focus_control_type = (
        object_fields[normalized_type]
    )

    # Connect to the running GLaser application
    app = Application(backend="uia").connect(path="GLaser.exe")
    window = app.window(title="Glaser")

    # Bring GLaser to the foreground
    hwnd = window.handle
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)

    # Verify that GLaser is actually in the foreground
    if win32gui.GetForegroundWindow() != hwnd:
        raise RuntimeError(
            "Could not bring the GLaser window to the foreground."
        )

    # Locate the object list
    object_list = window.child_window(
        auto_id=(
            "MainWindow.centralWidget.widget_ViewArea.rightPanel."
            "scrollArea.qt_scrollarea_viewport.ContentPanel."
            "ObjListDock.widget.widget_objlist.list_objList"
        ),
        control_type="List"
    )

    # Retrieve all objects from the list
    objects = object_list.descendants(control_type="ListItem")

    # Check whether the requested object index exists
    if not 0 <= object_index < len(objects):
        raise IndexError(
            f"Object index {object_index} is invalid. "
            f"Available objects: {len(objects)}"
        )

    # Select the requested object
    objects[object_index].select()
    time.sleep(0.3)

    # Locate the content input field
    content_field = window.child_window(
        auto_id=content_field_id,
        control_type="Edit"
    )

    # Write the new content
    content_field.set_edit_text(new_content)

    # Move focus to another property field to commit the change
    focus_field = window.child_window(
        auto_id=focus_field_id,
        control_type=focus_control_type
    )

    focus_field.set_focus()
    time.sleep(0.2)

    # Deselect the object to finish the modification
    objects[object_index].iface_selection_item.RemoveFromSelection()

    print(
        f"{object_type} object at index {object_index} "
        f"updated successfully: '{new_content}'"
    )


# Example calls:
# update_glaser_object("Text", 4, "12345")
# update_glaser_object("Barcode", 1, "123456789")
# update_glaser_object("QR-Code", 2, "https://example.com")
