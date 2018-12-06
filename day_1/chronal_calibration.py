import argparse
import logging


def get_frequency(start=0,
                  input_file='input.txt',
                  logger=None,
                  dupe=False,
                  verbose=False):
    logger = logger or logging.getLogger(__name__)
    reached = set()
    running = start
    found = False
    with open(input_file) as f:
        lines = f.readlines()
    if verbose:
        logger.info(f'input read: {len(lines)} lines')
    if dupe:
        while not found:
            found, running, reached = find_result(lines,
                                                  running,
                                                  reached,
                                                  verbose)
    else:
        _, running, reached = find_result(lines,
                                          running,
                                          reached,
                                          verbose)
        logger.info(f'Total: {running}')


def find_result(lines, running, reached, verbose=False):
    logger = logging.getLogger(__name__)
    for line in lines:
        line = line.strip()
        reached.add(running)
        oper = line[0]
        val = int(line[1:])
        if oper == '+':
            running += val
        else:
            running -= val
        if verbose:
            status = f'input: {line}, result: {running}'
            logger.info(status)
        if running in reached:
            logging.info(f'Duplicate found: {running}')
            return True, running, reached
    return False, running, reached


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--start',
        default=0
    )
    parser.add_argument(
        '-f',
        '--file',
        default='input.txt'
    )
    parser.add_argument(
        '-d',
        '--duplicate',
        action='store_true'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true'
    )
    parser.add_argument('--log_level', default='INFO')
    args = parser.parse_args()
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=args.log_level, format=log_fmt)
    get_frequency(start=args.start,
                  input_file=args.file,
                  dupe=args.duplicate,
                  verbose=args.verbose)
