import sqlite3
from flask import Flask, request

app = Flask(__name__)

# SETUP DATABASE  
conn = sqlite3.connect('my_shop.db', check_same_thread=False)
try:
    conn.execute("DROP TABLE IF EXISTS hats") 
    conn.execute("CREATE TABLE hats (name TEXT, price TEXT)")
    conn.execute("INSERT INTO hats VALUES ('Cowboy Hat', '$20')")
    conn.execute("INSERT INTO hats VALUES ('Baseball Cap', '$10')")
    conn.execute("INSERT INTO hats VALUES ('Top Hat', '$50')")
    conn.commit()
except:
    pass

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    
    if request.method == 'POST':
        # Get data from the form
        p = request.form.get('password')
        s = request.form.get('search')
        
        if p != "admin123":
            return "Wrong Password! Access Denied."
            
        sql = "SELECT * FROM hats WHERE name = '" + s + "'"
        
        print("DEBUG SQL: " + sql) 
        
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            if len(rows) > 0:
                result = "Found: " + s + "<br>"
                for row in rows:
                    result += "Item: " + row[0] + " Price: " + row[1] + "<br>"
            else:
                result = "No hats found for: " + s
                
        except Exception as e:
            result = "Error: " + str(e)

    # HTML Form
    html = """
    <h2>Hat Shop Inventory</h2>
    <form method="POST">
        Admin Password: <input type="password" name="password"><br><br>
        Search Hat Name: <input type="text" name="search"><br><br>
        <input type="submit" value="Check Stock">
    </form>
    <hr>
    <h3>Results:</h3>
    """ + result
    
    return html

if __name__ == "__main__":
    app.run(debug=True)