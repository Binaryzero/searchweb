# Open the file in read mode
with open(filename, "r") as file:
    # Iterate over each line in the file
    for line in file:
        # Remove leading and trailing whitespaces from the line
        host = line.strip()
        try:
            # Send a GET request to the host
            response = requests.get(f"http://{host}")
            # If the status code is 200, the request was successful
            if response.status_code == 200:
                # Print a success message
                print(f"Successfully connected to {host}")
            else:
                # If the status code is not 200, the request failed
                print(f"Failed to connect to {host}")
        except Exception as e:
            # If an exception occurred during the request, print an error message
            print(f"Error connecting to {host}: {e}")
