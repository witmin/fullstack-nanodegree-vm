from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUB Operations from Lession 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2 class='restaurant-name'>Create new restaurant</h2>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<label for='restaurant-name' >Name</label>"
                output += "<input type='text' name='newRestaurantName' placeholder='Required' id='restaurant-name'>"
                output += "<button type='submit'>Create</button>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<label for='restaurant-name' >Name</label>"
                    output += "<input type='text' name='newRestaurantName' value='%s' id='restaurant-name'>" % myRestaurantQuery.name
                    output += "<button type='submit'>Rename</button>"
                    output += "</form></body></html>"

                    self.wfile.write(output)
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<button type='submit'>Delete</button>"
                    output += "<a href='/restaurants'>Cancel</button>"
                    output += "</form></body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                # add new restaurant
                output += "<a href='/restaurants/new'>Create a new restaurant</a>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += "<div class='restaurant-name'>"
                    output += restaurant.name
                    output += "</div>"
                    output += "<div class='restaurant-actions'>"
                    output += "<a class='edit' href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a class='delete' href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</div>"

                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    # POST new restaurant data
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                myRestrantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestrantQuery:
                    session.delete(myRestrantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                )
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestrantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestrantQuery != []:
                        myRestrantQuery.name = message_content[0]
                        session.add(myRestrantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                )
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    new_restaurant = Restaurant(name=message_content[0])
                    session.add(new_restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
