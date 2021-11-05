import random
import math
import os

headers = '''// Masukkan nama-nama siswa dibawah
// Buat setiap baris untuk satu nama

// Gunakan "//" didepan nama untuk mengabaikan sebuah baris atau nama ketika membuat kelompok
// Contoh: // Abdul Latif
'''

try:
    with open('nama siswa.txt') as file:
        students = [line.strip() for line in file.readlines()
                    if not line.strip().startswith('//') and line.strip()]
        n_students = len(students)
        file.close()
except FileNotFoundError:
    with open('nama siswa.txt', 'w') as file:
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
        error_message(f'Tidak bisa membuat kelompok dengan {k} anggota')
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
    text = [f'Jumlah siswa : {n_students}\n']
    for index, group in enumerate(data, start=1):
        text.append(f'Kelompok {index}')
        for order, member in enumerate(group, start=1):
            text.append(f'{order}. {member}')
        text.append('')
    with open('kelompok.txt', 'w') as f:
        f.write('\n'.join(text))
        f.close()


def main() -> None:
    method = ''
    while True:
        try:
            method = input('Metode Pembagian:\n1. Jumlah per kelompok\n2. Jumlah kelompok\n\nPilihan : ')
            method = int(method)
            if method in range(1, 3):
                break
            else:
                error_message(f'Tidak ada metode {method}')
        except ValueError:
            error_message(f'Tidak ada metode {method}')

    os.system('cls')
    while True:
        try:
            limit = int(input(f'Jumlah{" orang per " if method == 1 else " "}kelompok: '))
        except ValueError:
            error_message('Hanya menerima angka')
        else:
            if method == 1:
                result = distribute_by_member(n_students, limit)
                if result is None:
                    continue
                elif limit > round(n_students / 2):
                    error_message('Tidak bisa memilih murid lebih banyak dari setengah jumlah murid')
                    continue
            elif method == 2 and limit > n_students:
                error_message('Tidak bisa membuat kelompok lebih banyak dari jumlah murid')
                continue
            break
    construct(method, limit)


if __name__ == '__main__':
    os.system('title Pembagian Kelompok')
    os.system('color B')

    if students:
        main()
    else:
        error_message('Tidak ada nama siswa\nIsi nama-nama siswa di file "nama siswa.txt"')
