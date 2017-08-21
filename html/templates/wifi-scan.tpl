{% set import network %}
{% set authmodes = ['Open', 'WEP', 'WPA', 'WPA2', 'WPA/WPA2', 'WPA/WPA2'] %}
{% set network.WLAN(network.STA_IF).active(True) %}
{% for mynetwork in sorted(network.WLAN(network.STA_IF).scan(), key=lambda x: x[3], reverse=True) %}
{% set quality_bars = round(5 * (0 if mynetwork[3] < -100 else (1 if mynetwork[3] > -50 else 2e-2 * (mynetwork[3] + 100)))) %}
<div class="network" onclick="toggle_connectform(this)">
	<div class="network_name">{{mynetwork[0].decode('utf-8')}}</div>
	<div class="network_encryption">{{authmodes[mynetwork[4]]}}</div>
	<div class="network_strength">{% for i in range(quality_bars) %}I{% endfor %}<span class="empty_bars">{% for i in range(5-quality_bars) %}I{% endfor %}</span></div>
	<div class="network_connect"><form>
	<input type="hidden" name="essid" value="{{mynetwork[0].decode('utf-8')}}" />
	Password: <input type="password" name="password" /><button type="button" onclick="connect_wifi(this)">Connect!</button></form></div>
</div>
{% endfor %}