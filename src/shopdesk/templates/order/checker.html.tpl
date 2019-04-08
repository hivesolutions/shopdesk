<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>Order</th>
                <th>Customer</th>
                <th>Street</th>
            </tr>
        </thead>
        <tbody>
            {% for order in orders %}
                <tr>
                    <td>{{ order.s_name }}</td>
                    <td>{{ order.s_shipping_name }}</td>
                    <td>{{ order.s_shipping_street }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
