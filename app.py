from flask import Flask, request, redirect, render_template_string
import sqlite3
from pathlib import Path
app=Flask(__name__); DB=Path(__file__).with_name("expenses.db")
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with db() as c:
 c.execute("CREATE TABLE IF NOT EXISTS tx(id INTEGER PRIMARY KEY, kind TEXT, label TEXT, amount REAL, day TEXT)")
PAGE="""<!doctype html><html><head><title>Expense Tracker</title><style>body{font:16px system-ui;max-width:850px;margin:30px auto;background:#f4f7f6;padding:0 16px;color:#18342c}.card{background:white;padding:18px;border-radius:12px;margin:14px 0}input,select,button{padding:10px;margin:4px;border-radius:7px;border:1px solid #ccd8d2}button{background:#147d64;color:white}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid #ddd}.stats{display:flex;gap:12px;flex-wrap:wrap}.stats div{background:#e5f6ef;padding:14px;border-radius:9px}</style></head><body><h1>💸 Expense Tracker</h1><div class=stats><div>Income: <b>₹{{'%.2f'|format(income)}}</b></div><div>Expenses: <b>₹{{'%.2f'|format(expense)}}</b></div><div>Balance: <b>₹{{'%.2f'|format(income-expense)}}</b></div></div><div class=card><h2>Add transaction</h2><form method=post><select name=kind><option>Expense</option><option>Income</option></select><input name=label placeholder="Description" required><input name=amount type=number min=.01 step=.01 placeholder="Amount" required><input name=day type=date required><button>Add</button></form></div><div class=card><h2>Transactions</h2><table><tr><th>Date</th><th>Type</th><th>Description</th><th>Amount</th><th></th></tr>{% for t in tx %}<tr><td>{{t.day}}</td><td>{{t.kind}}</td><td>{{t.label}}</td><td>₹{{'%.2f'|format(t.amount)}}</td><td><a href="/delete/{{t.id}}">Delete</a></td></tr>{% else %}<tr><td colspan=5>No transactions yet.</td></tr>{% endfor %}</table></div></body></html>"""
@app.route("/",methods=["GET","POST"])
def index():
 if request.method=="POST":
  amount=float(request.form["amount"])
  if amount<=0:return "Amount must be greater than zero.",400
  with db() as c:c.execute("INSERT INTO tx(kind,label,amount,day) VALUES(?,?,?,?)",(request.form["kind"],request.form["label"].strip(),amount,request.form["day"]))
  return redirect("/")
 with db() as c:
  tx=c.execute("SELECT * FROM tx ORDER BY day DESC,id DESC").fetchall()
  income=c.execute("SELECT COALESCE(SUM(amount),0) FROM tx WHERE kind='Income'").fetchone()[0]
  expense=c.execute("SELECT COALESCE(SUM(amount),0) FROM tx WHERE kind='Expense'").fetchone()[0]
 return render_template_string(PAGE,tx=tx,income=income,expense=expense)
@app.get("/delete/<int:i>")
def delete(i):
 with db() as c:c.execute("DELETE FROM tx WHERE id=?",(i,))
 return redirect("/")
if __name__=="__main__":app.run(debug=True)
