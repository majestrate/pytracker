import pytracker
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--action", default="run")
    args = ap.parse_args()
    action = args.action.lower()
    if action == 'run':
        pytracker.run(debug=True)
    elif action == 'nuke':
        pytracker.nuke()
    elif action == 'seed':
        pytracker.seed()


if __name__ == '__main__':
    main()
