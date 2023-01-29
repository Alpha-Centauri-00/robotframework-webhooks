# robotframework-webhooks

The purpose of this repository is to automatically send the results of executing test cases to MS-Teams / Slack. 
by adding an App "WebHook" to your preferable channel, which will generate a URL that you have to use, in order to send the results immediately.
<br/>
<br/>

> Adding an Incoming Webhook for [MS-Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=dotnet)<br/>
> Adding an Incoming Webhook for [Slack](https://api.slack.com/messaging/webhooks)


for now you should change the variable "Web_Hook" inside __init__.py to the link that you got by adding the Webhook
<br/><br/>
Then you have to install requirements.txt <br/>

```
pip install -r requirements.txt
```

<br/>


finally just run the following command:<br/>
<br/>
```
robot --listener webhooks test.robot
```

## .features / .todo
- [ ] Did not test it with slack. yet
- [ ] Change Message Details / improve
- [ ] New way to add URL to End user
- [ ] Add more ideas in here!! maybe [Discord](https://www.digitalocean.com/community/tutorials/how-to-use-discord-webhooks-to-get-notifications-for-your-website-status-on-ubuntu-18-04)
- [ ] only test it on Windows. is it necessary for mac or linux? or irrelevant 
