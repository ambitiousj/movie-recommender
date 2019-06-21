"""
Recommendations Web Application : Uses Cherrypy,W3C CSS, and some open source Javascript
"""

import os.path
import cherrypy
import rec_gen
import pageblocks
import class_content_based


blocks = pageblocks.PageBlocks()

class HomePage:

    @cherrypy.expose
    def index(self):
        return blocks.getHomePage()

class NewUser:

    @cherrypy.expose
    def index(self):
        return blocks.getNewUserRegistrationPage(True)
        
    @cherrypy.expose
    def validateAndRegisterUser(self, name=None, userage=None, userocc=None, gender=None):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
        message = ""                       
        if len(name) == 0 :
            message = 'Please provide a valid name'
        elif userage.isdigit() == False:
            message = 'Please provide a valid age'
        elif len(userocc) == 0 :
            message = 'Please provide a valid occupation'
        elif gender == None:
            message = 'Please provide a valid gender'
        if message != "":
            return blocks.getNewUserRegistrationPage(False,name, userage, userocc, gender, message)
        else:
            userage = int(userage)
            
            return blocks.getNewUserMovieRatingPage(userage, userocc, gender)

    @cherrypy.expose
    def validateRatings(self,movietitle=None,rating=None,userage=None, userocc=None, gender=None):
        recsEngine = rec_gen.RecsEngine()
        cherrypy.session['recsengine'] = recsEngine
        recsEngine.add_new_user(userage, userocc, gender, movietitle, rating)
        message = ("your user id:" +str(recsEngine.currentuserid))
        userid = recsEngine.currentuserid
        cherrypy.log("USER REGISTERED. NEW ID ASSIGNED => "+str(recsEngine.currentuserid))
        cherrypy.log("USER REGISTERED. NEW ID ASSIGNED => "+str(recsEngine.ratings))
        return blocks.getNextOptionsPage(True,movietitle, message, userid) 
        
class Login:
    @cherrypy.expose
    def index(self):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = None
        return blocks.getLoginPage()

    @cherrypy.expose
    def validateUserAndSignin(self,loginuserid=None,name=None):
        recsEngine = rec_gen.RecsEngine()
        cherrypy.session['recsengine'] = recsEngine
        error = False
    
        if(loginuserid.isdigit()):
            loginuserid = int(loginuserid)
            if recsEngine.check_if_user_exists(loginuserid):
                cherrypy.log("EXISTING USER :"+str(loginuserid))
            else:
                error = True
                message = 'The User ID provided does not exist. Please register or try again.'
        else:
            error = True
            message = 'please provide valid ID'
        if error:          
            return blocks.getLoginPage(name,message)
        else:
            if cherrypy.session.get('recsengine') != None:
                recsEngine = cherrypy.session.get('recsengine')
            existinguserid = recsEngine.currentuserid 
            return blocks.getExistingUserMovieRatingPage(existinguserid)

    @cherrypy.expose
    def validateRatings(self,movietitle=None,rating=None,userid=None):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
        recsEngine.add_new_rating(movietitle,rating)
        cherrypy.log("UPDATED RATINGS : \n"+ str(recsEngine.currentuserid))
        cherrypy.log("UPDATED RATINGS : \n"+str(recsEngine.ratings))
        userid = recsEngine.currentuserid
        return blocks.getNextOptionsPage(False,movietitle)

class ExistingUser:
    @cherrypy.expose
    def index(self):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
        existinguserid = recsEngine.currentuserid 
        return blocks.getExistingUserMovieRatingPage(existinguserid)
            
    @cherrypy.expose
    def validateRatings(self,movietitle=None,rating=None,userid=None):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
        recsEngine.add_new_rating(movietitle,rating)
        cherrypy.log("UPDATED RATINGS : \n"+str(recsEngine.ratings))
        userid = recsEngine.currentuserid 
        return blocks.getNextOptionsPage(False,movietitle)
          
class Recommendations:
    @cherrypy.expose
    def index(self):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
            cherrypy.log("CHECKING DATA"+str(recsEngine.currentuserid))
        return blocks.getRecommendations()

    @cherrypy.expose
    def showRecommendations(self,algorithm = None):
        message = "" 
        if algorithm == None:
            message = "Please select what recommendations you would like to see."
            return blocks.getRecommendations(message)
        else:
            if cherrypy.session.get('recsengine') != None:
                recsEngine = cherrypy.session.get('recsengine')
            tagStart = '''<div class="w3-button w3-indigo" style="display:block;width:500px;clear:both;margin-top:5px;">'''
            recsHTML = ""
            watchrecsHTML = ""
            recEntry = ""
            tagEnd = "</div>"
            recsEngine.recommend(recsEngine.currentuserid,algorithm)
            for i in range(len(recsEngine.recommended_titles)):
                recEntry = str(tagStart) + str(recsEngine.recommended_titles[i]) + str(tagEnd)
                recsHTML = recsHTML  + str(recEntry)
            for j in range(len(recsEngine.watch_again_titles)):
                recEntry = str(tagStart) + str(recsEngine.watch_again_titles[j]) + str(tagEnd)
                watchrecsHTML = watchrecsHTML  + str(recEntry)
            return blocks.showRecommendations(recsHTML,watchrecsHTML)
        
class SignOut:
    @cherrypy.expose
    def index(self):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
        saveCompleted = recsEngine.sign_out()
        if saveCompleted:
            recsEngine = None
            return blocks.getSignOutPage()
            
    @cherrypy.expose
    def validateRatings(self,movietitle=None,rating=None,userid=None):
        if cherrypy.session.get('recsengine') != None:
            recsEngine = cherrypy.session.get('recsengine')
        recsEngine.add_new_rating(movietitle,rating)
        cherrypy.log("UPDATED RATINGS : \n"+str(recsEngine.ratings))
        userid = recsEngine.currentuserid
        return blocks.getNextOptionsPage(False,movietitle)
    
class GuestUser():
    @cherrypy.expose
    def index(self):
        return blocks.getGuestUserRegistration(recsHTML=None,movietitle=None)
    
    @cherrypy.expose
    def pickMovie(self, name = None, movietitle = None):
        ContBased = class_content_based.ContentBasedRec()
        cherrypy.session['contbased'] = ContBased
        if cherrypy.session.get('contbased') != None:
            ContBased = cherrypy.session.get('contbased')

        tagStart = '''<div class="w3-button w3-indigo" style="display:block;width:500px;clear:both;margin-top:5px;">'''
        recsHTML = ""
        watchrecsHTML = ""
        recEntry = ""
        tagEnd = "</div>"
        ContBased.movie_title = str(movietitle)
        print(ContBased.movie_title)
        print(type(ContBased.movie_title))

        
        ContBased.content_recommender()
        print(ContBased.recommendations)
        for i in range(len(ContBased.recommendations)):
            recEntry = str(tagStart) + str(ContBased.recommendations.values[i]) + str(tagEnd)
            recsHTML = recsHTML  + str(recEntry)
        return blocks.getGuestUserRegistration(recsHTML, movietitle)
    
root = HomePage()
root.newuser = NewUser()
root.existinguser = ExistingUser()
root.login = Login()
root.getrecs = Recommendations()
root.signout = SignOut()
root.guestuser = GuestUser()

if __name__ == '__main__':

    conf = {
        '/': {
            'server.socket_port': 8080,
            'tools.sessions.on': True,
            'tools.staticdir.on': True,
            'tools.staticdir.root': '/Misc/Jorrell/static/',
            'tools.staticdir.dir': '/Misc/Jorrell/static/'
        }
    }

cherrypy.engine.stop()
cherrypy.server.stop()
cherrypy.server.restart()
cherrypy.quickstart(root,config=conf)
