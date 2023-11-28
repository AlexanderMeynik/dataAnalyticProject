#some junk file with example
from dbService import databaseService;
def print_hi(name):
    db= databaseService();
    a=db.getTopTag(10)
    b=db.getTagsDynamics('COVID-19')

    #print(a,len(a))


    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

