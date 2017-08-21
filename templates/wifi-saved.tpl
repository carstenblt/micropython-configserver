{% set import wifi_database %}
{% for mynetwork in wifi_database.iter_wifis() %}
<div class="network">
	<div class="network_name">{{mynetwork[0]}}</div>
</div>
{% endfor %}