<!-- submit_expense.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Submit Expense</title>
</head>
<body>
    <h1>Submit Expense</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
    <a href="{% url 'expenses' %}">Go back to Expenses</a>
</body>
</html>
