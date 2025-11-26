from flask import Flask, request, render_template
import db_helper 

app = Flask(__name__)

# Setup DB on start
db_helper.setup_db()

@app.route('/')
def index():
    # Show the login page
    return render_template('home.html', result_msg="")

@app.route('/search', methods=['POST'])
def search_inventory():
    pwd = request.form.get('password')
    item = request.form.get('item_name')
    
    if pwd != "admin123":
        return render_template('home.html', result_msg="<b style='color:red'>Wrong Password!</b>")

    # Connect to DB
    conn = db_helper.get_connection()
    cursor = conn.cursor()
    
    sql_query = "SELECT * FROM inventory WHERE name = '" + item + "'"
    
    print("DEBUG SQL: " + sql_query)

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        # Preparing the HTML
        output = "<h3>Results for: " + item + "</h3><ul>"
        
        if rows:
            for row in rows:
                output += "<li>Item: " + row[0] + " | Qty: " + row[1] + "</li>"
        else:
            output += "<li>No stock found.</li>"
            
        output += "</ul>"
        
        return render_template('home.html', result_msg=output)
        
    except Exception as e:
        return "System Error: " + str(e)

if __name__ == "__main__":
    app.run(debug=True)