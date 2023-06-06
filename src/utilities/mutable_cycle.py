# @credits: github/gou177
def mutable_cycle(arr: list):
  while True:
    i = 0
    while i < len(arr):
       yield arr[i]
       i += 1
