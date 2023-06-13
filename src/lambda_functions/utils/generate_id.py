import uuid

def generate_random_uuid():
    random_uuid = uuid.uuid4().hex  # Generate a random UUID and convert it to hexadecimal representation
    return random_uuid