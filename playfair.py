from polybius import Polybius
from utils import GroupsOfTwoError, Override

'''
Implementation of the Playfair encryption algorithm - https://en.wikipedia.org/wiki/Playfair_cipher
By @ Mohammad Arafat Zaman
'''

# Base Playfair class
class Playfair(Polybius):
    BOGUS_LETTER = "X"
    '''
    Since Playfair uses a modified polybius grid, we will extend it to utilize its grid system 
    and override the encrypt and decrypt methods
    '''
    @Override
    def encrypt(self, text):
        '''
        Encrypt the text following the playfair encryption protocol
        '''
        text = text.upper()
        text = self._replaceJwithI(text)
        
        if len(text) % 2 != 0:
            text += self.BOGUS_LETTER
        
        # Split ---- 
        groups = []
        _bufferText = ""

        for x in text:
            _bufferText += x
            if len(_bufferText) == 2:
                # Clean the group before adding it to the stack
                '''
                _isClean returns 
                {
                    "clean" : bool
                    "value" : str
                }
                '''
                CLEANED = self._isClean(_bufferText)
                
                if CLEANED["clean"]:
                    # The group is clean
                    groups.append(_bufferText)
                    _bufferText = ""

                else:
                    # The group is not clean
                    groups.append(CLEANED["value"])
                    _bufferText = f"{_bufferText[1]}"

        '''
        If buffer is not empty, add the bogus letter and add it to the stack
        '''
        if len(_bufferText) != 0 and len(_bufferText) == 1:
            groups.append(_bufferText + self.BOGUS_LETTER)

        encryptedGroups = []
        # Iterate through each group and encrypt them --- 
        for i in groups:
            index1 = self.SANITIZED_KEYWORD.index(i[0])
            index2 = self.SANITIZED_KEYWORD.index(i[1])

            # Calculate rows and columns
            row1 = (index1 // 5) + 1
            column1 = (index1 % 5) + 1
            row2 = (index2 // 5) + 1
            column2 = (index2 % 5) + 1


            if row1 == row2:
                '''
                If they are in the same row
                '''
                # Update column
                column1 += 1
                column2 += 1
                # Wrap column
                column1 = self._wrapRowsAndColumns(column1)
                column2 = self._wrapRowsAndColumns(column2)
            
            elif column1 == column2:
                '''
                If they are in the same column
                '''
                # Update rows
                row1 += 1
                row2 += 1
                # Wrap rows
                row1 = self._wrapRowsAndColumns(row1)
                row2 = self._wrapRowsAndColumns(row2)

            else:
                '''
                Else form a imaginary rectangle
                Since they form a vertices
                Just simply swap columns
                '''
                _bufferColumn = column1
                column1 = column2
                column2 = _bufferColumn
            
            # -1 to match the zero index rule of arrays
            newGroup = f"{self.GRID[row1-1][column1-1]}{self.GRID[row2-1][column2-1]}"
            encryptedGroups.append(newGroup)
        
        encryptedText = ''.join(encryptedGroups)
        
        return encryptedText


    def _isClean(self, group):
        '''
        Checks if the group is clean.
        '''
        if len(group) != 2:
            raise GroupsOfTwoError("Text was not split into groups of two.")

        newGroup = group
        clean = True

        if group[0] == group[1]:
            newGroup =  f"{group[0]}{self.BOGUS_LETTER}"
            clean = False

        return {
            "clean": clean,
            "value": newGroup
        }
        
    def _wrapRowsAndColumns(self, rc):
        '''
        If a row or column is over the limit, bring it to the first one and vice versa
        '''

        if rc > 5:
            rc = rc - 5
        elif rc < 1:
            rc = rc + 5
        
        return rc

    @Override
    def decrypt(self, encryptedText):
        '''
        Decrypt the text reversing the encryption rules
        '''
        encryptedText = encryptedText.upper()
        encryptedText = self._replaceJwithI(encryptedText)

        if len(encryptedText) % 2 != 0:
            raise GroupsOfTwoError("Not a valid encrypted text.")

        # Split into groups ---
        groups = []
        _bufferText = ""

        for x in encryptedText:
            _bufferText += x
            if len(_bufferText) == 2:
                groups.append(_bufferText)
                _bufferText = ""

        decryptedGroups = []
        # Iterate through each group and decrypt th
        for i in groups:
            index1 = self.SANITIZED_KEYWORD.index(i[0])
            index2 = self.SANITIZED_KEYWORD.index(i[1])

            # Calculate rows and columns
            row1 = (index1 // 5) + 1
            column1 = (index1 % 5) + 1
            row2 = (index2 // 5) + 1
            column2 = (index2 % 5) + 1

            if row1 == row2:
                '''
                If they are in the same row
                '''
                # Update column
                column1 -= 1
                column2 -= 1
                # Wrap column
                column1 = self._wrapRowsAndColumns(column1)
                column2 = self._wrapRowsAndColumns(column2)
            
            elif column1 == column2:
                '''
                If they are in the same column
                '''
                # Update rows
                row1 -= 1
                row2 -= 1
                # Wrap rows
                row1 = self._wrapRowsAndColumns(row1)
                row2 = self._wrapRowsAndColumns(row2)

            else:
                '''
                Else form a imaginary rectangle
                Since they form a vertices
                Just simply swap columns
                '''
                _bufferColumn = column1
                column1 = column2
                column2 = _bufferColumn

            # -1 to match the zero index rule of arrays
            newGroup = f"{self.GRID[row1-1][column1-1]}{self.GRID[row2-1][column2-1]}"
            decryptedGroups.append(newGroup)
        
        _decryptedText = ''.join(decryptedGroups)

        # Remove bogus texts
        decryptedText = ""

        for x in _decryptedText:
            if x != self.BOGUS_LETTER:
                decryptedText += x
        
        return decryptedText

    def _replaceJwithI(self, text):
        ALPHABETS = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        new_text = ""
        for x in text:
            if x == "J":
                x = "I"

            if x not in ALPHABETS:
                x = ""
            new_text += x

        return new_text


if __name__ == "__main__":
    cipher = Playfair()
    print(cipher)
    print(cipher.encrypt("helloworld"))
    print(cipher.decrypt("KCNVMPYMQMCY"))