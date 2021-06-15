import pathlib
import pickle
import typing as tp

from model_stuff import stemmer
from bottle import redirect, request, route, run, template
from news.db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label.is_(None))
    return template("news_template", rows=rows)


@route("/all_news")
def news_list():
    s = session()
    rows = s.query(News)
    return template("classified_template", rows=rows)


@route("/add_label/")
def add_label():
    params = request.query
    s = session()
    entry = s.query(News).filter(News.id == params["id"]).first()
    entry.label = params["label"]
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    new_arrivals = get_news("https://news.ycombinator.com/newest")
    batch_size = 30

    s = session()

    marker = s.query(News).first()
    for i, el in enumerate(new_arrivals):
        if el["title"] == marker.title and el["author"] == marker.author:
            batch_size = i
    new_arrivals = new_arrivals[:batch_size]

    for _, el in enumerate(new_arrivals):
        obj = News(
            title=el["title"],
            author=el["author"],
            url=el["url"],
            comments=el["comments"],
            points=el["points"],
        )
        s.add(obj)
        s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    path_to_model = pathlib.Path("model/model.pickle")

    query = s.query(News).filter(News.label.is_(None)).all()
    unclassified: tp.List[tp.Tuple[int, str]] = [(el.id, stemmer.clear_sentence(el.title)) for el in query]

    x: tp.List[str] = [i[1] for i in unclassified]

    if not path_to_model.is_file():
        raise ValueError("Классификатор не натренирован")

    with path_to_model.open("rb") as model_file:
        model = pickle.load(model_file)

    labels = model.predict(x)
    for i, el in enumerate(unclassified):
        extract = s.query(News).filter(News.id == el[0]).first()
        extract.label = labels[i]
        s.commit()

    rows = s.query(News).filter(News.label is not None).order_by(News.label).all()
    return template("classified_template", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)
