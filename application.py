from flask import Flask
from flask import request, jsonify
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)


def authenticateClient(endpoint="https://dssd-sentimen.cognitiveservices.azure.com/",subscription_key="77594e6a1c7c4d30a73180e6d6db4c1c"):
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credentials=credentials)
    return text_analytics_client

def sentiment(lng,text):
    
    client = authenticateClient()

    try:
        document = [{"id" : 1,"language": lng, "text": text } ]

        return client.sentiment(documents=document).documents

    except Exception as err:
        return ("Encountered exception. {}".format(err))


@app.route('/')
def hello():
    return """
    <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" >
            <title>Sentiment analysis by jemix</title>
          </head>
          <body>
          <div class="container">
              <div class="row" style="margin-top:30px;">
                <h1>This is Sentiment analysis with azure by jemix</h1>
              </div>
              <div class="row">
                <div class="col-lg-8">
                    <form method="post" action="/submit" id="form">
                      <div class="form-group">
                        <label for="lng">Select Langage</label>
                        <select class="form-control" name="lng" id="lng">
                          <option value="en">English</option>
                          <option value="fr">Français</option>
                          <option value="ar">عربي</option>
                        </select>
                      </div>
                      <div class="form-group">
                        <label for="text">Text for analysis</label>
                        <textarea class="form-control" name="text" id="text" rows="4"></textarea>
                      </div>
                      <div class="form-group">

                        <p id="res" style="font-size:100px"></p>
                        <p id="res_p" style="font-size:20px"></p>
                        
                      </div>
                      <div class="form-group">
                        <input type="submit" class="btn btn-primary btn-lg" id="sub">
                      </div>
                    </form>
                </div>
              </div>
            </div>


            <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" ></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" ></script>

            <script>

                        $('#sub').click(function(e){
                            e.preventDefault();

                            $.post( "/submit", $( "#form" ).serialize() ).done(function(data){
                                

                                if(data < 0.2){
                                    $("#res").html("&#x1F62D;");
                                }

                                if(data > 0.2 && data < 0.49){
                                    $("#res").html("&#x1F62A;");
                                }

                                if(data > 0.5 && data < 0.7){
                                    $("#res").html("&#x1F610;");
                                }

                                if(data > 0.7){
                                    $("#res").html("&#x1F603;");
                                }

                                $("#res_p").text((data*100) + " %");
                            });
                        });

            </script>
          </body>
        </html>
    """

@app.route('/submit', methods=['POST'])
def sub():
    if request.method == 'POST' :     
        lng = request.form.get('lng')
        text = request.form.get('text')
        score = sentiment(lng,text)
        return "{:.2f}".format(score[0].score)
    return "0.0"

