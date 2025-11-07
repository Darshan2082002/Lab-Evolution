def max_heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)

def build_max_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)

def heap_sort(arr):
    n = len(arr)
    build_max_heap(arr)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        max_heapify(arr, i, 0)
    return arr

n = int(input())
arr = list(map(int, input().split()))


heap_sort(arr)
arr.reverse()  

print("Sorted Customer Details")
print(*arr)

valuable_customers = arr[:3]
print("Valuable Customers")
print(*valuable_customers)

deleted_customers = arr[-2:]
print("Deleted Customers")
print(*deleted_customers)

updated_customers = arr[:-2]
print("Customer Details after Deletion")
print(*updated_customers)
