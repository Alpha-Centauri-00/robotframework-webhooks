# robotframework-webhooks

This repository contains a custom listener designed for the Robot Framework to enhance test management and immediacy in response. When a test case fails, the listener triggers an automatic notification to a specified *Microsoft Teams* channel using Webhooks. This ensures that the team is instantly alerted, enabling prompt investigation and action. like this
[example](https://github.com/Alpha-Centauri-00/robotframework-webhooks/blob/main/img/img1.png)
<br/>
<br/>

# Installation

You can install robotframework-webhooks simply by running:



```
pip install robotframework-webhooks
```


## How to:
How to Create Incoming Webhooks for MS-Teams.

- Open Apps in MS-Teams and seach for [Workflows](https://github.com/Alpha-Centauri-00/robotframework-webhooks/blob/main/img/img2.png)
- Choose an [instant](https://github.com/Alpha-Centauri-00/robotframework-webhooks/blob/main/img/img3.png) called **Post to a channel when a webhook request is received**
- Follow the steps. and choose a specific channel where error messages will be sent.
- At the end Microsoft Teams will generate a URL link for your webhook.
- Copy this URL and save it in your `robot.toml` file using the following format:

```toml
[variables]
webhook_url = "PASTE-YOUR-URL-IN-HERE"

[listeners]
webhooks = []
```

- You can add the listener inside the `robot.toml` file, or you can call it directly using:

```shell
robot --listener webhooks <your test.robot>
```


## Reporting Issues

If you encounter any bugs, have questions, or want to suggest improvements, please don't hesitate to open an [Issues](https://github.com/Alpha-Centauri-00/robotframework-webhooks/issues). Your feedback is valuable and helps make this project better for everyone.

Thank you for checking out this project! If you appreciate the work put into it, a ⭐ would be greatly appreciated.