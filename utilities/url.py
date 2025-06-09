# All helper functions for url formating or checking

# Check for required url
# is_valid_url: (str, str) -> bool
# interp. is_valid_url checks if a given url has the required destination and returns 
#         true if it does, else false
def is_valid_url(url: str, destination: str) -> bool:
    return url.find(destination) != -1


# Assemble url to the required page
# assemble_url: (str, str) -> str
# interp. assemble_url takes a base url removes any text and adds a destination and returns the full url
def assemble_url(base_url: str, remove: str, destination: str) -> str:
    base_url = base_url.replace(remove, "", 1)
    return f"{base_url}/{destination}"