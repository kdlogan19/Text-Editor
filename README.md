
**How to run the Program:**

    "python piece_table_editor.py"

I am on Windows machine so I am using corresponding dictionary path.

**Approach to the problem :** 

This was a interesting question and after looking at the assignment, first problem I could see with the editor was it was performing cut/paste operations on a string. As strings are immutable, each call to those functions were costing us generating a new string alltogther with complexity O(n). Another problem I saw with the "editor_mispellings" function. As in the dictionary there would be a lot of words and varying length, to check for a correct spelling would take comparisons of length of Hash-key size of dictionary.
I started with solving that problem first with our existing data strctures. Simply using list instead of string could have been better if there are very insert and delete operations otherwise it would also perform with similar complexity. 

Next, I came across a few data structures that are very useful in performing efficient string manipulations. There are three interesting data structures that intimidated me the most:
1. Gap Buffers
2. Rope 
3. Piece Table

I chose piece table as it has numerous advantage above others and unknowingly I have used this data structure in number of problems. In this data structure we keep original file intact and we keep a new buffer in which we only append. There is additional list of Piece objects which keep track of sequence of indexes. Only changes we have to made is either performing append operation to the buffer string and modification to piece objects. 

I found followig advantages of using Piece Table:
1. Original file is kept intact and we only append to buffer. This makes undo operations much easier.
2. We don't have to perform shift operations on string anymore. We only take care of their indexes.
3. File size is bounded by number of edits. 

To address the second problem, I designed a Trie. Lookup in a Trie would be much faster and it would go uptil O(k) (k = length of word). I also, created a set of word documents, which improved the performance (depending on type of words present) as there is no need of checking each word over and over again.


**Design Trade-offs:**

1. In the piece-table data structure we are storing two buffers, (original and edits) and list of piece nodes. To improve the performance we are using atleast the size of filespace. If there are significant amount of edits, we are saving all of them. In SimpleEditor methods the memory used was the size of file.  
2. For retrieving text of the whole file content, it has to go back and forth between two buffers based on the piecelist. For smaller file, it performs poor but for larger files, it works great.
3. To make dictionary lookup performance better we would have to make a Trie which would have a height of lengest word in the dictionarty and also each node might have upto 26 characters. We would save memory and lookup would be O(k) (k = length of word).


**Observations**:

After running the test cases, for small input string, the earlier editor is a suitable use but when I increase the size of the input, the PieceTableEditor significantly outperforms the simple editor by 1000X. 

Here are the test results:

Test cases:
 1. s1 = "hello friends"
 2. s2 = "hello friends" * 1000000

       **Simple Editor Result**

              Evaluating case: 1
              100 cut paste operations took 5.8499999999996055e-05 s
              100 copy paste operations took 4.470000000000168e-05 s
              100 text retrieval operations took 1.3800000000001311e-05 s
              100 mispelling operations took 5.350000000000493e-05 s
              Evaluating case: 2
              100 cut paste operations took 1.085579 s
              100 copy paste operations took 0.5340540000000003 s
              100 text retrieval operations took 1.5700000000062886e-05 s
              100 mispelling operations took 17.5898558 
              

       **Piece Table Editor Result**

              Evaluating case: 1
              100 cut paste operations took 0.0004702999999999999 s
              100 copy paste operations took 0.0004951000000000053 s
              100 text retrieval operations took 3.949999999999787e-05 s      
              100 mispelling operations took 0.0001229999999999981 s
              Evaluating case: 2
              100 cut paste operations took 0.0004813000000000178 s
              100 copy paste operations took 0.00032440000000000246 s
              100 text retrieval operations took 3.430000000004263e-05 s      
              100 mispelling operations took 10.969945899999999 s

**Extensions :**

I could only give handful hours to this project but if given more time following extensions would be great:
1. Undo operation would be a easy one and would be very handy for a text-editor.
2. Instead of Piece-list, I could have used AVL tree/ Binary Search, because most of the time of total computation is used in searching the correct piece in the piece list which is O(n) right now and can be decreased to O(log n).




