import os

for key, value in os.env.items():
    globals()[key] = value
