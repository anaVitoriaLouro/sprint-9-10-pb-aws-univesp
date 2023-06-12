import uuid

def generate_random_uuid():
    # Generate a random UUID and convert it to hexadecimal representation
    random_uuid = uuid.uuid4().hex
    return random_uuid