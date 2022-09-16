# Proving binary search is faster than naïve search.
import random, time

# Naive approach
def naive_search(l, target):
    for i in range(len(l)):
        if target == l[i]:
            return 'Found'
    
    return 'Not found'

# Recursive binary search
def bin_search(l, target, low, high):

    # Base case: Target not in list
    if low > high:
        return 'Not found'
    
    mid = (low + high)// 2

    # Determine is at middle or search in left and right sublists
    if target == l[mid]:
        return 'Found'
    elif target > l[mid]: # right side
        return bin_search(l, target, mid+1, high)
    else: # left side
        return bin_search(l, target, low, mid-1)

length = 1000
test_list = set()

while len(test_list) < length:
    test_list.add(random.randint(-30*length, 30*length))

test_list = sorted(list(test_list))
test_target = random.choice(test_list)


print('Searching for {}'.format(test_target))

# Search for the target using 
start = time.time()
naive_search(test_list,test_target)
end = time.time()
print('Naive search took {}'.format(end-start))

start = time.time()
bin_search(test_list, test_target, 0, len(test_list)-1)
end = time.time()
print('Binary search took {}'.format(end-start))