def print_tree(arr, level=0):
    indent = "   " * level
    print(f"{indent}{arr}")

    if len(arr) <= 1:
        return

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    print_tree(left, level + 1)
    print_tree(right, level + 1)


if __name__ == "__main__":
    arr = [1, 3, 3, 3, 5, 3, 8, 2, 4, 3]
    print_tree(arr)