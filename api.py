from flask import Flask, jsonify
import pandas as pd
import re 


app = Flask(__name__)

card_df = pd.read_pickle('iin.pickle')

class Card:

    def __init__(self, iin_df, cardno):
        
        self.cardno = ''
        self.cardno_length = 0
        self.is_valid = ''
        self.issuing_network = ''
        self.iin_df = ''

        if type(cardno) == str and type(iin_df) == pd.DataFrame:
            self.cardno = cardno
            self.cardno_length = len(cardno)
            self.iin_df = iin_df

            self.is_valid = self.check_luhn()
            self.issuing_network = self.get_issuing_network()
    
    # get rows from df that matches the first digits
    def get_rows_matching_first_digit(self, df, cardno):
        matching_rows = df.loc[df['first_digits'].apply(lambda x: cardno[0] in x)]
        return matching_rows
    
    # checks if the card number starts with any one of the numbers in IIN Ranges
    def find_iin(self, cardno, iinranges):

        iinranges_list = iinranges.split(', ')
        found = False 
        
        # check if the card number starts with any of the numbers in the IIN
        for iin in iinranges_list:
            pat = re.compile("^" + iin)
            if bool(pat.match(cardno)) == True:
                found = True
                break
        return found

    
    def get_issuing_network(self):

        # get rows for which first digits match
        relevant_rows = self.get_rows_matching_first_digit(self.iin_df, self.cardno)

        # look for the issuing network in df
        issuing_network = relevant_rows.loc[relevant_rows['IIN_ranges'].apply(lambda x: self.find_iin(self.cardno, x))== True, ['Issuing_network']]
        issuing_network = issuing_network.to_string(index=False).split('\n')[1:]
        
        if "Columns" in issuing_network[0]:
            return 'Not Found'
        else:
            return [net.strip() for net in issuing_network]
    
    # Luhn's algorithm (mod10)
    def check_luhn(self):
        if self.cardno != '':
            rnum = list(self.cardno[-1::-1])
            
            checksum = 0

            for i in range(0, self.cardno_length):
                if i%2 != 0:
                    prd = int(rnum[i]) * 2

                    if prd > 9:
                        prd = str(prd)
                        prd = str(int(prd[0]) + int(prd[1]))
                        rnum[i] = prd
                    else:
                        rnum[i] = prd

                checksum += int(rnum[i])
            
            if checksum%10 == 0:
                self.is_valid = True
                
            else:
                self.is_valid = False
        return self.is_valid

def get_error(err_code):

    error_responses = {
        "404": "Resource not found. Please refer to the documentation.",
        "419": "The requested resource is missing required arguments. Please refer to the documentation.",
        "420": "The requested resource does not support one or more of the given parameters. Please refer to the documentation.",
        "405": "This method type is not currently supported. Please refer to the documentation."
    }
    return {
        "status": "failed",
        "status_code": str(err_code),
        "result": {"error": error_responses[err_code]}
    }


@app.errorhandler(404)
def invalid_route(e):
    return jsonify(get_error("404"))

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(get_error("405"))

@app.route("/api/cc")
@app.route("/api/cc/")
def missing_arguments():
    return jsonify(get_error("419"))

# suggest visitor to check the documentation
@app.route("/api/")
@app.route("/api/docs")
@app.route("/api/docs/")
@app.route("/")
def docs():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CreditCardCheck-API Docs</title>
</head>
<body>
    <h2>CardCheck-API</h2>
    <br/>
    <p>Please refer to docs: <a href="https://github.com/shine-jayakumar/cardcheck-api">https://github.com/shine-jayakumar/cardcheck-api</a></p>
</body>
</html>
'''

# endpoint to get the cardnumber
@app.route("/api/cc/<string:cardnumber>", methods = ['GET'])
def cardinfo(cardnumber):

    if cardnumber.isdecimal() == False or len(cardnumber) > 20:
        return jsonify(get_error("420"))

    else:
        cc = Card(card_df, cardnumber)

        return jsonify(
            {   "status": "success",
                "status_code": "200",
                "result": {
                    "cardnumber": cc.cardno,
                    "length": cc.cardno_length,
                    "is_valid": cc.is_valid,
                    "issuing_network": cc.issuing_network 
                }                
            }
        )

if __name__ == "__main__":
    app.run(debug=False, port=8080)

