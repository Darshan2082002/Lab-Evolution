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

def extract_max(arr):
    n = len(arr)
    if n == 0:
        return None
    arr[0], arr[-1] = arr[-1], arr[0]
    max_val = arr.pop()
    max_heapify(arr, len(arr), 0)
    return max_val

n = int(input())
arr = list(map(int, input().split()))
build_max_heap(arr)
temp = arr.copy()
sorted_list = []
for _ in range(len(temp)):
    sorted_list.append(extract_max(temp))
print("Sorted Customer Details")
print(*sorted_list)
valuable_customers = sorted_list[:3]
print("Valuable Customers")
print(*valuable_customers)
deleted_customers = sorted_list[-2:]
print("Deleted Customers")
print(*deleted_customers)
updated_customers = sorted_list[:-2]
print("Customer Details after Deletion")
print(*updated_customers)
