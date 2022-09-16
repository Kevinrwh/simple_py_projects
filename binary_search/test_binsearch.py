from binsearch import bin_search, random

length = 1000
test_list = set()

while len(test_list) < length:
     test_list.add(random.randint(-30*length, 30*length))
    
test_list = sorted(list(test_list))
test_target = random.choice(test_list)

def test_bin_search_true():
    assert bin_search(test_list, test_target, 0, length-1) == 'Found' 

def test_binsearch_false():
    assert bin_search (test_list, -80000, 0, length-1) == 'Not found'