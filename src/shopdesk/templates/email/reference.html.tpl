{% extends "email/layout.html.tpl" %}
{% block title %}Referência Multibanco{% endblock %}
{% block content %}
    <p>
        A sua referência multibacno acabou de ser criada! Para completar a sua compra por
        favor efetua o pagamento da mesma a partir de uma caixa multibanco ou da sua conta
        de home banking.
    </p>
    {{ h2("Multibanco") }}
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:ajuda@webook.pt", "ajuda@webook.pt", False) }}.
    </p>
{% endblock %}
