class Validator:
  
  def validate_text(self,text):
    space = " "
    min = 3
    max = 20  
    return (min<= len(text) <=max and not(space in text))
  
  def password_match(self,input1,input2):
    return (input1 == input2)

  # def __init__(self,name,password):
  #       self.name = name
  #       self.password = password

  def validate_input(self,name,password,password_verified):
      if not self.validate_text(name):
        self.errors['error_name'] = "Username is invalid" 
        self.errors['contains_error'] = True

      if not self.validate_text(password):
        self.errors['error_password'] = "Password is invalid" #No spaces, <3 or >20
        self.errors['contains_error'] = True

      if not self.password_match(password,password_verified):
        self.errors['error_match'] = "Passwords do not match"   
        self.errors['contains_error'] = True

  errors = {
        "error_name" : "",
        "error_password" : "",
        "error_match" : "",
        "contains_error" : False
    }

