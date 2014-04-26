{% extends "email/layout.html.tpl" %}
{% block title %}Referência Multibanco{% endblock %}
{% block content %}
    <p>
        A sua referência Multibanco para a encomenda {{ order.s_name }} acabou de ser criada!
        Dispõe de 24 horas para efectuar o pagamento. Caso este prazo seja ultrapassado a sua
        encomenda será cancelada.
    </p>
    <p>
        Pode efectuar o pagamento numa caixa multibanco, basta selecionar a opção "Pagamentos
        de Serviços" e introduzir a entidade, referência e valor. O pagamento pode também ser
        efectuado on-line em qualquer tipo de serviço "home banking" prestado pelo seu banco.
    </p>
    {{ h2("Dados Multibanco") }}
    <p>
        <strong>Entidade:</strong>
        <span>{{ order.entity }}</span>
    </p>
    <p>
        <strong>Referência:</strong>
        <span>{{ order.reference }}</span>
    </p>
    <p>
        <strong>Valor:</strong>
        <span>{{ order.s_total_price }} {{ order.s_currency }}</span>
    </p>
    {{ h2("Estamos Sempre Consigo") }}
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:ajuda@webook.pt", "ajuda@webook.pt", False) }}.
    </p>
{% endblock %}
