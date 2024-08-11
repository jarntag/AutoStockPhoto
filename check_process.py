class CheckProcess :
    def __init__(self):
        pass

    def check_path(path):
        try:
            if path is None:
                pathcheak = False
                print("please select path1")
                
            else:
                pathcheak = True
        except NameError:
            pathcheak = False
            print("please select path2")
            
        return pathcheak