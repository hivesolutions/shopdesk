{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Shopdesk{% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux complete">
    <div id="header" class="header">
        {% include "partials/header.html.tpl" %}
        {% block header %}
            <ul class="side-links">
                <li>Home</li>
                <li>Orders</li>
                <li>Products</li>
                <li>Sales</li>
                <li>Reports</li>
            </ul>
        {% endblock %}
    </div>
    <div id="content" class="content">{% block content %}{% endblock %}</div>
    <div id="footer" class="footer">
        {% include "partials/footer.html.tpl" %}
        {% block footer %}{% endblock %}
    </div>
</body>
{% include "partials/end_doctype.html.tpl" %}
