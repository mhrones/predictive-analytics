#
# CICS 397A Homework 0
#
# Fill in the bodies of the missing functions as specified by the comments and docstrings.
#
import random

# Exercise 1
#
def three_lens(list_one, list_two, list_three):
    """Return the lengths of three sequences (tuples, lists, or strings) as a list.

    Hint: check out the Python docs on built-in functions for getting the length of a sequence:
    https://docs.python.org/3/library/functions.html

    """
    #
    # fill in function body here
    #
    x = len(list_one)
    y = len(list_two)
    z = len(list_three)

    return [x, y, z]  # replace this line!


# Exercise 2
#
def splice_em(list_one, list_two):
    """Splice two equal-length lists together.

    Returns a list with alternating elements from the two lists.  For example:
    splice_em(['a', 'b', 'c'], [1, 2, 3]) => ['a', 1, 'b', 2, 'c', 3]

    Hint: you'll probably want to use a for or while loop to iterate.  The enumerate() or zip()
    built-in functions might be helpful here: https://docs.python.org/3/library/functions.html

    """
    #
    # fill in function body here
    #
    len1 = len(list_one)
    len2 = len(list_two)
    spliced_len = len1+len2

    spliced = [0]*spliced_len
    counter = 0
    for x in range(0, len1):
        spliced[counter] = list_one[x]
        spliced[counter+1] = list_two[x]
        counter = counter + 2

    return spliced  # replace this line!


# Exercise 3
#
def smush_em(*args):
    """Take all arguments, put them in a string separted by the pipe character ('|').

    Hint: the method signature uses a special syntax for capturing a variable number of function
    arguments.  See: https://www.geeksforgeeks.org/args-kwargs-python/

    To build the return string, you can concatenate the arguments one at a time or all at once
    using join().  Also note that the arguments passed in might not alrady be strings, if that's
    the case you'll need to convert them using str().  See:
    https://docs.python.org/3/library/stdtypes.html#string-methods

"""
    #
    # fill in function body here
    #
    string = ""
    for arg in args:
        if isinstance(arg, str):
            string = string+arg
        else:
            convert = str(arg)
            string = string+convert
        string = string+"|"
    string = string[0:len(string)-1]
    return string  # replace this line!


# Exercise 4
#
def is_increasing(numbers):
    """  Returns True if list of numbers is strictly increasing, False otherwise.
    """
    #
    # fill in function body here
    #
    x = len(numbers)

    for x in range(0, x-1):
        if(x==0):
            continue
        if(numbers[x] < numbers[x-1]):
            return False

    return True  # replace this line!


# Exercise 5
#
def factorial(n):
    """Recursive function for calculating the factorial function.

    Hint: recall that a recursive function is one that calls itself (usually on a simpler version)
    of the problem, grounded out in some trivial "base case".  For this example, you can calculate
    the factorial of some number n in terms of the value for n-1, with factorial(0) returning 1.
    """
    #
    # fill in function body here
    #
    if n == 0:
        return 1
    result = 1
    result = n * factorial(n-1)


    return result


# Exercise 6
#
def pairwise_sums(primo, secondo):
    """Returns a list of the sums of all possible combinations of elements from two lists.

    Hint: use a nested loop to iterate through boths lists, and make sure you maintain the same
    order of the elements.  For example: pairwise_sums([0, 3, 6], [9, 2]) => [9, 2, 12, 5, 15, 8]

    """
    #
    # fill in function body here
    #
    len1 = len(primo)
    len2 = len(secondo)
    final_len = len1*len2
    final = [0]*final_len
    counter = 0

    for x in primo:
        for y in secondo:
            final[counter] = x+y
            counter = counter + 1


    return final  # replace this line!


# Exercise 7
#
def char_counts(some_text):
    """Return a dictionary containing each character in the text as keys, and the number of times
    they occur as values.

    Hint: recall that since a string is a sequence, you can loop through it as you would a list.
    For help with dictionaries, see the Python docs:
    https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

    """
    #
    # fill in function body here
    #
    my_text = some_text.lower()
    clean_text = my_text.replace(" ","").replace("!","")

    dictionary = {}

    for i in clean_text:
        dictionary[i] = dictionary.get(i,0)+1

    return dictionary  # replace this line!


# Exercise 8
#
def add_mult_equal(primero, segundo):
    """Returns true if the sum of the first list of numbers is equal the product of the second.

    Hint: Pythong has a built-in function for calculating the sum of a list of numbers.  For the
    product, you'll have to do it yourself.

    """
    #
    # fill in function body here
    #

    sum = 0
    product = 1

    for x in primero:
        sum = sum+x

    for y in segundo:
        product = product*y

    if(sum == product):
        return True
    else:
        return False



# Exercise 9
#
def coin_flip():
    """Return "heads" or "tails", with a 0.5 probability for each.

    Hint: to generate a random number, you'll need to use Python's random module:
    https://docs.python.org/3/library/random.html

    """
    #
    # fill in function body here
    #
    value = random.randint(0,1)
    if value == 0:
        return "heads"
    if value == 1:
        return "tails"




# Exercise 10
#
def bleep(some_text, bad_words):
    """Censors some text by replacing a Python set of "bad words" with asterisks.

    Hint: you can assume that the text contains no punctuation.  However, you must account for
    different capitalization of the letters.  See the docs for some helpful methods:
    https://docs.python.org/3/library/stdtypes.html#string-methods)

    Also, make sure your replacement strings have the same number of characters as the bad words.
    One way to do this is to use the multiplication operator with the string '*':
    https://www.pythoncentral.io/use-python-multiply-strings/

    """
    #
    # fill in function body here
    #
    words = some_text.split()
    result_string = ""

    index = 0

    for x in words:
        for y in bad_words:
            if x == y:
                words[index] = "*"*len(y)
        result_string = result_string+words[index]+" "
        index+=1
    final_string = result_string[0:len(result_string)-1]
    return final_string  # replace this line!


# The main() function below will be executed when your program is run.  Note that Python does not
# require a main() function, but it is considered good style.  The comments on each line show
# what shold be output if your code is running correctly.
def main():
    print(three_lens("397A", (42,), ['y', 'y', 'z']))       # [4, 1, 3]
    print(splice_em(['r', 'd'], [2, 2]))                    # ['r', 2, 'd', 2]
    print(smush_em("this", "must", "be", "the", "place"))   # this|must|be|the|place
    print(is_increasing([0, 3, 5, 7, 6, 8]))                # False
    print(factorial(6))                                     # 720
    print(pairwise_sums([2, 4, 6], [1, 3]))                 # [3, 5, 5, 7, 7, 9]
    print(char_counts("slanted and enchanted")['e'])        # 3
    print(add_mult_equal([19, 99], [59, 2]))                # False
    print(coin_flip())                                      # heads OR tails
    print(bleep("Shut the front door", {"door", "front"}))  # Shut the ***** ****


###################################

# The line below is a common Python idiom for creating Python programs that have useful functions.
# For more info, see: https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/
if __name__ == '__main__':

    main()
