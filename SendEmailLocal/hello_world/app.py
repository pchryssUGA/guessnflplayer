import json
import boto3
from botocore.exceptions import ClientError

returnImageChoiceAPI = "https://t9bpl2e4m3.execute-api.us-east-2.amazonaws.com/test?"

def lambda_handler(event, context):
    SENDER = "RandomGen <philipchryssochoos@gmail.com>"
    RECIPIENT = "philipchryssochoos@gmail.com"
    #CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-2"
    SUBJECT = "Fix Reported Player"
    playerID = event["queryStringParameters"]["playerID"]
    playerName = event["queryStringParameters"]["playerName"]
    imageOne = event["queryStringParameters"]["imageOne"]
    imageTwo = event["queryStringParameters"]["imageTwo"]
    imageThree = event["queryStringParameters"]["imageThree"]
    imageFour =  event["queryStringParameters"]["imageFour"]
    API = "https://t9bpl2e4m3.execute-api.us-east-2.amazonaws.com/test/return?"
    imageOneAPICall = API + "id=" + playerID + "&url="+imageOne 
    imageTwoAPICall = API + "id=" + playerID + "&url="+imageTwo 
    imageThreeAPICall = API + "id=" + playerID + "&url="+imageThree 
    imageFourAPICall = API + "id=" + playerID + "&url="+imageFour 

    BODY_TEXT = ("Amazon SES Test\n"
                 "This email was sent with Amazon SES using\n"
                 "AWS SDK for Python (Boto).")
    BODY_HTML = """<html>
                    <head>
                        <style>
                            #image {
                                height: 170px;
                                width: 350px;
                                border: 5px solid black;
                                border-radius: 15px;
                                margin-bottom: 15px;
                            }
                            .img_div {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                            }
                            .button {
                                 margin-left: 10px;
                            }
                        </style>
                    </head>
                    <body>
                    <h1>Amazon SES Test (SDK for Python)</h1>
                        <div class="img_div">
                            <img id="image" src="""+imageOne+""">
                        </div>
                        <div class="img_div">
                            <img id="image" src="""+imageTwo+""">
                        </div>
                        <div class="img_div">
                            <img id="image" src="""+imageThree+""">
                        </div>
                        <div class="img_div">
                            <img id="image" src="""+imageFour+""">
                        </div>
                    </body>
                    </html>
                """
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
#            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"{e.response['Error']['Message']}"
            }),
        }
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Email sent! Message ID:"
            }),
        }       
    

