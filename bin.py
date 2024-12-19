import os


def get_next_filename(directory="examples"):
    max_number = 0

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # List the files in the directory
    for filename in os.listdir(directory):
        # Check if the filename matches the expected format
        if filename.endswith("-output.md"):
            try:
                # Extract the number part
                number = int(filename.split("-")[0])
                # Update max_number if this number is larger
                if number > max_number:
                    max_number = number
            except ValueError:
                continue

    # The next number in sequence
    next_number = max_number + 1
    # Construct the filename
    new_filename = f"{next_number}-output.md"
    return os.path.join(directory, new_filename)


if __name__ == '__main__':
    filename = str(get_next_filename())
    cmd = f'cp output.md {filename}'
    print(cmd)
    os.system(cmd)

