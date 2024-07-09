from app import db

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    borrows = db.relationship('Borrow', back_populates='user')

    def __repr__(self):
        return f"Name : {self.name}, Email: {self.email}"
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)

    borrows = db.relationship('Borrow', back_populates='book')

    def __repr__(self):
        return f"Title : {self.title}, Author: {self.author}, Publish date: {self.published_date}, Available: {self.available}"
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date,
            'available': self.available
        }
    
class Borrow(db.Model):
    __tablename__ = 'borrow'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    user = db.relationship('User', back_populates='borrows')
    book = db.relationship('Book', back_populates='borrows')

    def __repr__(self):
        return f"User ID : {self.user_id}, Book ID: {self.book_id}, Borrow date: {self.borrow_date}, Return date: {self.return_date}"
    
    def json(self):
        return {
            'book_id': self.book.id,
            'title': self.book.title,
            'author': self.book.author,
            'borrow_date': self.borrow_date
        }