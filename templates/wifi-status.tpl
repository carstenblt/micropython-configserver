{% set import network %}
{% set import wifi_database %}
{% if network.WLAN(network.STA_IF).isconnected() is True and wifi_database.active_wifi is not None %}
{% set quality_bars = 0 %}
{% for mynetwork in network.WLAN(network.STA_IF).scan() %}
{% if mynetwork[0].decode('utf-8') == wifi_database.active_wifi %}
{% set quality_bars = round(5 * (0 if mynetwork[3] < -100 else (1 if mynetwork[3] > -50 else 2e-2 * (mynetwork[3] + 100)))) %}
{% endif %}
{% endfor %}
	<div id="current_name">{{wifi_database.active_wifi}}</div>
	<div id="current_strength">{% for i in range(quality_bars) %}I{% endfor %}<span class="empty_bars">{% for i in range(5-quality_bars) %}I{% endfor %}</span></div>
{% else %}
ERROR
{% endif %}