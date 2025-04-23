def search(arr):
    if len(arr) < 7:
        return -1
    max_fives = -1
    current_fives = 0
    sequence = False
    counter_elements = 0
    for i in range(0, len(arr)):
        if arr[i] == 5:
            current_fives += 1
            counter_elements += 1
        elif arr[i] == 2 or arr[i] == 3:
            counter_elements = 0
            current_fives = 0
            sequence = False
        else:
            counter_elements += 1

        if sequence:
            if arr[i - 7] == 5:
                current_fives -= 1
                counter_elements -= 1
            else:
                counter_elements -=1

        if counter_elements == 7:
            max_fives = max(max_fives, current_fives)
            sequence = True
    return max_fives


n = int(input())
arr1 = list(map(int, input().split()))
print(search(arr1))
