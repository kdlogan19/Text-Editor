import Trie
from Piece import Piece

class PieceTableEditor:
   
   #Initialization 
    def __init__(self, document):
        self.textLength = len(document)
        self.original = document
        self.buffer = ""
        self.pieces = [Piece(False, 0, len(document))]
        self.dictionary = Trie.Trie()
        # On windows, the dictionary can often be found at:
        # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
        with open("C:/Users/kirti/AppData/Roaming/Microsoft/Spelling/en-US/default.dic") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.insert(word.lower())
        self.pasteText = ""

    #Insert text at a particular index
    def insert(self, text, index):
        if not len(text):
            return
        # Finding piece that overlaps the given index
        pieceIndex, pieceOffset = self.getPieceIndexAndOffset(index)
        current = self.pieces[pieceIndex]

        # Append text to added buffer
        added_offset = len(self.buffer)
        self.buffer += text
        self.textLength += len(text)

        # If insertion is at the end and the piece points to the end of the add buffer,
        # just increase the length
        if (current.inBuffer
            and pieceOffset == current.offset + current.length == added_offset):
            current.length += len(text)
            return

        # Spliting into three pieces
        insertPiece = []
        insertPiece.append( Piece(current.inBuffer, current.offset, pieceOffset - current.offset))
        insertPiece.append(Piece(True, added_offset, len(text)))
        insertPiece.append(Piece(current.inBuffer,pieceOffset,current.length - (pieceOffset - current.offset)))
        insertPiece = list(filter(lambda piece: piece.length > 0, insertPiece))
        self.pieces = self.replacePieces(pieceIndex, 1, insertPiece)
    
    
    def getPieceIndexAndOffset(self, index):
        remainingOffset = index
        for i in range(len(self.pieces)):
            piece = self.pieces[i]
            if remainingOffset <= piece.length:
                return (i, piece.offset + remainingOffset)
            remainingOffset -= piece.length

    def replacePieces(self, start, replace_count, items):
        return self.pieces[:start] + items + self.pieces[start + replace_count:]

    def delete(self, index, length):
       
        if length == 0:
            return
        if length < 0:
            self.delete(index + length, -length)
            return
        if index < 0:
            raise IndexError("Text index out of range")

        # Get overlapping pieces
        startIndex, startOffset = self.getPieceIndexAndOffset(index)
        stopIndex, stopOffset = self.getPieceIndexAndOffset(index + length)
        self.textLength -= length

        # If single piece, check if delete is at the start or end the piece
        if startIndex == stopIndex:
            piece = self.pieces[startIndex]

            if startOffset == piece.offset:
                piece.offset += length
                piece.length -= length
                return
            elif stopOffset == piece.offset + piece.length:
                piece.length -= length
                return

        startPiece = self.pieces[startIndex]
        endPiece = self.pieces[stopIndex]

        # Spliting into two pieces
        deletePieces = []
        deletePieces.append(Piece(startPiece.inBuffer,startPiece.offset,startOffset - startPiece.offset))
        deletePieces.append(Piece(startPiece.inBuffer,startPiece.offset,startOffset - startPiece.offset,))
        deletePieces.append(Piece(endPiece.inBuffer,stopOffset,endPiece.length - (stopOffset - endPiece.offset)))

        deletePieces = list(filter(lambda piece: piece.length > 0, deletePieces))

        delete_count = stopIndex - startIndex + 1
        self.pieces = self.replacePieces(
            startIndex, delete_count, deletePieces
        )

    def get_text(self):

        document = ""
        for piece in self.pieces:
            if piece.inBuffer:
                document += self.buffer[piece.offset:piece.offset + piece.length]
            else:
                document += self.original[piece.offset:piece.offset + piece.length]
        return document

    #Getting string of length at an index 
    def getString(self, index, length):
        if length < 0:
            return self.getString(index + length, -length)

        document = ""

        # Get overlapping pieces
        startIndex, startOffset = self.getPieceIndexAndOffset(index)
        stopIndex, stopOffset = self.getPieceIndexAndOffset(index + length)

        startPiece = self.pieces[startIndex]
        buffer = self.buffer if startPiece.inBuffer else self.original

        # If single piece, return text from piece
        if startIndex == stopIndex:
            document = buffer[startOffset:startOffset + length]
        else:
            document = buffer[startOffset:startPiece.offset + startPiece.length]
            for i in range(startIndex + 1, stopIndex + 1):
                cur_piece = self.pieces[i]
                buffer = self.buffer if cur_piece.inBuffer else self.original

                # If the ending piece, only add remaining length to the string
                if i == stopIndex:
                    document += buffer[cur_piece.offset:stopOffset]
                else:
                    document += buffer[cur_piece.offset:cur_piece.offset + cur_piece.length]

        return document
    
    def cut(self, i, j):
        self.pasteText = self.getString(i, j-i)
        self.delete(i, j-i)
    
    def copy(self, i, j):
        self.pasteText = self.getString(i, j-i)

    def paste(self, i):
        self.insert(self.pasteText, i)
    
    def misspellings(self):
        result = 0
        doc = self.get_text()
        doc = set(doc.split(" "))
        for word in doc:
            if not self.dictionary.search(word):
                result = result + 1
        return result


import timeit

class EditorBenchmarker:
    new_editor_case = """
from __main__ import PieceTableEditor
s = PieceTableEditor("{}")"""

    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(3, 5)
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, 3)
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""

    def __init__(self, cases, N):
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)

    def benchmark(self):
        for i, case in enumerate(self.cases):
            print("Evaluating case: {}".format(i+1))
            new_editor = self.new_editor_case.format(case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))
            

if __name__ == "__main__":
    s1 = "hello friends"
    s2 = "hello friends" * 1000000
    s3 = "This was  ainteresting question and after looking at the assignment, first problem I could see with the editor was it was performing cut/paste operations on a string. As strings are immutable, each call to those functions were costing us generating a new string alltogther with complexity O(n). Another problem I saw with the editor_mispellings function. As in the dictionary there would be a lot of words and varying length, to check for a correct spelling would take comparisons of length of key size of dictionary. I started with solving that problem first with our existing data strctures. Simply using list instead of string could have been better if there are very insert and delete operations otherwise it would also perform with similar complexity"
    b = EditorBenchmarker([s1, s2, s3], 100)    
    b.benchmark()



