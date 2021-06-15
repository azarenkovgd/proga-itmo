import csv
import pathlib

from sklearn.model_selection import train_test_split

from model_stuff import bayes, stemmer


def main():
    path_to_dataset = pathlib.Path("data_for_byes_testing/SMSSpamCollection")

    with path_to_dataset.open(encoding="utf8") as f:
        data = list(csv.reader(f, delimiter="\t"))

    x, y = [], []
    for i, sample in enumerate(data):
        if len(sample) == 1:
            continue
        x.append(sample[1])
        y.append(sample[0])

    print("начата обработка данных. может занять несколько минут")
    x = stemmer.clear_dataset(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, test_size=0.2)

    print("начато обучение. может занять несколько минут")
    model = bayes.NaiveBayesClassifier(0.1)
    model.fit(x_train, y_train)

    print("итоговый score для 20 процентов датасета:", model.score(x_test, y_test))


if __name__ == "__main__":
    main()
