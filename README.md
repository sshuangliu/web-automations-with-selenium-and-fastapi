# web-automations-with-selenium-and-fastapi


GitHub supports emoji!
:+1: :sparkles: :camel: :tada:
:rocket: :metal: :octocat:

~~~
[Unit]
Description=fastapi automation timesheet
After=network.target

[Service]
Type=simple
WorkingDirectory=/selenium_fastapi
ExecStart=python3 -m uvicorn fastapi_timesheet:app --host '0.0.0.0' --port 8000 --reload
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
~~~
