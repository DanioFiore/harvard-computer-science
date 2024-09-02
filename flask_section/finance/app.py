import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = rows[0]["cash"]

    holdings = db.execute("""
        SELECT symbol, SUM(shares) as shares
        FROM portfolios
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
    """, user_id)

    total_value = cash

    stocks = []

    for holding in holdings:
        stock = lookup(holding["symbol"])
        if stock:
            current_price = stock["price"]
            total = current_price * holding["shares"]
            total_value += total
            stocks.append({
                "symbol": holding["symbol"],
                "shares": holding["shares"],
                "price": current_price,
                "total": total
            })

    return render_template("index.html", cash=cash, stocks=stocks, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        user_id = session["user_id"]

        # Retrieve and validate the stock symbol and number of shares
        stock_symbol = request.form.get("symbol")
        stock_info = lookup(stock_symbol)
        shares_str = request.form.get("shares")

        # Check if the stock symbol is valid
        if not stock_symbol or not stock_info:
            return apology("Attention! The symbol is not valid!")

        # Validate that the number of shares is a positive integer
        if not shares_str.isdigit() or int(shares_str) <= 0:
            return apology("Attention! The number of shares must be a positive integer!")

        shares = int(shares_str)
        transaction_cost = shares * stock_info["price"]

        # Retrieve the user's cash balance
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Check if the user has enough cash to complete the transaction
        if user_cash < transaction_cost:
            return apology("Attention! You don't have enough funds!", 401)

        # Update user's cash balance after the purchase
        updated_cash_balance = user_cash - transaction_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash_balance, user_id)

        # Insert the transaction into the portfolios table
        db.execute(
            "INSERT INTO portfolios (user_id, symbol, shares, paid_price, current_price, stock_value) VALUES (?, ?, ?, ?, ?, ?)",
            user_id,
            stock_symbol,
            shares,
            stock_info["price"],
            stock_info["price"],
            stock_info["price"] * shares
        )

        # Record the transaction in the history table
        db.execute(
            "INSERT INTO history (user_id, symbol, shares, action, balance) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock_symbol,
            shares,
            "BOUGHT",
            user_cash,
        )
        transaction_value = int(shares) * stock_info["price"]
        update_cash = user_cash - transaction_value
        flash(f"Successfully bought {shares} shares of {stock_symbol} for {usd(transaction_value)} Updated cash = {usd(update_cash)}")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    user_portfolio = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)

    return render_template("history.html", user_portfolio=user_portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol", "").strip()

        stock_data = lookup(symbol)

        if not stock_data:
            return apology("Attention! Invalid stock symbol!")
        stock_data["price"] = usd(stock_data["price"])

        return render_template("quoted.html", stock=stock_data)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Extract and strip input fields to ensure clean data
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirmation = request.form.get("confirmation", "").strip()

        # Check for empty fields
        if not all([username, password, confirmation]):
            return apology("Fields cannot be empty!")

        # Username validation
        if len(username) < 4:
            return apology("Username must be at least 4 characters long!", 403)

        # if not username.isalnum():
        #     return apology("Username must contain only letters and digits!", 403)

        # Password validation
        if len(password) < 8:
            return apology("Password must be at least 8 characters long!", 403)

        # if not (re.search("[a-zA-Z]", password) and re.search("[0-9]", password) and re.search("[!@#$%^&*()]", password)):
        #     return apology("Password must contain letters, digits, and symbols!", 403)

        # Password confirmation
        if password != confirmation:
            return apology("Passwords do not match!", 400)

        # Check if username is already taken
        if db.execute("SELECT 1 FROM users WHERE username = ?", username):
            return apology("Username already taken!", 400)

        # Insert new user into the database
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Log in the new user
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Retrieve user ID from session
    user_id = session["user_id"]

    # Fetch the user's portfolio
    user_portfolio = db.execute("SELECT * FROM portfolios WHERE user_id = ? GROUP BY symbol", user_id)

    if request.method == "POST":
        # Get stock symbol and number of shares from the form
        stock_symbol = request.form.get("symbol")
        stock_data = lookup(stock_symbol)
        initial_shares_to_sell = int(request.form.get("shares"))
        shares_to_sell = int(request.form.get("shares"))

        # Check if the user owns the stock
        owned_stocks = db.execute(
            "SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?",
            user_id,
            stock_symbol,
        )

        if not owned_stocks:
            return apology(f"You don't own any shares of {stock_symbol}!")

        # Check if the user has enough shares to sell
        total_owned_shares = sum(stock["shares"] for stock in owned_stocks)
        if total_owned_shares < shares_to_sell:
            return apology("You don't have enough shares to sell!")

        # Retrieve user's cash balance
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash[0]["cash"]

        # Calculate the value of the shares being sold and update cash balance
        share_price = stock_data["price"]
        user_cash += shares_to_sell * share_price

        # Process the sale of shares
        for stock in owned_stocks:
            if stock["shares"] > shares_to_sell:
                db.execute(
                    "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
                    stock["shares"] - shares_to_sell,
                    user_id,
                    stock_symbol,
                )
                break
            else:
                db.execute(
                    "DELETE FROM portfolios WHERE user_id = ? AND symbol = ?",
                    user_id,
                    stock_symbol,
                )
                shares_to_sell -= stock["shares"]

        # Format balance for display
        new_balance = f"${user_cash:,.2f} (+${(shares_to_sell * share_price):,.2f})"

        # Update user's cash balance in the database
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, user_id)

        # Record the transaction in the history
        db.execute(
            "INSERT INTO history (user_id, symbol, shares, action, balance) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock_symbol,
            initial_shares_to_sell,
            "SOLD",
            new_balance
        )

        transaction_value = int(initial_shares_to_sell) * share_price
        flash(f"Successfully sold {initial_shares_to_sell} shares of {stock_symbol} for {usd(transaction_value)} Updated cash = {usd(user_cash)}")
        # flash(f"Successfully sold {initial_shares_to_sell} shares of {stock_symbol}!")
        return redirect("/")

    # Render the sell page for GET requests
    return render_template("sell.html", portfolio=user_portfolio)

@app.route("/add_funds", methods=["GET", "POST"])
@login_required
def add_funds():
    if request.method == "POST":
        funds = int(request.form.get("funds"))
        if funds < 1:
            return apology("The minimum funds you can add are 1$")
        user_id = session["user_id"]
        user_cash = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", (user_cash[0]["cash"] + funds), user_id)
        flash(f"Successfully added {funds}$ to your wallet!")
        return redirect("/")
    return render_template("add_funds.html")
