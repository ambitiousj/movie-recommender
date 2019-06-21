
class PageBlocks:

    def __init__(self):
        print("PageBlocks initialized")
        self.header = '''
<!DOCTYPE html>
<html>
<head>
<title>JORRELL-MOVIE RECS</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="../../5star.css">
<script type="text/javascript" src="../../autocomplete.js" charset="UTF-8" ></script>
</head>
<body>
<div style="width:100%;text-align:left" class="w3-container w3-teal">
<h1>Jorrell's Movie Recommender System</h1>
</div>
        '''
        self.footer = '''</body></html>'''
        
    # Home page
    def getHomePage(self):
        return self.header + '''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Welcome to Jorrell's Movie Recommender</h4>
</div>

<div class="w3-container" style="padding:20px;width:200px">
  <a href="/newuser/" class="w3-button w3-green" style="font-size:16px;padding:10px;width:200px" >I am a New User</a>
</div>
<div class="w3-container" style="padding:20px;width:200px">
<a href="/login/" class="w3-btn w3-orange" style="font-size:16px;padding:10px;width:200px">I am an Existing User</a>
</div>
 <div class="w3-container" style="padding:20px;width:200px">
    <a href="/guestuser/" class="w3-btn w3-aqua" style="font-size:16px;padding:10px;width:200px">I am a Guest User</a>
  </div>
        ''' + self.footer
        
    # New User Registration
    def getNewUserRegistrationPage(self,firsttime=None,name=None,userage=None, userocc=None, gender=None, message=None):
        nametext = agetext = occtext = gentext = "teal"
        if firsttime :
            name = userage = userocc = gender = message = ""
        else:
            print("notfirsttime")
            if name == None:
                name = ""
            if userage == None:
                userage = ""
            if userocc == None:
                userocc = ""
            if gender == None:
                gender = ""
            if message != None:
                message = '''<div style="display:block;margin-top:10px;" class="w3-button w3-red">''' + message+ '''</div>'''
        return self.header + f'''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Register your details</h4>
</div>
<div style="width:600px;text-align:left">
<form action="validateAndRegisterUser" method="GET" class="w3-container">
  <div style="padding-top:20px;"><div class="w3-text-{nametext}" style="width:100px; float:left;"><b>Name</b></div>
      <input class="w3-input w3-border w3-light-grey" style="margin-left:10px;display:inline;width:300px;" type="text" name="name" value="{name}" required>
  </div>
  <div style="padding-top:20px;"><div class="w3-text-{agetext}" style="width:100px; float:left;"><b>Age</b></div>
      <input class="w3-input w3-border w3-light-grey" style="margin-left:10px;display:inline;width:300px;" type="text" name="userage" value="{userage}" required>
  </div>
  <div style="padding-top:20px;"><div class="w3-text-{occtext}" style="width:100px; float:left;"><b>Occupation</b></div>
      <input class="w3-input w3-border w3-light-grey" style="margin-left:10px;display:inline;width:300px;" type="text" name="userocc" value="{userocc}" required>
  </div>
  <div style="padding-top:20px;"><div class="w3-text-{gentext}" style="width:100px; float:left;"><b>Gender</b></div>
      <input class="w3-radio" style="margin-left:5px;width:30px;" type="radio" name="gender" value="M"><label>Male</label>
      <input class="w3-radio" style="width:30px;" type="radio" name="gender" value="F"><label>Female</label>
  </div>
  {message}
  <div class="w3-container" style="display:block;float:left;width:400px;clear:both;text-align:center;padding:30px;">
      <input type="submit" value="Register" class="w3-btn w3-blue" style="width:200px;">
  </div>
</form>
</div>''' + self.footer

    # New user Rate Movie
    def getNewUserMovieRatingPage(self,userage=None, userocc=None, gender=None, ):
        hidden_elements = f'''<input type="hidden" name="userage" value="{userage}" ><input type="hidden" name="userocc" value="{userocc}" ><input type="hidden" name="gender" value="{gender}" >'''
        return self.getMovieRatingHTML(hidden_elements)

    # Existing user Rate Movie
    def getExistingUserMovieRatingPage(self,userid=None):
        hidden_elements = f'''<input type="hidden" name="userid" value="{userid}" >'''
        return self.getMovieRatingHTML(hidden_elements)

    # Rate Movie HTML
    def getMovieRatingHTML(self,hidden_elements=None):
        return self.header + f'''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Rate your movie</h4>
</div>
<!--Make sure the form has the autocomplete function switched off:-->
<form autocomplete="off" action="validateRatings">
  <div class="autocomplete" style="display:block;float:left;width:600px;clear:both;padding-top:20px;">
    <div class="w3-text-teal" style="margin-top:10px;width:200px;float:left;margin-left:10px;"><b>Please select your movie:</b></div>
    <input class="w3-input w3-border w3-light-grey" style="margin-left:10px;display:inline;width:350px;" id="movie" type="text" name="movietitle" placeholder="Select your movie...">
  </div>
  <div class="autocomplete" style="margin-top:10px;display:block;float:left;width:600px;clear:both;padding-top:20px;">
    <div class="w3-text-teal" style="width:200px;float:left;margin-left:10px;"><b>Please select your rating:</b></div>
    <ul class="rate-area" style="float:left;padding-left:10px;margin-top:-10px;">
      <input type="radio" id="5-star" name="rating" value="5" /><label for="5-star" title="Amazing">5 stars</label>
      <input type="radio" id="4-star" name="rating" value="4" /><label for="4-star" title="Good">4 stars</label>
      <input type="radio" id="3-star" name="rating" value="3" /><label for="3-star" title="Average">3 stars</label>
      <input type="radio" id="2-star" name="rating" value="2" /><label for="2-star" title="Not Good">2 stars</label>
      <input type="radio" id="1-star" name="rating" value="1" /><label for="1-star" title="Bad">1 star</label>
    </ul> 
  </div>
  {hidden_elements}
  <div class="w3-container" style="display:block;float:left;width:400px;clear:both;text-align:center;padding:30px;">
      <input type="submit" value="Rate Movie" class="w3-btn w3-blue" style="width:200px;">
  </div>
</form>
<script>
autocomplete(document.getElementById("movie"), movies);
</script>
          ''' + self.footer

    #Rate More or Get Recommendations
    def getNextOptionsPage(self,signup=None, movie=None, message = None, userid=None):
        message = " signing up and rating the movie " + movie if signup else " rating the movie " + movie
        useridmessage = f'''<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber"><h4>Your User ID is : {userid} </h4></div>''' if userid != None else ""
        return self.header + f'''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Thank you for {message}</h4>
</div>
{useridmessage}
<div style="width:100%;text-align:left;font:weigfht:bold;padding:10px;" class="w3-container">
    What would like to do now?
</div>
<div class="w3-container" style="padding:20px;width:200px">
    <a href="/existinguser/" class="w3-button w3-green" style="width:400px">Rate more movies</a>
</div>
<div class="w3-container" style="padding:20px;width:200px">
    <a href="/getrecs/" class="w3-btn w3-purple" style="width:400px">See your recommended movies</a>
</div>
<div class="w3-container" style="padding:20px;width:200px">
    <a href="/signout/" class="w3-btn w3-purple" style="width:400px">Save your ratings and sign out</a>
</div>
        ''' + self.footer

    #Login Page
    def getLoginPage(self,name=None,message=None):
        if name == None:
            name = ""
        message = '''<div style="display:block;margin-top:10px;" class="w3-button w3-red">''' + message+ '''</div>''' if message != None else ""
        return self.header + f'''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Please Login!</h4>
</div>
<div style="margin-top:10px;display:block;float:left;width:600px;clear:both;padding-top:20px;">
<form action="validateUserAndSignin" method="GET" class="w3-container">
  <label class="w3-text-teal" style="padding-top:20px;"><b>Name</b></label>
  <input class="w3-input w3-border w3-light-grey" type="text" name="name" value="{name}" required>
  <label class="w3-text-teal"><b>UserID</b></label>
  <input class="w3-input w3-border w3-light-grey" type="text" name="loginuserid" required> 
  {message}
  <div class="w3-container" style="display:block;float:left;width:400px;clear:both;text-align:center;padding:30px;">
      <input type="submit" value="LOGIN" class="w3-btn w3-blue" style="width:200px;">
  </div>
</form>
</div> ''' + self.footer

    #Get Recommendations
    def getRecommendations(self,message=None):
        message = '''<div style="display:block;margin-top:10px;" class="w3-button w3-red">''' + message+ '''</div>''' if message != None else ""
        return self.header + f'''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Choose your recommendation</h4>
</div>
<div style="margin-top:10px;display:block;float:left;width:600px;clear:both;padding-top:20px;">
<form action="showRecommendations" method="GET" class="w3-container">
  <div class="w3-container">
      <label class="container">Show me movies similar to what I like <input type="radio" name="algorithm" value="similar_items">  <span class="checkmark"></span></label>
  </div>
  <div class="w3-container">
    <label class="container">Show me movies that people like me liked <input type="radio" name="algorithm" value="similar_users">  <span class="checkmark"></span></label>
  </div>
  {message}
  <div class="w3-container" style="display:block;float:left;width:400px;clear:both;text-align:center;padding:30px;">
      <input type="submit" value="Show Recommendations" class="w3-btn w3-blue" style="width:250px;">
  </div>''' + self.footer

    #Show Recommendations
    def showRecommendations(self,recsHTML,watchrecsHTML):
         return self.header + f'''

<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Your Recommended Movies</h4>
</div>
<div style="width:100%;text-align:left;font:weigfht:bold;padding:20px;" class="w3-container">
    We recommend the following movies based on other people who like similar movies:
</div>
<div class="w3-container"> {recsHTML} </div>
<div style="width:100%;text-align:left;font:weigfht:bold;padding:20px;" class="w3-container">
    You may want to watch the following movies again:
</div>
<div class="w3-container"> {watchrecsHTML} </div>
<div class="w3-container" style="padding:20px;width:200px">
    <a href="/signout/" class="w3-btn w3-purple" style="width:400px">signout?</a>
</div>
</body>
</html>
        ''' + self.footer
    
    # Home page
    def getSignOutPage(self):
        return self.header + '''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>You have signed out - Thank you for using this recommender system</h4>
</div>

<div class="w3-container" style="padding:20px;width:200px">
  <a href="/newuser/" class="w3-button w3-green" style="font-size:16px;padding:10px;width:200px" >I am a New User</a>
</div>
<div class="w3-container" style="padding:20px;width:200px">
<a href="/login/" class="w3-btn w3-orange" style="font-size:16px;padding:10px;width:200px">I am an Existing User</a>
</div>
<div class="w3-container" style="padding:20px;width:200px">
    <a href="/guestuser/" class="w3-btn w3-aqua" style="font-size:16px;padding:10px;width:200px">I am a Guest User</a>
  </div>
        ''' + self.footer

    # Guest user login
    def getGuestUserRegistration(self,recsHTML,movietitle):
        recsHTML = f'''<div style="display:block;width:100%;text-align:left;clear:both;font-weight:16px;margin:30px 0 20px 10px;" class="w3-text-indigo"><b>Your recommendations based on the movie : <span class="w3-text-blue">{movietitle}</span> are:</b></div><div class="w3-container">{recsHTML}</div>''' if recsHTML != None else ""
        return self.header + f'''
<div style="height:50px;width:100%;text-align:left" class="w3-container w3-amber">
<h4>Guest User : Recommendations</h4>
</div>
<!--Make sure the form has the autocomplete function switched off:-->
<form autocomplete="off" action="pickMovie">
  <div class="w3-text-teal" style="margin-top:30px;width:200px;float:left;margin-left:10px;"><b>Please enter your name:</b></div>
      <input class="w3-input w3-border w3-light-grey" style="margin-top:20px;margin-left:10px;display:inline;width:300px;" type="text" name="name" required>
  </div>
  <div class="autocomplete" style="display:block;float:left;width:600px;clear:both;padding-top:20px;">
    <div class="w3-text-teal" style="margin-top:10px;width:200px;float:left;margin-left:10px;"><b>Please select your movie:</b></div>
    <input class="w3-input w3-border w3-light-grey" style="margin-left:10px;display:inline;width:350px;" id="movie" type="text" name="movietitle" placeholder="Select your movie..." required>
  </div>
  <div class="w3-container" style="display:block;float:left;width:400px;clear:both;text-align:center;padding:30px;">
      <input type="submit" value="Show Recommendations" class="w3-btn w3-blue" style="width:300px;">
  </div>
</form>
<script>
autocomplete(document.getElementById("movie"), ContBased);
</script>
{recsHTML}

        ''' + self.footer 
