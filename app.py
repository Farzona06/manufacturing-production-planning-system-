from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_db
from datetime import date
from ml.forecast import forecast_production

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

@app.before_request
def setup():
    init_db()

@app.route("/")
def dashboard():
    db = get_db()
    products = db.execute("SELECT COUNT(*) n FROM products").fetchone()["n"]
    orders = db.execute("SELECT COUNT(*) n FROM orders WHERE status != 'Completed'").fetchone()["n"]
    plans = db.execute("SELECT COUNT(*) n FROM production_plans").fetchone()["n"]
    materials = db.execute("SELECT COUNT(*) n FROM raw_materials WHERE quantity <= min_quantity").fetchone()["n"]
    recent = db.execute("""SELECT p.plan_date, pr.name product_name, p.planned_quantity,
                         p.completed_quantity, p.status
                         FROM production_plans p JOIN products pr ON pr.id=p.product_id
                         ORDER BY p.id DESC LIMIT 6""").fetchall()
    return render_template("dashboard.html", products=products, orders=orders,
                           plans=plans, materials=materials, recent=recent)

@app.route("/products", methods=["GET", "POST"])
def products():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sku = request.form.get("sku", "").strip()
        unit_price = request.form.get("unit_price", "0")
        if not name or not sku:
            flash("Mahsulot nomi va kodi kiritilishi shart.", "error")
        else:
            try:
                db.execute("INSERT INTO products(name, sku, unit_price) VALUES(?,?,?)",
                           (name, sku, float(unit_price)))
                db.commit()
                flash("Mahsulot muvaffaqiyatli qo‘shildi.", "success")
            except Exception:
                db.rollback()
                flash("Mahsulot kodi takrorlangan yoki ma’lumot noto‘g‘ri.", "error")
        return redirect(url_for("products"))
    rows = db.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return render_template("products.html", products=rows)

@app.post("/products/<int:item_id>/delete")
def delete_product(item_id):
    db = get_db()
    try:
        db.execute("DELETE FROM products WHERE id=?", (item_id,))
        db.commit()
        flash("Mahsulot o‘chirildi.", "success")
    except Exception:
        db.rollback()
        flash("Bu mahsulot ishlab chiqarish rejasida ishlatilgan. Avval rejani o‘chiring.", "error")
    return redirect(url_for("products"))

@app.route("/plans", methods=["GET", "POST"])
def plans():
    db = get_db()
    if request.method == "POST":
        try:
            db.execute("""INSERT INTO production_plans
                (product_id, plan_date, planned_quantity, completed_quantity, status)
                VALUES(?,?,?,?,?)""",
                (int(request.form["product_id"]), request.form["plan_date"],
                 int(request.form["planned_quantity"]), 0, "Planned"))
            db.commit()
            flash("Ishlab chiqarish rejasi yaratildi.", "success")
        except Exception:
            db.rollback()
            flash("Reja ma’lumotlarini tekshiring.", "error")
        return redirect(url_for("plans"))
    products = db.execute("SELECT * FROM products ORDER BY name").fetchall()
    rows = db.execute("""SELECT pp.*, p.name product_name FROM production_plans pp
                         JOIN products p ON p.id=pp.product_id ORDER BY pp.plan_date DESC""").fetchall()
    return render_template("plans.html", plans=rows, products=products, today=date.today().isoformat())

@app.post("/plans/<int:plan_id>/complete")
def complete_plan(plan_id):
    db = get_db()
    try:
        qty = max(0, int(request.form["completed_quantity"]))
        row = db.execute("SELECT planned_quantity FROM production_plans WHERE id=?", (plan_id,)).fetchone()
        status = "Completed" if row and qty >= row["planned_quantity"] else "In progress"
        db.execute("UPDATE production_plans SET completed_quantity=?, status=? WHERE id=?",
                   (qty, status, plan_id))
        db.commit()
        flash("Bajarilgan miqdor yangilandi.", "success")
    except Exception:
        db.rollback()
        flash("Miqdor noto‘g‘ri.", "error")
    return redirect(url_for("plans"))

@app.route("/materials", methods=["GET", "POST"])
def materials():
    db = get_db()
    if request.method == "POST":
        try:
            db.execute("INSERT INTO raw_materials(name, unit, quantity, min_quantity) VALUES(?,?,?,?)",
                       (request.form["name"].strip(), request.form["unit"].strip(),
                        float(request.form["quantity"]), float(request.form["min_quantity"])))
            db.commit()
            flash("Xomashyo qo‘shildi.", "success")
        except Exception:
            db.rollback()
            flash("Ma’lumotlarni tekshiring.", "error")
        return redirect(url_for("materials"))
    rows = db.execute("SELECT * FROM raw_materials ORDER BY name").fetchall()
    return render_template("materials.html", materials=rows)

@app.route("/orders", methods=["GET", "POST"])
def orders():
    db = get_db()
    if request.method == "POST":
        try:
            db.execute("INSERT INTO orders(customer_name, product_id, quantity, status) VALUES(?,?,?,?)",
                       (request.form["customer_name"].strip(), int(request.form["product_id"]),
                        int(request.form["quantity"]), request.form["status"]))
            db.commit()
            flash("Buyurtma saqlandi.", "success")
        except Exception:
            db.rollback()
            flash("Buyurtma ma’lumotlarini tekshiring.", "error")
        return redirect(url_for("orders"))
    products = db.execute("SELECT * FROM products ORDER BY name").fetchall()
    rows = db.execute("""SELECT o.*, p.name product_name FROM orders o
                         JOIN products p ON p.id=o.product_id ORDER BY o.id DESC""").fetchall()
    return render_template("orders.html", orders=rows, products=products)

@app.route("/forecast")
def forecast():
    result = forecast_production()
    return render_template("forecast.html", result=result)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "Manufacturing Production Planning System"})

if __name__ == "__main__":
    app.run(debug=True)
