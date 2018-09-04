import argparse
from src.exp_imp import Individuation

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='Subject ID', default='007')
    parser.add_argument('--tgt', help='Path to trial table',
                        default='tables/test.txt')
    parser.add_argument('--finger', help='Which finger to use',
                        default=0)
    args = parser.parse_args()

    demo = Individuation(id=args.id, finger=args.finger, trial_table=args.tgt)
    with demo.dev:
        demo.run()
