
# Import the function to update objects in GLaser
from glaser import update_glaser_object

# Import datetime to retrieve the current date
from datetime import datetime

# Get today's date in DD.MM.YYYY format
today = datetime.now().strftime("%d.%m.%Y")

# Update the content of the first Text object (index 0) in GLaser
update_glaser_object("Text", 0, today)
