from flask import Flask, render_template, request, redirect, url_for
from models.order_model import db, Order

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/<int:table_number>")
def main_menu(table_number: int):
    return render_template("main_menu.html", table_number=table_number)

@app.route("/order/<int:table_number>", methods=["POST"])
def order(table_number: int):
    order_summary = request.form.get("order_summary", "")
    customer_name = request.form.get("customer_name", "").strip()

    if not customer_name:
        customer_name = "Anonymous"

    new_order = Order(
        customer_name=customer_name,
        orders=order_summary.strip(),
        table_number=table_number
    )
    try:
        db.session.add(new_order)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    order_dict = {
        "id": new_order.id,
        "customer_name": new_order.customer_name,
        "table_number": new_order.table_number,
        "orders": new_order.orders,
        "order_items": [line for line in new_order.orders.split("\n") if line.strip()],
    }

    return render_template("order_summary.html", order=order_dict)

@app.route("/kitchen/")
def kitchen():
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template("kitchen.html", orders=orders)

@app.route("/delete/<int:id>")
def delete(id: int):
    order_obj = Order.query.get(id)
    if order_obj is not None:
        try:
            db.session.delete(order_obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
    return redirect(url_for("kitchen"))

if __name__ == "__main__":
    app.run(debug=True)
