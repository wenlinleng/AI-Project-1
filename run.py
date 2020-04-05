from search.__main__ import main
import sys


if __name__ == '__main__':
    for i in range(1, 2):
        sys.argv = [
            '',
            'test/test_cases/test-level-{}.json'.format(i)
        ]
        print('{:.79}'.format('test-level-{}'.format(i) + '-' * 79))
        main()
        print('-' * 79)
        print()
