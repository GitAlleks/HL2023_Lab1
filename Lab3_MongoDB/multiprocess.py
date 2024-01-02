import multiprocessing
import csv
import subprocess


def import_batch(batch):
    # # Создайте команду mongoimport для импорта батча
    command = [
        "mongoimport",
        "--host=localhost",
        "--port=27017",
        "--db=london",
        "--collection=rides",
        "--type=csv",
        "--headerline",
        "--ignoreBlanks",
        "--file=./taxi.csv",
        "--batchSize=100000",
    ]
    command.extend(batch)
    # Запустите команду
    subprocess.run(command)


def main():
    # Разделите файл на батчи
    with open("taxi.csv", "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        batch = []
        for row in reader:
            batch.append(row)
            if len(batch) == 100000:
                break

    # Создайте пул процессов
    pool = multiprocessing.Pool()

    # Отправьте задачи в пул процессов
    tasks = []
    for row in batch:
        tasks.append(pool.apply_async(import_batch, args=[row]))

    # Ждите завершения задач
    for task in tasks:
        task.get()


if __name__ == "__main__":
    main()