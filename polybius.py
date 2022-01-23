from utils import GroupsOfTwoError
'''
Implementation of the Polybius cipher - https://en.wikipedia.org/wiki/Polybius_square
By @ Mohammad Arafat Zaman
'''

'''
Polybius Cipher Base class 
'''
class Polybius:

    def __init__(self, keyword="ABCDEFGHIKLMNOPQRSTUVWXYZ"):
        self.KEYWORD = keyword.upper()
        self._sanitizeKeyword()
        self._createPolybiusGrid()
        self._UNIDENTIFIED_SYMBOL = "_"
        self._UNIDENTIFIED_GROUP = "-1"


    def _sanitizeKeyword(self):
        '''
        Removes all the duplicate chars from the keyword
        Removes all characters which are not present in the preset ALPHABETS
        Replace J with I since only 25 slots are available.
        If the length is less than 25, fill it with alphabets not present in the sanitized keyword
        Then remove the excess chars

        The keyword is still stored for future references
        '''
        ALPHABETS = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        self.SANITIZED_KEYWORD = ""

        for x in list(self.KEYWORD):
            # Replace J with I
            if x == "J":
                x == "I"

            if x not in self.SANITIZED_KEYWORD and x in ALPHABETS:
                self.SANITIZED_KEYWORD += x

        for x in ALPHABETS:
                if x not in self.SANITIZED_KEYWORD:
                    self.SANITIZED_KEYWORD += x
                
        if len(self.SANITIZED_KEYWORD) > 25:
            self.SANITIZED_KEYWORD = self.SANITIZED_KEYWORD[:25]
            

    def _createPolybiusGrid(self):
        '''
        Creates a 5x5 polybius grid with the sanitized keyword 
        '''
        self.GRID = []

        curr_row = [] 

        for i, j in enumerate(self.SANITIZED_KEYWORD):
            curr_row.append(j)

            if (i+1) % 5 == 0:
                self.GRID.append(curr_row)
                curr_row = []


    
    def __str__(self):
        '''
        This method is called when str() or print() is called so users can easily visualize the grid
        '''
        SPACES = 2
        HEADER = [" ", "1", "2", "3", "4", "5"]
        
        final_string = ""
        final_string += str(SPACES*" ").join(HEADER) + "\n"

        for i, j in enumerate(self.GRID):
            final_string += f"{str(i+1)}" + SPACES*" "
            for char in j:
                final_string += f"{char}" + SPACES*" "

            final_string += "\n"

        return final_string


    def encrypt(self, text="", UNIDENTIFIED_GROUP=None):
        '''
        Encrypt a text using the grid
        If a char is not present in the system, use -1
        '''
        encryptedText = ""

        for char in list(text):
            try:
                index = self.SANITIZED_KEYWORD.index(char)
            except ValueError:
                if UNIDENTIFIED_GROUP:
                    encryptedText += UNIDENTIFIED_GROUP
                else:
                    encryptedText += self._UNIDENTIFIED_GROUP
                continue
            
            # Calculate row and column
            # 1 is added since arrays are zero-indexed
            row = (index // 5) + 1
            column = (index % 5) + 1

            encryptedText += f"{str(row)}{str(column)}"

        return encryptedText

    def decrypt(self, encryptedText="", UNIDENTIFIED_SYMBOL=None):
        '''
        Decrypt the encrypted text following the grid system.
        -1 indicates that it has not been identified so use underscore (_) by default
        '''
        text = ""

        if len(encryptedText) % 2 != 0:
            raise GroupsOfTwoError("Encrypted text should be a multiple of two.")
        
        # Split into groups of two
        groups = []
        _bufferText = ""
        
        for x in encryptedText:
            _bufferText += x

            if len(_bufferText) == 2:
                groups.append(_bufferText)
                _bufferText = ""
        
        # Iterate through each groups and decipher using the row-column grid protocol
        for i in groups:

            if i == "-1" or not self._isValidGroup(i):
                if UNIDENTIFIED_SYMBOL:
                    text += UNIDENTIFIED_SYMBOL
                else:
                    text += self._UNIDENTIFIED_SYMBOL
            
            else:

                # 1 is subtracted to match with the zero-index rule of arrays
                rows = int(i[0]) - 1
                column = int(i[1]) - 1

                text += f"{self.GRID[rows][column]}"

        return text

    def _isValidGroup(self, group):
        '''
        Check if the group is a valid group from the grid system
        '''
        VALID_NUMBERS = ['1', '2', '3', '4', '5']

        for i in group:
            if i not in VALID_NUMBERS:
                return False
        
        return True
        


if __name__ == "__main__":

    cipher = Polybius()
    
    print(cipher)

    print(cipher.encrypt("HELLO WORLD"))

    print(cipher.decrypt("2315313134-15234423114"))
    
