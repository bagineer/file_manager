def isNumber(num : str) -> bool:
    return _isInteger(num) or _isFloat(num)

def _isInteger(num : str) -> bool:
    try:
        _n = int(num)
        return True
    except:
        return False
    
def _isFloat(num : str) -> bool:
    try:
        _n = float(num)
        return True
    except:
        return False
    

if __name__ == "__main__":
    print("asdf", isNumber("asdf"))
    print("123", isNumber("123"))
    print("1sdf", isNumber("1sdf"))
    print("a2df", isNumber("a2df"))
    print("123.4", isNumber("123.4"))
    print("123.", isNumber("123."))
    print("123.0", isNumber("123.0"))
    print("123..", isNumber("123.."))
    print("0123", isNumber("0123"))