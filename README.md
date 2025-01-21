## Weather Api

Configure your project with a .env file, Please add these values:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TO_PHONE_NUMBER`
- `API_KEY_WAPI`

With Pulumi:

```bash
pulumi config set weather_api:TWILIO_ACCOUNT_SID your_twilio_account_sid --secret
pulumi config set weather_api:TWILIO_AUTH_TOKEN your_twilio_auth_token --secret
pulumi config set weather_api:TWILIO_PHONE_NUMBER your_twilio_phone --secret
pulumi config set weather_api:API_KEY_WAPI your_weather_apy_key --secret
pulumi config set weather_api:TO_PHONE_NUMBER your_recipient_phone_number
```

You can enter to the ec2 instance via ssh with your .pem file
see the logs after execute `pulumi up`

Example:
```bash
ssh -i weather-api.pem ec2-user@3.85.67.69
```

If you see that the image is not created or the container is not running

Run:
```bash
docker build -t weather-api-image /var/opt/weather_api
docker run -it --name weather-container weather-api-image
```

You can run the whole flow with this command

```bash
docker exec -it weather-container sh -c "python src/app.py"
```
