statusCodeDict = {
    "200": "Login successful!",
    "201": "Sign-up successful!",
    "202": "Booked successfully!",
    "204": "Session ended successfully.",
    "400": "Invalid command.",
    "401": "Invalid username or password.",
    "409": "Username already exists.",
    "423": "This seat is booked.",
    "500": "An error occurred.",
    "502": "Error reading seats file, using default seats."
}

def statusCodeToMessage(status_code):
    try:
        return statusCodeDict[status_code]
    except KeyError:
        return "Unknown status code."
