# CardCheck-API
----
  Validates a card number and returns the status and issuing network in json format

* #### URL

  /api/cc/:cardnumber

* #### Method

  `GET`
  
* #### URL Params
  
   **Required:**
 
   `cardnumber=[integer]`

* #### Data Params

  None

* #### Success Response:

  ```json
  {
   "result":{
      "cardnumber":"5100000010001004",
      "is_valid":true,
      "issuing_network":[
         "Mastercard"
      ],
      "length":16
   },
   "status":"success",
   "status_code":"200"
  }
  ```
 
* #### Error Response

  **404:** Endpoint does not exist
  
  ```json
  {
    "result": {
        "error": "Resource not found. Please refer to the documentation."
    },
    "status": "failed",
    "status_code": "404"
  }
  ```
  **405:** A method except GET was used
  ```json
  {
    "result": {
        "error": "This method type is not currently supported. Please refer to the documentation."
    },
    "status": "failed",
    "status_code": "405"
  }
  ```
  **419:** Argument (cardnumber) missing
  ```json
  {
    "result": {
        "error": "The requested resource is missing required arguments. Please refer to the documentation."
    },
    "status": "failed",
    "status_code": "419"
  }
  ```
  **420:** Invalid arguments. Card number can only be digits not more than 20 characters.
  ```json
  {
    "result": {
        "error": "The requested resource does not support one or more of the given parameters. Please refer to the documentation."
    },
    "status": "failed",
    "status_code": "420"
  }
  ```
  **500:** Internal Server Error
    ```json
    {
      "result": {
          "error": "Internal Server Error"
      },
      "status": "failed",
      "status_code": "500"
    }
    ```
* #### Sample Call
  **Curl:**
  ```curl
  curl https://cardcheck-api.herokuapp.com/api/cc/5100000010001004
  ```
  
  **Python:**
  ```python
    import requests
    response = requests.get("https://cardcheck-api.herokuapp.com/api/cc/5100000010001004")
    print(response)
  ```
  **JavaScript:**
  ```javascript
  // GET Request.
  fetch('https://cardcheck-api.herokuapp.com/api/cc/5100000010001004')
  // Handle success
  .then(response => response.json())  // convert to json
  .then(json => console.log(json))    //print data to console
  .catch(err => console.log('Request Failed', err)); // Catch errors
   ```
   
  #### ABOUT
  CardCheck-API was written by [Shine Jayakumar](https://github.com/shine-jayakumar).
  More features to be added to the API soon.
   
  #### LICENSE
  [MIT LICENSE](https://github.com/shine-jayakumar/CardCheck-API/blob/main/LICENSE)
