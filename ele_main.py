import argparse
from ele_api import getData, getConsumption
from ele_parser import test_parse, parse_data, parse_consumption

class Greeting:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

def main():
    parser = argparse.ArgumentParser(description="Greet a user.")

    # Optional argument with default value
    parser.add_argument('--name', type=str, help='Name of the person to greet', default=None)
    parser.add_argument('--date', type=str, help='Name of the person to greet', default='now')
    # Obligatory positional argument
    #parser.add_argument('name', type=str, help='Name of the person to greet (required)')

    args = parser.parse_args()

    if args.name:
        greeting = Greeting(args.name)
        print(greeting.greet())

    mode = 0
    if args.date == 'now':
        mode = 1
    if args.date == 'tomorrow':
        mode = 2
    print (f"Date: {args.date} Mode: {mode}")

    data = getData(mode)
    #print (data)
    keys, values = parse_data(data)

    c = getConsumption()
    if c:
        parse_consumption(c)
    #test_parse()

if __name__ == "__main__":
    main()
