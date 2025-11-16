# -------------------------------
# AUTHOR CLASS
# -------------------------------
class Author:
    def __init__(self, name):
        # Validate name
        if not isinstance(name, str):
            raise TypeError
        if len(name) == 0:
            raise ValueError
        self._name = name  # immutable
        self._articles = []  # list to track articles by this author

    @property
    def name(self):
        return self._name  # immutable, no setter

    def articles(self):
        # returns all Article instances for this author
        return self._articles

    def magazines(self):
        # returns unique magazines this author has contributed to
        return list({article.magazine for article in self._articles})

    def add_article(self, magazine, title):
        # create a new Article and associate it with this author
        return Article(self, magazine, title)

    def topic_areas(self):
        # returns unique categories of magazines
        if not self._articles:
            return None
        return list({article.magazine.category for article in self._articles})

# -------------------------------
# MAGAZINE CLASS
# -------------------------------
class Magazine:
    all = []  # track all magazine instances

    def __init__(self, name, category):
        # validate name and category
        if not isinstance(name, str):
            raise TypeError
        if not (2 <= len(name) <= 16):
            raise ValueError
        if not isinstance(category, str):
            raise TypeError
        if len(category) == 0:
            raise ValueError

        self._name = name
        self._category = category
        self._articles = []
        Magazine.all.append(self)

    # mutable name with validation
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError
        if not (2 <= len(value) <= 16):
            raise ValueError
        self._name = value

    # mutable category with validation
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError
        if len(value) == 0:
            raise ValueError
        self._category = value

    def articles(self):
        return self._articles

    def contributors(self):
        # return unique authors or None if no articles
        if not self._articles:
            return None
        return list({article.author for article in self._articles})

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        if not self._articles:
            return None
        count = {}
        for article in self._articles:
            count[article.author] = count.get(article.author, 0) + 1
        result = [author for author, c in count.items() if c > 2]
        return result if result else None

# -------------------------------
# ARTICLE CLASS
# -------------------------------
class Article:
    all = []  # track all article instances

    def __init__(self, author, magazine, title):
        # validations
        if not isinstance(author, Author):
            raise TypeError
        if not isinstance(magazine, Magazine):
            raise TypeError
        if not isinstance(title, str):
            raise TypeError
        if not (5 <= len(title) <= 50):
            raise ValueError

        self._author = author
        self._magazine = magazine
        self._title = title  # immutable

        # associate article with author and magazine
        author._articles.append(self)
        magazine._articles.append(self)
        Article.all.append(self)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError
        # remove from old magazine's articles
        if hasattr(self, "_magazine") and self in self._magazine._articles:
            self._magazine._articles.remove(self)
        # assign new magazine and link
        self._magazine = value
        value._articles.append(self)

    @property
    def title(self):
        # immutable
        return self._title
