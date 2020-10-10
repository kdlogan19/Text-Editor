#Trie Node Class
class TrieNode: 
    def __init__(self): 
        self.children = {}
        self.isWord = False

#Trie Class
class Trie:
    #constructor 
    def __init__(self): 
        self.root = TrieNode()
    
    #inserting node by traversing each level 
    #corresponding to each character of given word
    def insert(self, word):
        node = self.root
        for i in word:
            if i not in node.children:
                node.children[i] = TrieNode()                
            node = node.children[i]
        node.isWord = True
    
    #search a node by traversing each level 
    #corresponding to each character of given word
    #At the end, we return last character's node's "isWord" value
    def search(self, word): 
        node = self.root 
        length = len(word) 
        for i in word:
            if i not in node.children:
                return False               
            node = node.children[i]
        return node.isWord