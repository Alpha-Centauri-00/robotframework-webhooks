
# Better Not Use it

![Working](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzI3cGR1Y2g3MTA4Y3Fub3k4cDcwcjN3YWJxcnN3djl3dWF1aGZsbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/oA88lDC8EJasiPLqhZ/200.webp)


# robotframework-webhooks

The purpose of this repository is to automatically send only the failed test cases to MS-Teams / Slack as a listener. 
by adding an App "WebHook" to your preferable channel, which will generate a URL that you have to use, in order to send the results to your channal immediately. like this
[For example](https://github.com/Alpha-Centauri-00/robotframework-webhooks/blob/main/ms_teams.png)
<br/>
<br/>

# Installation

You can install robotframework-webhooks simply by running:



```
pip install robotframework-webhooks
```


## How to:
How to Create Incoming Webhooks for MS-Teams or Slack
<br/>
> Adding Webhook for [MS-Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=dotnet)<br/>
> Adding Webhook for [Slack](https://api.slack.com/messaging/webhooks)
<br/>


- change the variable "url" inside \_\_init\_\_.py file and paste Your URL "`Lib\site-packages\webhooks\__init__.py`"
- finally just run the following command:<br/>
```
robot --listener webhooks <your test.robot>
```

## .features / .todo
- [x] ~~Improvements idea: Make PyPi package which can installed from command line (by Tatu)~~
- [x] ~~Did not test it with slack. yet~~
- [x] ~~Change Message Details / improve~~
- [x] ~~New way to add URL to End user~~
- [ ] Add more ideas in here!! maybe [Discord?](https://www.digitalocean.com/community/tutorials/how-to-use-discord-webhooks-to-get-notifications-for-your-website-status-on-ubuntu-18-04) because I guess it's possible.
- [ ] only test it on Windows. Is it necessary for mac or linux? or irrelevant

<br/>
<br/>
