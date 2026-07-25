import hashlib

def sha256(filepath):
  hash = hashlib.sha256()
  with open(filepath, "rb") as file:
    while chunk := file.read(8192):
      hash.update(chunk)
  return hash.hexdigest()