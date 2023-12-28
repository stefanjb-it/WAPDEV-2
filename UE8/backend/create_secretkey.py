from django.core.management import utils
open(".env", "w").write("SECRET_KEY=%s" % utils.get_random_secret_key())
print(".env file written.")
