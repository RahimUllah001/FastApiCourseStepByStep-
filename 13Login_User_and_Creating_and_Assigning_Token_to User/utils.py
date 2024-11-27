# here we define utility function ==> are thoose functions which are reusable adn are not hardly tied with program e.g hasihng password str validation 


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
