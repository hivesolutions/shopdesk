{% extends "email/layout.html.tpl" %}
{% block title %}Referência Multibanco{% endblock %}
{% block content %}
    <p>
        A sua referência multibacno acabou de ser criada! Para completar a sua compra por
        favor efetue o pagamento da mesma a partir de uma caixa multibanco ou da sua conta
        de home banking.
    </p>
    <p>
    	A validade da referência emitida é de dois dias, após o qual se o pagamento não for
    	efetuado a entidade e a encomenda serão canceladas.
    </p>
    {{ h2("Multibanco") }}
    <p>
        <strong>Entidade:</strong>
        <span>{{ entity }}</span>
    </p>
    <p>
        <strong>Referência:</strong>
        <span>{{ reference }}</span>
    </p>
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:ajuda@webook.pt", "ajuda@webook.pt", False) }}.
    </p>
{% endblock %}
