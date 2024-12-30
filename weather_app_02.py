import sys
#contains modules requried for app
import requests
#used to request apis
from PyQt5.QtWidgets import QApplication,QLabel,QVBoxLayout,QWidget,QLineEdit,QPushButton,QHBoxLayout
#widgets are the building blocks in qt framework
from PyQt5.QtCore import Qt
from requests import HTTPError


#Qt is used for alignment

#class weatherapp is inheritining from parent Qwidget
#super is used to get access to all the class and object and functions of parent class
#this is the app window
class weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        #self means window (the class itself)
        #all the labels,buttons,searchbar required for the app(they are widgets)
        self.city_label = QLabel("Enter your city:",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("get weather",self)
        self.temperature_label = QLabel(self)
        self.humidity_label = QLabel(self)
        self.humidity_text=QLabel("Humidity",self)
        self.wind_speed_text = QLabel("wind speed",self)
        self.wind_speed = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label =QLabel(self)



        self.initUI()

    #this is used the design the user interface (widgets above)
    def initUI(self):
        self.setWindowTitle("weather app")


        vbox = QVBoxLayout()
        #creating grid for the interface
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.humidity_text)
        vbox.addWidget(self.humidity_label)
        vbox.addWidget(self.wind_speed_text)
        vbox.addWidget(self.wind_speed)

        #here all the overlapping widgets are arranged vertically
        self.setLayout(vbox)

            #aligning all the widgets(button not included)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.humidity_text.setAlignment(Qt.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.wind_speed_text.setAlignment(Qt.AlignCenter)
        self.wind_speed.setAlignment(Qt.AlignCenter)

        #applying css style using object name
        #setting up object name
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        self.humidity_text.setObjectName("humidity_text")
        self.humidity_label.setObjectName("humidity_label")
        self.wind_speed_text.setObjectName("wind_speed_text")
        self.wind_speed.setObjectName("wind_speed")
        #adding css style to all widgets
        self.setStyleSheet("""
        QLabel,QPushButton{
        font-family:arial;
        }
        QLabel#city_label{
        font-size:40px;
        font-style:italic;
        color:#f02222;
        }
        QLineEdit#city_input{
        font-size:30px;
        }
        QPushButton#get_weather_button{
        font-size:20px;
        font-weight:Bold;
        }
        QLabel#temperature_label{
        font-size:50px;
        }
        QLabel#emoji_label{
        font-size:100px;
        font-family:segoe UI emoji
        }
        QLabel#description_label{
        font-size:30px;
        }
        QLabel#humidity_text{
        color:#f02222;
        font-size:25px;
        }
        QLabel#humidity_label{
        color:#f02222;
        font-size:15px;
        }
        """)
        #connecting buttons to their actions
        self.get_weather_button.clicked.connect(self.get_weather)
    #method to connect get_weather_button ,when the button is clicked this method is activated
    def get_weather(self):
        #fetching wheather data from api
        api_key = "b234845fa3700b2306a2b15371eb6908"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        #when we pass an api request we get response which need to be stored in a variable
        #we need to convert this response to json format
        #if cod in data is 200 then data is safe to use else we must return error using expection handling
        try:#we have to rise a httperror because try block doesnt catch this
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            #data is dictionary containing weather data by using ['cod'] we are checking to see if proper data has been returned

            if data['cod'] == 200:
                self.display_weather(data)
        #this httperror is found in request module so we cant just decalre it
        #we will use match case using status code
        except requests.exceptions.HTTPError as httperror:
            match response.status_code:
                case 400:
                    self.display_error("bad request: \n please check your input ")
                case 401:
                    self.display_error("unauthorised: \n invalid API key ")
                case 403:
                    self.display_error("forbidden: \n access is denied ")
                case 404:
                    self.display_error("not found: \n city not found")
                case 500:
                    self.display_error("internal server error :\n please try again later")
                case 502:
                    self.display_error("bad gate way: \n invalid response from the server ")
                case 503:
                    self.display_error("service unaviable: \n server is down ")
                case 504:
                    self.display_error("gate way time out :\n no response from server ")
                case _:#this is wild card error
                    self.display_error(f"HTTP error has occured :\n {httperror}")


        #network and url error
        except requests.exceptions.ConnectionError:
            self.display_error("connection error:\n check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("time out error:\n the request time out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("too many redirects:\n check url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"request error:\n {req_error}")

    #the error is stored in message variable
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:15px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.humidity_label.clear()
        self.wind_speed.clear()
    #displaying the temperature when no error found,but must convert to c to f as its in kelvin
    def display_weather(self,data):
        #the data store in from of dictionary can be accessed
        self.temperature_label.setStyleSheet("font-size:50px")
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        weather_id = data['weather'][0]['id']
        weather_desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        w_speed = data['wind']['speed']
        print(data)
        #displaying temperature
        #dispalyign weather
        self.temperature_label.setText(f"{temperature_c:.0f}°c")
        self.description_label.setText(f"{weather_desc}")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.humidity_label.setText(f'{humidity}')
        self.wind_speed.setText(f'{w_speed}')

    #This is a independent method for returning emoji
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200<= weather_id <= 232:
            return '⛈️'
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <=531:
            return "🌦️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "♨️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "

#sys.argv is used for command line execution
#exec_() handles event in our application
#this code executes if the program is running directly
if __name__ =="__main__":
    app = QApplication(sys.argv)
    weather_app = weatherapp()
    weather_app.show()
    sys.exit(app.exec_())