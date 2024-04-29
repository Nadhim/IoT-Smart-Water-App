from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

import requests, jsonify, math

app = Flask(__name__)
app.secret_key = 'my_secure_secret_key_with_random_characters_12345'

# Simulated user database (user email as key and tuple of name and password as value)
users = {
    "nadhim@watersaver.com": ("Mohamed Nadhim", "1111"),
    "drhemalatha@watersaver.com": ("Dr. R. Hemalatha", "1111")
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email][1] == password:
        session['logged_in'] = True  # Mark the user as logged in
        session['user_email'] = email  # Store user email in session for later use
        flash('Login successful!', 'success')
        return redirect(url_for('success'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('home'))

@app.route('/success')
def success():
    if session.get('logged_in'):
        user_email = session.get('user_email')
        user_name = users[user_email][0]  # Get user's name from the database
        credit_score = 345


        channel_id = '2501461'
        read_api_key = 'KARHZ6YMTULILF1Y'
        url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}'

        response = requests.get(url)
        data = response.json()

        water_level_data = []
        water_usage_data = []
        created = []

        # Assuming you have two fields named 'field1' and 'field2'
        for entry in data['feeds']:
            water_level_data.append(entry['field1']) 
            water_usage_data.append(entry['field2']) 
            created.append(entry['created_at'][:-1])



        water_level_test = water_usage_data
        x = [i for i in range(len(water_level_test))]
        water_level_test = [round(float(i),2) for i in water_level_test]
        # plt.scatter(x[:-4],water_level_test[:-4])

        def linear_regression(X, Y):
            n = len(X)

            # Calculate the mean of X and Y
            mean_x = sum(X) / n
            mean_y = sum(Y) / n

            # Calculate the slope (m) and intercept (b)
            numerator = sum((X[i] - mean_x) * (Y[i] - mean_y) for i in range(n))
            denominator = sum((X[i] - mean_x) ** 2 for i in range(n))
            slope = numerator / denominator
            intercept = mean_y - slope * mean_x

            return slope, intercept

        # Example data
        X = x  # Independent variable
        Y = water_level_test  # Dependent variable

        # Perform linear regression
        slope, intercept = linear_regression(X, Y)

        # Plot the data points[]
        # plt.scatter(created[:-4], Y, label='Data')
        # plt.xticks(rotation=45)

        x_value = 7
        y_value = slope * x_value + intercept

        y_value = round(y_value,2)


        x_value1 = 30
        y_value1 = slope * x_value1 + intercept

        y_value1 = round(y_value1,2)

        x_value2 = 1
        y_value2 = slope * x_value2 + intercept

        y_value2 = round(y_value2,2)
        # print("The y value for x = 30 is: ",y_value)
        # Plot the regression line
        regression_line = [slope * x + intercept for x in X]
        # plt.plot(X, regression_line, color='red', label='Regression Line')

        # # Add labels and legend
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # plt.title('Linear Regression')
        # plt.legend()
        # Generate some example data and plot
        x = created
        y = Y

        # fig, ax = plt.subplots()
        # ax.scatter(created[:-4], Y, label = 'Water Flow Rate')
        # ax.plot(X, regression_line, color='red', label='Regression Line')
        # ax.set_xticks(created)
        # ax.set_xticklabels(created,rotation=45)
        # ax.set_xlabel('Time')
        # ax.set_ylabel('Litres of water consumed')
        # ax.set_title('Predicted Water Usage Level Plot')

        # water_prediction()

        # # Render the HTML template with the plot data
        # return render_template('index.html', plot_data=plot_data,y_value = y_value)

        return render_template('success.html', user_name=user_name, credit_score = credit_score, y_value = y_value, y_value1=y_value1, y_value2=y_value2,water_used = math.floor(float(water_usage_data[-1])))
    else:
        flash('Please log in first!', 'error')
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove the 'logged_in' flag from the session
    session.pop('user_email', None)  # Remove the 'user_email' from the session
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/get_water_data')
def get_water_data():
    # Fetch water level data from ThingSpeak
    channel_id = '2501461'
    read_api_key = 'KARHZ6YMTULILF1Y'
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}'

    response = requests.get(url)
    data = response.json()

    water_level_data = []
    created_dates = []

    for entry in data['feeds']:
        water_level_data.append(float(entry['field1']))
        created_dates.append(entry['created_at'])

    return jsonify({
        'created_dates': created_dates,
        'water_level_data': water_level_data
    })


if __name__ == '__main__':
    app.run(debug=True)
