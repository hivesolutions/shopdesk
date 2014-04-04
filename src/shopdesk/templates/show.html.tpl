{% extends "partials/layout.html.tpl" %}
{% block title %}Show{% endblock %}
{% block style %}no-header{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-grey" data-link="/accounts/own/edit">Edit</div>
{% endblock %}
{% block extras %}
    <div class="side-panel border-box">
        <form class="form">
            <h1>Get news updates</h1>
            <input type="text" class="text-field" placeholder="Your email address"
                   data-object="textfield" autocomplete="off" data-value="" />
            <div class="buttons">
                <div class="button button-color button-green button-confirm" data-submit="1">Sign Up</div>
                <div class="button button-color button-grey button-cancel">Cancel</div>
            </div>
        </form>
    </div>
{% endblock %}
{% block content %}
   <div class="show-panel">
        <div class="panel-header">
            <img class="image" src="http://webook.pt/accounts/own/image" />
            <div class="details">
                <h2>João Magalhães</h2>
            </div>
            <div class="buttons">
                {{ self.buttons() }}
            </div>
        </div>
        <div class="panel-contents">
            <dl class="inline">
                <div class="item">
                    <dt>First Name</dt>
                    <dd>Super</dd>
                </div>
                <div class="item">
                    <dt>Last Name</dt>
                    <dd>Administrator</dd>
                </div>
                <div class="item">
                    <dt>Birthday</dt>
                    <dd class="timestamp" data-format="%B %d, %Y">N/A</dd>
                </div>
                <div class="item">
                    <dt>Gender</dt>
                    <dd class="capital">male</dd>
                </div>
                   <div class="separator"></div>
                <div class="item">
                    <dt>Email</dt>
                    <dd>root@root.com</dd>
                </div>
                <div class="item">
                    <dt>Phone</dt>
                    <dd>+351999999999</dd>
                </div>
                <div class="item">
                    <dt>Address</dt>
                    <dd>
                        Rua das Mimosas, 120<br />
                        4420-204 Porto - Portugal<br />
                        Portugal<br />
                    </dd>
                </div>
                <div class="separator"></div>
                <div class="item">
                    <dt>About</dt>
                    <dd>N/A</dd>
                </div>
            </dl>
        </div>
    </div>
{% endblock %}
