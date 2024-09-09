import random
from BigHomework import *
import pytest

    
#create random-length string of random letters
def randWord():
    num = random.randint(1, 10)
    word = ""
    for i in range(num):
        l = chr(random.randint(65,122))
        word += l
    return word

# Test function to insert random words into the cuckoo hash and check the count
def test_insert():
    c = CuckooHash(10000)
    counter = 0
    for i in range(1000):
        word = randWord()
        if c.find(word):
            counter += 1
        c.insert(word, random.randint(1,100))
    counter += c.numItems
    assert counter == 1000

# Test function to insert random words into the cuckoo hash and check if they can be found
def test_find():
    c = CuckooHash(10000)
    words = []
    for i in range(1000):
        word = randWord()
        c.insert(word, random.randint(1,100))
        words.append(word)
    for word in words:
        assert c.find(word)

# Test function to insert random words into the cuckoo hash, delete them, and check count
def test_delete():
    c = CuckooHash(10000)
    words = []
    for i in range(1000):
        word = randWord()
        c.insert(word, random.randint(1, 100))
        words.append(word)
    for word in words:
        c.delete(word)
        
    assert c.numItems == 0
    
    for i in range(100):
        assert not c.find(randWord())

# Test function to grow hash and insert random words, checking count
def test_growHash():
    c = CuckooHash(10)
    counter = 0
    for i in range(10000):
        word = randWord()
        if c.find(word):
            counter += 1
        c.insert(word, random.randint(1,100))
    counter += c.numItems
    assert counter == 10000

# Test function with random operations (insert, delete) and count verification
def test_random():
    c = CuckooHash(100)
    count = 0
    
    for i in range(10000):
        choice = random.randint(0,1)
        word = randWord()
        
        if choice == 0:
            if not c.find(word):
                count += 1
            c.insert(word, word)
            
        if choice == 1:
            if c.find(word):
                count -= 1
            c.delete(word)
            
    assert count == c.numItems


# test function to check edge case of inserting and deleting the same item
def test_insertDeleteSameItem():
    c = CuckooHash(100)
    word = randWord()
    c.insert(word, 42)
    c.delete(word)
    assert not c.find(word)

# test function to check finding items that were not inserted
def test_findNonexistentItem():
    c = CuckooHash(100)
    assert c.find(randWord()) is None

# New test function to check deleting items that were not inserted
def test_deleteNonexistentItem():
    c = CuckooHash(100)
    assert c.delete(randWord()) is None
    
def test_torture():
    c = CuckooHash(100)
    count = 0
    
    for i in range(20000): 
        choice = random.randint(0,2)  
        word = randWord()
        
        if choice == 0:
            if not c.find(word):
                count += 1
            c.insert(word, word)
            
            # Check if the inserted word can be found
            assert c.find(word) == word
            
        elif choice == 1:
            if c.find(word):
                count -= 1
            c.delete(word)
            
            # Check if the deleted word cannot be found
            assert c.find(word) is None
            
        else:
            # Test rehashing after a certain number of insertions
            if i == 10000:
                assert c.numItems > 0  # Ensure some items are inserted before rehashing
                old_num_items = c.numItems
                old_table1 = c.table1[:]
                old_table2 = c.table2[:]
                
                c.rehash()
                
                # Check if all items are still in the hash table after rehashing
                for item in old_table1 + old_table2:
                    if item:
                        assert c.find(item.key) == item.data
                        
                # Check if the number of items is preserved after rehashing
                assert c.numItems == old_num_items

    assert count == c.numItems



pytest.main(["-v", "-s", "test_cuckooHash.py"])
