from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    # store as one long string, separated by newlines
    orders = db.Column(db.Text, nullable=False)
    table_number = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "orders": self.orders,
            "table_number": self.table_number,
        }
