'''
Some core utilities used along the project
'''
def Override(func):
    '''
    Override a method from the parent class
    '''
    def new_method(*args, **kwargs):
        return func(*args, **kwargs)

    return new_method


'''
This error is raised when the encrypted text is not a multiple of two
'''
class GroupsOfTwoError(Exception):
    pass
