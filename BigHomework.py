#"I hereby certify that this program is solely the result of my own work and 
#is in compliance with the Academic Integrity policy of the course syllabus and 
#the academic integrity policy of the CS department.”

import time
import random
from BitHash import BitHash, ResetBitHash

class Item(object):
    def __init__(self, key, data):
        self.key = key
        self.data = data

class CuckooHash(object):
    def __init__(self, size):
        self.size = size
        self.numItems = 0
        self.table1 = [None] * size
        self.table2 = [None] * size
        self.__maxTry = 10
        
    def hash1(self, k):
        return BitHash(k) % self.size

    def hash2(self, k):
        return (BitHash(k) * 2) % self.size    
        
    def find(self, k):
        #indexes to look in each table
        index1 = self.hash1(k)
        index2 = self.hash2(k)
        
        #if find the item in the first table, return its data
        if self.table1[index1] is not None and \
           self.table1[index1].key == k:
            return self.table1[index1].data
            
        #if find the item in the second table, return its data
        elif self.table2[index2] is not None and \
           self.table2[index2].key == k:
            return self.table2[index2].data
            
        return None


    def insert(self, k, d):    
        #if the table is half full, rehash to bigger tables
        if self.numItems >= 0.5 * self.size:
            self.rehash()     
            
        item = Item(k, d)
        #if the item is already in the cuckoo hash then return
        if self.find(k):
            return 
        
        #ensure that there is no infinite loop
        for i in range(self.__maxTry):
            #indexs to look in each table
            index1 = self.hash1(item.key)
            index2 = self.hash2(item.key)
            
            #if index in the first table is empty then insert the item
            #and increment numItems
            if self.table1[index1] is None:
                self.table1[index1] = item
                self.numItems += 1
                return
            else:
                #if there is an item already there then
                #insert the item and make the new item what was in the index
                item, self.table1[index1] = self.table1[index1], item
    
            #repeat the process with the second table
            if self.table2[index2] is None:
                self.table2[index2] = item
                self.numItems += 1
                return
            else:
                item, self.table2[index2] = self.table2[index2], item
        
        # Rehash the tables if insertion fails after max attempts
        self.rehash()
        # Try to insert the item again after rehashing
        self.insert(item.key, item.data)

        
        
    def rehash(self):
        # Double the size of the tables
        self.size *= 2
        
        # Make two new references for the old tables
        old1 = self.table1
        old2 = self.table2
        
        # Create two new tables
        self.table1 = [None] * self.size
        self.table2 = [None] * self.size
        
        # Reinsert items from old tables to new tables
        for old_table in [old1, old2]:
            for item in old_table:
                if item:
                    # track if item has been successfully inserted
                    inserted = False
                    
                    # Try to insert the item into new tables
                    for i in range(self.__maxTry):
                        index1 = self.hash1(item.key)
                        index2 = self.hash2(item.key)
                        
                        # Try to insert into the first table
                        if not self.table1[index1]:
                            self.table1[index1] = item
                            inserted = True
                            break
                        # If collision occurs, insert item and 
                        #new item is previous item in that index
                        item, self.table1[index1] = self.table1[index1], item
                        
                        # Try to insert into the second table
                        if not self.table2[index2]:
                            self.table2[index2] = item
                            inserted = True
                            break
                        # If collision occurs, insert item and 
                        #new item is previous item in that index                        
                        item, self.table2[index2] = self.table2[index2], item
                    
                    # If the item couldn't be inserted after max attempts,
                    # resize the hash table and reinsert all items
                    if not inserted:
                        self.rehash()
                        return

        

    
    def delete(self,k):
        index1 = self.hash1(k)
        index2 = self.hash2(k)
        ans = None
        
        #if the key is in the first table, make that bucket refer to nothing
        if self.table1[index1] is not None and \
           self.table1[index1].key == k:
            self.numItems -= 1            
            ans = self.table1[index1].data            
            self.table1[index1] = None

            
        #if the key is in the second table, make that bucket refer to nothing
        elif self.table2[index2] is not None and \
           self.table2[index2].key == k:
            self.numItems -= 1
            ans = self.table2[index2].data            
            self.table2[index2] = None

    
        
        return ans
                    



#Tests:
    
hashTab = CuckooHash(5)

# insert
hashTab.insert("apple", 1)
hashTab.insert("banana", 2)
hashTab.insert("orange", 3)
hashTab.insert("grape", 4)

# test find
print("banana:" + str(hashTab.find("banana")))
print("orange:" + str(hashTab.find("orange")))  
print("grape:" + str(hashTab.find("grape")))   
print("cherry:" + str(hashTab.find("cherry")))

hashTab.insert("watermelon", 5)

#test find after rehash
print("apple:" + str(hashTab.find("apple"))) 
print("orange:" +  str(hashTab.find("orange")))
print("grape:" + str(hashTab.find("grape")))
print("watermelon:" + str(hashTab.find("watermelon")))


#test delete
print(hashTab.delete("banana"))
print("banana:" + str(hashTab.find("banana")))

c = CuckooHash(10)

for i in range(100):
    c.insert(str(i),i)
    
print('table 1:')
for i in range(c.size):
    if c.table1[i]:
        print(c.table1[i].key)
print('table 2:')
for i in range(c.size):
    if c.table2[i]:
        print(c.table2[i].key)
        
print(c.find('95'))