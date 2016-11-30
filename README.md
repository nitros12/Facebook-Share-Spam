# Facebook-Share-Spam
Comments on posts by a particular user, and also shares everything from some pages


install requirements with ```pip install -r requirements.txt```

make sure you use python 3.x

copy ```baseConfig.json``` to ```config.json```

Add in your id's and messages to the ```comment_conf``` section. (id's should be the numerical id, google how to get it)

Get an api token from here:

```https://developers.facebook.com/tools/explorer/145634995501895/```

Create one with the v2.3 api and give it access to ```publish_actions``` and ```user_posts```

place this in the ```api_key``` section of the config

Place your facebook numerical id in the ```self_id``` secction. (google how to)


run it
