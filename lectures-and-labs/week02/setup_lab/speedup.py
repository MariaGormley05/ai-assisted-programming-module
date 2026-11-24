"""Make your code faster."""
import time

STAGES = ("Analysing", "Optimising", "Rewriting", "Finalising")

for stage in STAGES:
    print(f"{stage}...", end="", flush=True)
    time.sleep(0.6)
    print(" ok")

print("Done. Your code is now exactly as fast as it was before.")
