import jwt
import bcrypt
from datetime import timezone, datetime
        
class user_controller:
    def __init__(self, appLogger, db, jwt_secret):
        self.logger = appLogger
        self.db = db
        self.secret = jwt_secret
    
    def addUser(self, userName, password, role):
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode(), salt)
        self.db.addUser(userName, password, role)

    def login(self, userName, plain):
        user = self.db.findUser(userName)
        if not user:
            return None
        return user.login(plain, self.secret)

    def authenticate(self, token):
        try:
            method, jwtoken = token.split(" ")
            assert(method == "Bearer")

            payload = jwt.decode(jwtoken, self.secret, algorithms="HS256")
            now = int(datetime.now(tz=timezone.utc).timestamp())
            assert(payload['exp'] >= now)

            return self.db.findUser(payload['userName'])
        except Exception as e:
            # self.logger.info(e.__repr__());
            pass
        return None
     
    def passwd(self, userName, plain):
        user = self.db.findUser(userName)
        if not user:
            return None
        return user.passwd(plain, self.secret)

