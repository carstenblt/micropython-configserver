{% args req %}
{% set import wifi_database %}
{% if wifi_database.connect_and_add_wifi(req.form['essid'], req.form['password']) is True %}
OK
{% else %}
ERROR
{% endif %}