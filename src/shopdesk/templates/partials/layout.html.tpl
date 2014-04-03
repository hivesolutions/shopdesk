{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>webook{% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux full">
    <div id="header" class="header">
        {% include "partials/header.html.tpl" %}
        {% block header %}{% endblock %}
    </div>
    <div id="content" class="content">{% block content %}{% endblock %}</div>
    <div id="footer" class="footer">
        {% include "partials/footer.html.tpl" %}
        {% block footer %}{% endblock %}
    </div>
</body>
{% include "partials/end_doctype.html.tpl" %}
