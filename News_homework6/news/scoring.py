import pathlib
import pickle

from model_stuff import bayes, stemmer
from news.db import News, session
from sklearn.model_selection import train_test_split


def train_and_show_score_on_test_data():
    s = session()

    print("Загрузка данных")
    x, y = [], []
    classified_data = [(el.title, el.label) for el in s.query(News).filter(News.label.isnot(None)).all()]

    for title, label in classified_data:
        x.append(title)
        y.append(label)

    print("обработка данных. это может занять несколько минут")
    x = stemmer.clear_dataset(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=False, test_size=0.3)

    print("генерация предсказаний. это может занять несколько минут")
    model = bayes.NaiveBayesClassifier(alpha=0.25)
    model.fit(x_train, y_train)

    print("Точность: ", model.score(x_test, y_test))

    path_to_model = pathlib.Path("model/model.pickle")
    path_to_model.parent.mkdir(parents=False, exist_ok=True)

    with pathlib.Path("model/model.pickle").open("wb") as model_file:
        pickle.dump(model, model_file)


if __name__ == '__main__':
    train_and_show_score_on_test_data()
