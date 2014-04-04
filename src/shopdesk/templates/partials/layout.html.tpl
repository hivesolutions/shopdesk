{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Shopdesk {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux panels grey no-footer">
    {% block extras %}{% endblock %}
    <div id="header" class="header">
        {% include "partials/bar.html.tpl" %}
        {% include "partials/header.html.tpl" %}
        {% block header %}
            <ul class="side-links">
                <li class="selected">Home</li>
                <li>Orders</li>
                <li>Products</li>
                <li>Sales</li>
                <li>Reports</li>
                <li class="separator"></li>
                <li>About</li>
                <li class="swindow">Window</li>
                <li class="side">Side</li>
                <li class="hide">Hide</li>
            </ul>
        {% endblock %}
    </div>
    <div id="content" class="content {% block style %}{% endblock %}">
        <div class="content-header">
            <h1>{{ self.title() }}</h1>
            <div class="content-buttons">
                {% block buttons %}{% endblock %}
            </div>
        </div>
        <div class="content-container">
            {% block content %}{% endblock %}
        </div>
    </div>
    <div id="footer" class="footer">
        {% include "partials/footer.html.tpl" %}
        {% block footer %}{% endblock %}
    </div>
</body>
{% include "partials/end_doctype.html.tpl" %}
