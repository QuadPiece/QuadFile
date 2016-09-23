# Very, very simple auth feature.
def basicauth(key, configured):
  if configured == "":
    return True
  elif configured == key:
    return True
  else:
    return False