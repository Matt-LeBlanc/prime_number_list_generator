#!/usr/bin/env python3
import datetime
import json
import math
import os
import sys
import time
from curtsies.fmtfuncs import yellow, bold, cyan
import concurrent.futures
import pickle

global loop_count, loop_time, num_of_cores, multiplier


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_primes(n1, n2):
    loop = 0
    primes = []
    time.sleep(0.1)
    for i in range(n1, n2):
        if is_prime(i):
            primes.append(i)
            loop += 1
            time.sleep(0.00000000001)
            if loop % 10_000 == 0:
                display_time()
    with open(f'{os.getcwd()}/prime_numbers.json', 'a') as f:
        json.dump(primes, f)


def display_time():
    global loop_count, loop_time
    os.system('clear')
    print('\n')
    print(yellow(bold(f"    Current Date: {datetime.datetime.now().strftime('%m/%d/%Y')} \n")))
    print(yellow(bold(f'    Elapsed Time: {time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))}  \n')))
    print(cyan(bold(f'    Loop Count: {loop_count} \n')))
    print(cyan(bold(f'    Loop Time: {time.strftime("%H:%M:%S", time.gmtime(time.time() - loop_time))}')))


def init_primes(a_list, b_list, number):
    global loop_count, loop_time
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(find_primes, a_list, b_list, )
    loop_count -= 1
    size = os.path.getsize(f'{os.getcwd()}/prime_numbers.json')
    size = size / (1024 * 1024)
    if size > 1024:
        size = size / 1024
        size = f'{size:.2f} GB'
    else:
        size = f'{size:.2f} MB'
    os.system('clear')
    print(f"    Current Date: {datetime.datetime.now().strftime('%m/%d/%Y')} \n")
    print(f'    Elapsed Time: {time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))} \n')
    print(f'    Loop Count: {loop_count} \n')
    print(f'    Loop Time: {time.strftime("%H:%M:%S", time.gmtime(time.time() - loop_time))}')
    print(f'    Size of prime_numbers.json: {size}  \n')
    with open('number.p', 'wb') as f:
        pickle.dump(number, f)
    time.sleep(1)
    main()


def main():
    global loop_count, loop_time, num_of_cores, multiplier
    while loop_count > 0:
        loop_time = time.time()
        with open('number.p', 'rb') as f:
            number = pickle.load(f)
            number -= 1
        a_list = []
        b_list = []
        for _ in range(num_of_cores):
            a_list.append(number + 1)
            number += multiplier
            b_list.append(number)
        time.sleep(0.1)
        init_primes(a_list, b_list, number)


if __name__ == '__main__':
    num_of_cores = 15
    core = 1
    multiplier = 1_000_000
    loop_count = 100
    start_time = time.time()
    loop_time = time.time()
    os.system('clear')
    print(cyan(bold(f"""
    ____  _                 _   _   __  __ _    ___ _   _  __ _ _   _ 

                        Prime Number List Generator

                        Date: {datetime.datetime.now().strftime('%m/%d/%Y')}

    ____  _      ___      ____ __ _    ___ _   _  __ _ _   _ ___ _   _                        
    """)))
    time.sleep(1.0)
    if not os.path.exists('number.p'):
        num = 1
        a = []
        b = []
        for _ in range(num_of_cores):
            a.append(num + 1)
            num += multiplier
            b.append(num)
        time.sleep(0.1)
        init_primes(a, b, num)
    else:
        main()
    sys.exit(0)
