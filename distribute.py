import random
import math
import os

headers = '''// Insert student names below
// Separate each name with newlines

// Use "//" infront of the names to ignore the line or the names
// Example: // Galactic647
'''

try:
    with open('student names.txt') as file:
        students = [line.strip() for line in file.readlines()
                    if not line.strip().startswith('//') and line.strip()]
        n_students = len(students)
        file.close()
except FileNotFoundError:
    with open('student names.txt', 'w') as file:
        file.write(headers)
        file.close()
    students = ()


def error_message(message: str) -> None:
    print(message)
    input()
    os.system('cls')


def distribute_by_group(n: int, k: int) -> tuple:
    if k > n:
        raise ValueError("k can't be bigger than n")
    member = math.ceil(n / k)
    max_ = n % k
    max_ = max_ if max_ else k
    return tuple([member] * max_ + [member - 1] * (k - max_))


def distribute_by_member(n: int, k: int) -> tuple:
    if k > round(n / 2):
        raise ValueError("k can't be bigger than n / 2")
    group = int(n / k)
    max_ = n % group
    result = tuple([k + 1] * max_ + [k] * (group - max_))
    if sum(result) != n:
        error_message(f"Can't create group with {k} members")
        return None
    return result


def construct(method: int, limit: int) -> None:
    if method == 1:
        indexes = distribute_by_member(n_students, limit)
    else:
        indexes = distribute_by_group(n_students, limit)

    if indexes is not None:
        groups = []
        for index in indexes:
            members = random.sample(students, k=index)
            groups.append(members)
            for member in members:
                students.remove(member)
        save(groups)


def save(data: tuple) -> None:
    text = [f'Number of students : {n_students}\n']
    for index, group in enumerate(data, start=1):
        text.append(f'Group {index}')
        for order, member in enumerate(group, start=1):
            text.append(f'{order}. {member}')
        text.append('')
    with open('groups.txt', 'w') as f:
        f.write('\n'.join(text))
        f.close()


def main() -> None:
    method = ''
    while True:
        try:
            method = input('Distribution method:\n1. Students per group\n2. Numbers of group\n\nChoice : ')
            method = int(method)
            if method in range(1, 3):
                break
            else:
                error_message(f"There's no method {method}")
        except ValueError:
            error_message(f"There's no method {method}")

    os.system('cls')
    while True:
        try:
            limit = int(input(f'Number of{" student per " if method == 1 else " "}group: '))
        except ValueError:
            error_message('Only accept numbers')
        else:
            if method == 1:
                result = distribute_by_member(n_students, limit)
                if result is None:
                    continue
                elif limit > round(n_students / 2):
                    error_message(f"Can't take more students than half of the total number of students")
                    continue
            elif method == 2 and limit > n_students:
                error_message(f"Can't take more students than the total number of students")
                continue
            break
    construct(method, limit)


if __name__ == '__main__':
    os.system('title Group Distribution')
    os.system('color B')

    if students: 
        main()
    else:
        error_message("There's no names\nAdd the names on \"student names.txt\"")
