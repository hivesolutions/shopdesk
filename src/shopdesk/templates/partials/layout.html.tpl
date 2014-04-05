{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Shopdesk {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux fluid grey no-footer">
    {% block extras %}{% endblock %}
    <div id="header" class="header">
        {% include "partials/bar.html.tpl" %}
        {% include "partials/header.html.tpl" %}
        {% block header %}
            <div class="side-links">
                <a class="selected">Home</a>
                <a>Orders</a>
                <a>Products</a>
                <a>Sales</a>
                <a>Reports</a>
                <a class="separator"></a>
                <a>About</a>
                <a class="swindow">Window</a>
                <a class="side">Side</a>
                <a class="hide">Hide</a>
            </div>
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
