numbers = [2, 16, 20, 4, 7, 12, 14, 5, 18]


def bubble_sort(values: list[int]) -> list[int]:
    arr = values.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


if __name__ == "__main__":
    print(bubble_sort(numbers))