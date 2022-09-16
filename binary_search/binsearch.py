# Proving binary search is faster than naïve search.

# Naive approach
def naive_search(l, target):
    for i in range(len(l)):
        if target == l[i]:
            return 'Found'
    
    return 'Did not find'

# Recursive binary search
def bin_search(l, target, low, high):

    # Base case: Target not in list
    if low > high:
        return 'did not find'
    
    mid = (low + high)/2

    # Determine is at middle or search in left and right sublists
    if target == l[mid]:
        return 'Found'
    elif target > l[mid]: # right side
        return bin_search(l, target, mid+1, high)
    else: # left side
        return bin_search(l, target, low, mid-1)

