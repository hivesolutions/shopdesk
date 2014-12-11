{% extends "email/layout.html.tpl" %}
{% block title %}Test{% endblock %}
{% block content %}
    <p>
        This is a simple test mail for the Shopdesk infra-structure.<br/>
        If you're reading this message the message has been correctly processed and delivered using <strong>{{ config.conf("SMTP_HOST") }}</strong>.
    </p>
    <p>
        If you're receiving this message and it's marked as SPAM please contact your system administrator immediately.
    </p>
{% endblock %}
