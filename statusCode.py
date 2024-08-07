statusCodeDict = {
    "200 OK": "Login successful!",
    "201 Created": "Sign-up successful!",
    "202 Booked": "Booked successfully!",
    "204 No Content": "Session ended successfully.",
    "400 Bad Request": "Invalid command.",
    "401 Unauthorized": "Invalid username or password.",
    "409 Conflict": "Username already exists.",
    "423 Already Booked": "This seat is booked.",
    "500 Internal Server Error": "An error occurred.",
    "502 Error": "Error reading seats file, using default seats."
}

def statusCodeToMessage(status_code):
    try:
        return statusCodeDict[status_code]
    except KeyError:
        return "Unknown status code."
