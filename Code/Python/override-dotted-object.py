from pprint import pprint

def main():

    ## Dictionaries cannot be accessed via dot-notation
    try:
        d = dict()
        d.Name = "Not Valid Code"
    except AttributeError as e:
        print("Exception has occurred: AttributeError")
        print("'dict' object has no attribute 'Name'")
        pass

    ## Neither can base objects
    try:
        o = object()
        o.Name = "Not Valid Code"
    except AttributeError:
        print("Exception has occurred: AttributeError")
        print("'object' object has no attribute 'Name'")
        pass

    ## Generally you are supposed to inherit object and specifically define the variables you use
    class MyClass(object):
        __slots__ = 'foo', 'bar', 'Name'

    my = MyClass()
    my.Name = "Valid Code"
    print(my.Name)

    ## This is inconvenient to declare classes where not needed, additionally you can't dynamically add properties
    try:
        my.FirstName = my.Name
        my.LastName = "Not Valid Code"
        pprint(my.FirstName)
        pprint(my.LastName)
    except AttributeError:
        print("Exception has occurred: AttributeError")
        print("'MyClass' object has no attribute 'FirstName'")
        print("'MyClass' object has no attribute 'LastName'")
        pass

    ## Notice you also can't set properties on a NoneType, specifically for the next case
    try:
        args = None
        args.verbose = 0
    except AttributeError:
        print("Exception has occurred: AttributeError")
        print("'NoneType' object has no attribute 'verbose'")
        pass

    ## The solution is to use lambda's
    args = lambda: None
    args.verbose = 0
    pprint(args.verbose)


if __name__=="__main__":
    main()
