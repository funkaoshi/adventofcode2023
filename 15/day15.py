import argparse


def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store", default="test.txt")
    args = parser.parse_args()

    filename = args.filename

    with open(filename) as f:
        file = f.read().splitlines()

    for line in file:
        commands = line.split(",")
        hashes = [hash(command) for command in commands]
        print(hashes)
        print(sum(hashes))
