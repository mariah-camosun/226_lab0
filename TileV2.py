class Tile:
    def __init__(self):
        self.contents="empty"

    def __init__(self, xcoord: int, ycoord: int):
        self.contents="empty"
        self.xcoord=xcoord
        self.ycoord=ycoord

    def __str__(self):
        '''
        Display the Contents of the tile

        :return self.contents.name: the 'name' of the contents item
        '''
        return f'{self.contents.name}'

    def clearContents():
        '''
        Empty the Contents of the tile
        '''
        self.contents="empty"

    def addContents( content: enumOrClass? ):
        '''
        Change or add new contents to the tile

        :param content: the 'class or enum' of the contents item to add
        '''
        self.contents=content

    def findCoords():
        '''
        get position of this Tile
        :return: array of [x,y] position coordinates [int, int]
        '''
        return [self.xcoord, self.ycoord]
# should teh tile track xy coords or the board?
# can i have multiple init statements?