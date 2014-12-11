{% extends "email/layout.html.tpl" %}
{% block title %}Test email{% endblock %}
{% block content %}
    <p>
        This is a simple test email for the Shopdesk infra-structure.<br/>
        If you're reading this message the message has been correctly processed and delivered using <strong>{{ config.conf("SMTP_HOST") }}:{{ config.conf("SMTP_PORT", "25") }}</strong>.
    </p>
    <p>
        If you're receiving this message and it's marked as SPAM please contact your system administrator immediately.<br/>
        Please beware that the fact that you're receiving this email using your provider does not guarantee that other providers will receive the same email.
    </p>
    <p>
        For other questions regarding SMTP email sending please refer to you system administrator.
    </p>
{% endblock %}
